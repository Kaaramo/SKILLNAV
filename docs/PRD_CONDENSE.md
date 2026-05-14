# PRD CONDENSÉ — SKILLNAV

> **Skills Navigator — Observatoire des Compétences IA & Data Science par Web Mining**
> Version condensée, orientée schémas. La version exhaustive reste dans [`PRD.md`](PRD.md).

| | |
|---|---|
| **Cadre académique** | M242 — Analyse de Web · ENSA-Tétouan · Diplôme d'Ingénieur, filière Sciences des Données, Big Data et IA (SDBIA) |
| **Encadrement** | Pr. Imad Sassi |
| **Auteurs** | Karamo Sylla & Bachirou Konaté |
| **Soutenance** | 28 mai 2026 (15 min + 4 min démo + 10 min Q&A) |
| **Volume cible MVP** | 500–2 000 offres · Maroc + International |
| **Architecture** | NoSQL polyglotte — MongoDB + Neo4j + Elasticsearch |
| **Coût total MVP** | < $50 (free tiers + Anthropic + Apify) |

---

## 1. SUJET → SECTIONS DU PRD

```
┌──────────────────────────────────────────────────────────────────┐
│  SUJET PR. SASSI — 6 EXIGENCES                                   │
│                                                                  │
│  E1 ─ 3 axes Web Mining (Content / Structure / Usage) ─→ §2 + §6│
│  E2 ─ NoSQL hybride justifiée ──────────────────────────→ §5     │
│  E3 ─ Pipeline IA + HuggingFace Transformers ──────────→ §6.B    │
│  E4 ─ Étude comparative ≥ 3 algos par tâche ───────────→ §8      │
│  E5 ─ RGPD + robots.txt + anonymisation ───────────────→ §9      │
│  E6 ─ 6 livrables : scripts, BD, IA, dashboard, rapport, soutenance│
│                                                          → §10   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. MAPPING PROJET ↔ 3 AXES WEB MINING

| Axe | Pondération | Technique | Algos comparés | Livrable principal |
|---|:---:|---|---|---|
| **Content** | 35 % | NER + extraction structurée | BERT-multi · CamemBERT-NER · DistilBERT (+ baseline règles) | Notebook `02_ner_comparison` · page `/ner-explorer` |
| **Structure** | 30 % | Graphe Skill ↔ Job ↔ Family + détection communautés | Louvain · Label Propagation · Leiden | Neo4j AuraDB · page `/graph` |
| **Usage** | 30 % | Forecasting compétences émergentes | ARIMA · Prophet · LSTM | Notebook `04_forecasting_comparison` · page `/forecasting` |
| **Transverse** | 5 % | Data Quality + Pipeline + Dashboard | — | Pages `/quality`, `/methodology`, `/comparative-study` |

---

## 3. PARCOURS INTERNE — BINÔME (parcours optimisé, exécuté à chaque sprint)

```
┌─────────────────────────────────────────────────────────────────┐
│  DÉBUT DE SPRINT — Karamo & Bachirou Konaté                     │
│  Repo cloné · Poetry installé · DBs cloud free tier             │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 — COLLECTE                          (Karamo lead)      │
│  Scrapy + Playwright + Apify MCP + Firecrawl                    │
│   • Maroc        : Rekrute, EmploiTIC, LinkedIn MA              │
│   • International: LinkedIn, Indeed, builtin.com, WTTJ          │
│   • Signaux      : Google Trends, GitHub, HuggingFace           │
│   • Persistence  : MongoDB Atlas — collection raw_jobs          │
│  ~30 min / 500 offres                                           │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 — EXTRACTION IA + NER               (Karamo lead)      │
│  $ poetry run skillnav extract --batch=last                     │
│   • Pydantic AI + Claude Sonnet 4.5  → extracted_jobs           │
│   • HF Transformers × 3 modèles      → ner_annotations          │
│   • Quarantaine auto si confidence < 0.75                       │
│  ~30 min / 500 offres · coût ~$5–10                             │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 — GRAPHE                  (Bachirou Konaté lead)       │
│  $ poetry run skillnav graph build                              │
│   • Co-occurrences Skill ↔ Skill ↔ Job ↔ Family                 │
│   • Neo4j AuraDB (nœuds + arêtes)                               │
│   • Algos : PageRank, Louvain, Label Propagation                │
│  ~10 min                                                        │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 4 — INDEX + FORECASTING              (Karamo lead)       │
│  $ poetry run skillnav index push                               │
│  $ poetry run skillnav forecast run                             │
│   • Elasticsearch : jobs_search + skills_timeseries             │
│   • ARIMA / Prophet / LSTM sur skill_count(time)                │
│  ~15 min                                                        │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 5 — NOTEBOOKS + DATA QUALITY         (binôme)            │
│   01_data_quality          (Bachirou Konaté)                    │
│   02_ner_comparison        (Karamo)                             │
│   03_graph_analysis        (Bachirou Konaté)                    │
│   04_forecasting_comparison(Karamo)                             │
│   05_dashboard_data_prep   (Karamo)                             │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 6 — DASHBOARD NEXT.JS                (Karamo lead)       │
│  $ cd web && pnpm dev                                           │
│   • 8 pages : /, /skills, /graph, /forecasting,                 │
│     /ner-explorer, /methodology, /comparative-study, /quality   │
│   • Données : FastAPI + JSON pré-calculés                       │
│   • Visu : Recharts, Tremor, react-force-graph, Plotly          │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 7 — RAPPORT L5 + DECK                                    │
│   • Bachirou Konaté : rédaction L5 intégrale                    │
│   • Karamo          : captures dashboard, schémas archi, deck   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. FONCTIONNALITÉS MVP → V1.5 → V2

