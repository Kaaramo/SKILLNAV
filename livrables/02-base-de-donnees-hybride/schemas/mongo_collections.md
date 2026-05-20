# Schéma MongoDB — `skillnav.jobs`

> Cluster : MongoDB Atlas (free tier M0, AWS Frankfurt)
> Base : `skillnav`
> Collection principale : `jobs` (3 467 documents)

---

## Connexion

Le client est paramétré dans `scripts/ingestion/ingest_mongodb.py`. URI lue
depuis `.env` (`MONGODB_URI`), le mot de passe n'est pas committé. Le
certificat TLS vient du bundle `certifi` pour éviter le bug Windows.

```python
from pymongo import MongoClient
import certifi
client = MongoClient(os.environ["MONGODB_URI"], tls=True, tlsCAFile=certifi.where())
db = client["skillnav"]
jobs = db["jobs"]
```

---

## Schéma de la collection `jobs`

Modélisation issue de `skillnav/schemas/job.py` (Pydantic v2). Chaque document
correspond à une offre d'emploi unique, identifiée par son `_id` :
`job_<source>_<job_id>`.

| Champ | Type | Description |
|---|---|---|
| `_id` | `str` | Identifiant unique (clé primaire), format `job_<source>_<job_id>` |
| `job_id` | `str` | Identifiant interne dans la source d'origine |
| `origine` | `str` | `"Maroc"` ou `"International"` |
| `source` | `str` | Nom de la plateforme (`rekrute`, `linkedin-ma`, `intl-ai-corpus`, …) |
| `posted_month` | `str` | Mois de publication, format `YYYY-MM` |
| `title` | `str` | Titre original de l'offre |
| `title_canonical` | `str` | Titre normalisé (lowercase, sans accents) |
| `job_family` | `str` | Famille métier (`DATA_SCIENTIST`, `ML_ENGINEER`, …) |
| `ai_type` | `str` | `ai-first`, `ai-support`, `ml-first`, `non-ai` |
| `company` | `str` | Nom de l'employeur |
| `stage` | `str` | Stade de l'entreprise (`startup`, `scale-up`, `enterprise`, …) |
| `focus` | `str` | Focus métier (texte court) |
| `is_customer_facing` | `bool` | Rôle en contact client |
| `is_management` | `bool` | Rôle managérial |
| `responsibilities` | `str` | Responsabilités (texte) |
| `use_cases` | `str` | Cas d'usage métier (texte) |
| `skills` | `object` | 10 sous-listes thématiques de compétences |

### Sous-objet `skills`

| Sous-champ | Exemple |
|---|---|
| `skills.genai` | `["LLM", "RAG", "Prompt Engineering"]` |
| `skills.ml` | `["Machine Learning", "Deep Learning", "TensorFlow"]` |
| `skills.web` | `["React", "Next.js"]` |
| `skills.databases` | `["PostgreSQL", "MongoDB"]` |
| `skills.data` | `["Spark", "Hadoop", "ETL"]` |
| `skills.cloud` | `["AWS", "GCP", "Azure"]` |
| `skills.ops` | `["Docker", "Kubernetes", "MLflow"]` |
| `skills.languages` | `["Python", "SQL", "R"]` |
| `skills.domains` | `["Banque", "E-commerce"]` |
| `skills.other` | `["Power BI", "Tableau"]` |

---

## Indexes appliqués

Tous les indexes sont créés par `creer_indexes()` dans
`scripts/ingestion/ingest_mongodb.py`.

### Indexes simples (7)

| Champ | Direction | Usage |
|---|---|---|
| `origine` | ascendant | Filtrer Maroc vs International |
| `source` | ascendant | Filtrer par plateforme |
| `posted_month` | descendant | Tri chronologique inverse |
| `ai_type` | ascendant | Filtrer par type IA |
| `job_family` | ascendant | Filtrer par famille métier |
| `company` | ascendant | Filtrer par employeur |
| `title_canonical` | ascendant | Recherche exacte / facette |

### Indexes multikey (9)

Un index par sous-famille de compétence, pour pouvoir requêter `skills.cloud: "AWS"` en O(log n) :

```
skills.genai, skills.ml, skills.web, skills.databases, skills.data,
skills.cloud, skills.ops, skills.languages, skills.domains
```

### Index full-text (1)

```
{ title: "text", responsibilities: "text", focus: "text" }
default_language: "french"
name: "text_search_idx"
```

Permet la recherche libre `db.jobs.find({ $text: { $search: "..." } })` avec
scoring naturel sur le titre + responsabilités + focus.

---

## Autres collections (réservées)

Le code prévoit également les collections suivantes dans la même base
`skillnav`, alimentées par d'autres pipelines :

| Collection | Schéma | Pipeline qui l'alimente |
|---|---|---|
| `raw_jobs` | `RawJob` | scraping live (futur) |
| `extracted_jobs` | `JobExtraction` | extraction LLM (futur) |
| `ner_annotations` | `NerAnnotation` | content mining |
| `skills_taxonomy` | (libre) | structure mining |
| `skills_timeseries` | `SkillTimeSeries` | usage mining |
| `forecasts` | `Forecast` | usage mining |
| `graph_metrics` | `GraphMetrics` | structure mining |
| `curricula` | `CurriculumExtraction` | curriculum mining (gap analysis) |

Pour le livrable 2, seule la collection `jobs` est obligatoirement remplie.
Les autres sont créées au besoin par leurs pipelines respectifs.

---

## Commandes de vérification rapide

```javascript
// Total documents
db.jobs.countDocuments()
// → 3467

// Répartition Maroc vs International
db.jobs.aggregate([
  { $group: { _id: "$origine", n: { $sum: 1 } } }
])
// → [ { _id: "Maroc", n: 381 }, { _id: "International", n: 3086 } ]

// Top 5 compétences GenAI
db.jobs.aggregate([
  { $unwind: "$skills.genai" },
  { $group: { _id: "$skills.genai", n: { $sum: 1 } } },
  { $sort: { n: -1 } },
  { $limit: 5 }
])
```

D'autres exemples concrets dans [`../queries/mongo_examples.md`](../queries/mongo_examples.md).
