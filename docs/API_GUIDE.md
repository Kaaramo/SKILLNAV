# Guide API SKILLNAV (FastAPI)

> Module M242 Analyse de Web · ENSA-Tétouan
> Backend qui expose les données SKILLNAV (Mongo + OpenSearch + NER) au
> dashboard Next.js.

---

## 1. Démarrer l'API en local

```powershell
cd "F:\Web Mining Project"
python -m uvicorn api.main:app --reload --port 8000
```

L'API démarre sur `http://localhost:8000`. Trois URL essentielles :

| URL | Description |
|---|---|
| `http://localhost:8000/` | Page racine (métadonnées) |
| `http://localhost:8000/docs` | **Swagger UI interactive** (à utiliser pour tester) |
| `http://localhost:8000/openapi.json` | Schéma OpenAPI brut (utile pour générer les types TypeScript) |

---

## 2. Endpoints disponibles (préfixe `/api/v1`)

### Santé et méta

| Méthode | Path | Description |
|---|---|---|
| GET | `/health` | Statut des dépendances (Mongo, OpenSearch, NER) |

### Vue d'ensemble (page `/`)

| Méthode | Path | Description |
|---|---|---|
| GET | `/overview` | KPI globaux : volumétrie, par origine, par type, par famille |

### Jobs (pages `/jobs`, détail offre)

| Méthode | Path | Paramètres | Description |
|---|---|---|---|
| GET | `/jobs` | `origine`, `ai_type`, `job_family`, `company`, `limit`, `skip` | Liste paginée |
| GET | `/jobs/{job_id}` | (none) | Détail complet d'une offre |

### Skills (pages `/skills`, détail compétence)

| Méthode | Path | Paramètres | Description |
|---|---|---|---|
| GET | `/skills/top` | `famille`, `origine`, `limit` | Top compétences |
| GET | `/skills/{name}/jobs` | `limit` | Offres associées à une compétence |

### Companies et titres

| Méthode | Path | Paramètres | Description |
|---|---|---|---|
| GET | `/companies/top` | `origine`, `limit` | Top employeurs |
| GET | `/titles/top` | `origine`, `limit` | Top intitulés de poste |

### Recherche full-text (page `/search`)

| Méthode | Path | Paramètres | Description |
|---|---|---|---|
| GET | `/search` | `q`, `origine`, `ai_type`, `job_family`, `limit`, `skip` | Recherche dans OpenSearch avec highlight |

### NER (page `/ner-explorer`)

| Méthode | Path | Body / Params | Description |
|---|---|---|---|
| POST | `/ner/extract` | `{text: str, score_min: float}` | Extraction d'entités via Union 3 BERT (live, ~10 s) |
| GET | `/ner/status` | (none) | Statut de chargement des modèles |
| GET | `/ner/comparison` | (none) | Tableau §N2.1 chiffré |

### Étude comparative (page `/comparative-study`)

| Méthode | Path | Description |
|---|---|---|
| GET | `/comparative` | Liste des sections §N2 disponibles |
| GET | `/comparative/n21` | Tableau §N2.1 NER détaillé |

---

## 3. Exemples d'appels (curl + Python)

### Vue d'ensemble

```bash
curl http://localhost:8000/api/v1/overview
```

### Top 10 compétences GenAI au Maroc

```bash
curl "http://localhost:8000/api/v1/skills/top?famille=genai&origine=Maroc&limit=10"
```

### Recherche full-text « python aws »

```bash
curl "http://localhost:8000/api/v1/search?q=python+aws&limit=5"
```

### Extraction NER live

```bash
curl -X POST http://localhost:8000/api/v1/ner/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "Senior AI Engineer at Mistral AI, Paris. Skills: Python, RAG, LangChain.", "score_min": 0.5}'
```

En Python :

```python
import requests

r = requests.get("http://localhost:8000/api/v1/skills/top", params={"limit": 5})
print(r.json())

r = requests.post(
    "http://localhost:8000/api/v1/ner/extract",
    json={"text": "AI Engineer at OpenAI, San Francisco. Python, GPT, RAG.", "score_min": 0.5},
)
print(r.json())
```