| # | Axe | Fonctionnalité | MVP | V1.5 | V2 |
|---|:---:|---|:---:|:---:|:---:|
| F01 | T | Scraping Maroc (Rekrute, EmploiTIC, LinkedIn MA) | ✅ | ✅ | ✅ |
| F02 | T | Scraping International (LinkedIn, Indeed, builtin, WTTJ) | ✅ | ✅ | ✅ |
| F03 | T | Signaux faibles (Google Trends, GitHub, HF) | ✅ | ✅ | ✅ |
| F04 | C | Extraction Pydantic AI (skills + responsibilities + use cases) | ✅ | ✅ | ✅ |
| F05 | C | NER comparatif 3 modèles HF | ✅ | ✅ | ✅ |
| F06 | C | Normalisation taxonomique (sentence-transformers) | ✅ | ✅ | ✅ |
| F07 | C | Classification 10 familles IA / DS | ✅ | ✅ | ✅ |
| F08 | S | Graphe Neo4j (Skill / Job / Family / Source) | ✅ | ✅ | ✅ |
| F09 | S | PageRank — top compétences-pivot | ✅ | ✅ | ✅ |
| F10 | S | Communautés (Louvain · Label Propag · Leiden) | ✅ | ✅ | ✅ |
| F11 | U | Séries temporelles skill_count(time) mensuelles | ✅ | ✅ | ✅ |
| F12 | U | Forecasting (ARIMA · Prophet · LSTM) | ✅ | ✅ | ✅ |
| F13 | U | Détection émergence (3 méthodes comparées) | ✅ | ✅ | ✅ |
| F14 | T | Indexation Elasticsearch | ✅ | ✅ | ✅ |
| F15 | T | API FastAPI typée OpenAPI | ✅ | ✅ | ✅ |
| F16 | T | Dashboard Next.js (8 pages) | ✅ | ✅ | ✅ |
| F17 | T | 5 notebooks Jupyter numérotés | ✅ | ✅ | ✅ |
| F18 | T | Rapport méthodologique L5 (PDF) | ✅ | ✅ | ✅ |
| F19 | T | Deck soutenance + démo live | ✅ | ✅ | ✅ |
| F20 | T | Exports datasets anonymisés | ✅ | ✅ | ✅ |
| F25 | C | Fine-tuning CamemBERT sur gold set SKILLNAV | — | ✅ | ✅ |
| F26 | T | Déploiement public skillnav.ma | — | ✅ | ✅ |
| F27 | T | Pipeline live (Celery + APScheduler) | — | — | ✅ |
| F28 | C | Agents prospectifs (Claude Agent SDK) | — | — | ✅ |
| F29 | T | API publique versionnée | — | — | ✅ |

