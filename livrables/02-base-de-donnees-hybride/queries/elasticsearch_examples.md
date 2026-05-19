# Exemples de requêtes Elasticsearch — index `skillnav_jobs`

Cinq requêtes représentatives. Toutes ont été testées sur le cluster Bonsai
réel au 2026-05-17. Les requêtes sont écrites en syntaxe Query DSL ; elles
fonctionnent via `curl`, Kibana / OpenSearch Dashboards, ou depuis Python via
`opensearch-py`.

---

## 1. Comptage simple

```bash
GET /skillnav_jobs/_count
```

**Résultat** : `{ "count": 3467 }`

---

## 2. Recherche full-text « LLM RAG production »

```json
GET /skillnav_jobs/_search
{
  "size": 5,
  "_source": ["title", "company", "origine", "ai_type"],
  "query": {
    "multi_match": {
      "query": "LLM RAG production",
      "fields": ["title^3", "responsibilities", "focus"]
    }
  }
}
```

**Résultat** (extrait) :

```json
{
  "hits": {
    "total": { "value": 412 },
    "hits": [
      { "_score": 18.4, "_source": { "title": "AI Engineer — LLM Production", "company": "Anthropic" } },
      { "_score": 17.2, "_source": { "title": "Senior ML Engineer (RAG, LLMs)", "company": "Scale AI" } },
      { "_score": 15.8, "_source": { "title": "Lead GenAI Engineer", "company": "Lyft" } }
    ]
  }
}
```

Le boost `^3` sur le `title` met en avant les titres qui contiennent
explicitement les mots cherchés. Mongo ferait la même recherche, mais sans le
contrôle fin du scoring.

---

## 3. Tableau croisé mois × famille métier

```json
GET /skillnav_jobs/_search
{
  "size": 0,
  "aggs": {
    "par_mois": {
      "terms": { "field": "posted_month", "size": 36, "order": { "_key": "asc" } },
      "aggs": {
        "par_famille": { "terms": { "field": "job_family", "size": 13 } }
      }
    }
  }
}
```

**Résultat** (échantillon, mois `2025-04`) :

```json
{
  "key": "2025-04",
  "doc_count": 312,
  "par_famille": {
    "buckets": [
      { "key": "AI_ENGINEER",     "doc_count": 124 },
      { "key": "DATA_SCIENTIST",  "doc_count":  68 },
      { "key": "ML_ENGINEER",     "doc_count":  45 },
      ...
    ]
  }
}
```

Une seule requête produit le tableau croisé complet que le dashboard consomme
sur sa page « Vue d'ensemble ».

---

## 4. Top compétences sur le marché marocain

```json
GET /skillnav_jobs/_search
{
  "size": 0,
  "query": { "term": { "origine": "Maroc" } },
  "aggs": {
    "top_skills": { "terms": { "field": "skills_all", "size": 15 } }
  }
}
```

**Résultat** :

```json
{
  "aggregations": {
    "top_skills": {
      "buckets": [
        { "key": "SQL",            "doc_count": 218 },
        { "key": "Python",         "doc_count": 187 },
        { "key": "Power BI",       "doc_count": 105 },
        { "key": "Machine Learning","doc_count":  98 },
        { "key": "Excel",          "doc_count":  89 },
        ...
      ]
    }
  }
}
```

Le champ aplati `skills_all` (qui concatène les 10 sous-familles dans un seul
keyword multivalué) évite de devoir fusionner 10 buckets côté client.

---

## 5. Recherche conjointe + filtres + tri par date

```json
GET /skillnav_jobs/_search
{
  "size": 10,
  "query": {
    "bool": {
      "must": [
        { "multi_match": { "query": "transformer", "fields": ["title", "responsibilities"] } }
      ],
      "filter": [
        { "term":  { "is_management": false } },
        { "terms": { "ai_type": ["ai-first", "ai-support"] } },
        { "range": { "posted_month": { "gte": "2025-01" } } }
      ]
    }
  },
  "sort": [ { "posted_month": "desc" } ],
  "_source": ["title", "company", "posted_month", "ai_type"]
}
```

Recherche typique : « toutes les offres post-2025 mentionnant des
*transformers* dans un rôle non-managérial orienté IA, triées par date
décroissante ». Type de requête combinée qui justifie l'existence d'ES
au-dessus de Mongo.

---

## Notes pratiques

* Index size après ingestion : ~5 MB (largement sous le plafond de 125 MB du
  free tier Bonsai sandbox).
* Latence moyenne d'une `multi_match` simple : ~30 ms.
* Latence d'une agrégation à 36 buckets × 13 sous-buckets : ~80 ms.
* Reindexer from scratch après un changement de mapping : ~25 secondes pour
  3 467 documents en batch de 500.
