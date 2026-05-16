# SKILLNAV : Guide de modélisation (volet Structure Mining)

> Module M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi
> Document de référence interne. Pour la version condensée à partager au format PDF, voir [`handoff/SKILLNAV_Guide_Modelisation_Structure_Mining.pdf`](handoff/SKILLNAV_Guide_Modelisation_Structure_Mining.pdf).

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

### 2.1 Nœuds et arêtes

```
       (Job)─[:POSTED_BY]──>(Company)
        │
        └─[:REQUIRES { weight: int }]──>(Skill)
```

### 2.2 Propriétés des nœuds

**Job** (3 467 instances) :

| Propriété          | Type   | Description                                                            |
|--------------------|--------|------------------------------------------------------------------------|
| `node_id`          | String | Identifiant unique au format `job_<source>_<job_id>`                   |
| `title_canonical`  | String | Titre normalisé via canonicalisation (Data Scientist, AI Engineer...)  |
| `ai_type`          | String | `ai-first`, `ai-support`, `ml-first` ou `non-ai`                       |
| `job_family`       | String | Famille canonique parmi les 13 du schéma SKILLNAV                      |
| `posted_month`     | String | Mois de publication au format `YYYY-MM`                                |
| `origine`          | String | `Maroc` ou `International`                                             |
| `source`           | String | Plateforme source (`rekrute`, `linkedin-ma`, `intl-ai-corpus`, ...)    |

**Skill** (8 082 instances) :

| Propriété  | Type   | Description                                                                 |
|------------|--------|-----------------------------------------------------------------------------|
| `node_id`  | String | Identifiant unique au format `skill_<nom_canonique_alphanumerise>`          |
| `name`     | String | Nom canonicalisé de la compétence (Python, RAG, LangChain, ...)             |
| `famille`  | String | Famille parmi `genai`, `ml`, `web`, `databases`, `data`, `cloud`, `ops`, `languages`, `domains`, `other` |

**Company** (1 522 instances) :

| Propriété | Type   | Description                                                                  |
|-----------|--------|------------------------------------------------------------------------------|
| `node_id` | String | Identifiant unique au format `company_<nom_alphanumerise>`                   |
| `name`    | String | Nom de l'entreprise tel que collecté                                         |
| `stage`   | String | Stade de financement (Public, Series B, Seed...), souvent renseigné côté INTL |
| `focus`   | String | Domaine d'activité (texte libre court)                                        |

### 2.3 Arêtes

| Arête       | Source → Cible      | Volume     | Propriétés         |
|-------------|---------------------|------------|--------------------|
| `REQUIRES`  | Job → Skill         | 58 874     | `weight` (entier)  |
| `POSTED_BY` | Job → Company       | 3 467      | (aucune)           |

**Volumétrie totale : 13 071 nœuds et 62 341 arêtes.** Le quota AuraDB Free Tier (50 000 nœuds, 175 000 relations) est largement couvert (26 % nœuds, 36 % relations).

---

## 3. Artefacts de données prêts à l'emploi

Le script `scripts/build_dataset.py` produit trois fichiers consommables directement par les bases cibles. À régénérer après toute évolution du corpus YAML.

| Fichier                    | Format        | Volume         | Usage                                                |
|----------------------------|---------------|----------------|------------------------------------------------------|
| `data/jobs.jsonl`          | JSON Lines    | 3 467 lignes, 6 Mo | Import bulk MongoDB Atlas via `mongoimport`      |
| `data/graph_nodes.csv`     | CSV           | 13 071 nœuds, 1 Mo | Chargement Neo4j (Job, Skill, Company)            |
| `data/graph_edges.csv`     | CSV           | 62 341 arêtes, 3.3 Mo | Chargement Neo4j (REQUIRES, POSTED_BY)        |

**Régénération** :

```bash
python scripts/build_dataset.py
```

Le script lit le corpus YAML via `skillnav_eda.charger_corpus()`, applique la canonicalisation trois niveaux (compétences + titres + famille de poste) et écrit les trois fichiers en environ une minute.

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
# Les trois CSV doivent exister
ls data/jobs.jsonl data/graph_nodes.csv data/graph_edges.csv

# Le driver Python neo4j doit être installé
poetry run python -c "import neo4j; print(neo4j.__version__)"
```

### 5.2 Lancement du notebook starter

Le notebook `notebooks/02_graph_starter.ipynb` enchaîne automatiquement :

1. Connexion Neo4j AuraDB via les variables `.env`
2. Création des contraintes d'unicité (`CREATE CONSTRAINT IF NOT EXISTS`)
3. Chargement bulk des 13 071 nœuds (transactions par batches de 500)
4. Chargement bulk des 62 341 arêtes (idem)
5. Validation par comptages
6. Première exécution de Louvain en exemple
7. Trois cellules `TODO` pour Leiden, Label Propagation et PageRank

Lancer le notebook :

```bash
poetry run jupyter notebook notebooks/02_graph_starter.ipynb
```

Temps total estimé de chargement : 3 à 5 minutes sur AuraDB Free Tier.

---

## 6. Tableau comparatif §N2.2 (à compléter et reporter dans le rapport L5)

Après exécution des quatre algorithmes dans le notebook starter, compléter le tableau ci-dessous. Les colonnes attendues sont alignées avec la section §N2.2 du PRD et la grille d'évaluation §16 du rapport L5.

| Algorithme         | Nombre de communautés | Modularité    | Temps (s)     | Notes interprétatives                            |
|--------------------|-----------------------|---------------|---------------|--------------------------------------------------|
| Louvain            | _à compléter_         | _à compléter_ | _à compléter_ | Méthode itérative classique                      |
| Leiden             | _à compléter_         | _à compléter_ | _à compléter_ | Amélioration de Louvain (connexité garantie)     |
| Label Propagation  | _à compléter_         | _à compléter_ | _à compléter_ | Très rapide, non-déterministe                    |
| PageRank           | n/a                   | n/a           | _à compléter_ | Centralité plutôt que partition                  |

### Critères d'acceptation du livrable §N2.2

- Toutes les cellules « à compléter » sont renseignées avec des valeurs numériques.
- Un paragraphe d'interprétation de deux à trois lignes accompagne le tableau dans le rapport L5.
- L'algorithme retenu pour la version 1.0 de SKILLNAV est justifié explicitement.
- Une visualisation du graphe est exportée en PNG haute résolution depuis Neo4j Bloom ou via `py2neo` + `networkx`.

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