---

## 5. SOURCES DE DONNÉES

```
┌──────────────────────────────────────────────────────────────────┐
│  3 CATÉGORIES → MongoDB raw_jobs                                 │
└──────────────────────────────────────────────────────────────────┘
```

### 5.1 Maroc (national)

| Source | Mode | Particularité |
|---|---|---|
| **Rekrute** | Scrapy (HTML statique) | Premier portail MA · sitemap accessible |
| **EmploiTIC** | Scrapy + Playwright (JS) | Spécialisé IT — IA / DS / dev |
| **LinkedIn MA** | Apify MCP `linkedin-jobs-scraper` | Plafond 200 offres / session |
| **Pages carrières** | Firecrawl MCP | OCP, INWI, banques, scale-ups |

### 5.2 International

| Source | Mode | Particularité |
|---|---|---|
| **LinkedIn Inter.** | Apify (FR + EU + US) | Volume principal |
| **Indeed** (.fr / .com) | Scrapy + Playwright | HTML stable, FR + EN |
| **builtin.com** | Scrapy | Tech-only US, IA pointue |
| **Welcome to the Jungle** | Playwright (SPA) | Marché tech FR, descriptions denses |
| **Otta** *(si bandwidth)* | Firecrawl | Tech jobs UK / EU |

### 5.3 Signaux faibles (validation Usage Mining)

| Source | Type | Library |
|---|---|---|
| **Google Trends** | Recherches publiques | `pytrends` |
| **GitHub Trending** | Repos tendance | API GitHub |
| **HuggingFace Trending** | Modèles / datasets | API HF Hub |
| **Papers With Code** | Papers IA tendance | Scraping |

### 5.4 Volume cible MVP

```
Maroc national       : 300 –   500 offres
International (FR/EN): 800 – 1 500 offres
Signaux faibles      :  50 –   100 séries temporelles
                      ─────────────────────────────
TOTAL                :       500 – 2 000 offres
```

### 5.5 Conformité — registre source

```yaml
- id: rekrute_ma
  name: Rekrute
  base_url: https://www.rekrute.com
  robots_txt_compliant: true
  tos_reviewed_at: 2026-05-08
  rate_limit_seconds: 5
  user_agent: "SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)"
```

---

## 6. ARCHITECTURE TECHNIQUE

### 6.A Pipeline global

```
   ┌──────────────────────────────────────────┐
   │  COLLECTE  (Karamo)                      │
   │  Scrapy · Playwright · Apify · Firecrawl │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  data/raw/{source}_{date}.jsonl          │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INGESTION (Pydantic) → MongoDB raw_jobs │
   │  Dédup SHA-256 (company+title+location)  │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  CONTENT  (Karamo)                       │
   │  ┌──────────────────────────────────────┐│
   │  │ Pydantic AI + Claude Sonnet 4.5      ││
   │  │  → extracted_jobs                    ││
   │  └──────────────────────────────────────┘│
   │  ┌──────────────────────────────────────┐│
   │  │ HF Transformers × 3 modèles          ││
   │  │  → ner_annotations                   ││
   │  └──────────────────────────────────────┘│
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  STRUCTURE  (Bachirou Konaté)            │
   │  Graphe → Neo4j AuraDB                   │
   │  PageRank · Louvain · Label Propag       │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  USAGE  (Karamo)                         │
   │  Séries temporelles skill_count(time)    │
   │  ARIMA · Prophet · LSTM                  │
   │  Détection émergentes (3 méthodes)       │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INDEXATION → Elasticsearch              │
   │  jobs_search · skills_timeseries         │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  API + DASHBOARD                         │
   │  FastAPI ↔ Mongo / Neo4j / ES            │
   │  Next.js 15 ↔ FastAPI                    │
   │  Render (API) + Vercel (UI)              │
   └──────────────────────────────────────────┘
```

