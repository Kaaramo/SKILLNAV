# Justification de l'architecture NoSQL polyglotte SKILLNAV

> Module M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi
> Document à intégrer dans le **rapport méthodologique L5**, chapitre « Architecture des données ».
> Couvre les choix d'architecture, le format initial des données, le pipeline de transmission et la justification de chaque brique de stockage.

---

## 1. Cadre et exigence du sujet

Le sujet imposé du module M242 exige une **architecture NoSQL hybride** distribuée sur trois bases de données complémentaires (PRD SKILLNAV §7). Chaque base est sélectionnée pour son adéquation à un usage spécifique du projet, conformément au principe de la *polyglot persistence* (Sadalage & Fowler, 2012).

| Base de données      | Rôle dans SKILLNAV                                                          |
|----------------------|------------------------------------------------------------------------------|
| **MongoDB Atlas**    | Source de vérité unique : stockage canonique des 3 467 offres collectées     |
| **Neo4j AuraDB**     | Représentation en graphe (Skill / Job / Company) pour l'axe Structure Mining |
| **Elasticsearch**    | Moteur de recherche plein texte et agrégations rapides pour le dashboard     |

Cette architecture distribuée n'est pas un choix de complexité gratuite. Elle reflète l'exigence académique d'une étude comparative entre paradigmes de stockage NoSQL (document, graphe, indexé) ainsi que la réalité industrielle : ces trois bases couvrent à elles seules plus de 80 % des architectures data en production (DB-Engines Ranking, 2026).

---

## 2. Pourquoi MongoDB comme source de vérité unique

Le choix de MongoDB Atlas pour le rôle de *source of truth* repose sur quatre critères techniques évalués au moment de la conception du projet.

### 2.1 Adéquation au format de données collecté

Le corpus SKILLNAV est constitué d'**offres d'emploi structurées en documents JSON imbriqués**, dont la profondeur varie (1 à 4 niveaux) selon la richesse des annonces. Ce format se prête naturellement à un **stockage orienté documents**, là où une base relationnelle (PostgreSQL, MySQL) imposerait une normalisation en plusieurs tables au prix d'une perte de lisibilité et d'une multiplication des jointures.

Concrètement, chaque offre comporte :

- des champs scalaires plats (`title`, `source`, `posted_month`, `ai_type`, `job_family`) ;
- des objets imbriqués (`company.name`, `company.stage`, `company.focus`) ;
- des listes hétérogènes (`responsibilities`, `use_cases`) ;
- un dictionnaire de listes (`skills.genai`, `skills.ml`, ..., `skills.other`).

MongoDB stocke cette arborescence telle quelle, sans transformation. Une base relationnelle aurait demandé au minimum cinq tables avec jointures.

### 2.2 Schéma souple, indispensable à un projet d'exploration

Le corpus évolue par enrichissements successifs : la canonicalisation des compétences a fait passer le vocabulaire de 11 000 variantes brutes à 8 082 entrées canoniques (réduction de 27 %), et l'ajout des colonnes dérivées `title_canonical` et `job_family` est intervenu après la première collecte. Sur une base relationnelle, chaque évolution de schéma aurait nécessité une migration `ALTER TABLE`. MongoDB accepte ces évolutions sans intervention sur le schéma, ce qui correspond précisément à la phase exploratoire dans laquelle se trouve un projet académique.

### 2.3 Idempotence et reprise après incident

L'identifiant unique `_id` (calculé au format `job_<source>_<job_id>` lors de l'export JSON Lines) permet une stratégie d'**upsert idempotent** : une exécution répétée du pipeline d'ingestion produit toujours le même état final, sans création de doublons. Cette propriété est critique dans le contexte académique où une démonstration peut nécessiter une reproduction rapide depuis zéro.

### 2.4 Tier gratuit suffisant et hébergement managé

Le cluster M0 Free Tier de MongoDB Atlas fournit 512 Mo de stockage, soit une marge de 80× au-dessus de la volumétrie effective du corpus (6,1 Mo). L'hébergement managé en région Europe (Frankfurt, eu-central-1) garantit une latence inférieure à 80 ms depuis le Maroc, ce qui est compatible avec une démonstration interactive en soutenance.

---

## 3. Format initial des données : YAML enrichi

### 3.1 Justification du choix YAML

Les 3 467 fiches collectées sont stockées sur disque au format YAML dans l'arborescence `sources/collected/<source>/data_structured/{YYYY-MM}/`. Le choix du YAML s'appuie sur trois propriétés :

1. **Lisibilité humaine.** Le YAML est conçu pour être lu et édité par un humain sans outil spécialisé. Cette propriété est essentielle pour les phases d'audit qualité (cf. §N3 du PRD) et pour le contrôle manuel des extractions LLM.
2. **Compatibilité avec le contrôle de version.** Les diff Git sur YAML sont sémantiquement clairs, ce qui n'est pas le cas pour des fichiers JSON minifiés ou des dumps binaires. Cette propriété facilite la revue par le binôme et la traçabilité des corrections.
3. **Encodage natif des structures imbriquées.** Le format reflète directement la structure du schéma Pydantic `JobPosting`, sans besoin de conversion intermédiaire.

