<div align="center">

# SKILLNAV

### Skills Navigator — Observatoire des Compétences IA & Data Science par le Web Mining

*Démonstration académique d'un pipeline complet Web Mining sur le marché de l'expertise IA — Maroc + International.*

[![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 15](https://img.shields.io/badge/next.js-15-000000?logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.6-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Pydantic AI](https://img.shields.io/badge/pydantic--ai-claude--sonnet--4.5-2251FF)](https://ai.pydantic.dev/)
[![License MIT](https://img.shields.io/badge/license-MIT-051C2C)](#license)
[![Status](https://img.shields.io/badge/status-pre--alpha-C77700)](#6-livrables-imposes-pr-sassi)

</div>

---

## Cadre académique

| | |
|---|---|
| **Module** | M242 — Analyse de Web |
| **Établissement** | ENSA-Tétouan · Université Abdelmalek Essaâdi |
| **Cursus** | Diplôme d'Ingénieur, filière Sciences des Données, Big Data et IA (SDBIA) |
| **Encadrement** | Pr. Imad Sassi |
| **Équipe** | Karamo Sylla & Bachirou Konaté |
| **Soutenance** | **28 mai 2026** — 15 min présentation + 4 min démo + 10 min Q&A |

---

## En bref

SKILLNAV démontre la couverture rigoureuse des **trois axes canoniques du Web Mining** (Content, Structure, Usage) appliqués à un domaine en évolution rapide : **les compétences en Intelligence Artificielle et Data Science**.

```
┌──────────────────────────────────────────────────────────────────┐
│                   3 AXES — 3 ÉTUDES COMPARATIVES                  │
│                                                                   │
│  CONTENT    NER skills · 3 modèles HF comparés                   │
│             BERT-multi · CamemBERT-NER · DistilBERT (+ baseline) │
│                                                                   │
│  STRUCTURE  Graphe Skill ↔ Job ↔ Family · Neo4j AuraDB           │
│             Louvain · Label Propagation · Leiden                 │
│                                                                   │
│  USAGE      Forecasting compétences émergentes                   │
│             ARIMA · Prophet · LSTM (MAPE chiffré)                │
└──────────────────────────────────────────────────────────────────┘
```

**Volume cible MVP** : 500–2 000 offres analysées sur Maroc + International, sur une fenêtre 3–6 mois.

**Architecture NoSQL polyglotte** : MongoDB Atlas (source of truth) + Neo4j AuraDB (graphe) + Elasticsearch Cloud (recherche + agrégations).

**Pipeline IA** : Pydantic AI + Claude Sonnet 4.5 pour l'extraction structurée ; HuggingFace Transformers pour la NER comparative. Schémas Pydantic v2 comme source de vérité unique.

**Dashboard** : Next.js 15 + TypeScript + Tailwind v4 + Shadcn/ui, déployé sur Vercel. Direction artistique McKinsey-inspired (cf. charte graphique).

**Coût total MVP** : **< $50** (free tiers DBs + Anthropic ~$10–20 + Apify ~$5–10).

---

## Architecture — vue pipeline

```
   ┌──────────────────────────────────────────┐
   │  COLLECTE                                │
   │  Crawl4AI · Playwright · Firecrawl · Apify│
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INGESTION → MongoDB Atlas (raw_jobs)    │
   │  Pydantic v2 · dédup SHA-256             │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  CONTENT MINING                          │
   │   Pydantic AI + Claude → extracted_jobs  │
   │   HF Transformers × 3 → ner_annotations  │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  STRUCTURE MINING → Neo4j AuraDB         │
   │  PageRank · Louvain · Label Propagation  │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  USAGE MINING → forecasts                │
   │  ARIMA · Prophet · LSTM · émergence      │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INDEX → Elasticsearch (recherche/agg)   │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  API FastAPI ↔ Dashboard Next.js 15      │
   │  Render (API) + Vercel (UI)              │
   └──────────────────────────────────────────┘
```

---

## Quick start

```bash
# 1. Cloner
git clone https://github.com/<owner>/skillnav.git
cd skillnav

# 2. Setup complet (Python + web + pre-commit hooks)
make setup

# 3. Variables d'environnement (à remplir)
cp .env.example .env
cp web/.env.example web/.env.local
# Éditer .env avec : ANTHROPIC_API_KEY, MONGODB_URI, NEO4J_URI, ELASTIC_*, APIFY_TOKEN

# 4. Vérifier la qualité du code
make quality              # ruff + mypy strict + pytest

# 5. Lancer
make api                  # API FastAPI sur :8000
make web-dev              # Dashboard Next.js sur :3000
poetry run skillnav --help
```

---

## Documentation

> Tous les documents-clés vivent dans `docs/`. Le PRD condensé est la lecture la plus rapide pour comprendre le projet.

| Document | Rôle |
|---|---|
| [`docs/PRD_CONDENSE.md`](docs/PRD_CONDENSE.md) | **Lecture rapide** — PRD condensé orienté schémas (~660 lignes, 17 sections, ASCII partout) |
| [`docs/PRD_CONDENSE_SKILLNAV.pdf`](docs/PRD_CONDENSE_SKILLNAV.pdf) | PRD condensé — version premium 25 pages A4 (cover Navy, TOC, tables, schémas) |
| [`docs/PRD.md`](docs/PRD.md) | **Référence exhaustive** — PRD complet (~2 600 lignes, 27 sections + N1–N4) |
| [`docs/CHARTE_GRAPHIQUE_SKILLNAV.pdf`](docs/CHARTE_GRAPHIQUE_SKILLNAV.pdf) | Charte graphique officielle — 13 pages premium (palette, typographie, composants) |
| [`docs/RAPPORT_METHODOLOGIQUE.md`](docs/RAPPORT_METHODOLOGIQUE.md) | Livrable **L5** — rapport académique (en cours de rédaction) |
| [`docs/PLAN_SOUTENANCE.md`](docs/PLAN_SOUTENANCE.md) | Livrable **L6** — plan détaillé soutenance 25 min |
| [`docs/RGPD_DPIA.md`](docs/RGPD_DPIA.md) | DPIA simplifiée + protocole robots.txt + base légale art. 6.1.f |
| [`CLAUDE.md`](CLAUDE.md) | Consignes Claude Code (conventions, env, RGPD, ne pas faire) |
| [`docs/Projet Final Analyse de Web_Sujet 1.pdf`](docs/) | Sujet imposé par le Pr. Sassi — **intangible** |

> **Sources Word des PDFs** : `docs/CHARTE_GRAPHIQUE_SKILLNAV.docx` et `docs/PRD_CONDENSE_SKILLNAV.docx` restent éditables dans Word pour toute révision future (re-export PDF natif).

---

## Stack technique

| Couche | Technologie | Version |
|---|---|---|
| **Language** | Python | 3.12 |
| **Package mgr** | Poetry | 1.8+ |
| **Extraction IA** | Pydantic AI + Anthropic Claude (Sonnet 4.5 + Haiku 4.5) | latest |
| **NLP** | HuggingFace Transformers · sentence-transformers · spaCy · fasttext-langdetect | 4.40+ |
| **Web scraping** | Crawl4AI · Playwright · Firecrawl · Apify (LinkedIn actor) | latest |
| **Storage** | MongoDB Atlas (M0) · Neo4j AuraDB Free · Elasticsearch Cloud Free | — |
| **Drivers** | motor · neo4j · elasticsearch | latest |
| **Graph algos** | NetworkX · python-louvain · igraph · neo4j-GDS | latest |
| **Time series** | statsmodels · prophet · neuralforecast (Nixtla) · pytrends | latest |
| **API** | FastAPI · uvicorn | 0.110+ |
| **Frontend** | Next.js 15 · React 19 · TypeScript 5.6 · Tailwind v4 · Shadcn/ui | — |
| **State / data** | TanStack Query 5 | latest |
| **Charts** | Recharts · Tremor · react-force-graph-2d · Plotly | latest |
| **DevOps** | GitHub · Render (API) · Vercel (UI) | — |
| **Quality** | ruff · mypy strict · black · pytest (couverture ≥ 70 %) | latest |

---

## Structure du repository

```
.
├── skillnav/                # Package Python (entry: skillnav.cli:app)
│   ├── schemas/             # Pydantic v2 — source de vérité unique
│   │   └── converters/      # → BSON / Cypher / ES document
│   ├── db/                  # Connexions MongoDB · Neo4j · Elasticsearch
│   ├── pipelines/           # content_mining · structure_mining · usage_mining
│   ├── scrapers/            # Rekrute · EmploiTIC · Apify · Indeed · builtin · weak_signals
│   ├── comparative_studies/ # NER · communautés · forecasting · émergence (PRD §N2)
│   ├── api/                 # FastAPI endpoints
│   └── cli.py               # Typer CLI
│
├── web/                     # Next.js 15 — dashboard 8 pages
│   └── src/{app,components,lib/api}/
│
├── notebooks/               # 5 notebooks numérotés
│   ├── 00_setup_dev.ipynb
│   ├── 01_data_quality.ipynb            # complétude · bruit · biais (PRD §N3)
│   ├── 02_ner_comparison.ipynb          # étude comparative NER (PRD §N2.1)
│   ├── 03_graph_analysis.ipynb          # PageRank · Louvain · Leiden (PRD §N2.2)
│   ├── 04_forecasting_comparison.ipynb  # ARIMA · Prophet · LSTM (PRD §N2.3)
│   └── 05_dashboard_data_prep.ipynb     # JSON pré-calculés pour /web
│
├── tests/                   # pytest + 30 fixtures gold (couverture ≥ 70 %)
│   ├── unit/
│   ├── integration/         # marqueur @pytest.mark.integration (skip CI sans secrets)
│   └── fixtures/
│
├── data/                    # raw/, exports/, audit/ gitignored ; gold_set/ commit
├── sources/registry.yaml    # Registre conformité robots.txt + TOS (PRD §8.5)
├── docs/                    # PRD, charte, rapport L5, plan soutenance
├── scripts/                 # Scripts utilitaires (seed taxonomy, etc.)
│
├── pyproject.toml           # Poetry + ruff + mypy + black + pytest configs
├── .pre-commit-config.yaml  # ruff + black + mypy + check-yaml + detect-secrets
├── Makefile                 # Commandes courantes
├── CLAUDE.md                # Consignes Claude Code
└── .env.example             # Template variables d'environnement
```

---

## 6 livrables imposés (Pr. Sassi)

| # | Livrable | Forme livrée |
|---|---|---|
| **L1** | Scripts de collecte documentés | Repo `skillnav/` (`scrapers/`, `pipelines/`) + README |
| **L2** | Base de données hybride | MongoDB Atlas + Neo4j AuraDB + Elastic Cloud (dumps fournis) |
| **L3** | Pipeline IA validé par métriques | Notebook `02_ner_comparison.ipynb` + page `/comparative-study` |
| **L4** | Dashboard interactif | `skillnav.vercel.app` (8 pages) |
| **L5** | Rapport méthodologique | `docs/RAPPORT_METHODOLOGIQUE.md` → PDF (25–40 pages) |
| **L6** | Présentation soutenance | `docs/PLAN_SOUTENANCE.md` + deck PPTX + démo live |

---

## Quality gates

> Quality gate manuel : `make quality` exécute le pipeline complet localement (lint + typecheck + test). Pre-commit hooks bloquent les commits non conformes.

### Python

| Gate | Outil | Règle |
|---|---|---|
| Lint | `ruff check .` | E · F · W · I · B · C4 · UP · N · SIM · RET · ARG · PTH |
| Format | `black --check .` | line-length 100, target py312 |
| Typecheck | `mypy --strict skillnav` | aucun `Any` toléré sur fonctions publiques |
| Tests | `pytest` | couverture **≥ 70 %** sur `schemas/`, `pipelines/`, `comparative_studies/` |

### TypeScript

| Gate | Outil | Règle |
|---|---|---|
| Lint | `pnpm lint` (ESLint Next.js 15) | aucun `any`, react-hooks/exhaustive-deps strict |
| Typecheck | `pnpm typecheck` | `tsc --noEmit` strict (`noUncheckedIndexedAccess`, etc.) |
| Format | `pnpm format:check` | Prettier + plugin Tailwind |
| Build | `pnpm build` | Next.js production build doit passer |

### Pre-commit hooks

`make setup` installe `pre-commit install`. Hooks à chaque commit : ruff (fix + format) · mypy · check-yaml · check-toml · detect-secrets · trailing-whitespace · end-of-file-fixer.

---

## Commandes Make

```
make help          # liste complète

make install       # poetry install
make install-web   # pnpm install (web/)
make setup         # install + install-web + pre-commit install

make lint          # ruff check
make format        # black + ruff format
make typecheck     # mypy strict
make test          # pytest avec couverture
make test-fast     # pytest sans -m "slow" ni "integration"
make quality       # lint + typecheck + test  (CI gate)

make api           # uvicorn FastAPI dev (:8000)
make web-dev       # Next.js dev (:3000)
make cli           # poetry run skillnav --help

make clean         # supprime caches (pytest, mypy, ruff, coverage)
```

---

## Conventions

### Git

- Branches courtes par sprint et par feature : `feat/sprint-1-mongodb-setup`, `fix/scraper-rekrute-pagination`
- **Conventional Commits** : `feat:` `fix:` `docs:` `refactor:` `test:` `chore:` `perf:`
- PR review systématique en binôme avant merge sur `main`
- Pre-commit hooks obligatoires (`make setup` les installe)

### Pydantic = source de vérité unique

Tous les schémas (MongoDB / Neo4j / Elasticsearch) **dérivent** des modèles Pydantic v2 dans [`skillnav/schemas/`](skillnav/schemas/) :

```
skillnav/schemas/
├── job.py          # JobExtraction, RawJob — sources de vérité
├── ner.py          # NerAnnotation, Entity
├── graph.py        # SkillNode, JobNode, Edge
├── timeseries.py   # SkillTimeSeries, Forecast
└── converters/
    ├── to_mongo.py # Pydantic → BSON
    ├── to_neo4j.py # Pydantic → params Cypher
    └── to_es.py    # Pydantic → ES document
```

Une mutation de schéma **doit** casser au type-check tous les converters. C'est voulu.

### Pattern d'ajout d'une fonctionnalité

1. Schéma Pydantic d'abord (`skillnav/schemas/`)
2. Converter vers la DB cible (`skillnav/schemas/converters/`)
3. Implémentation pipeline (`skillnav/pipelines/<axe>/`)
4. Test unitaire (`tests/unit/`)
5. Test intégration si DB externe (`tests/integration/` + marker `@pytest.mark.integration`)
6. Endpoint FastAPI si exposé (`skillnav/api/`)
7. Type généré côté front (`web/src/lib/api/types.ts` — `pnpm generate-types`)
8. Composant React (`web/src/components/`)
9. Page Next.js (`web/src/app/<route>/page.tsx`)

---

## Conformité RGPD

```
┌──────────────────────────────────────────────────────────────────┐
│  BASE LÉGALE   art. 6.1.f RGPD — intérêt légitime                │
│  CADRE         Recherche académique encadrée (ENSA-Tétouan)      │
│  PÉRIMÈTRE     Données publiques d'entités JURIDIQUES uniquement │
│                Aucune donnée personnelle de candidat collectée   │
└──────────────────────────────────────────────────────────────────┘
```

| Donnée | Statut |
|---|---|
| Nom employeur, ville, secteur d'activité | Collecté (entité morale) |
| Description offre, compétences, salaire | Collecté (donnée publique) |
| Nom recruteur, email, téléphone | **Jamais** collecté |
| URL profil candidat, photo, parcours | **Jamais** collecté |

- robots.txt : respect strict, parsing systématique, log compliance dans `data/audit/`
- Rate limiting : 5 s minimum sur sources statiques ; respect des `Crawl-delay`
- User-Agent identifié : `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)`
- Toutes les sources inscrites au registre [`sources/registry.yaml`](sources/registry.yaml) avec date de revue TOS

DPIA complète : [`docs/RGPD_DPIA.md`](docs/RGPD_DPIA.md).

---

## Équipe

Projet porté en **binôme** par **Karamo Sylla** et **Bachirou Konaté**, élèves-ingénieurs en filière SDBIA à l'ENSA-Tétouan, sous l'encadrement du **Pr. Imad Sassi** (module M242).

Couverture parallèle des trois axes Web Mining (Content · Structure · Usage), de la collecte des données à la soutenance, en pair-rédaction sur les sections critiques.

---

## License

MIT License — voir le champ `license` de [`pyproject.toml`](pyproject.toml).

Projet pédagogique. Toute réutilisation académique bienvenue avec citation : *« SKILLNAV — Sylla K. & Konaté B., M242 ENSA-Tétouan, 2026 »*.

---

<div align="center">

**Mai 2026 · Karamo Sylla & Bachirou Konaté**
*Diplôme d'Ingénieur SDBIA — ENSA-Tétouan*
M242 Analyse de Web · Pr. Imad Sassi

</div>
