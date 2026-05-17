# SKILLNAV : Guide d'ingestion des bases de données

> Module M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi
> Couvre l'ingestion des 3 467 fiches consolidées (`data/jobs.jsonl`) dans les trois bases NoSQL du PRD §7.

---

## 1. Architecture cible

| Base                  | Statut           | Rôle                                                              | Volume          |
|-----------------------|------------------|-------------------------------------------------------------------|-----------------|
| **MongoDB Atlas**     | opérationnel     | Source of truth des offres                                        | 3 467 documents |
| **Neo4j AuraDB**      | Bachirou         | Graphe Skill <-> Job <-> Company (§N2.2 du PRD)                    | 13 071 nœuds    |
| **Elasticsearch**     | à brancher       | Recherche plein texte et agrégations (dashboard `/search`)        | 2 indexes       |

---

## 2. MongoDB Atlas : ingestion

### 2.1 Prérequis

- Cluster `skillnav-cluster` créé sur MongoDB Atlas Free Tier (M0)
- Network Access avec `0.0.0.0/0` autorisé pour le dev (sécurité par mot de passe)
- Variables `MONGODB_URI` et `MONGODB_DB` renseignées dans `.env` à la racine
- Packages Python : `pymongo[srv]`, `python-dotenv`, `certifi`

```bash
pip install --user "pymongo[srv]" python-dotenv certifi
```

### 2.2 Format de la connection string dans `.env`

Le mot de passe doit être URL-encodé si caractère réservé (`#`, `@`, `:`, `/`).

| Caractère | URL-encodé |
|-----------|------------|
| `#`       | `%23`      |
| `@`       | `%40`      |
| `:`       | `%3A`      |
| `/`       | `%2F`      |

Exemple :

```
MONGODB_URI=mongodb+srv://skillnav_admin:Database2026%23%23@skillnav-cluster.xxxxx.mongodb.net/?appName=skillnav-cluster
MONGODB_DB=skillnav
```

### 2.3 Lancement de l'ingestion

```bash
python scripts/ingestion/ingest_mongodb.py
```

Sortie attendue (résumée) :

```
Connexion au cluster MongoDB Atlas...
  Connexion OK  ->  base cible : skillnav.jobs

Lecture du fichier data/jobs.jsonl ...
  Batch upserté  (  500 documents)
  ...
  Batch upserté  ( 3467 documents)

3467 documents upsertés en 18.3 s (190 docs/s)

Création des indexes...
  Index simple  : origine, source, posted_month, ai_type, job_family, company, title_canonical
  Index multikey: skills.genai, skills.ml, skills.web, ... (9 familles)
  Index full-text : title + responsibilities + focus

=== Résumé final ===
  Total documents          : 3467
  Origine Maroc            : 381
  Origine International    : 3086
```

Le script est idempotent : chaque document utilise son `_id` issu de `jobs.jsonl`, donc une nouvelle exécution remplace simplement les documents existants sans créer de doublons.

### 2.4 Vérification post-ingestion

Depuis la console Atlas (onglet **Browse Collections** sur le cluster) :

- Database `skillnav` présente avec collection `jobs`
- Compte des documents = 3 467
- 17 indexes dans l'onglet **Indexes** de la collection

Ou en ligne de commande Python :

```python
from pymongo import MongoClient
import certifi, os
from dotenv import load_dotenv
load_dotenv()
client = MongoClient(os.environ['MONGODB_URI'], tlsCAFile=certifi.where())
db = client['skillnav']
print(db.jobs.count_documents({}))
print(db.jobs.find_one({"origine": "Maroc"}))
```

### 2.5 Indexes créés

| Index                                           | Type        | Utilité                                                           |
|-------------------------------------------------|-------------|-------------------------------------------------------------------|
| `origine`, `source`                             | Simple ASC  | Filtres Maroc/INTL et par plateforme                              |
| `posted_month`                                  | Simple DESC | Tri chronologique (récent d'abord)                                |
| `ai_type`, `job_family`                         | Simple ASC  | Filtres par catégorie de poste                                    |
| `company`, `title_canonical`                    | Simple ASC  | Recherche par employeur / intitulé                                |
| `skills.genai`, `skills.ml`, `skills.web`, ...  | Multikey    | Filtre `db.jobs.find({"skills.genai": "LLM"})`                    |
| `title + responsibilities + focus`              | Full-text   | Recherche `db.jobs.find({"$text": {"$search": "data scientist"}})` |

---

## 3. Issue connue : `TLSV1_ALERT_INTERNAL_ERROR` au démarrage

Symptôme : le script échoue avec `SSL handshake failed ... TLSV1_ALERT_INTERNAL_ERROR`.

Cause : l'IP publique actuelle n'est pas dans la liste **Network Access** d'Atlas. Atlas accepte la connexion TCP mais ferme le handshake TLS.

Diagnostic rapide :

```bash
python -c "import urllib.request; print(urllib.request.urlopen('https://api.ipify.org').read().decode())"
```

Comparer le résultat avec la liste **Security > Network Access** d'Atlas. Si l'IP n'y figure pas :

1. Aller dans **Security > Network Access**
2. **+ ADD IP ADDRESS** > **ALLOW ACCESS FROM ANYWHERE** (`0.0.0.0/0`)
3. Attendre le statut **Active** (30 s à 2 min)
4. Relancer le script

> Le `0.0.0.0/0` est sécurisé tant que le mot de passe reste protégé. Pour la prod, restreindre à des IPs précises.

---

## 4. Neo4j AuraDB : ingestion

Voir [`MODELISATION_GUIDE.md`](./MODELISATION_GUIDE.md) et le notebook
[`notebooks/02_graph_starter.ipynb`](../notebooks/02_graph_starter.ipynb). Cette
partie relève de la responsabilité de Bachirou Konaté (cf. matrice RACI du PRD §3.5).

---

## 5. Elasticsearch : ingestion (à venir)

À implémenter. Provider recommandé : Bonsai Free Tier (125 Mo, sans limite de durée). Deux indexes à produire :

- `jobs_search` : full-text sur title + responsibilities + use_cases
- `skills_timeseries` : agrégations temporelles (compétence × mois)

Script cible : `scripts/ingestion/ingest_elasticsearch.py` (non encore créé).
