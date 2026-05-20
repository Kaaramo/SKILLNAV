<div align="center">

# SKILLNAV

### Skills Navigator : observatoire des compétences IA & Data Science par Web Mining

*Pipeline complet de Web Mining sur le marché de l'expertise IA (Maroc et International), produit dans le cadre du module **M242 Analyse de Web**, ENSA-Tétouan.*

[![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 15](https://img.shields.io/badge/next.js-15-000000?logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.6-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Pydantic AI](https://img.shields.io/badge/pydantic--ai-claude--sonnet--4.5-2251FF)](https://ai.pydantic.dev/)
[![Status](https://img.shields.io/badge/status-collecte%20termin%C3%A9e%20%E2%80%A2%203%20468%20fiches-0F8F65)](#3-r%C3%A9sultats-collecte)

</div>

---

## Cadre académique

| | |
|---|---|
| **Module** | M242 Analyse de Web |
| **Établissement** | ENSA-Tétouan, Université Abdelmalek Essaâdi |
| **Cursus** | Diplôme d'Ingénieur, filière Sciences des Données, Big Data et IA (SDBIA) |
| **Encadrement** | Pr. Imad Sassi |
| **Équipe** | Karamo Sylla et Bachirou Konaté |
| **Soutenance** | **28 mai 2026**, 15 min présentation et 10 min Q&A |
| **Énoncé du sujet** | [`docs/SUJET_M242.md`](docs/SUJET_M242.md) |

---

## Sommaire

1. [Objectif](#1-objectif)
2. [Couverture des 3 axes Web Mining](#2-couverture-des-3-axes-web-mining)
3. [Résultats collecte](#3-résultats-collecte)
4. [Architecture pipeline](#4-architecture-pipeline)
5. [Stack technique](#5-stack-technique)
6. [Livrables imposés par le prof](#6-livrables-imposés-par-le-prof)
7. [Structure du dépôt](#7-structure-du-dépôt)
8. [Reproductibilité](#8-reproductibilité)
9. [Conformité RGPD](#9-conformité-rgpd)
10. [Avancement projet](#10-avancement-projet)

---

## 1. Objectif

SKILLNAV construit un pipeline complet de **Web Intelligence** appliqué au marché des compétences en **Intelligence Artificielle et Data Science** : de la collecte de données brutes sur le Web (LinkedIn, Indeed, Glassdoor, builtin.com, pages carrières) jusqu'à la modélisation prédictive de l'évolution des compétences.

Le projet couvre les **trois axes piliers du Web Mining** (Content, Structure, Usage) avec une étude comparative de **trois approches algorithmiques distinctes** par axe, comme exigé par le sujet.

---

## 2. Couverture des 3 axes Web Mining

```
┌──────────────────────────────────────────────────────────────────┐
│                  3 AXES, 3 ÉTUDES COMPARATIVES                   │
│                                                                  │
│  CONTENT    NER skills, 3 modèles HF comparés                    │
│             BERT-multi vs CamemBERT-NER vs DistilBERT            │
│                                                                  │
│  STRUCTURE  Graphe Skill <-> Job <-> Family, Neo4j AuraDB        │
│             Louvain vs Label Propagation vs Leiden               │
│                                                                  │
│  USAGE      Forecasting compétences émergentes                   │
│             ARIMA vs Prophet vs LSTM (MAPE chiffré)              │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Résultats collecte

> Le volet collecte est **terminé** : 3 468 fiches Data/IA propres (100 % descriptions exploitables) prêtes pour les volets aval (ingestion NoSQL, NER, dashboard).

### Volumes par groupe

| Groupe | Fiches | Période publication |
|---|:-:|---|
| Maroc | 381 | Décembre 2022 à Mai 2026 |
| International (Corpus Tech INTL) | 3 087 | Août 2025 à Avril 2026 |
| **Total** | **3 468** | **Août 2022 à Mai 2026** |

### Distribution par source (7 sources)

| Source | Pays | Postings | Outil de collecte |
|---|:-:|:-:|---|
| ANAPEC | MA | 2 | Playwright MCP |
| Rekrute | MA | 27 | Playwright MCP |
| Indeed MA | MA | 67 | Playwright + recovery Apify |
| LinkedIn MA | MA | 207 | Apify (actor `cheap-advance-linkedin-jobs-scraper`) |
| Pages carrières MA | MA | 6 | JSON-LD + BeautifulSoup |
| Glassdoor MA | MA | 72 | Firecrawl + recovery |
| Corpus Tech INTL | 6 pays | 3 087 | Pipeline 5 étapes (cf. `sources/collected/intl-ai-corpus/scrapers/`) |
| **Total** | | **3 468** | |

### Architecture 3 couches uniforme

Toutes les sources adoptent la même structure de stockage :

```
sources/collected/<source>/
├── data_raw/{YYYY-MM}/<id>_<co>_<title>.yaml         (Couche 1 : extraction brute)
├── data_structured/{YYYY-MM}/<id>_<co>_<title>.yaml  (Couche 2 : enrichissement LLM)
└── postings/NNN.{json,md}                            (Couche 3 : pivot Pydantic DB-ready)
```

L'organisation `{YYYY-MM}/` reflète la date de **publication** de l'offre (alignement avec l'axe Usage Mining), pas la date de scraping.

---

## 4. Architecture pipeline

```
   ┌──────────────────────────────────────────┐
   │  COLLECTE  (terminé)                     │
   │  Playwright, Firecrawl, Apify            │
   │  3 468 fiches en pipeline 3 couches      │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INGESTION (en cours)                    │
   │  MongoDB Atlas (raw_jobs, jobs)          │
   │  Pydantic v2, dédup SHA-256              │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  CONTENT MINING                          │
   │   Pydantic AI + Claude (extracted_jobs)  │
   │   HF Transformers x 3 (ner_annotations)  │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  STRUCTURE MINING : Neo4j AuraDB         │
   │  PageRank, Louvain, Label Propagation    │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  USAGE MINING : forecasts                │
   │  ARIMA, Prophet, LSTM, émergence         │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  API FastAPI + Dashboard Next.js 15      │
   └──────────────────────────────────────────┘
```

---

## 5. Stack technique

| Couche | Technologie | Version |
|---|---|---|
| Language backend | Python | 3.12 |
| Package manager | Poetry | 1.8+ |
| Extraction IA | Pydantic AI + Claude Sonnet 4.5 | latest |
| NER | HuggingFace Transformers (BERT-multi, CamemBERT-NER, DistilBERT) | 4.40+ |
| Storage NoSQL | MongoDB Atlas + Neo4j AuraDB + Elasticsearch Cloud | free tiers |
| API | FastAPI + uvicorn | 0.110+ |
| Front | Next.js 15 + TypeScript 5.4 + Tailwind v4 + Shadcn/ui | latest |
| Charts | Recharts, Tremor, react-force-graph-2d, Plotly | latest |
| Outils de scraping | Playwright, Firecrawl, Apify, requests + BeautifulSoup | latest |

---

## 6. Livrables imposés par le sujet

Le sujet impose **6 livrables** ([détail dans `docs/SUJET_M242.md`](docs/SUJET_M242.md)) :

| # | Livrable | Lien direct |
|:-:|---|---|
| 1 | **Scripts de collecte** — code documenté pour le scraping et les appels API | [`Kaaramo/SKILLNAV-COLLECT`](https://github.com/Kaaramo/SKILLNAV-COLLECT) (dépôt séparé, ouvert aux contributeurs externes) |
| 2 | **Base de données hybride** — MongoDB + Neo4j + Elasticsearch | [`livrables/02-base-de-donnees-hybride/`](livrables/02-base-de-donnees-hybride/) |
| 3 | **Pipeline IA** — modèles entraînés, testés, validés par métriques | [`livrables/03-pipeline-ia/`](livrables/03-pipeline-ia/) |
| 4 | **Dashboard interactif** — Next.js 16 / React 19, 6 pages | [`web/`](web/) (code) · `https://skillnav.vercel.app` (live) |
| 5 | **Rapport** — méthodologie, analyse, justifications, recommandations | [`docs/Rapport.md`](docs/Rapport.md) (export PDF au rendu) |
| 6 | **Présentation** — orale synthétique | `docs/Soutenance.pdf` (à produire) |

> Cette table est aussi la carte officielle des livrables livrée au correcteur.
> Une version compacte uniquement-liens est dans [`LIVRABLES.md`](LIVRABLES.md).

---

## 7. Structure du dépôt

```
Web Mining Project/
├── README.md                          (ce fichier)
├── CLAUDE.md                          (consignes Claude Code)
├── Makefile                           (tâches dev)
├── pyproject.toml                     (dépendances Python)
├── .env.example, .gitignore           (config)
│
├── docs/
│   ├── SUJET_M242.md                  (énoncé officiel du prof)
│   ├── PRD.md                         (Product Requirements Document)
│   ├── PRD_CONDENSE.md                (PRD version courte)
│   ├── CHARTE_GRAPHIQUE_SKILLNAV.*    (direction artistique)
│   └── tools/
│       ├── firecrawl.md               (justification outil)
│       ├── apify.md                   (justification outil)
│       └── playwright.md              (justification outil)
│
├── sources/
│   └── collected/                     (3 468 fiches, pipeline 3 couches)
│       ├── README.md                  (protocole de collecte)
│       ├── COLLECTION_PROTOCOL.md     (méthode versionnée v1.0)
│       ├── _schema/                   (JSON Schema Pydantic)
│       ├── _restructure_ma_to_3_layers.py
│       ├── _enrich_ma_structured.py
│       ├── _audit_ma_quality.py
│       ├── _eliminate_incomplete_postings.py
│       ├── anapec/                    (2 fiches)
│       ├── rekrute/                   (27 fiches)
│       ├── indeed-ma/                 (67 fiches, scripts recovery)
│       ├── linkedin-ma/               (207 fiches)
│       ├── pages-carrieres-ma/        (6 fiches)
│       ├── glassdoor-ma/              (72 fiches, scripts recovery)
│       └── intl-ai-corpus/            (3 087 fiches)
│           └── scrapers/              (pipeline 5 étapes)
│
├── skillnav/                          (package Python, scaffolding)
│   ├── api/, db/, pipelines/, schemas/, scrapers/, comparative_studies/
│   └── cli.py
│
├── web/                               (Next.js 15, scaffolding dashboard)
├── notebooks/                         (6 notebooks numérotés)
├── tests/                             (pytest, fixtures)
├── scripts/                           (utilitaires, à remplir)
└── data/                              (raw, exports, audit, gold_set)
```

---

## 8. Reproductibilité

### Prérequis

```bash
python --version            # 3.12 ou supérieur
poetry install              # installe les dépendances Python
cd web && pnpm install      # installe les dépendances front
```

### Variables d'environnement (`.env`)

```env
ANTHROPIC_API_KEY=sk-ant-...        # Claude Sonnet 4.5 (extraction Pydantic AI)
APIFY_TOKEN=apify_api_...           # actors LinkedIn et Indeed
MONGODB_URI=mongodb+srv://...       # Atlas free tier M0
NEO4J_URI=neo4j+s://...             # AuraDB free
NEO4J_USER=neo4j
NEO4J_PASSWORD=...
ELASTIC_CLOUD_ID=...                # ou auto-hébergement docker
ELASTIC_API_KEY=...
```

Voir `.env.example` pour le template complet.

### Lancer la collecte

```bash
# Audit qualité du corpus existant
python sources/collected/_audit_ma_quality.py

# Pipeline intl (5 étapes documentées)
cd sources/collected/intl-ai-corpus/scrapers
cat README.md     # voir la documentation détaillée
```

### Repo dédié collecte

Un dépôt séparé contient uniquement la couche collecte (data + scripts), pour permettre à un collaborateur de cloner seulement cette partie :

🔗 [github.com/Kaaramo/SKILLNAV-COLLECT](https://github.com/Kaaramo/SKILLNAV-COLLECT)

---

## 9. Conformité RGPD

| Règle | Application |
|---|---|
| Données personnelles de candidat | **Aucune** : pas de noms, emails, téléphones, photos, profils LinkedIn personnels |
| Entités morales uniquement | Noms d'entreprise et descriptions publiques d'offres |
| User-Agent identifié | `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)` |
| Rate limit | 5 secondes minimum entre requêtes sur sources statiques |
| robots.txt | Vérifié pour chaque source avant collecte |
| Schéma JSON officiel | `sources/collected/_schema/job_posting.schema.json` (validation Pydantic) |

---

## 10. Avancement projet

| Phase | Statut | Date |
|---|:-:|---|
| Cadrage (PRD, charte, sujet) | ✅ Terminé | 14 mai 2026 |
| **Collecte (7 sources, 3 468 fiches)** | ✅ **Terminé** | **16 mai 2026** |
| Recovery qualité (passage de 67 % à 100 % exploitable côté MA) | ✅ Terminé | 16 mai 2026 |
| Désanonymisation upstream et nettoyage repo | ✅ Terminé | 16 mai 2026 |
| Ingestion NoSQL hybride (Mongo + Neo4j + ES) | 🔄 En cours | Sprint 2 |
| Pipeline IA (NER comparatif + classification) | ⏳ À venir | Sprint 2 |
| Dashboard Next.js | ⏳ À venir | Sprint 2 |
| Rapport méthodologique L5 | ⏳ À venir | Sprint 3 |
| Soutenance | ⏳ À venir | **28 mai 2026** |

---

**Mai 2026** · SKILLNAV · M242 ENSA-Tétouan · Pr. Imad Sassi · Karamo Sylla & Bachirou Konaté