### 6.B Pipeline NER détaillé

```
   raw_text + lang
        │
        ▼
   ┌────────────────────────────────┐
   │  Cleaning                      │
   │   BeautifulSoup → text propre  │
   │   fasttext-langdetect (lang)   │
   │   spaCy (tokenization)         │
   └────────┬───────────────────────┘
            │
   ┌────────▼───────────────────────┐
   │  Pydantic AI + Claude Sonnet 4.5│
   │  → extracted_jobs (BSON)       │
   │  Confidence ≥ 0.75 sinon quaran│
   └────────┬───────────────────────┘
            │
   ┌────────▼───────────────────────┐
   │  HF Transformers (en parallèle)│
   │   • bert-multi  → tous langues │
   │   • camembert   → fr seulement │
   │   • distilbert  → en seulement │
   │  Mapping → SKILL/TOOL/FRAMEWORK│
   │           /MODEL/LANGUAGE/ROLE │
   └────────┬───────────────────────┘
            │
   ┌────────▼───────────────────────┐
   │  Normalisation taxonomique     │
   │   sentence-transformers        │
   │   cosine sim ≥ 0.85 → alias    │
   └────────────────────────────────┘
```

### 6.C Architecture des données

```
MONGODB ATLAS  (source of truth)
   sources              ─→ registre des origines + conformité
   raw_jobs             ─→ HTML brut + metadata
       │1
       ▼N
   extracted_jobs       ─→ Pydantic AI structuré
       │1
       ▼N
   ner_annotations      ─→ 3 docs/offre (1 par modèle NER)
   skills_taxonomy      ─→ canoniques + aliases
   skills_timeseries    ─→ volumes mensuels
   forecasts            ─→ ARIMA / Prophet / LSTM + IC
   graph_metrics        ─→ PageRank, Louvain modularité

NEO4J AURADB   (dérivé)
   (:Skill)-[:CO_OCCURS_WITH {weight}]->(:Skill)
   (:Job)-[:REQUIRES {confidence}]->(:Skill)
   (:Skill)-[:BELONGS_TO]->(:SkillFamily)
   (:Job)-[:FROM_SOURCE]->(:Source)

ELASTICSEARCH  (dérivé)
   jobs_search          ─→ full-text + filtres pays/famille/période
   skills_timeseries    ─→ agrégations mensuelles
```

**Pydantic v2 = source de vérité unique** : tous les converters (`to_mongo`, `to_neo4j`, `to_es`) dérivent des modèles `schemas/*.py`. Une mutation de schéma casse au type-check tous les converters.

---

## 7. STACK TECHNIQUE

| Couche | Outil | Version |
|---|---|---|
| **Language** | Python | 3.12 |
| **Package** | Poetry | 1.8+ |
| **Scraping** | Scrapy · Playwright · Apify MCP · Firecrawl MCP | latest |
| **Extraction IA** | pydantic-ai · anthropic (Claude Sonnet 4.5 + Haiku 4.5) | latest |
| **NLP** | transformers · sentence-transformers · spaCy · fasttext-langdetect | 4.40+ |
| **Graph** | neo4j-driver · networkx · python-louvain · igraph · neo4j-GDS | 5.20+ |
| **Time series** | statsmodels · prophet · neuralforecast (Nixtla) · pytrends | latest |
| **Storage** | MongoDB Atlas (M0) · Neo4j AuraDB Free · Elastic Cloud Free | — |
| **Drivers** | motor · neo4j · elasticsearch | latest |
| **API** | FastAPI · uvicorn | 0.110+ |
| **Front** | Next.js 15 · TypeScript 5.4 · Tailwind v4 · Shadcn/ui · TanStack Query 5 | — |
| **Charts** | Recharts · Tremor · react-force-graph-2d · Plotly | latest |
| **DevOps** | GitHub · Render (API) · Vercel (UI) | — |
| **Quality** | ruff · mypy · black · pytest | latest |

