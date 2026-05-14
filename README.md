# SKILLNAV — Skills Navigator

> Observatoire académique des compétences en Intelligence Artificielle et Data Science par le Web Mining.

**Cadre** : Module M242 — Analyse de Web · ENSA-Tétouan · Diplôme d'Ingénieur, filière Sciences des Données, Big Data et Intelligence Artificielle (SDBIA)
**Encadrement** : Pr. Imad Sassi
**Équipe** : Karamo Sylla & Bachirou Konaté
**Soutenance** : 28 mai 2026

---

## En bref

SKILLNAV démontre la couverture rigoureuse des **trois axes canoniques du Web Mining** (Content, Structure, Usage) appliqués à un domaine en évolution rapide : les compétences IA / Data Science.

| Axe | Technique | Modèles comparés |
|---|---|---|
| Content | NER sur offres d'emploi IA / DS | BERT-multilingual · CamemBERT-NER · DistilBERT |
| Structure | Graphe Skill ↔ Job ↔ Family | Louvain · Label Propagation · Leiden (modularité chiffrée) |
| Usage | Forecasting compétences émergentes | ARIMA · Prophet · LSTM (MAPE comparé) |

**Volume cible MVP** : 500–2 000 offres analysées sur Maroc + International.

**Architecture NoSQL polyglotte** : **MongoDB Atlas** (source of truth) + **Neo4j AuraDB** (graphe) + **Elasticsearch Cloud** (recherche + agrégations).

**Pipeline IA** : Pydantic AI + Claude Sonnet 4.5 pour l'extraction structurée ; HuggingFace Transformers pour la NER comparative. Schémas Pydantic v2 comme source de vérité unique.

**Dashboard** : Next.js 15 + TypeScript + Tailwind v4 + Shadcn/ui, déployé sur Vercel. Direction artistique McKinsey-inspired (cf. charte graphique).

---

## Documents-clés

| Document | Rôle |
|---|---|
| [`docs/PRD.md`](docs/PRD.md) | Spécification produit **complète** (~2600 lignes, 27 sections + N1–N4) |
| [`docs/PRD_CONDENSE.md`](docs/PRD_CONDENSE.md) | **PRD condensé orienté schémas** (~660 lignes, 17 sections, ASCII partout) — lecture rapide pour le binôme et le jury |
| [`docs/PRD_CONDENSE_SKILLNAV.pdf`](docs/PRD_CONDENSE_SKILLNAV.pdf) | **PRD condensé — version premium** — 25 pages A4 (cover full-bleed Navy, TOC, sections eyebrow, tables compactes, schémas ASCII en boxes) |
| [`docs/PRD_CONDENSE_SKILLNAV.docx`](docs/PRD_CONDENSE_SKILLNAV.docx) | Source modifiable du PRD condensé premium (Word) |
| [`docs/CHARTE_GRAPHIQUE_SKILLNAV.pdf`](docs/CHARTE_GRAPHIQUE_SKILLNAV.pdf) | **Charte graphique officielle** — 13 pages premium (cover full-bleed Navy, palette en cards, typographie, composants) |
| [`docs/CHARTE_GRAPHIQUE_SKILLNAV.docx`](docs/CHARTE_GRAPHIQUE_SKILLNAV.docx) | Source modifiable de la charte (Word) |
| [`docs/CHARTE_GRAPHIQUE_SKILLNAV.md`](docs/CHARTE_GRAPHIQUE_SKILLNAV.md) | Référence technique étendue — détails composants Neo4j, Forecasting, NER |
| [`docs/RAPPORT_METHODOLOGIQUE.md`](docs/RAPPORT_METHODOLOGIQUE.md) | Livrable L5 (rapport académique, en cours de rédaction) |
| [`docs/PLAN_SOUTENANCE.md`](docs/PLAN_SOUTENANCE.md) | Livrable L6 (plan détaillé soutenance 25 min) |
| [`docs/RGPD_DPIA.md`](docs/RGPD_DPIA.md) | DPIA simplifiée + protocole robots.txt |
| [`docs/Projet Final Analyse de Web_Sujet 1.pdf`](docs/Projet%20Final%20Analyse%20de%20Web_Sujet%201.pdf) | Sujet imposé par le Pr. Sassi (référence) |

---

## 6 livrables prof M242

| # | Livrable | Statut |
|---|---|---|
| L1 | Scripts de collecte documentés (repo `skillnav/`) | À démarrer Sprint 1 |
| L2 | Base de données hybride (MongoDB + Neo4j + Elasticsearch) | À démarrer Sprint 1 |
| L3 | Pipeline IA validé par métriques (notebook `02_ner_comparison`) | À démarrer Sprint 2 |
| L4 | Dashboard interactif (`skillnav.vercel.app`) | À démarrer Sprint 1 |
| L5 | Rapport méthodologique (PDF 25–40 pages) | À démarrer Sprint 2 |
| L6 | Présentation soutenance (deck + démo live) | À finaliser Sprint 3 |