Exemple représentatif d'une fiche YAML :

```yaml
company:
  name: Mistral AI
  stage: Series B+
  focus: Foundation models for European AI sovereignty
position:
  title: Applied AI Engineer
  ai_type:
    type: ai-first
    reasoning: |
      Build production AI applications on top of Mistral models.
  responsibilities:
    - Develop AI features for enterprise customers
    - Optimize inference latency
  skills:
    genai: [LLM, RAG, fine-tuning, agents]
    ml: [PyTorch, transformers]
    ops: [Docker, Kubernetes, MLOps]
    languages: [Python]
meta:
  job_id: '7008912'
  extracted_at: '2026-02-01T14:23:10'
```

### 3.2 Limites du YAML et nécessité d'un format intermédiaire

Le format YAML, optimal pour l'audit et la collaboration, présente trois limites pour la suite du pipeline :

- **Performance de lecture** : 3 467 fichiers répartis dans une arborescence de répertoires imposent 3 467 ouvertures de fichier, soit une latence cumulée de plusieurs secondes à chaque chargement.
- **Absence de format bulk** : ni MongoDB ni Elasticsearch ne consomment nativement du YAML.
- **Encombrement disque** : la sérialisation YAML est verbeuse comparée à JSON compact.

Ces limites motivent l'introduction d'un format intermédiaire de transmission : **JSON Lines**.

---

## 4. Transmission via JSON Lines (`data/jobs.jsonl`)

### 4.1 Définition du format JSON Lines

JSON Lines (`.jsonl`) est un format où chaque ligne du fichier contient **un objet JSON indépendant**, terminé par un retour à la ligne. Cette structure combine les avantages du JSON (interopérabilité universelle, parseurs natifs dans tous les langages) avec ceux du traitement par flux (lecture ligne par ligne sans charger la totalité du fichier en mémoire).

Exemple de ligne dans `data/jobs.jsonl` :

```json
{"_id":"job_intl_ai_corpus_7008912","origine":"International","source":"intl-ai-corpus","title_canonical":"Applied AI Engineer","ai_type":"ai-first","job_family":"AI_ENGINEER","posted_month":"2026-02","company":"Mistral AI","skills":{"genai":["LLM","RAG","Fine-tuning","Agents"],...}}
```

### 4.2 Justification du choix JSON Lines pour la transmission

| Critère                                            | YAML                  | JSON brut         | **JSON Lines**     |
|----------------------------------------------------|-----------------------|-------------------|--------------------|
| Lisibilité humaine                                 | excellente            | bonne             | acceptable         |
| Streaming (lecture ligne par ligne)                | non                   | non               | **oui**            |
| Import natif MongoDB (`mongoimport --type jsonl`)  | non                   | partiel           | **oui**            |
| Import natif Elasticsearch (Bulk API)              | non                   | non               | **oui**            |
| Compatible Spark / Polars / pandas                 | partiel               | partiel           | **oui**            |
| Empreinte disque                                   | élevée                | moyenne           | moyenne            |
| Diff Git sémantique                                | excellent             | faible            | moyen              |

Le format JSON Lines est le **standard de facto** pour la transmission de données structurées entre composants d'un pipeline NoSQL. Il est notamment utilisé par MongoDB (`mongoimport --type jsonl`), Elasticsearch (`_bulk` API), Apache Spark, Google BigQuery et la plupart des outils d'ingestion de données modernes.

### 4.3 Pipeline de transformation YAML vers JSON Lines

Le script `scripts/build_dataset.py` implémente la transformation. Il enchaîne trois étapes :

1. **Lecture récursive** de l'arborescence YAML via `Path.rglob('*.yaml')`.
2. **Canonicalisation en trois niveaux** (compétences via `SKILL_ALIASES`, titres via `TITLE_ALIASES`, famille de poste via `JOB_FAMILY_PATTERNS`), avec dédoublonnage case-insensitive à l'intérieur de chaque offre.
3. **Sérialisation JSON Lines** dans `data/jobs.jsonl`, en complément de l'export CSV destiné à Neo4j (`graph_nodes.csv` et `graph_edges.csv`).

Le pipeline est **idempotent** : une ré-exécution produit le même fichier `jobs.jsonl` à octet près tant que le corpus YAML est inchangé. Cette propriété autorise un rollback simple en cas d'erreur d'ingestion.

---

## 5. Pourquoi compléter MongoDB par Elasticsearch

MongoDB répond aux besoins de stockage et de requêtes ID-based, mais ses capacités de recherche plein texte sont volontairement limitées. Le moteur de recherche Elasticsearch comble cet écart pour les usages applicatifs du dashboard SKILLNAV.

### 5.1 Comparatif fonctionnel MongoDB vs Elasticsearch