### 7.1 Coûts MVP

```
Apify (LinkedIn)        $5–10
Anthropic Claude        $10–20
MongoDB Atlas           $0       (Free M0)
Neo4j AuraDB            $0       (Free)
Elastic Cloud           $0       (Free 14j → couvre soutenance)
Vercel · Render · GH    $0       (Hobby / Free)
HuggingFace             $0       (inférence locale)
                        ──────
TOTAL MVP            < $50
```

---

## 8. ÉTUDE COMPARATIVE ALGORITHMIQUE (§N2 — CRITIQUE)

### 8.1 NER (axe Content)

| Modèle | Langues | Poids | F1 attendu (gold 30 offres) |
|---|---|---|---|
| Baseline règles (regex listes blanches) | toutes | 0 MB | témoin |
| **bert-base-multilingual-cased** | toutes | 700 MB | 0.62–0.68 |
| **Jean-Baptiste/camembert-ner** | FR | 440 MB | 0.78–0.85 (FR) |
| **distilbert-conll03-english** | EN | 260 MB | 0.80–0.87 (EN) |

**Choix MVP** : routage par langue détectée (camembert FR / distilbert EN / bert-multi fallback). Notebook `02_ner_comparison.ipynb` chiffre le gain réel.

### 8.2 Communautés (axe Structure)

| Algo | Bibliothèque | Modularité attendue | Stabilité |
|---|---|---|---|
| **Louvain** | python-louvain / Neo4j GDS | 0.45–0.60 | Moyenne |
| **Label Propagation** | networkx | 0.40–0.55 | Faible |
| **Leiden** | igraph | 0.45–0.62 | Élevée |

**Choix MVP** : Louvain par défaut (équilibre qualité / stabilité). Leiden = validateur. Label Propagation = baseline rapide.

### 8.3 Forecasting (axe Usage)

| Modèle | Famille | MAPE attendu (top 10 skills) |
|---|---|---|
| **ARIMA** | Statistique classique | 18–28 % |
| **Prophet** | Décomposition Meta | 12–18 % |
| **LSTM (neuralforecast)** | Deep learning | 10–22 % |

**Protocole** : train/test split 9 mois / 3 mois, MAPE médian top 10 skills, intervalles de confiance affichés sur `/forecasting`.

### 8.4 Détection émergence

| Méthode | Approche | Force | Faiblesse |
|---|---|---|---|
| **Heuristique pondérée** | Score = f(growth, recency, volume) | Interprétable | Seuils arbitraires |
| **Supervisé XGBoost** | Train sur 50 skills annotés | Précision ↑ | Coût annotation |
| **Clustering temporel** | KMeans sur trajectoires | Non supervisé | Bruité |

**Synthèse** → page `/comparative-study` : 4 tableaux chiffrés + interprétations + choix justifiés.

---

## 9. RGPD + ROBOTS.TXT (§N4 — CRITIQUE)

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
| Nom employeur, ville, secteur | ✅ Collecté (entité morale) |
| Description offre, compétences, salaire | ✅ Collecté (donnée publique) |
| Nom recruteur, email, téléphone | ❌ **Jamais** collecté |
| URL profil candidat, photo, parcours | ❌ **Jamais** collecté |

**Protocole robots.txt** : parsing systématique, log compliance, respect `Crawl-delay`, rate limiting 5 s minimum sur sources statiques. User-Agent identifié `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)`. Voir [`RGPD_DPIA.md`](RGPD_DPIA.md) pour le DPIA complet.

---

