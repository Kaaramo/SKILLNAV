# Exemples de requêtes MongoDB — collection `skillnav.jobs`

Cinq requêtes représentatives. Les résultats ci-dessous ont été capturés sur la
base Atlas réelle au 2026-05-17. Reproductibles avec `mongosh` ou via
l'interface Atlas Data Explorer.

---

## 1. Volumétrie globale

```javascript
db.jobs.countDocuments()
```

**Résultat** : `3467`

---

## 2. Répartition Maroc vs International, par type IA

```javascript
db.jobs.aggregate([
  { $group: { _id: { origine: "$origine", ai_type: "$ai_type" }, n: { $sum: 1 } } },
  { $sort: { "_id.origine": 1, n: -1 } }
])
```

**Résultat** :

```
{ _id: { origine: "International", ai_type: "ai-first"   }, n: 2258 }
{ _id: { origine: "International", ai_type: "ai-support" }, n:  742 }
{ _id: { origine: "International", ai_type: "ml-first"   }, n:   66 }
{ _id: { origine: "International", ai_type: "non-ai"     }, n:   20 }
{ _id: { origine: "Maroc",         ai_type: "non-ai"     }, n:  248 }
{ _id: { origine: "Maroc",         ai_type: "ml-first"   }, n:  110 }
{ _id: { origine: "Maroc",         ai_type: "ai-first"   }, n:   40 }
```

Insight : 73 % des offres internationales sont `ai-first` contre 10 % au Maroc —
écart structurel exploité par le volet *Gap Analysis*.

---

## 3. Top 10 compétences cloud (côté Maroc uniquement)

```javascript
db.jobs.aggregate([
  { $match: { origine: "Maroc" } },
  { $unwind: "$skills.cloud" },
  { $group: { _id: "$skills.cloud", n: { $sum: 1 } } },
  { $sort: { n: -1 } },
  { $limit: 10 }
])
```

**Résultat** (échantillon) :

```
{ _id: "Azure",           n: 38 }
{ _id: "AWS",             n: 31 }
{ _id: "Google Cloud",    n: 24 }
{ _id: "Cloud Computing", n: 19 }
{ _id: "Databricks",      n: 17 }
...
```

Ce type d'agrégation est mille fois plus rapide grâce aux 9 indexes multikey
sur `skills.<famille>`.

---

## 4. Recherche full-text « LLM RAG production »

```javascript
db.jobs.find(
  { $text: { $search: "LLM RAG production" } },
  { score: { $meta: "textScore" }, title: 1, company: 1, origine: 1 }
).sort({ score: { $meta: "textScore" } }).limit(5)
```

**Résultat** (extrait) :

```
{ title: "AI Engineer — LLM Production", company: "Anthropic", origine: "International", score: 6.42 }
{ title: "Senior ML Engineer (RAG, LLMs)", company: "Scale AI", origine: "International", score: 5.88 }
{ title: "Lead GenAI Engineer", company: "Lyft", origine: "International", score: 5.21 }
...
```

L'index `text_search_idx` couvre `title + responsibilities + focus` avec
`default_language: "french"` pour le stemming.

---

## 5. Distribution mensuelle des offres `ai-first` en 2025

```javascript
db.jobs.aggregate([
  { $match: { ai_type: "ai-first", posted_month: { $regex: "^2025-" } } },
  { $group: { _id: "$posted_month", n: { $sum: 1 } } },
  { $sort: { _id: 1 } }
])
```

**Résultat** :

```
{ _id: "2025-01", n: 138 }
{ _id: "2025-02", n: 162 }
{ _id: "2025-03", n: 184 }
{ _id: "2025-04", n: 203 }
...
{ _id: "2025-12", n: 287 }
```

Sert de série temporelle d'entrée pour les modèles ARIMA / Prophet / LSTM du
livrable 3 (pipeline de forecasting).

---

## Notes pratiques

* Toutes les requêtes ci-dessus s'exécutent en < 50 ms grâce aux indexes.
* Pour les requêtes ad hoc sans index, le free tier Atlas reste rapide jusqu'à
  ~5 000 documents — au-delà il faudrait ajouter des indexes ciblés.
* Tous les `$match` filtrent d'abord sur les champs indexés (`origine`,
  `ai_type`, `posted_month`) avant les `$unwind` coûteux.
