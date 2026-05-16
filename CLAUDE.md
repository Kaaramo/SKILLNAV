# CLAUDE.md — Consignes Claude Code pour SKILLNAV

> **Skills Navigator** — observatoire des compétences IA & Data Science par Web Mining.
> M242 — Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi · Soutenance **28 mai 2026**.
> Binôme : **Karamo Sylla** & **Bachirou Konaté**.

---

## Lecture obligatoire avant action

Lire dans cet ordre, à la première interaction d'une session :

1. **PRD condensé** — [`docs/PRD_CONDENSE.md`](docs/PRD_CONDENSE.md) (lecture rapide ASCII partout)
2. **PRD exhaustif** — [`docs/PRD.md`](docs/PRD.md) (référence détaillée)
3. **Charte graphique** — [`docs/CHARTE_GRAPHIQUE_SKILLNAV.pdf`](docs/CHARTE_GRAPHIQUE_SKILLNAV.pdf)
4. **Sujet imposé** — [`docs/Projet Final Analyse de Web_Sujet 1.pdf`](docs/) — **intangible**, ne jamais modifier
5. **Registre curricula ENSA** — [`sources/curricula/REGISTRY.md`](sources/curricula/REGISTRY.md) (volet écoles ↔ marché)

---

## Périmètre projet — verrouillé

### Période d'observation : 2023 → 2026 (36 mois)

Point d'ancrage = **sortie de ChatGPT en novembre 2022**, qui démocratise l'IA générative grand public. C'est le déclencheur structurel de l'évolution observée du marché des compétences IA.

### Périmètre métiers — *tout Data Science + Intelligence Artificielle*

Inclus sans exception : Data Analyst, Business Analyst, Data Scientist, Data Engineer, ML Engineer, MLOps Engineer, AI Engineer, NLP Engineer, CV Engineer, Research Scientist, Generative AI / LLM Engineer, et tout titre proche.

### Géographie

Maroc en priorité (Rekrute, EmploiTIC, LinkedIn MA, pages carrières) — International en complément (LinkedIn, Indeed, builtin.com, WTTJ).

### Stratégie de collecte historique (validée)

Triplet **Wayback Machine + scraping live + Google Trends** :

| Source | Couverture | Outil |
|---|---|---|
| Wayback Machine (archive.org) | 2023-2025 (offres expirées sinon perdues) | Crawl4AI / Playwright sur snapshots datés |
| Scraping live (mai 2026) | État actuel du marché | Crawl4AI · Playwright · Firecrawl · Apify |
| Google Trends + GitHub Trending + HF Hub | Signaux faibles continus 2023-2026 | pytrends + API HF + scraping |

**Raison** : LinkedIn / Indeed / Rekrute ne conservent pas les offres expirées. Sans Wayback, l'axe Usage Mining (forecasting ARIMA / Prophet / LSTM) ne tient pas. La stratégie est documentée dans le rapport L5 §3.1.

### Volet parallèle — Curricula ENSA Maroc (gap analysis)

SKILLNAV a un **deuxième axe analytique** : mesurer le désalignement entre les compétences **demandées** par le marché et les compétences **enseignées** par le réseau ENSA Maroc.

Recensement à jour dans [`sources/curricula/`](sources/curricula/REGISTRY.md) :

- 12 ENSA dans le réseau public marocain
- **8 ENSA** dispensent une filière Data Science / Big Data / IA en cycle ingénieur (3 ans, S1-S6)
- Programmes complets extraits pour **2/8** (ENSA Berrechid - ISIBD et ENSA Safi - IDIA)
- Programmes placeholder + TODOs pour les 6 autres (Tétouan SDBIA, Khouribga IID, Oujda IDSCC, Agadir SDBIA, Fès ILIA, El Jadida 2ITE)

Pipeline associé (à créer en Sprint 2) :
- `skillnav/pipelines/curriculum_mining/` — parse `filiere.md` → schéma Pydantic
- `skillnav/schemas/curriculum.py` — `CurriculumExtraction(school, filiere, semester, modules[], skills_taught[])`
- `notebooks/06_gap_analysis_market_vs_curriculum.ipynb` — chiffrer le recouvrement marché ↔ formation
- Page dashboard `/gap-analysis` — top compétences marché vs top enseignées

---

## Stack — référence rapide