## 10. LIVRABLES (alignement strict 6 livrables Pr. Sassi)

| # | Livrable imposé | Forme livrée | Section PRD | Owner |
|---|---|---|---|---|
| **L1** | Scripts de collecte documentés | Repo `skillnav/` (`scrapers/`, `pipelines/`) + README | §5, §6 | Karamo |
| **L2** | Base de données hybride | MongoDB Atlas + Neo4j AuraDB + Elastic Cloud (dumps fournis) | §6.C | Karamo + Bachirou Konaté |
| **L3** | Pipeline IA validé par métriques | Notebook `02_ner_comparison` + page `/comparative-study` | §6.B, §8.1 | Karamo |
| **L4** | Dashboard interactif | `skillnav.vercel.app` (8 pages) | §11 | **Karamo** |
| **L5** | Rapport méthodologique | `RAPPORT_METHODOLOGIQUE.md` → PDF (25–40 pages) | dédié | **Bachirou Konaté** |
| **L6** | Présentation soutenance | `PLAN_SOUTENANCE.md` + deck PPTX + démo live | §13 | Bachirou Konaté + Karamo |

### 10.1 Détail L5 — Rapport méthodologique

```
1. Introduction         (contexte, problème, contribution)
2. État de l'art        (Web Mining, NER, graph mining, forecasting IA skills)
3. Méthodologie
   3.1 Sources et collecte
   3.2 Architecture polyglotte (MongoDB + Neo4j + ES)
   3.3 Pipeline Content (Pydantic AI + Transformers)
   3.4 Pipeline Structure (Neo4j + PageRank + Louvain)
   3.5 Pipeline Usage (ARIMA + Prophet + LSTM)
   3.6 Data Quality Framework
   3.7 RGPD + éthique
4. Résultats — Étude comparative
   4.1 NER comparé           (tableau N2.1)
   4.2 Communautés comparées (tableau N2.2)
   4.3 Forecasting comparé   (tableau N2.3)
   4.4 Émergence comparée    (tableau N2.4)
5. Discussion              (limites, biais, plans B)
6. Conclusion + V1.5 / V2
7. Bibliographie
8. Annexes (schéma Pydantic, ADRs, captures dashboard)
```

**Cible** : 25–40 pages · Markdown + Pandoc + WeasyPrint · Auteur **Bachirou Konaté** (rédaction intégrale) · Contributions **Karamo** (captures dashboard, schémas, ADRs, données chiffrées).

---

## 11. UI / DASHBOARD NEXT.JS (8 pages)

| Route | Contenu | Lead |
|---|---|---|
| `/` | KPIs marché IA (Maroc + International) · top compétences | Karamo |
| `/skills` | Tableau filtrable · score émergence · family · growth | Karamo |
| `/graph` | Graphe Neo4j interactif (react-force-graph-2d) · Louvain | Karamo *(data : Bachirou Konaté)* |
| `/forecasting` | ARIMA + Prophet + LSTM superposés · MAPE chiffré | Karamo |
| `/ner-explorer` | Texte annoté side-by-side 3 modèles · badges confidence | Karamo |
| `/methodology` | 3 axes · sources · RGPD · glossaire | Karamo *(contenu : Bachirou Konaté)* |
| `/comparative-study` | 4 tableaux N2.1–N2.4 chiffrés · choix justifiés | Karamo |
| `/quality` | Complétude · bruit · biais (cf. Data Quality Framework) | Karamo *(notebook : Bachirou Konaté)* |

**Décisions** : pas d'auth en MVP (public read-only) · dark mode par défaut (Navy 1000) · cible desktop prioritaire.

---

## 12. STRUCTURE DU REPOSITORY

