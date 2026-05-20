# Schéma Elasticsearch — index `skillnav_jobs`

> Cluster : Bonsai (OpenSearch 2.x, fork open source d'Elasticsearch)
> Pourquoi OpenSearch : Bonsai sandbox est gratuit jusqu'à 125 MB, suffisant
> pour les 3 467 documents du corpus.
> Driver : `opensearch-py` (compatible API ES 7.x et OS 1.x/2.x)
> Code de référence : `scripts/ingestion/ingest_elasticsearch.py`

---

## Connexion

```python
from opensearchpy import OpenSearch
from urllib.parse import urlparse
parsed = urlparse(os.environ["ELASTIC_URL"])
client = OpenSearch(
    hosts=[{"host": parsed.hostname, "port": parsed.port or 443}],
    http_auth=(parsed.username, parsed.password),
    use_ssl=True,
    verify_certs=True,
)
```

L'URL stockée dans `.env` (`ELASTIC_URL`) inclut les credentials et n'est jamais
committée.

---

## Mapping de l'index `skillnav_jobs`

### Settings

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "analysis": {
      "analyzer": {
        "fr_en_mixed": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding"]
        }
      }
    }
  }
}
```

Analyzer `fr_en_mixed` : tokenization standard + lowercase + `asciifolding`
(suppression des diacritiques). Choisi pour gérer les fiches mélangeant français
et anglais sans faire d'erreur sur les accents (`données` ↔ `donnees`).

### Mapping des champs

```json
{
  "mappings": {
    "properties": {
      "origine":           { "type": "keyword" },
      "source":            { "type": "keyword" },
      "posted_month":      { "type": "keyword" },
      "title": {
        "type": "text", "analyzer": "fr_en_mixed",
        "fields": { "raw": { "type": "keyword" } }
      },
      "title_canonical":   { "type": "keyword" },
      "job_family":        { "type": "keyword" },
      "ai_type":           { "type": "keyword" },
      "company": {
        "type": "keyword",
        "fields": { "text": { "type": "text", "analyzer": "fr_en_mixed" } }
      },
      "stage":             { "type": "keyword" },
      "focus":             { "type": "text", "analyzer": "fr_en_mixed" },
      "is_customer_facing": { "type": "boolean" },
      "is_management":     { "type": "boolean" },
      "responsibilities":  { "type": "text", "analyzer": "fr_en_mixed" },
      "use_cases":         { "type": "text", "analyzer": "fr_en_mixed" },
      "skills": {
        "properties": {
          "genai":     { "type": "keyword" },
          "ml":        { "type": "keyword" },
          "web":       { "type": "keyword" },
          "databases": { "type": "keyword" },
          "data":      { "type": "keyword" },
          "cloud":     { "type": "keyword" },
          "ops":       { "type": "keyword" },
          "languages": { "type": "keyword" },
          "domains":   { "type": "keyword" },
          "other":     { "type": "keyword" }
        }
      },
      "skills_all":        { "type": "keyword" }
    }
  }
}
```

### Pourquoi ce mapping

| Décision | Raison |
|---|---|
| `title` en `text` + sous-champ `.raw` keyword | Recherche full-text **et** tri/facette sur le titre exact |
| `company` en `keyword` + sous-champ `.text` | Agréger par entreprise (facette) et chercher partial-match |
| Toutes les sous-listes de skills en `keyword` | Compétences = vocabulaire fermé, pas besoin de tokenization |
| `skills_all` aplati en `keyword` | Permet une seule agrégation cross-famille (top-N skills toutes catégories confondues) |
| Pas de date typée `date` sur `posted_month` | Garder le format `YYYY-MM` (string) pour simplifier les agrégations par mois |
| 1 shard, 0 replica | Volume modeste (3 467 docs ≈ 5 MB), un seul shard est plus rapide |

---

## Cas d'usage typiques (ce que cette base sait faire mieux que Mongo et Neo4j)

### 1. Recherche full-text scoring BM25

```json
GET /skillnav_jobs/_search
{
  "query": {
    "multi_match": {
      "query": "python pandas pyspark",
      "fields": ["title^3", "responsibilities", "focus"]
    }
  },
  "size": 10
}
```

Mongo le ferait avec son text index mais sans pondération fine, ES retourne les
documents triés par pertinence avec un boost configurable sur le titre.

### 2. Agrégation temporelle + facette

```json
GET /skillnav_jobs/_search
{
  "size": 0,
  "aggs": {
    "par_mois": {
      "terms": { "field": "posted_month", "size": 36, "order": { "_key": "asc" } },
      "aggs": { "par_famille": { "terms": { "field": "job_family", "size": 13 } } }
    }
  }
}
```

Permet de produire en une requête le tableau croisé mois × famille métier qui
sert à plusieurs pages du dashboard.

### 3. Top compétences sur un sous-ensemble

```json
GET /skillnav_jobs/_search
{
  "size": 0,
  "query": { "term": { "origine": "Maroc" } },
  "aggs": {
    "top_skills": { "terms": { "field": "skills_all", "size": 20 } }
  }
}
```

Le champ aplati `skills_all` évite de fusionner 10 agrégations distinctes.

---

## Volume

| Indicateur | Valeur |
|---|---|
| Documents indexés | **3 467** |
| Taille de l'index | ~5 MB |
| Limite Bonsai sandbox | 125 MB (largement sous le plafond) |
| Latence moyenne d'une requête multi_match | ~30 ms |

D'autres exemples concrets avec leurs résultats dans
[`../queries/elasticsearch_examples.md`](../queries/elasticsearch_examples.md).