---

## 4. Configuration (`.env`)

Toutes les variables se définissent dans `.env` à la racine du projet (gitignored).

| Variable | Défaut | Description |
|---|---|---|
| `MONGODB_URI` | (requis) | URI MongoDB Atlas |
| `MONGODB_DB` | `skillnav` | Nom de la database |
| `MONGODB_COLLECTION` | `jobs` | Nom de la collection |
| `ELASTIC_URL` | (requis) | URL OpenSearch Bonsai (avec credentials inline) |
| `ELASTIC_INDEX` | `skillnav_jobs` | Index OpenSearch |
| `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` | (optionnel) | Bachirou |
| `LOAD_NER_AT_STARTUP` | `False` | Si `True`, charge les 3 modèles BERT au démarrage |
| `DISABLE_NER` | `False` | Si `True`, l'endpoint `/ner/extract` renvoie 503 |
| `API_PREFIX` | `/api/v1` | Préfixe de toutes les routes |
| `CORS_ORIGINS` | liste | Origines CORS autorisées |

---

## 5. Architecture

```
F:\Web Mining Project\api\
├── main.py                # Application FastAPI + CORS + lifespan
├── config.py              # Settings via pydantic-settings
├── models/
│   └── common.py          # Schémas Pydantic v2 (réponses + erreurs)
├── db/
│   ├── mongo.py           # Client MongoDB + requêtes
│   └── elastic.py         # Client OpenSearch + requêtes
├── ml/
│   └── ner_pipeline.py    # Pipeline Union 3 BERT (lazy load)
└── routes/                # 8 routers (un par domaine fonctionnel)
    ├── health.py
    ├── overview.py
    ├── jobs.py
    ├── skills.py
    ├── companies.py
    ├── search.py
    ├── ner.py
    └── comparative.py
```

### Choix techniques

| Aspect | Choix |
|---|---|
| Driver Mongo | `pymongo` (sync, `tlsCAFile=certifi.where()` pour TLS Windows) |
| Driver ES | `opensearch-py` (HTTP basic auth via URL Bonsai) |
| ML | `transformers` + `torch` CPU |
| Auth | Aucune en V1 (académique) |
| CORS | Liste blanche : `localhost:3000`, `*.vercel.app` |
| Pagination | `limit` (default 20, max 100) + `skip` |
| Erreurs | `HTTPException` FastAPI standard |
| Lifespan | Ping Mongo + ES au démarrage, chargement NER optionnel |

### Tolérance aux pannes

- **Mongo down** → endpoints `/overview`, `/jobs`, `/skills` renvoient 500
- **OpenSearch down** → seul `/search` renvoie 500, les autres fonctionnent
- **Un modèle NER échoue à charger** → la pipeline Union continue avec les autres modèles
- **CamemBERT spécifiquement** : actuellement incompatible avec transformers 5.6 sur Windows, automatiquement skip à l'inférence. Le baseline complet a été évalué côté notebook (cf. `03_ner_improvement.ipynb`)

---

## 6. Déploiement (à venir)

L'API sera déployée sur **Render.com Free Tier** (supporte Python + ML CPU). Plan :

1. Créer un service Web Render depuis le repo GitHub Kaaramo/SKILLNAV
2. Build command : `pip install -r requirements.txt`
3. Start command : `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
4. Configurer les variables d'environnement (Mongo, ES, NER toggles)
5. Render attribue une URL `https://skillnav-api.onrender.com`
6. Le dashboard Next.js (Vercel) pointe vers cette URL

> Render Free Tier endort le service après 15 min d'inactivité. Premier appel à chaud = 30 s. Acceptable pour démo soutenance.

---

## 7. Pour aller plus loin

- Auth API par clé statique en header (30 min de code)
- Cache Redis sur `/overview` et `/skills/top` si latence devient un problème
- Endpoint `/graph` (Neo4j) à brancher quand Bachirou a fini son volet
- Endpoint `/forecasting/{skill}` (ARIMA, Prophet, LSTM) à brancher Sprint 3