```
skillnav/
├── pyproject.toml
├── README.md
├── CLAUDE.md                      # consignes Claude Code
├── .env.example
│
├── docs/
│   ├── PRD.md                     # version exhaustive
│   ├── PRD_CONDENSE.md            # ce document
│   ├── CHARTE_GRAPHIQUE_SKILLNAV.{md,docx,pdf}
│   ├── RAPPORT_METHODOLOGIQUE.md  # L5 (Bachirou Konaté)
│   ├── PLAN_SOUTENANCE.md         # L6
│   ├── RGPD_DPIA.md
│   └── archive/                   # versions anciennes
│
├── skillnav/                      # package Python
│   ├── schemas/                   # Pydantic v2 — source de vérité
│   │   ├── job.py
│   │   ├── ner.py
│   │   ├── graph.py
│   │   ├── timeseries.py
│   │   └── converters/{mongo,neo4j,es}.py
│   ├── db/{mongodb,neo4j,elasticsearch}/
│   ├── pipelines/
│   │   ├── content_mining/        # NER + Pydantic AI
│   │   ├── structure_mining/      # Graph builder + algos
│   │   └── usage_mining/          # Time series + forecasting
│   ├── scrapers/{rekrute,emploitic,apify,indeed,builtin,weak_signals}/
│   ├── comparative_studies/
│   │   ├── ner.py
│   │   ├── communities.py
│   │   ├── forecasting.py
│   │   └── emerging.py
│   ├── api/                       # FastAPI endpoints
│   └── cli.py                     # commande `skillnav`
│
├── notebooks/
│   ├── 00_setup_dev.ipynb
│   ├── 01_data_quality.ipynb           (Bachirou Konaté)
│   ├── 02_ner_comparison.ipynb         (Karamo)
│   ├── 03_graph_analysis.ipynb         (Bachirou Konaté)
│   ├── 04_forecasting_comparison.ipynb (Karamo)
│   └── 05_dashboard_data_prep.ipynb    (Karamo)
│
├── web/                           # Next.js 15 (Karamo)
│   ├── package.json
│   └── src/
│       ├── app/                   # pages App router
│       ├── components/
│       └── lib/api/types.ts       # généré depuis OpenAPI
│
├── tests/
│   ├── fixtures/                  # 30 offres gold annotées
│   ├── unit/
│   └── integration/
│
├── data/
│   ├── raw/                       # JSONL (gitignored)
│   ├── gold_set/                  # annotations manuelles
│   ├── exports/                   # datasets publics anonymisés
│   └── audit/                     # logs RGPD
│
└── scripts/
    ├── build_charte_docx.mjs
    └── seed_taxonomy.py
```

---

## 13. CALENDRIER — 18 jours · 3 sprints · soutenance 28 mai

```
Sprint 1 — Fondations            J1 → J6   (10–16 mai)
Sprint 2 — Cœur Web Mining       J7 → J12  (17–22 mai)
Sprint 3 — Forecasting + Finition J13 → J18 (23–28 mai)
SOUTENANCE                        J19       (28 mai 2026)
```

| Sprint | Karamo focus | Bachirou Konaté focus |
|---|---|---|
| **S1** J1–J6 | DBs · scrapers · schémas Pydantic · pipeline ingestion + extraction · **dashboard skeleton + Vercel** | Charte PDF · **notebook `01_data_quality`** · plan + chapitres 1–2 du rapport L5 |
| **S2** J7–J12 | NER + tableau F1 · normalisation · **pages `/ner-explorer` + `/graph` + `/skills`** · dark mode | Graph builder · PageRank · Louvain · Leiden · **rédaction §N1 + N2.1 + N2.2 + N3 + N4** du rapport L5 |
| **S3** J13–J18 | Forecasting (ARIMA + Prophet + LSTM) · **pages `/forecasting` + `/comparative-study`** · polish · démo | **Rapport L5 final (PDF)** · deck PPTX · répétitions |

---

## 14. SOUTENANCE — 25 minutes

```
┌────────────────────────────────────────────────────────────────┐
│  15 min PRÉSENTATION  +  4 min DÉMO LIVE  +  10 min Q&A        │
└────────────────────────────────────────────────────────────────┘
```

