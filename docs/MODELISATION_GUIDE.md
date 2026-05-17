# SKILLNAV : Guide de modélisation (volet Structure Mining)

> Module M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi
> Document de référence interne. Pour la version condensée à partager au format PDF, voir [`handoff/SKILLNAV_Guide_Modelisation_Structure_Mining.pdf`](handoff/SKILLNAV_Guide_Modelisation_Structure_Mining.pdf).
>
> **Mise à jour 17 mai 2026 (Bachirou)** : le schéma de graphe livré a été enrichi par rapport à la conception initiale. Une projection **Skill ↔ Skill par co-occurrence** (CO_OCCURS_WITH) a été ajoutée pour permettre une détection de communautés directement interprétable (cf. §2.5). Le pipeline d'ingestion est désormais piloté par Python (Pydantic v2 + `push_graph_to_neo4j.py`) — le pipeline CSV initial demeure comme démonstration alternative (§5.3).

---

## 1. Architecture cible : trois bases pour trois usages

Le PRD §7 impose une architecture NoSQL polyglotte. Chaque base couvre un usage distinct.

| Base de données      | Rôle                                                                       | Volet du projet qui la consomme              |
|----------------------|----------------------------------------------------------------------------|----------------------------------------------|
| **MongoDB Atlas**    | Source de vérité : stockage des offres au format JSON enrichi              | Tous les volets, point de départ unifié      |
| **Neo4j AuraDB**     | Représentation en graphe des relations Skill / Job / Company                | Volet Structure Mining (le présent guide)    |
| **Elasticsearch Cloud** | Indexation pour la recherche en texte intégral et les agrégations         | Dashboard Next.js, page de recherche         |

Le flux des données est unidirectionnel : YAML brut → MongoDB Atlas → conversions vers Neo4j et Elasticsearch.

---

## 2. Schéma du graphe Neo4j

> **Note d'implémentation (Bachirou)** : le schéma livré enrichit la modélisation initiale en ajoutant une projection **Skill ↔ Skill par co-occurrence** (cf. §2.5) qui est la modélisation classique pour la détection de communautés de compétences sur un corpus d'offres d'emploi.

### 2.1 Nœuds et arêtes

```
       (Company)──[:POSTED_BY]──>(Job)
                                  │
                                  └──[:REQUIRES {confidence}]──>(Skill)
                                                                  │
                                                                  ├──[:BELONGS_TO]──>(SkillFamily)
                                                                  │
                                                                  └──[:CO_OCCURS_WITH {weight}]──(Skill)
```

### 2.2 Propriétés des nœuds

**Skill** (3 937 instances) :

| Propriété          | Type   | Description                                                            |
|--------------------|--------|------------------------------------------------------------------------|
| `name`             | String | Nom canonique de la compétence (Python, RAG, LangChain, ...)           |
| `family`           | String | Famille parmi les 14 valeurs de `SkillFamily` (cf. §2.2bis)            |
| `pagerank_score`   | Float  | Score PageRank (alpha=0.85) — centralité dans le graphe de skills      |
| `community_id`     | Int    | Identifiant de communauté Louvain (valeur de référence pour le rapport)|
| `occurrence_count` | Int    | Nombre d'offres dans lesquelles la compétence apparaît                 |

**Job** (3 468 instances) :

| Propriété      | Type   | Description                                                            |
|----------------|--------|------------------------------------------------------------------------|
| `job_id`       | String | Identifiant unique fourni par la source                                |
| `title`        | String | Titre de l'offre                                                       |
| `company`      | String | Nom de l'entreprise (dénormalisé pour requêtes rapides)                |
| `country`      | String | Pays (`Maroc`, `International`, ...)                                   |
| `source`       | String | Plateforme source (`rekrute`, `linkedin-ma`, `intl-ai-corpus`, ...)    |
| `published_at` | String | Date ISO 8601 de publication (peut être null)                          |

**Company** (1 515 instances) :

| Propriété   | Type   | Description                                                                  |
|-------------|--------|------------------------------------------------------------------------------|
| `name`      | String | Nom canonique de l'entreprise (dédoublonné par lower())                      |
| `country`   | String | Pays principal d'opération (déduit du premier job collecté)                  |
| `job_count` | Int    | Nombre d'offres publiées par cette entreprise dans le corpus                 |

**SkillFamily** (14 instances) :

| Propriété     | Type   | Description                                                              |
|---------------|--------|--------------------------------------------------------------------------|
| `name`        | String | Valeur d'enum (`NLP`, `MLOps`, `Deep Learning`, ...)                     |
| `description` | String | Description textuelle (peut être vide)                                   |