---

## Setup

### Prérequis

- **Python 3.12** (`python --version`)
- **Poetry 1.8+** (`poetry --version`) — `pipx install poetry` recommandé
- **Node 20+** (`node --version`)
- **pnpm 9+** (`pnpm --version`) — `corepack enable && corepack prepare pnpm@9 --activate`
- Comptes free tier : MongoDB Atlas, Neo4j AuraDB, Elasticsearch Cloud, Anthropic, Apify

### Installation rapide

```bash
# 1. Cloner et entrer
git clone https://github.com/karamosylla/skillnav.git
cd skillnav

# 2. Setup complet (Python + web + pre-commit hooks)
make setup

# 3. Variables d'environnement (à remplir)
cp .env.example .env
cp web/.env.example web/.env.local

# 4. Vérifier l'installation
make quality      # ruff + mypy + pytest
poetry run skillnav --help
```

### Commandes Make principales

```
make help          # liste complète
make install       # poetry install
make install-web   # pnpm install (web/)
make lint          # ruff check
make format        # black + ruff format
make typecheck     # mypy strict
make test          # pytest avec couverture
make quality       # lint + typecheck + test (CI gate)
make api           # uvicorn FastAPI dev server
make web-dev       # Next.js dev server
make charte        # régénère charte graphique DOCX
make prd-condense  # régénère PRD condensé DOCX
```

---

## Structure du repository

```
.
├── skillnav/                # Package Python (entry: `skillnav.cli:app`)
│   ├── schemas/             # Pydantic v2 — source de vérité unique
│   ├── db/                  # Connexions Mongo / Neo4j / ES
│   ├── pipelines/           # content_mining · structure_mining · usage_mining
│   ├── scrapers/            # Rekrute, EmploiTIC, Apify, Indeed, builtin, weak_signals
│   ├── comparative_studies/ # NER, communautés, forecasting, émergence (PRD §N2)
│   ├── api/                 # FastAPI endpoints
│   └── cli.py               # Typer CLI
│
├── web/                     # Next.js 15 + TS + Tailwind v4 + Shadcn (Karamo lead)
├── notebooks/               # 5 notebooks Jupyter numérotés (PRD §11.1)
├── tests/                   # pytest + 30 fixtures gold (couverture ≥ 70 %)
├── data/                    # raw/ exports/ audit/ gitignored ; gold_set/ commit
├── sources/registry.yaml    # Registre conformité robots.txt + TOS (PRD §8.5)
├── docs/                    # PRD, charte, rapport L5, plan soutenance
├── scripts/                 # Build PDFs (charte + PRD condensé)
├── .github/workflows/       # CI : python (lint+typecheck+test) + web (lint+build)
├── pyproject.toml           # Poetry + ruff + mypy + black + pytest configs
├── Makefile                 # Commandes courantes
└── CLAUDE.md                # Consignes Claude Code (conventions, RGPD, env)
```

Voir [`docs/PRD_CONDENSE.md`](docs/PRD_CONDENSE.md) §12 pour le détail.

---

## Quality gates

- **Python** : `ruff` (E/F/W/I/B/C4/UP/N/SIM/RET/ARG/PTH) · `black` (line-length 100) · `mypy --strict` · `pytest` couverture ≥ 70 %
- **TypeScript** : `tsc --noEmit` strict · ESLint Next.js 15 · Prettier
- **Pre-commit hooks** : ruff + black + mypy + check-yaml + detect-secrets — installés via `make setup`
- **CI GitHub Actions** : `.github/workflows/ci.yml` exécute le pipeline complet sur PR

---

## Calendrier — 18 jours, 3 sprints

| Sprint | Période | Objectif |
|---|---|---|
| S1 | J1–J6 (10–16 mai 2026) | Fondations : DBs, scrapers, MongoDB ≥ 200 offres |
| S2 | J7–J12 (17–22 mai 2026) | Cœur : NER comparatif, Neo4j, dashboard pages-clés |
| S3 | J13–J18 (23–28 mai 2026) | Forecasting, étude comparative chiffrée, rapport L5, deck |
| Soutenance | 28 mai 2026 | 15 min présentation + démo live + 10 min Q&A |

---

## Conformité

- RGPD : base légale art. 6.1.f (intérêt légitime — recherche académique). Aucune donnée personnelle de candidat collectée. Voir `docs/RGPD_DPIA.md`.
- robots.txt : respect strict. User-Agent identifié `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)`.
- Rate limiting : 5 s / requête minimum sur sources statiques ; respect des `Crawl-delay`.

---

**Mai 2026 · Karamo Sylla & Bachirou Konaté · ENSA-Tétouan**