| Min | Section | Lead |
|:---:|---|:---:|
| M0–M1 | Ouverture (titre, équipe, contexte M242) | Karamo |
| M1–M2 | Sujet imposé + couverture 3 axes (§N1.2) | Karamo |
| M2–M4 | Architecture polyglotte + justification 3 DBs | Karamo |
| M4–M5 | Stack technique + 3 décisions clés (ADR) | Karamo |
| M5–M9 | **Démo live dashboard** — `/`, `/graph`, `/forecasting`, `/ner-explorer`, `/comparative-study` | Karamo |
| M9–M12 | Résultats étude comparative — 4 tableaux chiffrés | Karamo |
| M12–M13 | Data Quality + biais reconnus | Bachirou Konaté |
| M13–M14 | RGPD + robots.txt + DPIA | Bachirou Konaté |
| M14–M15 | Conclusion + roadmap V1.5 / V2 | Bachirou Konaté |

**Plan B démo HS** : projeter `web/screenshots/{page}.png` (HD préparés) + verbaliser.

---

## 15. INDICATEURS DE SUCCÈS

| Catégorie | KPI | Cible |
|---|---|---|
| **Technique** | Volume offres collectées | ≥ 500 (idéal 2 000) |
| | F1 NER (gold set 30 offres) | meilleur modèle ≥ 0.75 |
| | MAPE forecasting top 10 skills | ≤ 15 % |
| | Modularité Louvain | ≥ 0.40 |
| | Couverture tests | ≥ 70 % sur `schemas/` + `pipelines/` |
| **Académique** | Couverture 3 axes | ≥ 25 % chacun |
| | Algos comparés par tâche | ≥ 3 |
| | RGPD documenté | DPIA séparée publiée |
| | Livrables remis | 6 / 6 |
| **Produit** | Pages dashboard live | ≥ 7 |
| | Chargement page | < 3 s |
| | Dashboard accessible URL | live à J17 + 3h (test `curl -I`) |

---

## 16. PLANS B (sprints sous tension)

| Sprint | Si dérapage | Plan B |
|---|---|---|
| **S1** | Pipeline complet pas prêt | Scrape direct → MongoDB sans extraction IA. Notebook collecte stats brutes |
| **S2** | Neo4j AuraDB instable | Graphe **NetworkX en mémoire** + export GraphML. Démontre l'axe Structure |
| **S2** | Elasticsearch coûte trop de temps | **MongoDB Atlas Search** + `$facet` agrégations. ES = "évalué, plan B retenu" |
| **S3** | LSTM bug | ARIMA + Prophet seulement. Mention LSTM dans rapport en "perspective" |
| **S3** | Apify LinkedIn cassé | Sources statiques (Rekrute + Indeed + builtin) à ≥ 800 offres |
| **J18** | Dashboard Vercel HS | Screenshots HD préparés + démo locale `pnpm dev` projetée |

---

## 17. RACI — RÉPARTITION KARAMO / BACHIROU KONATÉ

```
R = Responsible · A = Accountable · C = Consulted · I = Informed
```

| Élément | Karamo | Bachirou Konaté |
|---|:---:|:---:|
| §6 Architecture | A R | R |
| §6.B Pipeline IA | A R | I |
| Structure Mining (Neo4j) | C | A R |
| Notebook `01_data_quality` | I | A R |
| Notebook `02_ner_comparison` | A R | C |
| Notebook `03_graph_analysis` | C | A R |
| Notebook `05_dashboard_data_prep` | A R | C |
| **Dashboard Next.js (L4)** | **A R** | C |
| **Rapport méthodologique (L5)** | C | **A R** |
| Charte graphique (PDF) | C | A R |
| Deck soutenance | R | A R |
| RGPD + DPIA (§N4) | R | A R |
| Étude comparative (§N2) | A R | R |

---

**Mai 2026 · Karamo Sylla & Bachirou Konaté · ENSA-Tétouan · M242 Pr. Imad Sassi**
