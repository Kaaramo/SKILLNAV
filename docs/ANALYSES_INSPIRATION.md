# Analyses inspirées du repo upstream : guide pour SKILLNAV

> **À l'attention de Bachirou.** Ce document décrit exhaustivement les analyses publiées par le repo upstream `ai-engineering-field-guide` (la source que nous avons importée pour notre `intl-ai-corpus/`) et propose un **plan d'analyses concret** à mener sur notre data SKILLNAV (3 468 fiches).
>
> **Objectif** : tu auras une vision claire de ce qui a été fait, des scripts à étudier comme référence, et d'un plan de 6 notebooks à coder pour notre rapport L5.

---

## Sommaire

1. [Vue d'ensemble du repo upstream](#1-vue-densemble-du-repo-upstream)
2. [Les 5 pages d'analyses publiées](#2-les-5-pages-danalyses-publiées)
3. [Les 10 scripts d'analyse Python](#3-les-10-scripts-danalyse-python)
4. [Le notebook analysis.ipynb (sandbox interactif)](#4-le-notebook-analysisipynb-sandbox-interactif)
5. [Notre data SKILLNAV vs leur data upstream](#5-notre-data-skillnav-vs-leur-data-upstream)
6. [Plan d'analyses pour SKILLNAV (6 notebooks proposés)](#6-plan-danalyses-pour-skillnav-6-notebooks-proposés)
7. [Quick start technique pour Bachirou](#7-quick-start-technique-pour-bachirou)

---

## 1. Vue d'ensemble du repo upstream

- **Source** : `github.com/alexeygrigorev/ai-engineering-field-guide`
- **Volume** : 2 445 fiches AI Engineer scrapées sur builtin.com (Q1 2026)
- **Couverture géo** : 5 villes (Los Angeles, New York, London, Amsterdam, Berlin) + Inde
- **Méthodologie** : pipeline 5 étapes (scrape, dédup, download HTML, extract YAML, enrichissement LLM)
- **Outputs analytiques** :
  - **5 pages markdown** publiées dans `role/` (1 463 lignes au total)
  - **10 scripts Python** dans `_internal/analysis/` (1 585 lignes au total)
  - **1 notebook Jupyter** `analysis.ipynb` (2 616 lignes, sandbox interactif)

L'auteur a séparé clairement :
- **Production de chiffres bruts** (scripts Python qui consomment `data_structured/*.yaml`)
- **Analyse qualitative narrative** (pages `role/*.md` rédigées avec aide LLM sur les outputs des scripts)
- **Exploration libre** (notebook Jupyter)

C'est exactement le pattern que nous allons appliquer.

---

## 2. Les 5 pages d'analyses publiées

### 2.1 `role/01-my-vision.md` (79 lignes) : Vision du rôle AI Engineer

**Contenu** :
- Comparaison narrative entre rôles : Data Scientist vs ML Engineer vs Data Engineer vs AI Engineer
- Adaptation du framework **CRISP-DM** au contexte AI (CRISP-DM for AI)
- Pattern d'évolution : où va le métier dans 2-3 ans
- Style éditorial, peu de chiffres

**Pertinence pour SKILLNAV** : modèle de **chapitre introductif** pour notre rapport L5 (positionner le rôle AI Engineer dans le paysage Data/ML/DE).

---

### 2.2 `role/02-skills.md` (507 lignes) : Skills analysis

**Le plus dense et le plus chiffré.** Sections :

1. **Job Types classification** :
   - AI-First : 621 jobs (69.4 %)
   - AI-Support : 255 jobs (28.5 %)
   - Machine Learning rebrandé : 16 jobs (1.8 %)
   - Pour chaque type : ce qu'ils construisent, exemples de responsabilités, titres typiques
2. **Dataset Statistics** : volumes par mois, par ville, par employeur
3. **Top skills** par catégorie (genai, ml, cloud, data, ops, languages)
4. **GenAI Framework Ecosystem** : LangChain, LlamaIndex, vector DBs adoption rates
5. **Supporting Roles** : ce que font les AI-Support (plateformes, infra, tooling)
6. **Skill Comparison AI-First vs AI-Support** : skills divergents
7. **Research vs Applied Roles** : exemples comparatifs
8. **What Other Titles Do AI Engineers Go Under?** : variations de titres
9. **How Much ML Do AI Engineers Need to Know?** : profondeur ML attendue
10. **What Else (Besides GenAI) Do AI Engineers Need?** : non-GenAI skills
11. **Fine-Tuning Requirements** : qui demande LoRA/RLHF/DPO
12. **Evaluation Skills** : RAGAS, LLM-as-judge, etc.
13. **Key Insight: RAG + Agents = 70%+ of Use Cases**
14. **Learning Path for AI Engineers** : roadmap apprentissage

**Pertinence pour SKILLNAV** : **template direct** pour notre page principale d'analyse. À reproduire avec notre data MA + INTL et y ajouter l'angle comparatif.

---

### 2.3 `role/03-responsibilities.md` (425 lignes) : Responsibilities

**Méthodologie clé** : 5 694 responsibilities extraites de 895 fiches, **catégorisées par LLM (Claude)** plutôt que par fréquence brute. C'est de l'analyse qualitative avec ancrage quantitatif.

Sections :
1. **Frequency Guide** : Very common / Common / Uncommon / Rare
2. **Typical Job Titles** : matrice titres ↔ classification AI
3. **Problems AI Engineers Solve** : organisé par problème métier, pas par techno
4. **Very Common** (catégorie) :
   - Building AI Systems
   - Productionizing AI
   - Evaluation and Quality
   - Using Provider APIs
5. **Common** :
   - RAG and Retrieval
   - Data Processing
   - Collaboration and Communication
   - Infrastructure and Platforms
   - Agents and Agentic Workflows
6. **Uncommon** :
   - Working with Customers
   - Frontend and User Interfaces
   - Performance Optimization
   - Self-Hosting Models
   - Fine-tuning Models

**Pertinence pour SKILLNAV** : on a déjà extrait les `responsibilities` dans nos `data_structured/`. À categoriser de la même manière.

---

### 2.4 `role/04-use-cases.md` (312 lignes) : Use cases business

4 525 use cases extraits, catégorisés.

**Catégories de problèmes résolus** :
- Automating Manual Workflows
- Finding Information in Company Data
- Answering Customer Questions at Scale
- Internal Operational Efficiency
- Deploying AI to Production Reliably
- Making Decisions from Data
- Ensuring AI Quality and Safety
- Creating Content at Scale
- Personalizing User Experiences
- Helping Developers Write Code
- Handling Specialized Domain Knowledge

**Domaines servis (avec chiffres concrets)** :
| Domaine | Mentions |
|---|:-:|
| Finance | 340+ |
| Healthcare | 232+ |
| Education | 181+ |
| Cybersecurity | 177+ |
| Legal/Regulatory | 157+ |
| Manufacturing/Industrial | 57+ |

**Pertinence pour SKILLNAV** : analyse identique sur notre data + ajout du **comparatif MA vs INTL** (par exemple : la finance est-elle aussi dominante en MA ? L'éducation y est-elle plus représentée ?).

---

### 2.5 `role/05-reality-vs-postings.md` (98 lignes) : Gap fiche vs réalité

**Méthodologie** : extraction qualitative à partir d'avis Reddit / Glassdoor / blogs de praticiens AI Engineer + comparaison avec ce que les fiches affichent.

Sections :
- AI Engineer vs ML Engineer : The Confusion
- What People Actually Report (témoignages)
- What AI Engineers Actually Do (3 work types principaux)
- Day-to-Day vs Assumptions (debug loop)
- Jobs vs Reality Gap
- The "Combo Role" Problem
- Key Takeaways

**Pertinence pour SKILLNAV** : moins prioritaire pour notre projet (le sujet du prof ne demande pas cette analyse qualitative). À envisager si on a du temps en V2.

---

## 3. Les 10 scripts d'analyse Python

Tous consomment les fichiers `data_structured/*.yaml` et impriment des résultats agrégés (Counter, defaultdict). Code simple Python pur sans pandas pour la plupart.

| Script | Lignes | Rôle |
|---|:-:|---|
| `common.py` | 26 | Helper `load_structured_jobs()` qui parcourt récursivement `data_structured/{YYYY-MM}/*.yaml` et retourne une liste de dicts. À utiliser par tous les autres scripts. |
| `analyze.py` | 216 | Statistiques globales : volumes par mois, par ville, par employeur, top 50 entreprises. Output texte console. |
| `analyze_patterns.py` | 195 | **Cooccurrences de skills** : pour chaque paire de skills (combinations 2 à 2), compte combien de fiches mentionnent les deux. Sortie : top 50 paires les plus fréquentes. C'est la base pour le graphe Neo4j. |
| `skills_analysis.py` | 192 | Top skills **par catégorie** (genai, ml, cloud, data, ops, languages, etc.). Cohérent avec nos 10 dimensions. |
| `extract_responsibilities.py` | 143 | Extrait toutes les `responsibilities` de tous les jobs et compte les phrases similaires. |
| `extract_use_cases.py` | 140 | Idem pour `use_cases`. |
| `finetuning_analysis.py` | 172 | Recherche les mentions de fine-tuning, LoRA, QLoRA, PEFT, RLHF, DPO. Output : qui demande quoi. |
| `support_roles.py` | 210 | Focus sur les rôles AI-Support : qui sont-ils, comment se distinguent-ils des AI-First. |
| `support_skills_analysis.py` | 161 | Skills spécifiques aux AI-Support (souvent : cloud + data + ops fort, GenAI faible). |
| `title_analysis.py` | 130 | Variations de titres : `Senior AI Engineer`, `Forward Deployed`, `AI Solutions Engineer`, etc. Patterns d'évolution. |

**Pattern récurrent dans les scripts** :

```python
from collections import Counter, defaultdict
from common import load_structured_jobs as load_all_jobs

def main():
    jobs = load_all_jobs()
    counter = Counter()
    for job in jobs:
        skills = job["position"]["skills"]["genai"]
        for s in skills:
            counter[s] += 1
    for skill, count in counter.most_common(30):
        print(f"  {skill:30s} {count:4d}")

if __name__ == "__main__":
    main()
```

C'est volontairement simple : pas de DataFrame, pas de viz, juste des chiffres console. Les pages `role/*.md` reprennent ces chiffres et les enrobent narrativement.

---

## 4. Le notebook `analysis.ipynb` (sandbox interactif)

2 616 lignes (cellules + outputs). C'est le notebook d'exploration que l'auteur a utilisé pour produire les analyses publiées.

**Patterns dedans** (devinés depuis la taille et le contexte) :
- Chargement des YAML via `common.load_structured_jobs`
- Conversion en `pd.DataFrame` pour analyse exploratoire
- Plots matplotlib pour les distributions
- Tableaux markdown formatés pour réutilisation dans `role/*.md`
- Tests rapides de patterns avant industrialisation dans un script `_internal/analysis/*.py`

**Pertinence pour SKILLNAV** : on aura les nôtres, numérotés 00 à 05, déjà scaffoldés dans `notebooks/`.

---

## 5. Notre data SKILLNAV vs leur data upstream

| Critère | Upstream | SKILLNAV |
|---|---|---|
| Volume total | 2 445 | **3 468** (+42 %) |
| Source(s) | 1 (builtin.com) | **7 sources distinctes** |
| Géographie | 6 villes anglophones | **Maroc (6 sources) + 6 pays anglophones (INTL)** |
| Période | Q1 2026 (4 mois) | **25 mois** (août 2022 à mai 2026) |
| Familles métiers | AI Engineer principalement | **13 familles** (DATA_SCIENTIST, ML_ENGINEER, MLOPS, NLP, CV, etc.) |
| Schéma data | YAML 10 dimensions skills | **Identique + champs SKILLNAV** (country, job_family, posted_date précis, etc.) |
| Comparaisons possibles | Inter-villes anglophones | **MA vs INTL** (angle inédit) |

### Ce qu'on peut faire qu'ils ne pouvaient pas

1. **Comparaison MA vs INTL** : émergence GenAI au Maroc vs États-Unis. Aucun observatoire francophone n'a fait ça.
2. **Analyse multi-famille** : pas que AI Engineer, mais aussi Data Analyst (DA), Data Engineer (DE), ML Engineer (MLE), MLOps, NLP, CV.
3. **Profondeur temporelle** : 25 mois de données permet du **forecasting réel** (axe Usage Mining du sujet) là où eux n'avaient que 4 mois.
4. **Diversité de sources** : 7 vs 1 permet d'analyser les **biais inter-plateformes** (LinkedIn vs Indeed vs Glassdoor : qui poste quoi ?).

---

## 6. Plan d'analyses pour SKILLNAV (6 notebooks proposés)

Les notebooks sont déjà scaffoldés dans `notebooks/`. Voici le contenu que je propose pour chacun.

### Notebook `00_setup_dev.ipynb`
- Test du loader `load_skillnav_jobs()` (à créer dans `skillnav/analysis/loaders.py`)
- Vérification volumes par source
- Sample d'1 fiche pour confirmer le schéma
- **Output minimal** : tableau de comptages cohérent avec l'audit qualité

### Notebook `01_data_quality.ipynb` (axe Data Quality Framework, exigence prof §3)
- Complétude par champ Pydantic (% non-vide pour title, company, description, skills_required, posted_date, etc.)
- Distribution des longueurs de descriptions
- Doublons SHA-256 cross-sources
- Outliers (titres anormalement courts, fiches sans pays inféré)
- Biais : langues FR/EN, géo, employeurs gros/PME, sectoriel
- **Output** : tableau de qualité par source + plots distributions

### Notebook `02_ner_comparison.ipynb` (axe Content Mining + étude §N2 PRD)
- Charger 30 fiches du gold set (à créer dans `data/gold_set/`)
- Annoter manuellement les entités (TOOL, FRAMEWORK, MODEL, LANGUAGE)
- Appliquer 3 modèles : BERT-multilingual, CamemBERT-NER, DistilBERT
- Métriques : F1 / Precision / Recall par modèle, par type d'entité
- **Output** : tableau comparatif chiffré + matrice de confusion + analyse qualitative

### Notebook `03_graph_analysis.ipynb` (axe Structure Mining)
**Inspiré de `analyze_patterns.py` upstream mais en plus poussé** :
- Construire le graphe Skill ↔ Job (NetworkX puis Neo4j)
- PageRank sur les Skill : quelles compétences sont les plus centrales ?
- Louvain communities : groupes naturels de skills (GenAI, MLOps, Cloud, Data, etc.)
- Comparaison communautés MA vs INTL : ont-elles les mêmes structures ?
- Top 30 paires de skills cooccurrents (équivalent direct du script upstream)
- **Output** : visualisation du graphe + table top paires + table communautés

### Notebook `04_forecasting_comparison.ipynb` (axe Usage Mining + étude §N2 PRD)
**Inédit côté upstream** (eux n'avaient que 4 mois) :
- Time series mensuelle d'apparition de chaque skill (depuis nos 25 mois de data)
- Focus sur skills émergents : LangChain, RAG, vector DBs, agents
- 3 modèles comparés : ARIMA, Prophet, LSTM
- Métriques : MAPE chiffré par modèle
- **Output** : graphes time series + tableau métriques + prédictions à 3 mois

### Notebook `05_dashboard_data_prep.ipynb`
- Préparation des données agrégées pour le dashboard Next.js
- KPIs : top 30 skills par pays, par mois, par AI type
- Pré-agrégats stockés dans MongoDB `dashboard_aggregates`
- Export JSON pour fallback Vercel
- **Output** : fichiers JSON consommables par le dashboard

### Bonus : Notebook `06_gap_market_ma_vs_intl.ipynb` (l'angle scientifique unique)
**Inspiré de la philosophie upstream mais sur notre data unique** :
- Diagramme de Venn : skills présents MA only, INTL only, partagés
- Heatmap skills × pays : où Python domine, où PyTorch domine, etc.
- Quelles compétences sont MA-only ? (probablement aucune)
- Quelles sont INTL-only ? (probablement RAG, LangChain, vector DBs en force)
- Décalage temporel : la moyenne d'émergence MA vs INTL est de combien de mois ?
- **Output** : graphes Venn + heatmaps + courbe d'émergence comparative
- **Insight clé pour le rapport L5** : démontrer que le marché MA suit le marché INTL avec environ N mois de décalage sur les compétences GenAI.

---

## 7. Quick start technique pour Bachirou

### Étape 1 : créer le loader (équivalent `common.py` upstream)

Fichier à créer : `skillnav/analysis/loaders.py`

```python
"""Loaders pour analyses SKILLNAV : equivalents au common.py upstream."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COLLECTED = PROJECT_ROOT / "sources" / "collected"

SOURCES_MA = ["anapec", "rekrute", "indeed-ma", "linkedin-ma", "pages-carrieres-ma", "glassdoor-ma"]
SOURCES_INTL = ["intl-ai-corpus"]
SOURCES_ALL = SOURCES_MA + SOURCES_INTL


def load_postings(sources: list[str] | None = None) -> list[dict]:
    """Charge tous les postings JSON SKILLNAV (couche pivot)."""
    sources = sources or SOURCES_ALL
    records = []
    for src in sources:
        postings_dir = COLLECTED / src / "postings"
        for json_file in sorted(postings_dir.glob("*.json")):
            with json_file.open("r", encoding="utf-8") as f:
                records.append(json.load(f))
    return records


def load_data_raw(sources: list[str] | None = None) -> Iterator[dict]:
    """Iterator sur les YAML data_raw (couche 1, texte brut)."""
    sources = sources or SOURCES_ALL
    for src in sources:
        for yaml_file in (COLLECTED / src / "data_raw").rglob("*.yaml"):
            with yaml_file.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data:
                yield {"_source": src, "_file": yaml_file.name, **data}


def load_data_structured(sources: list[str] | None = None) -> Iterator[dict]:
    """Iterator sur les YAML data_structured (couche 2, enrichissement LLM)."""
    sources = sources or SOURCES_ALL
    for src in sources:
        for yaml_file in (COLLECTED / src / "data_structured").rglob("*.yaml"):
            with yaml_file.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data:
                yield {"_source": src, "_file": yaml_file.name, **data}
```

### Étape 2 : premier script d'analyse (Top Skills MA vs INTL)

Fichier à créer : `notebooks/_first_analysis_top_skills.py` (ou directement en cellule du notebook 00)

```python
from collections import Counter
from skillnav.analysis.loaders import load_postings, SOURCES_MA, SOURCES_INTL

ma_jobs = load_postings(SOURCES_MA)
intl_jobs = load_postings(SOURCES_INTL)

def top_skills(jobs, top_n=30):
    counter = Counter()
    for job in jobs:
        for skill in job.get("skills_required", []):
            counter[skill] += 1
    return counter.most_common(top_n)

print(f"=== TOP SKILLS MAROC ({len(ma_jobs)} fiches) ===")
for skill, count in top_skills(ma_jobs):
    pct = 100 * count / len(ma_jobs)
    print(f"  {skill:30s} {count:4d} ({pct:.1f}%)")

print(f"\n=== TOP SKILLS INTL ({len(intl_jobs)} fiches) ===")
for skill, count in top_skills(intl_jobs):
    pct = 100 * count / len(intl_jobs)
    print(f"  {skill:30s} {count:4d} ({pct:.1f}%)")
```

### Étape 3 : reproduire l'analyse cooccurrences (graphe Neo4j embryo)

Fichier à créer : `notebooks/_cooccurrence_analysis.py`

```python
from collections import Counter
from itertools import combinations
from skillnav.analysis.loaders import load_postings

jobs = load_postings()

pair_counter = Counter()
for job in jobs:
    skills = sorted(set(job.get("skills_required", [])))
    for s1, s2 in combinations(skills, 2):
        pair_counter[(s1, s2)] += 1

print("=== TOP 30 PAIRES DE SKILLS COOCCURRENTES ===")
for (s1, s2), count in pair_counter.most_common(30):
    print(f"  {count:4d} : {s1} <-> {s2}")
```

Ces 2 scripts donnent immédiatement des résultats publiables. C'est le point de départ.

---

## 8. Récapitulatif et répartition possible Karamo / Bachirou

| Notebook | Estimation effort | Suggestion |
|---|:-:|---|
| `00_setup_dev` | 0.5 j | Karamo (loaders + helpers) |
| `01_data_quality` | 1 j | Karamo |
| `02_ner_comparison` | 2 j | Bachirou (étude comparative §N2 : partie HF Transformers) |
| `03_graph_analysis` | 2 j | Bachirou (axe Structure Mining + ingestion Neo4j) |
| `04_forecasting` | 2 j | Bachirou (axe Usage Mining + 3 modèles) |
| `05_dashboard_prep` | 1 j | Karamo (alimentation API FastAPI + dashboard) |
| `06_gap_ma_vs_intl` | 1 j | Bachirou (angle scientifique du rapport L5) |

Total estimé : 9.5 jours pour les 7 notebooks. À paralléliser sur 2 personnes : ~5 jours en sprint.

---

**Mai 2026** · SKILLNAV · M242 ENSA-Tétouan · Pr. Imad Sassi · Karamo Sylla & Bachirou Konaté
