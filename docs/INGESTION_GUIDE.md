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

## 5. Elasticsearch / OpenSearch : ingestion

### 5.1 Choix de provider et de moteur

Le cluster est hébergé chez **Bonsai** (plan Sandbox, gratuit permanent, sans carte bancaire). Bonsai Sandbox provisionne **OpenSearch 2.x**, le fork open source d'Elasticsearch lancé par AWS en 2021. L'API REST est compatible à 99 % avec Elasticsearch 7.x, ce qui rend le code portable. La justification académique du choix d'OpenSearch plutôt qu'Elasticsearch Enterprise tient en deux points :

- **Pérennité** : Elasticsearch Cloud Free est limité à 14 jours, ce qui ferait expirer la démonstration avant la soutenance ;
- **Licence** : OpenSearch est sous Apache 2.0, alors qu'Elasticsearch est désormais en licence AGPL + Elastic License v2. Pour un projet académique, OpenSearch est plus simple à justifier juridiquement.

### 5.2 Prérequis

- Compte Bonsai et cluster Sandbox créé (région `us-east-1`)
- Variable `ELASTIC_URL` renseignée dans `.env` avec l'URL **Full Access** (incluant les credentials)
- Package Python `opensearch-py`

```bash
pip install --user opensearch-py
```

### 5.3 Format de la connection URL

L'URL Bonsai inclut les credentials directement :

```
ELASTIC_URL=https://USERNAME:PASSWORD@hash-cluster.us-east-1.bonsaisearch.net
ELASTIC_INDEX=skillnav_jobs
```

### 5.4 Lancement

```bash
python scripts/ingestion/ingest_elasticsearch.py
```

Sortie attendue (résumée) :

```
Connexion au cluster Bonsai (OpenSearch)...
  Distribution  : opensearch
  Version       : 2.19.5
  Index cible   : skillnav_jobs

Préparation de l'index skillnav_jobs...
  Index skillnav_jobs créé avec mapping multilingue (FR + EN)

Lecture et bulk indexation depuis data/jobs.jsonl...

3467 documents indexés en 4.5 s (772 docs/s)

=== Résumé final ===
  Total documents indexés : 3467
  Distribution origine :
    International    3086
    Maroc             381
  Top 10 compétences globales :
    Python  AWS  Prompt Engineering  Docker  CI/CD  RAG  Azure  SQL  GCP  Kubernetes

  Test full-text : 'data scientist' au Maroc
    23 matches trouvés (top 3 affichés)
```

### 5.5 Mapping de l'index `skillnav_jobs`

L'index utilise un analyzer personnalisé `fr_en_mixed` (tokenizer standard + lowercase + asciifolding) qui couvre correctement le français et l'anglais sans dictionnaire externe. Champs principaux :

| Champ                                  | Type                | Utilité                                                    |
|----------------------------------------|---------------------|------------------------------------------------------------|
| `title`, `responsibilities`, `use_cases` | text (`fr_en_mixed`) | Recherche plein texte avec scoring BM25                   |
| `title_canonical`, `company` (keyword) | keyword             | Filtres exacts, agrégations                                |
| `ai_type`, `job_family`, `origine`     | keyword             | Facettes du dashboard                                       |
| `posted_month`                         | keyword             | Time-series via `date_histogram` (format `YYYY-MM`)        |
| `skills.genai`, `skills.ml`, ...       | keyword             | Recherche par famille de compétences                       |
| `skills_all`                           | keyword (dérivé)    | Agrégations top-skills toutes familles confondues          |

### 5.6 Issue corrigée : `_id` en metadata field

OpenSearch refuse l'inclusion du champ `_id` à l'intérieur du `_source` d'un document. Le script retire automatiquement `_id` du document via `doc.pop('_id')` avant l'envoi et le passe séparément dans l'action bulk. Sans cette correction, les 3 467 documents échouent avec `mapper_parsing_exception`.

### 5.7 Vérification post-ingestion

Depuis le dashboard Bonsai (onglet **Console**) :

```json
GET skillnav_jobs/_count
```

Doit renvoyer `{ "count": 3467, ... }`.

Test de recherche full-text :

```json
POST skillnav_jobs/_search
{
  "size": 5,
  "query": { "match": { "responsibilities": "data scientist" } },
  "highlight": { "fields": { "responsibilities": {} } }
}
```
