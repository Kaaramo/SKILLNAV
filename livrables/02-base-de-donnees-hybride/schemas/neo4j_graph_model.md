# Schéma Neo4j — graphe SKILLNAV

> Cluster : Neo4j AuraDB (free tier)
> Driver : `neo4j-python-driver` v5 (asynchrone)
> Code de référence : `skillnav/db/neo4j/client.py`, `skillnav/schemas/converters/to_neo4j.py`

---

## Connexion

Le client est instancié via la factory `make_neo4j_client()`. Les paramètres
viennent de `.env` (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`).

```python
from skillnav.db.neo4j.client import make_neo4j_client

async with make_neo4j_client() as neo:
    result = await neo.run("MATCH (s:Skill) RETURN count(s) AS n")
```

---

## Labels (5 types de nœuds)

Définitions dans `skillnav/schemas/graph.py`.

### `(:Skill)` — compétence canonique

| Propriété | Type | Description |
|---|---|---|
| `name` | `str` | Nom canonique de la compétence (clé unique) |
| `aliases` | `list[str]` | Variantes orthographiques détectées (`"pyspark"`, `"PySpark"`, …) |
| `family` | `str` | Famille SKILLNAV (`"GenAI"`, `"NLP"`, `"MLOps"`, etc. — voir `SkillFamily`) |
| `pagerank_score` | `float` | Score PageRank calculé sur la projection Skill-Skill |
| `community_id` | `int` | Identifiant de la communauté Louvain |
| `occurrence_count` | `int` | Nombre d'offres dans lesquelles la compétence apparaît |

### `(:Job)` — offre d'emploi

| Propriété | Type | Description |
|---|---|---|
| `job_id` | `str` | Clé unique (même qu'en Mongo) |
| `title` | `str` | Titre |
| `company` | `str` | Nom employeur |
| `country` | `str` | `MA`, `US`, `IN`, … |
| `source` | `str` | Plateforme d'origine |
| `published_at` | `datetime` | Date de publication |

### `(:Company)` — entreprise

| Propriété | Type | Description |
|---|---|---|
| `name` | `str` | Nom (clé unique) |
| `country` | `str` | Pays principal |
| `job_count` | `int` | Nombre d'offres publiées dans le corpus |

### `(:SkillFamily)` — famille de compétences

| Propriété | Type | Description |
|---|---|---|
| `name` | `str` | Nom de la famille (`"GenAI"`, `"NLP"`, …) |
| `description` | `str` | Description courte |

### `(:Source)` — plateforme d'origine

| Propriété | Type | Description |
|---|---|---|
| `name` | `str` | `rekrute`, `linkedin-ma`, `intl-ai-corpus`, … |
| `base_url` | `str` | URL canonique de la plateforme |

---

## Relations (4 types d'arêtes)

### `(:Skill)-[:CO_OCCURS_WITH {weight, period}]->(:Skill)`

Arête non-orientée (en pratique stockée comme orientée mais traversée dans
les deux sens). Le poids `weight` est le nombre d'offres dans lesquelles les
deux compétences apparaissent ensemble.

```cypher
MATCH (a:Skill {name: "Python"})-[r:CO_OCCURS_WITH]-(b:Skill)
RETURN b.name AS voisin, r.weight AS poids
ORDER BY poids DESC LIMIT 10
```

### `(:Job)-[:REQUIRES {confidence}]->(:Skill)`

Indique qu'une offre demande une compétence. `confidence` ∈ [0, 1] est le
score de l'extraction.

### `(:Skill)-[:BELONGS_TO]->(:SkillFamily)`

Rattache chaque compétence à exactement une famille.

### `(:Company)-[:POSTED_BY]->(:Job)`

Indique qu'une entreprise a publié une offre.

---

## Contraintes et indexes

Les contraintes d'unicité sont créées par `push_graph_to_neo4j()` avant tout
chargement de données :

```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (j:Job)   REQUIRE j.job_id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (f:SkillFamily) REQUIRE f.name IS UNIQUE;
```

Indexes secondaires sur les propriétés filtrantes courantes :

```cypher
CREATE INDEX IF NOT EXISTS FOR (j:Job) ON (j.country);
CREATE INDEX IF NOT EXISTS FOR (j:Job) ON (j.source);
CREATE INDEX IF NOT EXISTS FOR (s:Skill) ON (s.family);
```

---

## Algorithmes exécutés sur le graphe

| Algorithme | Lib | Sortie écrite dans Neo4j |
|---|---|---|
| Louvain | `networkx.algorithms.community.louvain_communities` | `Skill.community_id` |
| Leiden (comparaison) | `igraph` | métriques uniquement |
| Label Propagation (comparaison) | `networkx` | métriques uniquement |
| PageRank | `networkx.pagerank` | `Skill.pagerank_score` |

Les métriques globales (modularité, nombre de nœuds, nombre d'arêtes,
top 20 PageRank) sont sérialisées en parallèle dans MongoDB
(`graph_metrics` collection) pour servir le dashboard sans interroger Neo4j à
chaque page.

---

## Snapshot de référence (au 2026-05-17)

| Élément | Compte |
|---|---|
| `(:Skill)` nœuds | ~2 187 |
| `(:Job)` nœuds | 3 467 |
| `(:Company)` nœuds | ~900 |
| `(:SkillFamily)` nœuds | 14 |
| `(:CO_OCCURS_WITH)` arêtes | ~38 000 (non-dirigées) |
| `(:REQUIRES)` arêtes | ~22 000 |
| Modularité Louvain | Q = 0,256 |
| Modularité Leiden | Q = 0,298 (meilleure mais marginal) |

Les valeurs exactes au moment du jury sont disponibles via la requête de
vérification dans [`../queries/neo4j_examples.cypher`](../queries/neo4j_examples.cypher).