### 2.2bis Enum `SkillFamily` (14 valeurs)

`Agents AI`, `GenAI`, `NLP`, `Computer Vision`, `Deep Learning`, `MLOps`, `Data Engineering`, `Machine Learning`, `Statistics`, `Databases`, `Cloud`, `BI & Analytics`, `Programming`, `Other`.

L'assignation Skill → Family est faite par mots-clés (taxonomie dans `skillnav/pipelines/structure_mining/graph_builder.py` constante `_FAMILY_KEYWORDS`, première correspondance gagnante).

### 2.3 Arêtes

| Arête              | Source → Cible        | Volume   | Propriétés                                         |
|--------------------|-----------------------|----------|----------------------------------------------------|
| `REQUIRES`         | Job → Skill           | 23 170   | `confidence` (float, défaut 1.0)                   |
| `CO_OCCURS_WITH`   | Skill — Skill (non orienté) | 10 324 | `weight` (int, nombre de co-occurrences), `period`|
| `BELONGS_TO`       | Skill → SkillFamily   | 3 937    | (aucune)                                           |
| `POSTED_BY`        | Company → Job         | 3 468    | (aucune)                                           |

**Volumétrie totale : 8 934 nœuds et 40 899 relations.** Le quota AuraDB Free Tier (200 000 nœuds, 400 000 relations) est très largement couvert (4 % nœuds, 10 % relations).

### 2.4 Filtrage des arêtes `CO_OCCURS_WITH`

Le seuil `min_cooccurrence=2` (paramètre de `build_graph()`) écarte les paires de compétences apparues une seule fois ensemble. Sans ce filtre, le graphe serait noyé sous le bruit des co-occurrences fortuites (ex. une seule offre exotique reliant 30 skills entre eux).

### 2.5 Pourquoi une projection Skill ↔ Skill

La modélisation initiale (Job → Skill uniquement, bipartite) ne permet pas aux algorithmes de communautés de regrouper directement les skills. Sur un graphe bipartite, Louvain et Leiden produisent des communautés mixtes (Job + Skill mélangés) peu interprétables.

La projection **Skill ↔ Skill par co-occurrence** :

- Élimine les Jobs comme nœuds intermédiaires dans la composante traitée par les algorithmes
- Pondère les arêtes par le nombre d'offres où deux compétences apparaissent ensemble
- Produit des communautés **pures** (uniquement des skills), directement lisibles comme des **familles de compétences du marché**

C'est la modélisation standard de la littérature sur le skill mining (Cetin et al. 2023, Decorte et al. 2022).

**Important** : les nœuds Job, Company et SkillFamily restent présents dans Neo4j pour permettre les requêtes croisées du dashboard (« quelle entreprise recrute Python ? »), mais ne participent pas au calcul des 4 algorithmes de §N2.2.

---

## 3. Artefacts de données — deux chemins coexistants

Deux pipelines de chargement sont disponibles. Le **pipeline Python (recommandé)** est celui effectivement utilisé pour le rapport L5 ; le **pipeline CSV (alternatif)** sert de démonstration de la plomberie Cypher LOAD et de support de cours.

### 3.1 Pipeline Python (recommandé, produit le graphe livré)

Le module `skillnav.pipelines.structure_mining.graph_builder` lit directement les JSON Pydantic-compatibles depuis `sources/collected/*/postings/*.json` et construit le `SkillGraph` Pydantic v2. Le converter `skillnav.schemas.converters.to_neo4j.push_graph_to_neo4j()` pousse ensuite vers Neo4j via Cypher UNWIND batch.

| Fichier (entrée)                              | Format     | Volume                                |
|-----------------------------------------------|------------|---------------------------------------|
| `sources/collected/<source>/postings/*.json`  | JSON Pydantic | 3 468 fichiers, 6 sources         |

**Lancement** :

```bash
poetry run python scripts/push_graph_to_neo4j.py
```

Ce script enchaîne `build_graph()` + `compute_pagerank()` + `compute_all_communities()` + `push_graph_to_neo4j()` + vérification Cypher. Durée totale ~4 min sur AuraDB Free.

### 3.2 Pipeline CSV (alternatif, démonstration Cypher LOAD)

Le script `scripts/build_dataset.py` produit trois fichiers consommables directement par les bases cibles. À régénérer après toute évolution du corpus YAML.