| Couche | Technologie | Version |
|---|---|---|
| Language | Python | 3.12 |
| Package | Poetry | 1.8+ |
| Extraction IA | Pydantic AI + Claude Sonnet 4.5 + Haiku 4.5 | latest |
| NLP | HuggingFace Transformers (BERT-multi · CamemBERT-NER · DistilBERT) | 4.40+ |
| Storage | MongoDB Atlas + Neo4j AuraDB + Elasticsearch Cloud | free tiers |
| API | FastAPI + uvicorn | 0.110+ |
| Front | Next.js 15 + TypeScript 5.4 + Tailwind v4 + Shadcn/ui | — |
| Charts | Recharts · Tremor · react-force-graph-2d · Plotly | latest |
| Quality | ruff · mypy strict · black · pytest | latest |

---

## Pydantic = source de vérité unique

Tous les schémas dérivent des modèles **Pydantic v2** dans `skillnav/schemas/` :

```
skillnav/schemas/
├── job.py          # JobExtraction, RawJob — sources de vérité
├── ner.py          # NerAnnotation, Entity
├── graph.py        # SkillNode, JobNode, Edge
├── timeseries.py   # SkillTimeSeries, Forecast
├── curriculum.py   # CurriculumExtraction (volet écoles ENSA — sprint 2)
└── converters/
    ├── to_mongo.py # Pydantic → BSON
    ├── to_neo4j.py # Pydantic → Cypher params
    └── to_es.py    # Pydantic → ES document
```

Une mutation de schéma **doit** casser au type-check tous les converters. C'est voulu.

---

## Conventions Python

- **Format** : `black` (line-length 100) — `make format` ou `poetry run black .`
- **Lint** : `ruff` — règles E, F, W, I, B, C4, UP, N, SIM, RET, ARG, PTH
- **Typecheck** : `mypy --strict` — toute fonction publique typée, aucun `Any`
- **Tests** : `pytest` — fixtures sur 30 offres gold dans `tests/fixtures/`
- **Couverture** : ≥ 70 % sur `skillnav/schemas/`, `skillnav/pipelines/`, `skillnav/comparative_studies/`
- **Async** : motor (Mongo) + httpx — `asyncio_mode = auto` dans pytest
- **Paths** : `pathlib.Path`, jamais `os.path` (règle `PTH` activée)

## Conventions TypeScript / Next.js

- **Strict** : `tsc --noEmit` strict — pas de types `any`
- **ESLint** : config Next.js 15
- **Types API** : générés depuis `/openapi.json` via `openapi-typescript`
- **Composants** : Shadcn/ui d'abord, Tremor pour dashboards rapides, Recharts pour custom

## Conventions Git

- Branches courtes par sprint et par feature : `feat/sprint-1-mongodb-setup`, `fix/scraper-rekrute-pagination`
- **Conventional Commits** : `feat:` `fix:` `docs:` `refactor:` `test:` `chore:` `perf:`
- PR review systématique entre Karamo et Bachirou Konaté avant merge sur `main`
- Pre-commit hooks obligatoires : `make setup` les installe

---

## Variables d'environnement (.env)

| Variable | Usage |
|---|---|
| `ANTHROPIC_API_KEY` | Pydantic AI — extraction Claude Sonnet 4.5 |
| `MONGODB_URI` + `MONGODB_DB` | Source of truth |
| `NEO4J_URI` + `NEO4J_USER` + `NEO4J_PASSWORD` | Graphe Skill ↔ Job |
| `ELASTIC_CLOUD_ID` + `ELASTIC_API_KEY` | Recherche + agrégations |
| `APIFY_TOKEN` | LinkedIn jobs scraping conforme |
| `FIRECRAWL_API_KEY` | Pages dynamiques |
| `SCRAPER_USER_AGENT` | Identification scrapers (PRD §N4) |
| `SCRAPER_RATE_LIMIT_SECONDS` | Politesse minimum (5 s par défaut) |

Voir [`.env.example`](.env.example) pour le template complet.

---

## CLI principal

```bash
poetry run skillnav --help

# Pipeline standard d'un sprint
poetry run skillnav scrape --source=rekrute,emploitic
poetry run skillnav extract --batch=last
poetry run skillnav graph build
poetry run skillnav forecast run
poetry run skillnav index push
```

---

## Repository structure (référence rapide)