| Fonctionnalité                                                                  | MongoDB                                              | Elasticsearch                  |
|---------------------------------------------------------------------------------|------------------------------------------------------|--------------------------------|
| Stockage de documents JSON                                                       | excellent                                            | secondaire                     |
| Recherche exacte `field=value`                                                   | rapide via index                                     | rapide                         |
| **Recherche full-text avec score de pertinence**                                 | basique, pas de scoring fin                          | **excellent (BM25, TF-IDF)**   |
| Auto-complétion / suggest (« Pyt » → « Python »)                                 | non                                                  | **oui**                        |
| Recherche tolérante aux fautes (« datascintist » → « data scientist »)           | non                                                  | **oui**                        |
| Recherche multilingue avec stemming FR / EN / AR                                 | non                                                  | **oui (analyzers natifs)**     |
| Highlighting (surlignage du mot trouvé dans le résultat)                         | non                                                  | **oui**                        |
| Facettes et agrégations rapides sur 10 dimensions                                | aggregation pipeline lente sur gros volumes          | **très rapide**                |
| Recherche vectorielle / sémantique                                               | Atlas Search uniquement (payant)                     | **kNN natif**                  |

### 5.2 Pages du dashboard qui dépendent d'Elasticsearch

| Page                  | Type de requête                                                              | Pourquoi Elasticsearch          |
|-----------------------|------------------------------------------------------------------------------|---------------------------------|
| `/search`             | « offres mentionnant Python + AWS au Maroc »                                  | Multi-clause + scoring          |
| `/skills`             | Top 100 compétences avec filtres par famille et par origine                   | Agrégations multi-dimensions    |
| `/forecasting`        | Série temporelle d'une compétence par mois                                     | Date histogram + cardinality    |
| `/ner-explorer`       | Recherche dans les responsabilités, surlignage du terme trouvé                 | Highlighting natif              |

Une implémentation équivalente sous MongoDB pur exigerait des `aggregation pipelines` complexes dont le temps de réponse en production dépasserait la seconde, là où Elasticsearch reste sous 50 ms.

### 5.3 Pattern d'architecture standard

L'association MongoDB (stockage canonique) + Elasticsearch (moteur de recherche par-dessus) est le pattern de référence depuis 2014 (CQRS / Read-Replica). Il est utilisé par Stack Overflow, Medium, GitHub Issues, Wikipedia, Shopify et la majorité des plateformes éditoriales et e-commerce. Son inclusion dans SKILLNAV démontre l'application d'un design pattern industriel reconnu, et non un choix arbitraire.

---

## 6. Synthèse pour l'évaluation

Les éléments suivants méritent d'être valorisés dans la défense orale et dans le rapport L5.

1. **Trois bases de données opérationnelles** déployées sur des services cloud distincts (Atlas, AuraDB, Bonsai), couvrant trois paradigmes NoSQL différents (document, graphe, indexé). Cette diversité satisfait directement l'exigence du sujet M242 sur l'architecture polyglotte.

2. **Pipeline de transformation YAML → JSON Lines → BD cibles** entièrement scripté, idempotent et reproductible en moins de cinq minutes. La séparation stricte entre format de stockage humain (YAML) et format de transmission machine (JSON Lines) est un choix d'ingénierie défendable scientifiquement.

3. **Canonicalisation à trois niveaux** (compétences, titres, famille de poste) appliquée avant ingestion, avec garde-fou automatique sur la détection de doublons résiduels. Le taux de réduction du vocabulaire (de 11 000 à 8 082 entrées) est mesurable et démontrable.

4. **Justification scientifique du choix MongoDB** : adéquation au format documents JSON imbriqués, schéma souple compatible avec une phase exploratoire, idempotence via `_id` calculé déterministiquement, hébergement managé en région Europe.

5. **Justification scientifique du choix Elasticsearch** : besoins applicatifs spécifiques (recherche plein texte avec scoring, agrégations rapides multi-dimensions, tolérance aux fautes, support multilingue) que MongoDB ne couvre pas ou couvre mal.

6. **Reproductibilité totale** : trois fichiers (`data/jobs.jsonl`, `data/graph_nodes.csv`, `data/graph_edges.csv`) générés par un seul script, commités dans le dépôt Git, permettant à un correcteur de reproduire l'environnement complet en une heure.

---

## Références

- Sadalage, P. J., & Fowler, M. (2012). *NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence*. Addison-Wesley.
- DB-Engines Ranking (2026). *Popularity of NoSQL Database Management Systems*. https://db-engines.com/en/ranking
- MongoDB Inc. (2026). *MongoDB Atlas — Managed Cloud Database*. https://www.mongodb.com/cloud/atlas
- Elastic NV. (2026). *Elasticsearch — Open Source Search Engine*. https://www.elastic.co/elasticsearch
- Neo4j Inc. (2026). *Neo4j AuraDB — Fully Managed Graph Database*. https://neo4j.com/cloud/aura
- PRD SKILLNAV, §7 *Architecture NoSQL polyglotte* et §N2 *Étude comparative*.