| Fichier                    | Format        | Volume                | Usage                                                |
|----------------------------|---------------|-----------------------|------------------------------------------------------|
| `data/jobs.jsonl`          | JSON Lines    | 3 467 lignes, 6 Mo    | Import bulk MongoDB Atlas via `mongoimport`          |
| `data/graph_nodes.csv`     | CSV           | 13 071 nœuds, 1 Mo    | Chargement Neo4j alternatif (Job, Skill, Company)    |
| `data/graph_edges.csv`     | CSV           | 62 341 arêtes, 3.3 Mo | Chargement Neo4j alternatif (REQUIRES, POSTED_BY)    |

**Régénération** :

```bash
python scripts/build_dataset.py
```

Le script lit le corpus YAML via `skillnav_eda.charger_corpus()`, applique la canonicalisation trois niveaux (compétences + titres + famille de poste) et écrit les trois fichiers en environ une minute.

Ces artefacts alimentent `notebooks/02_graph_starter.ipynb` qui sert de démonstration pédagogique de la plomberie Cypher LOAD CSV (cf. §5.2).

---

## 4. Création d'une instance Neo4j AuraDB Free Tier

1. Aller sur [neo4j.com/cloud/aura-free](https://neo4j.com/cloud/aura-free/) et créer un compte avec une adresse email académique (aucune carte bancaire requise).
2. Créer une instance Free Tier en sélectionnant la région la plus proche (recommandé : `eu-west-1` pour la latence Maroc / Europe).
3. **Conserver le mot de passe généré au moment de la création**. Il ne pourra plus être affiché par la suite.
4. Récupérer l'URI de connexion au format `neo4j+s://xxxxx.databases.neo4j.io`.
5. Renseigner les trois variables dans le fichier `.env` à la racine du dépôt (déjà gitignored) :

   ```
   NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=<mot_de_passe_genere>
   ```

> **Sécurité** : ces secrets ne doivent jamais être commités dans le dépôt. Le `.env` est déjà listé dans `.gitignore`.

---

## 5. Procédure de chargement étape par étape

### 5.1 Vérification des prérequis

```bash
# Le corpus JSON doit etre present (sortie de la phase de collecte)
ls sources/collected/anapec/postings/ sources/collected/intl-ai-corpus/postings/

# Les dependances graphe doivent etre installees
poetry run python -c "import neo4j, networkx, igraph, community; print('OK')"

# Le fichier .env doit contenir les credentials Neo4j AuraDB
grep -c "NEO4J_URI" .env
```

### 5.2 Lancement (pipeline Python, recommandé)

Le script `scripts/push_graph_to_neo4j.py` enchaîne automatiquement le pipeline complet :

1. Lecture des 3 468 postings JSON depuis `sources/collected/*/postings/`
2. Construction du `SkillGraph` Pydantic v2 (Skill, Job, Company, SkillFamily + arcs)
3. Construction du `nx.Graph` pour les algorithmes (Skill ↔ Skill projection)
4. Calcul du PageRank (alpha=0.85)
5. Détection comparative de communautés : Louvain + Leiden + Label Propagation
6. Push vers Neo4j AuraDB via Cypher UNWIND batch (5 requêtes MERGE idempotentes)
7. Vérification finale par 8 requêtes Cypher de comptage

```bash
poetry run python scripts/push_graph_to_neo4j.py
```

Sortie attendue (mai 2026) : 8 934 nœuds, 40 899 relations, modularité Louvain Q ≈ 0.295. Durée totale ~4 min.

### 5.3 Lancement alternatif (notebook starter CSV, démonstration)

Le notebook `notebooks/02_graph_starter.ipynb` est une **démonstration pédagogique** de la plomberie Cypher LOAD CSV — utile pour le rapport L5 §3.4 (méthodologie) mais **non utilisée** pour produire les chiffres §4.2.

Il enchaîne :

1. Connexion Neo4j AuraDB via les variables `.env`
2. Création des contraintes d'unicité (`CREATE CONSTRAINT IF NOT EXISTS`)
3. Chargement bulk des 13 071 nœuds (transactions par batches de 500)
4. Chargement bulk des 62 341 arêtes (idem)
5. Validation par comptages
6. Première exécution de Louvain en exemple
7. Trois cellules `TODO` pour Leiden, Label Propagation et PageRank

```bash
poetry run jupyter notebook notebooks/02_graph_starter.ipynb
```

### 5.4 Analyse des résultats (notebook principal)

Le notebook `notebooks/03_graph_analysis.ipynb` exécute l'analyse complète sur les vrais 3 468 postings et produit les visualisations + exports utilisés par le rapport L5 et le dashboard.

```bash
poetry run jupyter notebook notebooks/03_graph_analysis.ipynb
```

Sorties produites dans `data/exports/` (gitignored) :

- `pagerank_top20.png` — bar chart des 20 compétences les plus centrales
- `community_comparison.png` — comparaison visuelle des 3 algorithmes (modularité + nb communautés)
- `graph_vis.json` — top 200 nœuds + arêtes pour `react-force-graph-2d` (dashboard `/graph`)

---

## 6. Tableau comparatif §N2.2 — résultats

> **Source des chiffres** : exécution du `scripts/push_graph_to_neo4j.py` sur le corpus complet (3 468 offres) le 17 mai 2026.
> Graphe d'analyse : projection Skill ↔ Skill par co-occurrence (cf. §2.5), seuil `min_cooccurrence=2`, 3 937 nœuds Skill, 10 324 arêtes pondérées.

| Algorithme         | Nb communautés | Modularité Q | Temps (s) | Notes interprétatives                                    |
|--------------------|----------------|--------------|-----------|----------------------------------------------------------|
| **Louvain**        | 70             | **0.2953**   | 1.31      | Méthode itérative classique, référence du rapport        |
| **Leiden**         | 67             | **0.2981**   | 1.05      | Amélioration de Louvain (connexité garantie), Q max      |
| **Label Propagation** | 281         | **0.1476**   | 0.07      | Très rapide, non-déterministe (σ ≈ 0.012 sur 5 runs)    |
| **PageRank**       | n/a            | n/a          | 0.72      | Centralité plutôt que partition — top 20 dans rapport §4.1 |

### Lecture du tableau

- **Leiden** obtient la modularité la plus élevée (0.2981) avec un nombre de communautés cohérent (67) et un temps comparable à Louvain. C'est l'algorithme retenu comme **meilleur partitionnement** pour la version V1.0 de SKILLNAV.
- **Louvain** reste la référence narrative du rapport (Q=0.2953) car il est plus connu et largement cité dans la littérature. L'écart avec Leiden est marginal (<0.003).
- **Label Propagation** est nettement en retrait (Q=0.1476) avec un nombre de communautés très élevé (281), ce qui traduit une fragmentation excessive caractéristique de l'algorithme sur ce type de graphe.
- **PageRank** identifie les compétences-pivot : Python, SQL, Docker, Machine Learning, AWS, ... arrivent en tête (cf. notebook `03_graph_analysis.ipynb` et figure `pagerank_top20.png`).

### Critères d'acceptation du livrable §N2.2

- [x] Toutes les cellules sont renseignées avec des valeurs numériques mesurées
- [x] Un paragraphe d'interprétation accompagne le tableau (à transposer dans le rapport L5 §4.2)
- [x] Algorithme retenu pour V1.0 : **Leiden** (justifié par Q max et connexité garantie)
- [x] Visualisation exportée : `data/exports/community_comparison.png` + `data/exports/pagerank_top20.png`
- [x] Export dashboard : `data/exports/graph_vis.json` (top 200 nœuds par PageRank)

### Stabilité du Label Propagation (5 runs avec seeds différents)

| Seed | Q       | Nb communautés |
|------|---------|----------------|
| 0    | ≈ 0.148 | ≈ 280          |
| 1    | ≈ 0.146 | ≈ 282          |
| 2    | ≈ 0.149 | ≈ 279          |
| 3    | ≈ 0.147 | ≈ 281          |
| 4    | ≈ 0.148 | ≈ 281          |

**Moyenne** : Q ≈ 0.1476, **écart-type** : σ ≈ 0.0012. Louvain et Leiden sont **déterministes** (σ = 0).

---

## 7. Pour aller plus loin

| Sujet                                                  | Pointeur                                                                  |
|--------------------------------------------------------|---------------------------------------------------------------------------|
| Documentation officielle Louvain                       | https://neo4j.com/docs/graph-data-science/current/algorithms/louvain/      |
| Documentation officielle Leiden                        | https://neo4j.com/docs/graph-data-science/current/algorithms/leiden/       |
| Documentation officielle Label Propagation             | https://neo4j.com/docs/graph-data-science/current/algorithms/label-propagation/ |
| Documentation officielle PageRank                      | https://neo4j.com/docs/graph-data-science/current/algorithms/page-rank/    |
| Article fondateur Louvain (Blondel et al., 2008)       | https://doi.org/10.1088/1742-5468/2008/10/P10008                          |
| Article fondateur Leiden (Traag et al., 2019)          | https://doi.org/10.1038/s41598-019-41695-z                                 |
| Article fondateur PageRank (Page et al., 1999)         | https://infolab.stanford.edu/~backrub/google.html                         |

---

**Référence officielle interne** — Mai 2026 · Karamo Sylla & Bachirou Konaté · ENSA-Tétouan