```
.
├── skillnav/                # Package Python (entry: skillnav.cli:app)
│   ├── schemas/             # Pydantic v2 — source de vérité
│   ├── db/                  # Connexions Mongo / Neo4j / ES
│   ├── pipelines/           # content_mining, structure_mining, usage_mining
│   ├── scrapers/            # Rekrute, EmploiTIC, Apify, Indeed, builtin, weak_signals
│   ├── comparative_studies/ # NER, communautés, forecasting, émergence (PRD §N2)
│   ├── api/                 # FastAPI endpoints
│   └── cli.py               # Typer CLI
│
├── web/                     # Next.js 15 (Karamo lead — voir PRD §11)
├── notebooks/               # 6 notebooks numérotés (00-05 + 06_gap_analysis)
├── tests/                   # pytest + 30 fixtures gold
├── data/                    # raw/ exports/ audit/ gitignored ; gold_set/ commit
├── sources/registry.yaml    # Registre conformité robots.txt + TOS (PRD §8.5)
├── sources/curricula/       # Curricula ENSA Maroc — volet gap analysis (8 écoles)
│   ├── REGISTRY.md          # Index humain + statut extraction par école
│   ├── registry.yaml        # Index machine-lisible (pipeline curriculum_mining/)
│   └── ensa-<slug>/         # 1 dossier par école : source.yaml + filiere.md
├── docs/                    # PRD, charte, rapport L5, plan soutenance
└── scripts/                 # Scripts utilitaires (seed taxonomy, etc.)
```

---

## RGPD — règles strictes (PRD §N4)

- **Jamais** de données personnelles de candidat (nom, email, téléphone, photo, profil LinkedIn personnel)
- Données collectées : entités morales (employeurs) + descriptions publiques d'offres uniquement
- Tous les scrapers respectent `robots.txt` + `Crawl-delay`
- User-Agent identifié : `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)`
- DPIA : [`docs/RGPD_DPIA.md`](docs/RGPD_DPIA.md)

---

## Sécurité supply-chain

L'écosystème npm a subi plusieurs attaques massives en 2025-2026 (Shai-Hulud, mini Shai-Hulud). Le 11 mai 2026, **42 packages `@tanstack/*`** ont été compromis (CVE-2026-45321) — la famille `@tanstack/query*` que nous utilisons a été confirmée *clean* mais on durcit quand même.

**Règles non-négociables** :

1. **Versions pinnées** (sans `^` ni `~`) pour les deps critiques de sécurité :
   - `@tanstack/react-query` et `@tanstack/react-query-devtools` → version exacte
   - Toute nouvelle dep utilisée pour traiter du contenu utilisateur ou exécuter du code → version exacte
2. **Lockfiles toujours commités** : `poetry.lock` (Python) et `web/pnpm-lock.yaml` (TS)
3. **Audit avant chaque push** : `make audit-all` (combine `pip-audit` côté Python et `pnpm audit` côté web)
4. **Bannis** :
   - `@tanstack/react-query-next-experimental` (CVE-2024-24558 XSS — on ne l'a jamais ajouté)
   - Toute dep marquée *experimental* / *alpha* sans audit préalable
5. **Update process** : `pnpm update` ou `poetry update` jamais en aveugle — toujours vérifier le changelog + lire un avis sécurité (Snyk, Wiz, GitHub Advisories) si la dep est critique

---

## Outillage MCP (optionnel)

Configurés dans `.claude/settings.json` (gitignored, à créer localement) :

- `apify` MCP — LinkedIn jobs scraping
- `firecrawl` MCP — pages dynamiques
- `mongodb` MCP — exploration données

---

## Ne jamais faire

- ❌ Committer `.env`, dumps de prod, données candidates identifiantes
- ❌ Scraper en ignorant robots.txt — refuser et signaler
- ❌ Modifier les PDFs livrables à la main — éditer le DOCX (Word) puis re-exporter en PDF
- ❌ Inventer des chiffres, métriques ou résultats sans notebook source — toute valeur publiée doit être traçable
- ❌ Ajouter des dépendances Python sans `poetry add` (jamais éditer `poetry.lock` à la main)

---

## Bonus — pattern de déclaration d'une nouvelle fonctionnalité

Quand vous (Claude Code) créez une nouvelle feature, structurer le commit ainsi :

1. Schéma Pydantic d'abord (`skillnav/schemas/`)
2. Converter vers la DB cible (`skillnav/schemas/converters/`)
3. Pipeline implémentation (`skillnav/pipelines/<axe>/`)
4. Test unitaire (`tests/unit/`)
5. Test intégration si DB externe (`tests/integration/` + marker `@pytest.mark.integration`)
6. Endpoint FastAPI si exposé (`skillnav/api/`)
7. Type généré côté front (`web/src/lib/api/types.ts` — auto)
8. Composant React (`web/src/components/`)
9. Page Next.js (`web/src/app/<route>/page.tsx`)

---

**Référence officielle — Mai 2026 · Karamo Sylla & Bachirou Konaté · ENSA-Tétouan**
