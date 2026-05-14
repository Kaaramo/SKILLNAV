# PRD COMPLET — SKILLNAV

> **Skills Navigator — Observatoire des Compétences IA & Data Science par Web Mining**
>
> **Version** : 2.0 — Pivot académique M242 (mai 2026)
> **Statut** : Validé — Prêt à implémenter
> **Date** : Mai 2026
> **Cadre académique** : M242 — Analyse de Web · ENSA-Tétouan · Diplôme d'Ingénieur, filière Sciences des Données, Big Data et Intelligence Artificielle (SDBIA)
> **Encadrement** : Prof. Imad Sassi
> **Auteurs** : Karamo Sylla & Bachirou Konaté
> **Soutenance** : 28 mai 2026

---

## CHANGELOG

### v1.x (interne) → v2.0 SKILLNAV (mai 2026) — Pivot académique M242

| Changement | Détail |
|------------|--------|
| **Pivot de scope** | Projet adapté pour le module M242 (ENSA-Tétouan) : focus exclusif sur les compétences IA / Data Science, géographie Maroc + International, équipe binôme Karamo + Bachirou Konaté, soutenance académique 28 mai 2026. Toutes les sections politiques/B2G/multi-secteurs ont été remplacées par les exigences pédagogiques du sujet imposé : 3 axes Web Mining (Content / Structure / Usage), étude comparative de 3 algorithmes, NoSQL hybride (MongoDB + Neo4j + Elasticsearch), RGPD/robots.txt renforcés |

---

## TABLE DES MATIÈRES

0. [Contexte académique](#0-contexte-académique)
1. [Contexte stratégique et scientifique](#1-contexte-stratégique-et-scientifique)
2. [Vision produit](#2-vision-produit)
3. [Audience et personas](#3-audience-et-personas)
4. [Parcours utilisateur](#4-parcours-utilisateur)
5. [Fonctionnalités MVP → V1.5 → V2](#5-fonctionnalités-mvp--v15--v2)
6. [Architecture technique](#6-architecture-technique)
7. [Architecture des données](#7-architecture-des-données)
8. [Sources de données](#8-sources-de-données)
9. [Pipeline d'extraction IA (Pydantic AI + Transformers)](#9-pipeline-dextraction-ia)
10. [Règles métier](#10-règles-métier)
11. [UI/UX par phase (Notebooks → Dashboard Next.js)](#11-uiux-par-phase)
12. [Authentification et rôles](#12-authentification-et-rôles)
13. [Livrables (alignement 6 livrables professeur)](#13-livrables)
14. [Stack technique](#14-stack-technique)
15. [Estimation des coûts](#15-estimation-des-coûts)
16. [Méthodologie de développement](#16-méthodologie-de-développement)
17. [Phasage d'implémentation (3 sprints × 6 jours)](#17-phasage-dimplémentation)
18. [Indicateurs de succès](#18-indicateurs-de-succès)
19. [Roadmap post-soutenance](#19-roadmap-post-soutenance)
20. [Checklist pré-implémentation](#20-checklist-pré-implémentation)
21. [Annexes](#21-annexes)
22. [Plan de soutenance 25 min](#22-plan-de-soutenance-25-min)

**Sections académiques critiques (nouvelles)** :

- N1. [Mapping projet ↔ 3 axes Web Mining](#n1-mapping-projet--3-axes-web-mining)
- N2. [Étude comparative algorithmique](#n2-étude-comparative-algorithmique)
- N3. [Data Quality Framework](#n3-data-quality-framework)
- N4. [RGPD, robots.txt et anonymisation](#n4-rgpd-robotstxt-et-anonymisation)
- Annexe RACI. [Répartition Karamo / Bachirou Konaté](#annexe-raci--répartition-karamo--bachirou)

---

## 0. CONTEXTE ACADÉMIQUE

### 0.1 Cadre — M242 Analyse de Web, ENSA-Tétouan

SKILLNAV est le projet de fin du module **M242 — Analyse de Web**, dispensé par le **Pr. Imad Sassi** dans le cadre du **Diplôme d'Ingénieur**, filière *Sciences des Données, Big Data et Intelligence Artificielle* (SDBIA) de l'**ENSA de Tétouan** (Université Abdelmalek Essaâdi).

Le module M242 forme les étudiants à l'ingénierie de la donnée du web et à l'analyse prédictive à partir de sources non-structurées : extraction, structuration, exploration, modélisation. SKILLNAV applique ces compétences à un domaine en expansion rapide — l'expertise IA elle-même — pour démontrer la couverture des trois axes canoniques du Web Mining.

### 0.2 Sujet imposé — reformulation

> *« Observatoire de Data Science et de l'IA — Ingénierie de la donnée et Analyse prédictive de l'évolution des compétences IA par le Web Mining. »*

Le sujet impose six exigences structurantes que ce PRD couvre intégralement :

| # | Exigence du sujet | Section du PRD qui y répond |
|---|---|---|
| E1 | Couverture des **trois axes** Web Mining (Content, Structure, Usage) | §N1 (mapping), §6 (architecture par axe), §9–10 |
| E2 | Architecture **NoSQL** justifiée (polyglot accepté) | §7, §7.0 (justification polyglot) |
| E3 | Pipeline d'**extraction IA** avec **HuggingFace Transformers** | §9, §9.4bis, §9.7 |
| E4 | **Étude comparative rigoureuse** d'au moins 3 algorithmes par tâche | §N2 (CRITIQUE) |
| E5 | **RGPD**, robots.txt, anonymisation, respect TOS sources | §N4 + document `RGPD_DPIA.md` séparé |
| E6 | **6 livrables** : scripts, BD, pipeline validé, dashboard, rapport, soutenance | §13 + §22 |

### 0.3 Équipe et répartition haute

SKILLNAV est porté par un **binôme** :

| Membre | Spécialisation | Responsabilités principales |
|---|---|---|
| **Karamo Sylla** | Backend, IA, dashboard Next.js | Web Content Mining (NER + Pydantic AI), Web Usage Mining (forecasting), pipeline FastAPI, modélisation MongoDB, **dashboard Next.js** + visualisations |
| **Bachirou Konaté** | Structure, qualité de la donnée, rédaction | Web Structure Mining (Neo4j, PageRank, Louvain), **Data Quality Framework**, **rédaction du rapport méthodologique L5**, charte graphique, deck soutenance |

La matrice **RACI** détaillée par section et par livrable est en [Annexe RACI](#annexe-raci--répartition-karamo--bachirou).

### 0.4 Calendrier — 18 jours, 3 sprints, soutenance 28 mai 2026

| Repère | Date | Jalon |
|---|---|---|
| J0 | 10 mai 2026 | Kick-off, PRD validé, charte SKILLNAV validée, accès aux DBs créés |
| Fin Sprint 1 | 16 mai 2026 | Fondations : scrapers Maroc + International, MongoDB peuplée ≥ 200 offres |
| Fin Sprint 2 | 22 mai 2026 | Cœur : NER comparatif validé, Neo4j peuplée, dashboard pages-clés |
| Fin Sprint 3 | 27 mai 2026 | Forecasting, étude comparative chiffrée, rapport L5 finalisé, deck répété |
| **Soutenance** | **28 mai 2026** | Présentation orale 15 min + Q&A 10 min devant Pr. Sassi et jury |

Voir détail sprint par sprint en [§17 Phasage](#17-phasage-dimplémentation).

---

## 1. CONTEXTE STRATÉGIQUE ET SCIENTIFIQUE

### 1.1 Genèse — l'explosion du marché IA / Data Science

Entre 2020 et 2025, le marché mondial des compétences IA / Data Science a connu une croissance sans précédent :

- **+74 %** de croissance annuelle des offres « AI Specialist » (LinkedIn *Future of Jobs Report 2025*)
- **2,3 millions** d'offres mondiales mentionnant *« generative AI »* en 2025 contre **40 000** en 2022
- Les compétences IA figurent en tête des **top growing skills** des rapports *WEF Future of Jobs 2025* et *OECD AI Skills Outlook 2024*

Cette accélération est portée par trois phénomènes simultanés : (i) le passage à l'échelle des LLMs depuis novembre 2022, (ii) la pénétration du *machine learning* dans tous les secteurs économiques, (iii) la financiarisation massive de l'écosystème (Microsoft–OpenAI, NVIDIA, fonds dédiés). Les marchés émergents — dont le Maroc — sont entraînés par effet d'aspiration, avec un décalage de 12–18 mois sur les compétences les plus pointues.

### 1.2 Diagnostic — un désalignement formation / marché

Les chiffres publiés par les organismes internationaux convergent :

- **OECD AI Skills Outlook 2024** : seul **22 %** des cursus universitaires en IA couvrent les compétences réellement demandées par le marché (analyse sur 14 pays OCDE + partenaires)
- **LinkedIn Workforce Report MENA 2025** : la demande en *MLOps engineers* a triplé en 18 mois, mais aucune formation d'ingénieur publique marocaine ne propose actuellement de spécialisation MLOps formalisée
- **Stack Overflow Developer Survey 2025** : 67 % des praticiens IA déclarent avoir appris leurs outils principaux **en autodidacte** plutôt qu'en cursus formel

Le constat est uniforme : **le marché évolue plus vite que les programmes**. Cette inadéquation pose une question scientifique mesurable : quelles compétences IA sont émergentes aujourd'hui, et comment leur trajectoire peut-elle être anticipée pour informer les choix pédagogiques et stratégiques ?

### 1.3 Problème scientifique à résoudre

Trois questions structurent SKILLNAV :

| # | Question scientifique | Approche Web Mining |
|---|---|---|
| Q1 | **Quelles compétences IA / DS sont effectivement demandées ?** (extraction, structuration, normalisation) | Web Content Mining — NER sur offres d'emploi |
| Q2 | **Comment ces compétences sont-elles structurellement reliées ?** (co-occurrences, communautés, centralité) | Web Structure Mining — graphe Neo4j, PageRank, Louvain |
| Q3 | **Comment leur popularité évolue-t-elle et que peut-on prévoir à 3–6 mois ?** | Web Usage Mining — séries temporelles, ARIMA / Prophet / LSTM |

Chaque question est rattachée à un axe canonique du Web Mining et donne lieu à une **étude comparative** chiffrée (cf. §N2).

### 1.4 Opportunité scientifique

Trois facteurs rendent ce projet pertinent au moment où il est réalisé :

- **Maturité des outils** — les *transformers* multilingues (BERT-multi, CamemBERT, DistilBERT) sont stables, ouverts et accessibles via HuggingFace ; ils permettent une NER de qualité sur des textes français/anglais mixtes typiques du marché marocain.
- **Maturité des stacks NoSQL polyglottes** — MongoDB, Neo4j et Elasticsearch offrent tous des *free tiers* cloud (Atlas, AuraDB, Elastic Cloud) suffisants pour un projet académique de cette envergure.
- **Disponibilité des sources** — l'écosystème offres d'emploi est très ouvert (sitemaps publics, API LinkedIn via Apify, builtin.com, Welcome to the Jungle), ce qui permet une collecte propre et reproductible.

### 1.5 Positionnement SKILLNAV

> **SKILLNAV est un observatoire académique des compétences en Intelligence Artificielle et Data Science, démontrant la couverture rigoureuse des trois axes du Web Mining sur un domaine en évolution rapide. Il produit (i) une base de données hybride normalisée, (ii) un pipeline IA validé par métriques chiffrées, (iii) un dashboard exploratoire interactif, (iv) un rapport méthodologique académique, (v) une étude comparative algorithmique reproductible.**

SKILLNAV se distingue des produits commerciaux comparables :

| Approche existante | Limite | Réponse SKILLNAV |
|---|---|---|
| LinkedIn Talent Insights | Boîte noire, prix prohibitifs, pas de méthodologie publiée | Méthodologie ouverte, étude comparative reproductible |
| Études cabinets (Gartner, McKinsey) | Cycles annuels, données propriétaires | Cycle 18 jours, données sourcées et ouvertes |
| Job aggregators (Indeed, Glassdoor) | Pas d'analyse de structure ni de prédiction | 3 axes Web Mining intégrés |
| Études universitaires ad hoc | Volumes faibles, pas de pipeline reproductible | Pipeline modulaire, 500–2 000 offres analysées |

### 1.6 Vision MVP / V1.5 / V2 — escalier de démonstration académique

SKILLNAV est structuré en **trois paliers**. Le palier MVP est celui qui sera défendu lors de la soutenance ; V1.5 et V2 sont des extensions post-soutenance documentées pour démontrer la maturité du projet.

```
┌──────────────────────────────────────────────────────────────────┐
│  MVP — J+18 (28 mai 2026, jour de soutenance)                    │
│  Géographie : Maroc + International (FR/EN)                      │
│  Mode opératoire : Pipeline complet sur 500–2 000 offres         │
│                    Notebooks Jupyter + Dashboard Next.js 7 pages │
│  Question : « Quelles compétences IA sont demandées, comment     │
│              sont-elles liées, comment évoluent-elles ? »        │
│  Sources : Rekrute, EmploiTIC, LinkedIn (Apify), Indeed,         │
│            builtin.com, WTTJ, Google Trends, GitHub Trending     │
│  Méthode : 3 axes Web Mining + étude comparative 3 algos × tâche │
│  Livrables : 6 livrables prof (cf. §13)                          │
│  Audience : Pr. Sassi + jury + binôme                            │
└──────────────────────────────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  V1.5 — post-soutenance (juin–juillet 2026)                      │
│  Élargissements modérés :                                        │
│   - Volume cible 5 000–10 000 offres                             │
│   - Fine-tuning CamemBERT sur dataset annoté SKILLNAV            │
│   - Article Medium / blog DataTalks                              │
│   - Déploiement public skillnav.ma                               │
└──────────────────────────────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  V2 — vision long terme (septembre 2026+)                        │
│  - Extension géographique (Afrique francophone + Europe)         │
│  - Pipeline live (Celery + APScheduler)                          │
│  - Agents prospectifs (Claude Agent SDK pour métiers émergents)  │
│  - Partenariats potentiels avec écoles / observatoires           │
└──────────────────────────────────────────────────────────────────┘
```

### 1.7 Inscription dans le module M242

SKILLNAV s'inscrit dans le quatrième chapitre du module *« Analyse de Web »* (Web Mining appliqué), qui forme à : (i) la collecte structurée de données web, (ii) la modélisation NoSQL polyglotte, (iii) la mise en œuvre de modèles statistiques et de *machine learning* sur données extraites, (iv) la communication scientifique des résultats. Chaque livrable décrit en §13 correspond directement à un critère d'évaluation du sujet imposé.

---

## 2. VISION PRODUIT

### 2.1 Mission SKILLNAV

> **Donner aux étudiants, chercheurs, recruteurs et stratèges du marché IA un instrument scientifique d'observation des compétences en Intelligence Artificielle et Data Science — par la rigueur méthodologique du Web Mining, la transparence des algorithmes comparés et la reproductibilité des résultats.**

### 2.2 Trois principes fondateurs

| # | Principe | Conséquence concrète |
|---|---|---|
| 1 | **Donnée réelle, jamais déclarative** | Extraction directe d'offres d'emploi publiées par employeurs et plateformes ; pas de sondage ni de proxy |
| 2 | **Couverture équilibrée des 3 axes Web Mining** | Chaque axe est démontré par au moins une page dashboard, une étude comparative, un livrable spécifique |
| 3 | **Transparence méthodologique radicale** | Méthodologie complète publiée (rapport L5), datasets ouverts (anonymisés), code repository, étude comparative reproductible |

### 2.3 Différenciation par palier

| Dimension | MVP (J+18) | V1.5 | V2 |
|---|---|---|---|
| Géographie | Maroc + International | + Afrique francophone | + Europe + analyse pays-par-pays |
| Volume d'offres analysées | 500–2 000 | 5 000–10 000 | 20 000+ |
| Mode d'exécution | Notebooks + dashboard statique | Pipeline semi-automatique | Live pipeline + agents IA |
| Algorithme phare | NER comparé + Louvain + Prophet | Fine-tuning CamemBERT | Agents prospectifs métiers émergents |
| Livrable principal | Rapport méthodologique L5 + soutenance | Article Medium + déploiement skillnav.ma | Rapport prospectif + API publique |
| Audience principale | Pr. Sassi + jury M242 | Étudiants, recruteurs IA, blog scientifique | Écoles, observatoires, partenariats |

### 2.4 Promesses par cible

**Pour le Pr. Sassi (évaluateur principal)** :
> *« Voici un projet qui couvre les trois axes du Web Mining avec la rigueur d'une publication scientifique : architecture polyglotte justifiée, étude comparative chiffrée pour chaque tâche, RGPD documentée, six livrables livrés. »*

**Pour un étudiant ou chercheur IA** :
> *« Tu peux comprendre, reproduire et étendre cette méthodologie. Le repository est documenté, les notebooks sont commentés, les choix algorithmiques sont justifiés. »*

**Pour un recruteur IA au Maroc** :
> *« Tu peux savoir quelles compétences IA croissent le plus vite, quelles communautés de compétences sont structurellement liées, et anticiper les tensions sur 3–6 mois. »*

### 2.5 Anti-positionnement

SKILLNAV n'est délibérément PAS :

- Un *job board* (pas d'agrégation pour candidats finaux)
- Un service de matching candidats / employeurs
- Une plateforme commerciale concurrente à LinkedIn Talent Insights
- Un outil de marketing RH

SKILLNAV **utilise les annonces** comme matière première statistique, mais sa mission est uniquement la **démonstration scientifique** des techniques Web Mining appliquées à un domaine d'intérêt académique.

---

## 3. AUDIENCE ET PERSONAS

### 3.1 Persona principal — Pr. Imad Sassi (évaluateur)

| Dimension | Description |
|---|---|
| **Rôle** | Professeur ENSA-Tétouan, responsable du module M242 |
| **Contexte d'évaluation** | Évaluation comparative de plusieurs projets de groupe sur le même sujet |
| **Critères d'attention** | Couverture rigoureuse des 3 axes, qualité de l'étude comparative, justification des choix techniques (architecture NoSQL polyglotte, modèles NER), respect RGPD, qualité de la soutenance |
| **Niveau technique** | Expert — connaît à fond Web Mining, IR, ML appliqué |
| **Format préféré** | Code clean et reproductible, rapport méthodologique structuré, présentation orale claire avec démo live |
| **Critère d'adoption mental** | « Ce projet vaut la note maximale parce qu'il fait ce que le sujet demande, avec des choix justifiés et des résultats chiffrés. » |

**Ce que le Pr. Sassi ne veut PAS** : un dashboard joli sans pipeline derrière, une étude comparative qualitative, des choix d'outils non justifiés, un rapport descriptif sans analyse critique.

### 3.2 Persona secondaire — Jury de soutenance

| Dimension | Description |
|---|---|
| **Rôle** | Enseignant·e·s du Diplôme d'Ingénieur SDBIA (Sciences des Données, Big Data et IA), parfois un industriel externe |
| **Contexte** | Présent·e·s pendant 25 min de soutenance ; questions techniques attendues |
| **Niveau technique** | Avancé — peuvent challenger sur choix d'algorithmes, métriques, robustesse |
| **Format préféré** | Slides denses mais lisibles, démo live qui marche, réponses chiffrées aux Q&A |

### 3.3 Persona V1.5 — Étudiant·e / chercheur·euse IA

| Dimension | Description |
|---|---|
| **Rôle** | Élève-ingénieur·e en filière IA/Data Science, chercheur junior, doctorant en *machine learning* |
| **Contexte** | Cherche à comprendre l'état de l'art Web Mining ou à reproduire la méthode |
| **Critère d'adoption** | Repository GitHub propre, notebooks reproductibles, README clair, dataset accessible |
| **Format préféré** | Notebooks Jupyter exécutables, article Medium / blog technique |

### 3.4 Persona V1.5 — Recruteur·euse IA au Maroc

| Dimension | Description |
|---|---|
| **Rôle** | Responsable recrutement tech, talent acquisition, head of HR dans une scale-up IA |
| **Contexte** | Cherche à comprendre les tensions sur le marché IA marocain, à anticiper les pénuries de compétences |
| **Niveau technique** | Modéré — comprend les concepts mais pas le code |
| **Format préféré** | Dashboard web filtrable, KPIs visuels, top compétences émergentes, infographies |
| **Critère d'adoption** | Données fraîches (≤ 1 mois), filtrage par technologie, partage facile vers stakeholders internes |

### 3.5 Persona interne — Binôme Karamo + Bachirou Konaté

| Dimension | Description |
|---|---|
| **Rôle** | Auteurs et opérateurs principaux du projet |
| **Niveau technique** | Karamo : confirmé Python, IA, NLP, pipelines / Bachirou Konaté : confirmé front, visualisation, graphes |
| **Besoin principal** | Outils qui s'enchaînent proprement, conventions de code respectées, peu de friction Git |
| **Format préféré** | Notebooks Jupyter, repo GitHub avec branches courtes, documentation inline |

### 3.6 Cartographie des besoins par persona

| Besoin | Pr. Sassi | Jury | Étudiant IA | Recruteur | Binôme |
|---|:---:|:---:|:---:|:---:|:---:|
| Rapport méthodologique (L5) | ✅✅✅ | ✅✅ | ✅✅ | — | ✅ |
| Étude comparative chiffrée | ✅✅✅ | ✅✅✅ | ✅✅ | — | ✅✅ |
| Dashboard explorable | ✅✅ | ✅✅ | ✅ | ✅✅✅ | ✅✅✅ |
| Démonstration live | ✅✅✅ | ✅✅✅ | ✅ | ✅ | ✅✅ |
| Repo GitHub reproductible | ✅✅ | ✅ | ✅✅✅ | — | ✅✅✅ |
| RGPD documentée | ✅✅✅ | ✅ | ✅ | ✅ | ✅ |
| Datasets exportables | ✅ | — | ✅✅✅ | ✅ | ✅✅ |
| KPIs visuels marché IA | ✅ | ✅ | ✅ | ✅✅✅ | ✅✅ |

---

## 4. PARCOURS UTILISATEUR

### 4.1 Parcours interne — binôme Karamo + Bachirou Konaté

C'est le parcours optimisé en priorité, exécuté à chaque sprint. **Tout tourne en local + DBs cloud free tier.**

```
┌─────────────────────────────────────────────────────────────────┐
│  DÉBUT DE SPRINT — Karamo & Bachirou Konaté sur leurs MacBooks         │
│  Repository cloné, environnement Poetry installé                │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 — Collecte (Karamo lead)                               │
│  Scrapy + Playwright + Apify MCP + Firecrawl                    │
│                                                                 │
│  → Sources Maroc :  rekrute, emploitic, linkedin MA             │
│  → Sources Inter :  linkedin, indeed, builtin.com, WTTJ         │
│  → Signaux faibles : Google Trends, GitHub Trending, HF         │
│  → Persistence : MongoDB Atlas (collection raw_jobs)            │
│  Durée par run : ~30 minutes pour ~500 offres                   │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 — Extraction IA + NER (Karamo lead)                    │
│  $ poetry run skillnav extract --batch=last                     │
│                                                                 │
│  → Pydantic AI + Claude Sonnet 4.5 (extraction structurée)      │
│  → HuggingFace Transformers (BERT-multi / CamemBERT / DistilBERT)│
│  → MongoDB : extracted_jobs + ner_annotations                   │
│  → Quarantaine auto si confidence < 0.75                        │
│  Durée : ~30 minutes pour 500 offres ; coût ~$5–10              │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 — Construction du graphe (Bachirou Konaté lead)               │
│  $ poetry run skillnav graph build                              │
│                                                                 │
│  → Co-occurrences skill ↔ skill ↔ job ↔ family                  │
│  → Persistence Neo4j AuraDB (nœuds Skill, Job, Family + edges)  │
│  → Algos : PageRank, Louvain, Label Propagation                 │
│  → Export résultats vers MongoDB pour API                       │
│  Durée : ~10 minutes                                            │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 4 — Indexation Elasticsearch + Forecasting (Karamo lead) │
│  $ poetry run skillnav index push                               │
│  $ poetry run skillnav forecast run                             │
│                                                                 │
│  → Elasticsearch : index jobs_search + skills_timeseries        │
│  → ARIMA / Prophet / LSTM sur séries skill_count(time)          │
│  → Stockage résultats forecasts + intervalles confiance         │
│  Durée : ~15 minutes                                            │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 5 — Data Quality + Notebooks (binôme)                    │
│  notebooks/01_data_quality.ipynb                                │
│  notebooks/02_ner_comparison.ipynb                              │
│  notebooks/03_graph_analysis.ipynb                              │
│  notebooks/04_forecasting_comparison.ipynb                      │
│  notebooks/05_dashboard_data_prep.ipynb                         │
│                                                                 │
│  → Compute complétude, bruit, biais                             │
│  → Tableau comparatif chiffré (entrée §N2)                      │
│  → Génération JSON pré-calculé pour dashboard                   │
│  Durée : 1–2h selon profondeur                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 6 — Dashboard Next.js (Karamo lead)                      │
│  $ cd web && pnpm dev                                           │
│                                                                 │
│  → Pages : /, /skills, /graph, /forecasting, /ner-explorer,     │
│             /methodology, /comparative-study, /quality          │
│  → Données : API FastAPI + JSON pré-calculés                    │
│  → Visualisations : Recharts, Tremor, react-force-graph, Plotly │
│  Iteration locale puis déploiement Vercel                       │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 7 — Rédaction rapport L5 + deck (binôme)                 │
│  docs/RAPPORT_METHODOLOGIQUE.md                                 │
│  docs/PLAN_SOUTENANCE.md                                        │
│                                                                 │
│  → Bachirou Konaté : intro, méthode, étude comparative, résultats, │
│    Data Quality, RGPD — rédaction L5 intégrale                  │
│  → Karamo : captures dashboard, schémas archi, ADR, deck        │
│  → Commits réguliers, peer review                               │
└─────────────────────────────────────────────────────────────────┘
```

**Moment AHA principal** : voir apparaître dans le notebook `02_ner_comparison` un tableau chiffré où CamemBERT-NER bat BERT-multilingual sur les entités françaises avec un F1 de +6.2 points — preuve directe que l'étude comparative produit des résultats actionnables, pas des opinions.

### 4.2 Parcours utilisateur du dashboard

```
Visite https://skillnav.vercel.app (lien public, pas d'auth en MVP)
   ↓
Page / : overview marché IA Maroc + international
   ↓
Navigation par menu : Skills, Graph, Forecasting, NER Explorer,
                     Methodology, Comparative Study, Data Quality
   ↓
Page /graph : exploration interactive du graphe de compétences
              avec communautés Louvain colorées
   ↓
Page /forecasting : sélection d'une compétence → visualisation
                    ARIMA / Prophet / LSTM superposés avec MAPE
   ↓
Page /comparative-study : tableau récapitulatif chiffré de toutes
                          les comparaisons (NER, Graph, Forecast)
```

### 4.3 Parcours évaluateur — Pr. Sassi

```
J+18 — Soutenance 28 mai 2026, 25 minutes
   ↓
M1–M2  : Contexte + sujet + 3 axes Web Mining (Karamo)
M3–M5  : Architecture polyglotte + stack justifiée (Karamo + Bachirou Konaté)
M6–M9  : Démo live dashboard sur skillnav.vercel.app (Karamo)
M10–M12: Résultats étude comparative chiffrée (Karamo)
M13–M14: RGPD + Data Quality (Bachirou Konaté)
M15    : Conclusion + roadmap (Bachirou Konaté)
   ↓
M16–M25 : Q&A 10 minutes
   ↓
Évaluation sur les 6 livrables remis (cf. §13)
```

---

## 5. FONCTIONNALITÉS MVP → V1.5 → V2

### 5.1 Tableau de phasage des fonctionnalités

Chaque fonctionnalité est rattachée à **un axe Web Mining** (C = Content, S = Structure, U = Usage, T = Transverse).

| # | Axe | Fonctionnalité | MVP | V1.5 | V2 |
|---|:---:|---|:---:|:---:|:---:|
| F01 | T | Scraping Maroc (Rekrute, EmploiTIC, LinkedIn MA via Apify) | ✅ | ✅ | ✅ |
| F02 | T | Scraping International (LinkedIn, Indeed, builtin.com, WTTJ) | ✅ | ✅ | ✅ |
| F03 | T | Collecte signaux faibles (Google Trends, GitHub Trending, HF) | ✅ | ✅ | ✅ |
| F04 | C | Extraction IA Pydantic AI (skills + responsibilities + use cases) | ✅ | ✅ | ✅ |
| F05 | C | NER comparatif (BERT-multi / CamemBERT-NER / DistilBERT) | ✅ | ✅ | ✅ |
| F06 | C | Normalisation taxonomique avec aliases (skills, frameworks, modèles) | ✅ | ✅ | ✅ |
| F07 | C | Classification automatique en 10 familles compétences IA / DS | ✅ | ✅ | ✅ |
| F08 | S | Construction graphe Neo4j (Skill, Job, Family, Source) | ✅ | ✅ | ✅ |
| F09 | S | Centralité PageRank — top compétences-pivot | ✅ | ✅ | ✅ |
| F10 | S | Détection de communautés (Louvain + Label Propagation + Leiden) | ✅ | ✅ | ✅ |
| F11 | U | Séries temporelles skill_count(time) — agrégation mensuelle | ✅ | ✅ | ✅ |
| F12 | U | Forecasting comparatif (ARIMA / Prophet / LSTM) | ✅ | ✅ | ✅ |
| F13 | U | Détection compétences émergentes (3 méthodes comparées) | ✅ | ✅ | ✅ |
| F14 | T | Indexation Elasticsearch (jobs_search, skills_timeseries) | ✅ | ✅ | ✅ |
| F15 | T | API FastAPI typée OpenAPI | ✅ | ✅ | ✅ |
| F16 | T | Dashboard Next.js (7 pages) | ✅ | ✅ | ✅ |
| F17 | T | Notebooks Jupyter (5 notebooks numérotés) | ✅ | ✅ | ✅ |
| F18 | T | Rapport méthodologique L5 (PDF) | ✅ | ✅ | ✅ |
| F19 | T | Deck soutenance (PPTX + PDF) | ✅ | ✅ | ✅ |
| F20 | T | Exports datasets anonymisés (JSON / CSV / Parquet) | ✅ | ✅ | ✅ |
| F21 | T | Page méthodologie publique | ✅ | ✅ | ✅ |
| F22 | T | Page étude comparative (`/comparative-study`) | ✅ | ✅ | ✅ |
| F23 | T | Page Data Quality (`/quality`) | ✅ | ✅ | ✅ |
| F24 | T | Page NER Explorer (`/ner-explorer`) avec side-by-side 3 modèles | ✅ | ✅ | ✅ |
| F25 | C | Fine-tuning CamemBERT sur dataset annoté SKILLNAV | — | ✅ | ✅ |
| F26 | T | Déploiement public skillnav.ma | — | ✅ | ✅ |
| F27 | T | Pipeline live (Celery + APScheduler) | — | — | ✅ |
| F28 | C | Agents prospectifs (Claude Agent SDK pour métiers émergents) | — | — | ✅ |
| F29 | T | API publique versionnée + documentation OpenAPI | — | — | ✅ |

### 5.2 MVP — Détail des fonctionnalités prioritaires

#### F04 — Extraction IA Pydantic AI

**Description** : Pour chaque offre brute non encore traitée, Pydantic AI + Claude API extrait un objet structuré contenant : titre normalisé, entreprise, localisation, contrat, séniorité, compétences requises, responsabilités, cas d'usage IA, frameworks mentionnés, modèles mentionnés, *sous-domaines* ML, niveau de confiance.

**Schéma de sortie Pydantic v2 (source de vérité unique) :**

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class JobExtraction(BaseModel):
    # Identifiants
    source: str = Field(..., description="rekrute, linkedin, indeed, ...")
    source_id: Optional[str] = None
    url: str

    # Poste
    title_raw: str
    title_normalized: str
    company: str
    company_size_estimate: Literal["TPE", "PME", "ETI", "GE", "Unknown"]

    # Géographie
    country: str = Field(..., min_length=2, max_length=2)
    city: Optional[str] = None
    remote_type: Literal["On-site", "Hybrid", "Remote", "Unspecified"]

    # Contrat
    contract_type: Literal["CDI", "CDD", "Stage", "Alternance", "Freelance", "Autre"]
    seniority: Literal["Débutant", "Junior", "Confirmé", "Senior", "Expert", "Direction"]
    experience_years_min: Optional[int] = None
    experience_years_max: Optional[int] = None
    education_required: Optional[str] = None

    # Triade Skills / Responsibilities / UseCases (méthodo Grigorev)
    skills_required: List[str] = Field(..., min_length=3, max_length=25)
    responsibilities: List[str] = Field(..., min_length=2, max_length=12)
    use_cases: List[str] = Field(default_factory=list, max_length=8)

    # Champs IA spécifiques
    ml_subdomains: List[Literal[
        "ML Classique", "Deep Learning", "NLP", "Computer Vision",
        "Data Engineering", "MLOps", "Cloud & Big Data",
        "AI Ethics", "Statistiques", "Outils & Soft Skills"
    ]] = Field(default_factory=list, max_length=4)
    frameworks_used: List[str] = Field(default_factory=list, max_length=15)
    models_mentioned: List[str] = Field(default_factory=list, max_length=10)

    # Classification
    role_family: Literal[
        "ML Classique", "Deep Learning", "NLP", "Computer Vision",
        "Data Engineering", "MLOps", "Cloud & Big Data",
        "AI Ethics", "Statistiques", "Outils & Soft Skills"
    ]
    job_type: Literal["Tech-Core", "Tech-Adjacent", "Tech-Enabled", "Non-Tech"]

    # Rémunération (optionnel)
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None

    # Qualité
    extraction_confidence: float = Field(..., ge=0.0, le=1.0)
    extraction_notes: Optional[str] = None
    extracted_at: str  # ISO 8601
    extraction_model: Literal["claude-sonnet-4-5", "claude-haiku-4-5"]
```

**Modèles utilisés** :
- **Claude Sonnet 4.5** pour l'extraction principale (qualité maximale)
- **Claude Haiku 4.5** pour la normalisation taxonomique secondaire (rapide, moins cher)

**Acceptance criteria** :
- Confidence ≥ 0.75 sur ≥ 90 % des offres traitées
- Temps moyen d'extraction < 8 secondes par offre
- Coût total extraction < 15 $ pour 1 000 offres

#### F05 — NER comparatif (BERT-multi / CamemBERT-NER / DistilBERT)

**Description** : Pour chaque offre, application en parallèle de **trois modèles NER** HuggingFace afin d'annoter les entités (skills, frameworks, modèles, langages, rôles). Stockage des annotations par modèle dans MongoDB pour comparaison.

**Modèles testés** :

| Modèle HuggingFace | Particularité | Taille |
|---|---|---|
| `bert-base-multilingual-cased` + tête NER fine-tunée | Multilingue (104 langues), robuste FR/EN | ~700 MB |
| `Jean-Baptiste/camembert-ner` | Spécialisé français, excellent sur entités françaises | ~440 MB |
| `elastic/distilbert-base-cased-finetuned-conll03-english` | DistilBERT NER anglais, 60 % plus rapide | ~260 MB |

**Comparaison cible** (cf. §N2.1) : F1-score micro / macro sur jeu test de 30 offres annotées manuellement, par modèle et par type d'entité.

**Acceptance criteria** :
- Les 3 modèles produisent des annotations comparables sur un même jeu test
- Tableau F1 chiffré par modèle × type d'entité documenté dans `notebooks/02_ner_comparison.ipynb`
- Choix d'un modèle « champion » justifié (latence vs F1) pour pipeline production MVP

#### F07 — Classification en 10 familles compétences IA / DS

**Familles** : ML Classique, Deep Learning, NLP, Computer Vision, Data Engineering, MLOps, Cloud & Big Data, AI Ethics, Statistiques, Outils & Soft Skills (cf. Charte SKILLNAV §02). La classification est faite : (i) par règles heuristiques sur les skills extraits, (ii) confirmée par Claude Haiku pour les cas ambigus.

#### F08–F10 — Graphe Neo4j + algos de structure

**Construction du graphe** :

```cypher
CREATE (s:Skill {name: "PyTorch", family: "Deep Learning"})
CREATE (j:Job {id: "...", title: "ML Engineer", company: "..."})
CREATE (f:SkillFamily {name: "Deep Learning"})
CREATE (j)-[:REQUIRES {weight: 1.0}]->(s)
CREATE (s)-[:BELONGS_TO]->(f)
CREATE (s1:Skill)-[:CO_OCCURS_WITH {weight: 4}]->(s2:Skill)
```

**Algos exécutés via `neo4j-graph-data-science` (GDS)** :
- `gds.pageRank.stream` — top compétences-pivot (centrality)
- `gds.louvain.stream` — communautés de compétences
- `gds.labelPropagation.stream` — communautés (méthode alternative)
- `gds.leiden.stream` *(si disponible)* ou implémentation Python via `igraph`

**Acceptance criteria** :
- Graphe peuplé avec ≥ 200 nœuds Skill et ≥ 800 arêtes CO_OCCURS_WITH
- 3 algos de détection de communautés exécutés sur le même graphe
- Tableau comparatif modularité × runtime × stabilité (cf. §N2.2)

#### F12 — Forecasting comparatif

**Tâche** : pour les 10 compétences les plus fréquentes (top 10 PageRank), prédire le volume d'offres sur les 3 prochains mois.

**Modèles testés** :

| Modèle | Library | Hyperparamètres clés |
|---|---|---|
| ARIMA | `statsmodels` | (p, d, q) sélectionnés via AIC |
| Prophet | `prophet` (Meta) | Seasonality auto, changepoint_prior_scale = 0.05 |
| LSTM | `neuralforecast` (Nixtla) | 2 couches × 50 unités, lookback 12 mois |

**Métriques** : MAPE, RMSE, MAE.

**Acceptance criteria** :
- Tableau comparatif chiffré (cf. §N2.3) sur ≥ 10 compétences
- MAPE ≤ 15 % pour au moins un modèle sur la médiane des compétences
- Graphiques superposés réalité + 3 forecasts dans dashboard `/forecasting`

#### F13 — Détection des compétences émergentes (3 méthodes comparées)

L'algorithme « **compétences émergentes** » remplace conceptuellement l'ancien algorithme de signaux faibles. Trois méthodes sont comparées :

**Méthode 1 — Heuristique pondérée** :
```
emerging_score = (volume_normalisé × 0.4)
              + (growth_rate_3m × 0.4)
              + (présence_signaux_faibles × 0.2)

Émergente si : emerging_score > 0.7  ET  volume_brut ≥ 5
```

**Méthode 2 — Apprentissage supervisé** sur jeu annoté de 50 skills labellisés (émergent / établi / déclinant), features : volume, growth, age, family, signal Google Trends, mentions GitHub. Modèle XGBoost.

**Méthode 3 — Clustering temporel** : KMeans sur trajectoires normalisées de volumes mensuels, identification du cluster « croissance forte récente ».

Comparaison sur précision, rappel, F1 vs un jeu de validation (cf. §N2 et §10.4).

### 5.3 V1.5 — Élargissements post-soutenance

- **F25 Fine-tuning CamemBERT** sur dataset SKILLNAV annoté (30–50 offres avec entités validées manuellement) — gain F1 attendu de +3–5 points sur entités techniques
- **F26 Déploiement public skillnav.ma** — domaine personnalisé, mise à jour mensuelle
- **Article Medium / DataTalks** — exposition de la méthodologie au public francophone

### 5.4 V2 — Vision long terme

- **F27 Pipeline live** — Celery + APScheduler, scraping hebdomadaire automatique
- **F28 Agents prospectifs** — Claude Agent SDK pour investigation libre sur métiers émergents (intégration MCP servers)
- **F29 API publique versionnée** — exposition des aggregates pour partenaires académiques

---

## 6. ARCHITECTURE TECHNIQUE

### 6.1 Diagramme général MVP — Pipeline global

Le pipeline SKILLNAV chaîne **8 étapes** sur 4 outils de stockage : système de fichiers (raw HTML / JSONL), MongoDB Atlas (collections enrichies), Neo4j AuraDB (graphe), Elasticsearch Cloud (index de recherche).

```
   ┌──────────────────────────────────────────┐
   │  COLLECTE (Karamo)                       │
   │   ┌────────────┐  ┌─────────────┐        │
   │   │ Scrapy     │  │ Playwright  │        │
   │   │ Rekrute    │  │ EmploiTIC   │        │
   │   │ Indeed     │  │ WTTJ        │        │
   │   └─────┬──────┘  └──────┬──────┘        │
   │         │                │                │
   │   ┌─────▼────────────────▼──────┐        │
   │   │ Apify MCP  +  Firecrawl     │        │
   │   │  LinkedIn MA + International│        │
   │   │  Pages JS dynamiques        │        │
   │   └─────────────┬──────────────┘         │
   │                 │                         │
   │   ┌─────────────▼──────────────┐         │
   │   │ Signaux faibles            │         │
   │   │  Google Trends (pytrends)  │         │
   │   │  GitHub Trending           │         │
   │   │  HuggingFace trending      │         │
   │   └─────────────┬──────────────┘         │
   └─────────────────┼─────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  data/raw/{source}_{date}.jsonl          │
   │  + raw HTML archivé                      │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INGESTION  (skillnav ingest)            │
   │  Pydantic validation → MongoDB raw_jobs  │
   │  Dédup SHA-256 (company+title+location)  │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  EXTRACTION IA + NER  (Karamo)           │
   │  ┌─────────────────────────────────────┐ │
   │  │ Pydantic AI + Claude Sonnet 4.5     │ │
   │  │   → extracted_jobs (MongoDB)        │ │
   │  └─────────────────────────────────────┘ │
   │  ┌─────────────────────────────────────┐ │
   │  │ HF Transformers NER × 3 modèles     │ │
   │  │   → ner_annotations (MongoDB)       │ │
   │  └─────────────────────────────────────┘ │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  STRUCTURE  (Bachirou Konaté)                   │
   │  Construction graphe → Neo4j AuraDB      │
   │  PageRank + Louvain + Label Propagation  │
   │  Export résultats vers MongoDB           │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  USAGE  (Karamo)                         │
   │  Séries temporelles skill_count(time)    │
   │  ARIMA + Prophet + LSTM                  │
   │  Détection émergentes (3 méthodes)       │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INDEXATION  (Karamo)                    │
   │  Elasticsearch Cloud                     │
   │   - index jobs_search (full-text + filt) │
   │   - index skills_timeseries              │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  API + DASHBOARD                         │
   │  FastAPI ↔ Mongo/Neo4j/ES                │
   │  Next.js 15 ↔ FastAPI                    │
   │  Déploiement : Render (API) + Vercel (UI)│
   └──────────────────────────────────────────┘
```

### 6.2 Diagramme par axe — Web Content Mining

```
   raw_jobs (MongoDB)
        │
        ▼
   ┌─────────────────────────────────────────┐
   │ Cleaner :                               │
   │   - HTML strip (BeautifulSoup)          │
   │   - Lang detect (fasttext langid)       │
   │   - Sentence split (spaCy)              │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ Pydantic AI + Claude (extraction)       │
   │   → extracted_jobs                      │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ HF Transformers (NER comparé) :         │
   │   - BERT-base-multilingual              │
   │   - CamemBERT-NER (FR)                  │
   │   - DistilBERT (EN)                     │
   │   → ner_annotations                     │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ Normalisation taxonomique :             │
   │   - sentence-transformers embeddings    │
   │   - Cosine similarity ≥ 0.85 → alias    │
   │   - Validation manuelle des doublons    │
   └─────────────────────────────────────────┘
```

### 6.3 Diagramme par axe — Web Structure Mining

```
   extracted_jobs + ner_annotations (MongoDB)
        │
        ▼
   ┌─────────────────────────────────────────┐
   │ Graph Builder (Python)                  │
   │   - Itère sur les offres                │
   │   - Crée nœuds Skill / Job / Family     │
   │   - Calcule arêtes CO_OCCURS_WITH       │
   │     (compteur de co-occurrences offre)  │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ Neo4j AuraDB (graph store)              │
   │   - Cypher queries via neo4j-driver     │
   │   - GDS library (PageRank, Louvain)     │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ Analytics (Python via neo4j-driver)     │
   │   - PageRank → top compétences          │
   │   - Louvain → communautés colorées      │
   │   - Label Propagation → communautés alt │
   │   - Leiden (via igraph) → communautés   │
   │   → métriques modularité × runtime      │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ Export résultats → MongoDB              │
   │ (graph_metrics, communities_louvain,    │
   │  pagerank_scores) pour API rapide       │
   └─────────────────────────────────────────┘
```

### 6.4 Diagramme par axe — Web Usage Mining

```
   extracted_jobs (MongoDB) + Google Trends + GitHub Trending
        │
        ▼
   ┌─────────────────────────────────────────┐
   │ Time Series Builder (Python)            │
   │   - Pour chaque skill, count par mois   │
   │   - Normalisation (% du total mois)     │
   │   - Stockage skills_timeseries (Mongo)  │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ Forecasting comparatif :                │
   │   - ARIMA (statsmodels)                 │
   │   - Prophet (prophet, Meta)             │
   │   - LSTM (neuralforecast, Nixtla)       │
   │   → MAPE, RMSE, MAE par modèle          │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ Émergence detector (3 méthodes) :       │
   │   - Heuristique pondérée                │
   │   - Supervisé XGBoost                   │
   │   - Clustering temporel KMeans          │
   └────────┬────────────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────┐
   │ Indexation Elasticsearch                │
   │   - jobs_search (full-text + filters)   │
   │   - skills_timeseries (aggregations)    │
   └─────────────────────────────────────────┘
```

### 6.5 Pipeline NER détaillé

```
   offer.raw_text
        │
        ▼
   ┌─────────────────────────────────────────┐
   │ Pré-traitement :                        │
   │   - lang detect (fasttext)              │
   │   - tokenization (transformers tokeniz.)│
   │   - troncature à 512 tokens (BERT)      │
   └────────┬────────────────────────────────┘
            │
       ┌────┴────┬─────────┬──────────┐
       ▼         ▼         ▼          ▼
   ┌──────┐ ┌──────┐ ┌────────┐ ┌──────────┐
   │BERT  │ │CamBT │ │DistilBT│ │Pydantic  │
   │multi │ │NER   │ │NER     │ │AI Claude │
   │      │ │(FR)  │ │(EN)    │ │(struct)  │
   └──┬───┘ └──┬───┘ └───┬────┘ └────┬─────┘
      │        │         │            │
      └────────┴────┬────┴────────────┘
                    ▼
   ┌─────────────────────────────────────────┐
   │ Fusion + dédup :                        │
   │   - Pour chaque entité : choisir le     │
   │     modèle avec meilleure confidence    │
   │   - Mapping aux types canoniques        │
   │     (SKILL / TOOL / FRAMEWORK / MODEL /  │
   │      LANGUAGE / ROLE / ORGANIZATION)    │
   │   - Persistance ner_annotations         │
   └─────────────────────────────────────────┘
```

### 6.6 Communication Python ↔ Next.js

**Principe** : zéro accès direct aux DBs depuis Next.js. Toute la communication passe par l'API FastAPI typée OpenAPI.

```
┌──────────────────────────────────────────────────────────┐
│  FastAPI (Python)                                        │
│  Génère openapi.json automatiquement                     │
└──────────────────────────────────────────────────────────┘
                         │ Téléchargé par Next.js au build
                         ▼
┌──────────────────────────────────────────────────────────┐
│  openapi-typescript (npm package)                        │
│  $ pnpm run generate-types                               │
│  Génère src/lib/api/types.ts                             │
│  Tous les types TypeScript = miroir des Pydantic models  │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│  Composants React utilisent l'API                        │
│  const { data } = useQuery(['top-skills'], ...)          │
│  → data est typé automatiquement                         │
│  → Si Pydantic change, TypeScript hurle au build         │
└──────────────────────────────────────────────────────────┘
```

**Conventions API REST MVP :**

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/aggregates/top-skills` | Top compétences (filtré par famille, géo, période) |
| GET | `/api/aggregates/emerging-skills` | Compétences émergentes (3 méthodes) |
| GET | `/api/aggregates/forecasts/{skill}` | Forecast ARIMA + Prophet + LSTM |
| GET | `/api/graph/pagerank` | Top compétences par PageRank |
| GET | `/api/graph/communities` | Communautés Louvain |
| GET | `/api/graph/full` | Graphe complet (nœuds + arêtes) pour rendu force |
| GET | `/api/ner/sample` | Sample d'offres annotées (3 modèles) |
| GET | `/api/ner/comparison` | Métriques comparatives NER (F1 micro/macro par modèle × type) |
| GET | `/api/quality/dataset-stats` | Stats Data Quality (complétude, biais) |
| GET | `/api/search` | Recherche full-text Elasticsearch |
| GET | `/api/comparative-study` | Données page `/comparative-study` |

---

## 7. ARCHITECTURE DES DONNÉES

### 7.0 Justification de l'architecture NoSQL polyglotte (CRITIQUE)

SKILLNAV utilise **trois stores complémentaires**. Cette section démontre pourquoi un seul SGBD (par exemple PostgreSQL) **n'aurait pas suffi** — c'est un critère d'évaluation explicite du sujet imposé.

| Store | Besoin couvert | Pourquoi ce SGBD spécifiquement |
|---|---|---|
| **MongoDB Atlas** | Stockage flexible des offres semi-structurées (texte brut + champs Pydantic + annotations NER) | Schéma souple essentiel : les offres ont des structures hétérogènes par source ; les `ner_annotations` ont une cardinalité variable (1 à 50 entités par offre). Indexation native sur champs nested. *Free tier 512 MB suffisant pour 2 000 offres.* |
| **Neo4j AuraDB** | Graphe de compétences (Skill, Job, Family, edges CO_OCCURS_WITH, REQUIRES, BELONGS_TO) | Algorithmes natifs (PageRank, Louvain, Label Propagation) via la bibliothèque GDS. Requêtes Cypher 100× plus rapides qu'un JOIN récursif SQL pour la centralité. *Free tier AuraDB suffisant pour ~200 000 nœuds.* |
| **Elasticsearch Cloud** | Recherche full-text + agrégations sur séries temporelles | Recherche full-text en français/anglais avec analyzers natifs (stemming, accents, langue). Agrégations efficaces pour `/forecasting`. *Free tier 14 jours, suffisant pour la soutenance.* |

**Stratégie d'écriture** : MongoDB est la *source of truth* pour les données d'offres ; Neo4j est dérivé (graphe reconstruit à la demande) ; Elasticsearch est dérivé (index réindexable). Cette stratégie permet de **rejouer** la pipeline à zéro depuis MongoDB seul, ce qui assure la reproductibilité scientifique.

**Plans B si une DB échoue** :

| Risque | Plan B |
|---|---|
| Free tier Elastic Cloud expire | MongoDB Atlas Search + agrégations Mongo (couverture ~80 % des cas, latence légèrement supérieure) |
| Free tier Neo4j AuraDB saturé | NetworkX en mémoire (Python pur) + persistance JSON dans MongoDB ; on perd Cypher mais on garde les algos |
| Free tier MongoDB Atlas saturé | SQLite local (pour MVP de soutenance uniquement) |

### 7.1 Modèle conceptuel — vue d'ensemble

```
┌─────────────────┐         ┌──────────────────┐
│  Source         │ 1     N │  RawJob          │
│ (catalogue      │─────────│ (offre brute)    │
│  scrapée)       │         │                  │
└─────────────────┘         └────────┬─────────┘
                                     │1
                                     │
                                     │1
                            ┌────────▼─────────┐
                            │ ExtractedJob     │
                            │ (Pydantic AI     │
                            │  + champs IA)    │
                            └────────┬─────────┘
                                     │1
                                     │
                                     │N
                            ┌────────▼─────────┐
                            │ NerAnnotation    │
                            │ (par modèle NER) │
                            └──────────────────┘

GRAPHE NEO4J (dérivé) :
   (:Skill)-[:CO_OCCURS_WITH {weight: int}]->(:Skill)
   (:Job)-[:REQUIRES {weight: float}]->(:Skill)
   (:Skill)-[:BELONGS_TO]->(:SkillFamily)
   (:Job)-[:FROM_SOURCE]->(:Source)

INDEX ELASTICSEARCH (dérivé) :
   jobs_search          (full-text, filtres : pays, famille, période)
   skills_timeseries    (agrégations sur volumes mensuels)
```

### 7.2 Schéma MongoDB

#### Collection `sources`

```json
{
  "_id": "rekrute_ma",
  "name": "Rekrute",
  "base_url": "https://www.rekrute.com",
  "country": "MA",
  "geography": "national",
  "scraper_type": "scrapy",
  "robots_txt_compliant": true,
  "tos_reviewed_at": "2026-05-08",
  "rate_limit_seconds": 5,
  "is_active": true,
  "last_scraped_at": "2026-05-14T08:30:00Z",
  "last_offers_count": 47
}
```

Catégories de sources : `national` (Rekrute, EmploiTIC), `linkedin_country` (Apify), `international` (Indeed, builtin.com, WTTJ), `weak_signal` (Google Trends, GitHub Trending).

#### Collection `raw_jobs`

```json
{
  "_id": "ObjectId",
  "source": "rekrute_ma",
  "url": "https://www.rekrute.com/offres/12345",
  "title_raw": "Data Scientist Senior — Python/PyTorch",
  "company_raw": "Casablanca Analytics",
  "location_raw": "Casablanca, Maroc",
  "raw_html": "<div>...</div>",
  "raw_text": "Description complète...",
  "dedup_hash": "a8f3...",
  "published_at": "2026-05-04",
  "scraped_at": "2026-05-06T08:30:00Z",
  "last_seen_at": "2026-05-06T08:30:00Z",
  "extraction_status": "pending"
}
```

**Index** : `{source: 1, dedup_hash: 1}` unique pour dédoublonnage ; `{extraction_status: 1}` pour le batch.

#### Collection `extracted_jobs`

Structure dérivée du schéma Pydantic `JobExtraction` (cf. §5.2 F04). Stockée 1-1 avec `raw_jobs.url` (clé de jointure).

#### Collection `ner_annotations`

```json
{
  "_id": "ObjectId",
  "job_url": "https://www.rekrute.com/offres/12345",
  "model": "Jean-Baptiste/camembert-ner",
  "language_detected": "fr",
  "annotations": [
    {"text": "PyTorch", "type": "FRAMEWORK", "start": 42, "end": 49, "confidence": 0.97},
    {"text": "BERT", "type": "MODEL", "start": 120, "end": 124, "confidence": 0.95},
    {"text": "Python", "type": "LANGUAGE", "start": 200, "end": 206, "confidence": 0.99}
  ],
  "annotated_at": "2026-05-06T09:00:00Z"
}
```

Pour chaque offre, 3 documents `ner_annotations` (un par modèle) — permet la comparaison.

#### Collections dérivées

- `skills_taxonomy` : compétences canoniques avec aliases (résultat normalisation sentence-transformers)
- `skills_timeseries` : volumes mensuels par compétence × période
- `forecasts` : prédictions ARIMA / Prophet / LSTM avec intervalles de confiance
- `graph_metrics` : PageRank scores, communautés Louvain, modularité

### 7.3 Schéma Neo4j

```cypher
// Nœuds
(:Skill {name: STRING, family: STRING, aliases: [STRING]})
(:Job {url: STRING, title: STRING, company: STRING, country: STRING})
(:SkillFamily {name: STRING, color_hex: STRING})
(:Source {id: STRING, country: STRING})

// Arêtes
(:Job)-[:REQUIRES {confidence: FLOAT}]->(:Skill)
(:Skill)-[:CO_OCCURS_WITH {weight: INT, normalized_weight: FLOAT}]->(:Skill)
(:Skill)-[:BELONGS_TO]->(:SkillFamily)
(:Job)-[:FROM_SOURCE]->(:Source)

// Index
CREATE INDEX skill_name FOR (s:Skill) ON (s.name);
CREATE INDEX job_url FOR (j:Job) ON (j.url);
```

### 7.4 Schéma Elasticsearch

```json
PUT /jobs_search
{
  "mappings": {
    "properties": {
      "title": {"type": "text", "analyzer": "french"},
      "description": {"type": "text", "analyzer": "french"},
      "company": {"type": "keyword"},
      "country": {"type": "keyword"},
      "city": {"type": "keyword"},
      "skills": {"type": "keyword"},
      "ml_subdomains": {"type": "keyword"},
      "frameworks": {"type": "keyword"},
      "role_family": {"type": "keyword"},
      "published_at": {"type": "date"},
      "scraped_at": {"type": "date"},
      "extraction_confidence": {"type": "float"}
    }
  }
}

PUT /skills_timeseries
{
  "mappings": {
    "properties": {
      "skill": {"type": "keyword"},
      "month": {"type": "date", "format": "yyyy-MM"},
      "count": {"type": "integer"},
      "normalized_pct": {"type": "float"},
      "family": {"type": "keyword"}
    }
  }
}
```

### 7.5 Pydantic v2 comme source de vérité

**Principe** : tous les schémas (MongoDB, Neo4j, Elasticsearch) **dérivent** de modèles Pydantic v2 centraux. Un convertisseur dédié transforme un objet Pydantic en payload Mongo / Cypher / ES.

```
skillnav/
└── schemas/
    ├── job.py           # JobExtraction, RawJob (sources de vérité)
    ├── ner.py           # NerAnnotation, Entity
    ├── graph.py         # SkillNode, JobNode, Edge
    ├── timeseries.py    # SkillTimeSeries, Forecast
    └── converters/
        ├── to_mongo.py  # Pydantic → BSON
        ├── to_neo4j.py  # Pydantic → Cypher params
        └── to_es.py     # Pydantic → ES document
```

**Avantages** : (i) validation à l'écriture, (ii) refactor cohérent (si le schéma change, tous les converters cassent au type-check), (iii) génération automatique du JSON Schema pour documentation.

---

## 8. SOURCES DE DONNÉES

### 8.1 Stratégie multi-sources

SKILLNAV agrège trois catégories de sources, chacune justifiée par sa fonction dans le pipeline :

| Catégorie | Fonction | Volume cible MVP |
|---|---|---|
| **Maroc (national)** | Ancrage géographique principal, conformité au sujet imposé (entité locale) | 300–500 offres |
| **International (FR + EN)** | Couverture des compétences émergentes (souvent absentes du marché local), benchmark de comparaison | 800–1 500 offres |
| **Signaux faibles** | Validation indépendante de l'émergence (Q3 axe Usage Mining) | 50–100 séries temporelles |

**Volume cible total** : **500–2 000 offres analysées**, réparties sur Maroc + International, sur une période de 3–6 mois.

### 8.2 Sources Maroc

| Source | URL | Mode collecte | Particularités |
|---|---|---|---|
| **Rekrute** | rekrute.com | Scrapy (HTML statique) | Premier portail emploi MA, ~3 000 offres actives, sitemap accessible |
| **EmploiTIC** | emploitic.com | Scrapy + Playwright (pagination JS) | Spécialisé IT — concentration IA / DS / dev |
| **LinkedIn Maroc** | linkedin.com (filtre `geo=MA`) | Apify MCP (`apify/linkedin-jobs-scraper`) | Plafond : 200 offres / session pour respecter quotas |
| **Pages carrières** | careers.ocp.ma, jobs.inwi.ma, etc. | Firecrawl MCP | Top 10 employeurs IA Maroc (banques, télécoms, OCP, scale-ups) |

**Rate limiting** : 5 secondes minimum entre requêtes sur sources statiques, respect `Crawl-delay` si présent dans robots.txt.

### 8.3 Sources Internationales

| Source | URL | Mode collecte | Particularités |
|---|---|---|---|
| **LinkedIn International** | linkedin.com | Apify (filtres : France, Europe, US) | Volume principal compétences mondiales |
| **Indeed** | indeed.fr, indeed.com | Scrapy + Playwright | Bon volume FR + EN, structure HTML stable |
| **builtin.com** | builtin.com | Scrapy | Tech-only US, riche en compétences IA pointues |
| **Welcome to the Jungle** | welcometothejungle.com | Playwright (SPA) | Marché tech FR, descriptions très détaillées |
| **Otta** *(si bandwidth)* | otta.com | Firecrawl | Tech jobs UK/EU, qualité descriptive élevée |

### 8.4 Signaux faibles (Usage Mining)

| Source | Type | Library |
|---|---|---|
| **Google Trends** | Recherches publiques (proxy d'intérêt) | `pytrends` |
| **GitHub Trending** | Repos tendance (langages / topics IA) | API GitHub + parsing HTML |
| **HuggingFace Trending** | Modèles / datasets tendance | API HF Hub |
| **Papers With Code Trending** | Papers IA tendance par benchmark | Scraping |

Ces signaux ne sont **pas** utilisés comme features dans le pipeline principal de prédiction, mais comme **validateurs externes** : si une compétence est détectée émergente par SKILLNAV ET trend Google Trends ET trend GitHub, sa qualification est renforcée (cf. §10.4).

### 8.5 Conformité — robots.txt et TOS

Chaque source est inscrite dans `sources/registry.yaml` avec :

```yaml
- id: rekrute_ma
  name: Rekrute
  base_url: https://www.rekrute.com
  robots_txt_url: https://www.rekrute.com/robots.txt
  robots_txt_compliant: true       # vérifié manuellement
  tos_url: https://www.rekrute.com/conditions
  tos_reviewed_at: 2026-05-08
  tos_reviewed_by: karamo
  rate_limit_seconds: 5
  user_agent: "SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)"
```

Voir [§N4 RGPD](#n4-rgpd-robotstxt-et-anonymisation) pour le protocole complet.

### 8.6 Schéma de sortie JSONL normalisé

Chaque source doit produire un JSONL conforme au schéma :

```jsonl
{"source":"rekrute_ma","collected_at":"2026-05-06T08:30:00Z","url":"https://www.rekrute.com/offres/12345","title_raw":"Data Scientist","company_raw":"Casablanca Analytics","location_raw":"Casablanca","contract_type_raw":"CDI","posted_at":"2026-05-04","raw_html":"<div>...</div>","raw_text":"..."}
```

**Champs obligatoires** : `source`, `collected_at` (ISO 8601 UTC), `url`, `title_raw`, `raw_text`. Tous les autres sont optionnels — l'extraction Pydantic AI les retrouvera dans `raw_text`.

---

## 9. PIPELINE D'EXTRACTION IA

### 9.1 Vue d'ensemble

Le pipeline d'extraction enchaîne **quatre étapes** :

1. **Cleaning** (HTML strip, lang detect)
2. **Extraction structurée** (Pydantic AI + Claude)
3. **NER comparative** (3 modèles HuggingFace)
4. **Normalisation taxonomique** (sentence-transformers + clustering)

### 9.2 Étape 1 — Cleaning

```python
from bs4 import BeautifulSoup
from fasttext.FastText import _FastText
import spacy

def clean_text(raw_html: str) -> tuple[str, str]:
    """Retourne (texte_nettoyé, langue_détectée)."""
    soup = BeautifulSoup(raw_html, "lxml")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    text = "\n".join(line for line in text.split("\n") if line.strip())
    lang = langid_model.predict(text[:500])[0][0].replace("__label__", "")
    return text, lang
```

### 9.3 Étape 2 — Extraction Pydantic AI

```python
from pydantic_ai import Agent
from anthropic import Anthropic
from schemas.job import JobExtraction

extraction_agent = Agent[None, JobExtraction](
    model="claude-sonnet-4-5",
    result_type=JobExtraction,
    system_prompt="""Tu es un extracteur de données structurées spécialisé
    dans les offres d'emploi IA / Data Science. Tu produis un objet JSON
    strictement conforme au schéma Pydantic JobExtraction. Confidence ≥ 0.75
    requis ; sinon, ajoute une note explicative."""
)

async def extract(raw_text: str) -> JobExtraction:
    result = await extraction_agent.run(raw_text)
    return result.data
```

**Pipeline batch** :

```python
async def batch_extract(batch_size: int = 50) -> None:
    pending = await mongo.raw_jobs.find(
        {"extraction_status": "pending"}
    ).limit(batch_size).to_list()

    for offer in pending:
        try:
            extracted = await extract(offer["raw_text"])
            await mongo.extracted_jobs.insert_one(extracted.model_dump())
            await mongo.raw_jobs.update_one(
                {"_id": offer["_id"]},
                {"$set": {"extraction_status": "success"}}
            )
        except ValidationError as e:
            await mongo.raw_jobs.update_one(
                {"_id": offer["_id"]},
                {"$set": {
                    "extraction_status": "quarantine",
                    "extraction_error": str(e)
                }}
            )
```

### 9.4 Étape 3 — NER classique (référence)

Avant les Transformers, on documente la **baseline** par règles (regex sur listes blanches) pour mesurer le gain réel apporté par les modèles ML. Cette baseline figure en témoin dans l'étude comparative §N2.1.

### 9.4bis — Étape 3' — Pipeline NER Transformers

Le pipeline NER Transformers exécute **trois modèles HuggingFace en parallèle** sur chaque offre :

```python
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

MODELS = {
    "bert-multi": "bert-base-multilingual-cased",   # fine-tune NER ajouté en local
    "camembert-fr": "Jean-Baptiste/camembert-ner",
    "distilbert-en": "elastic/distilbert-base-cased-finetuned-conll03-english",
}

ner_pipelines = {
    name: pipeline("ner", model=model_id, aggregation_strategy="simple")
    for name, model_id in MODELS.items()
}

def annotate_all(text: str, language: str) -> dict[str, list[Entity]]:
    """Retourne {model_name: [entities]}."""
    out = {}
    for name, pipe in ner_pipelines.items():
        # On peut sauter les modèles non adaptés à la langue détectée
        if name == "camembert-fr" and language != "fr":
            continue
        if name == "distilbert-en" and language != "en":
            continue
        out[name] = pipe(text[:512])
    return out
```

**Mapping vers types canoniques SKILLNAV** : un dictionnaire de mapping convertit les labels natifs (PER, ORG, MISC, LOC, B-SKILL, etc.) vers les types canoniques (`SKILL`, `TOOL`, `FRAMEWORK`, `MODEL`, `LANGUAGE`, `ROLE`, `ORGANIZATION`).

**Acceptance criteria** :
- ≥ 30 offres annotées manuellement (gold set) pour évaluation
- F1 micro / macro par modèle calculé dans `notebooks/02_ner_comparison.ipynb`
- Choix justifié du modèle champion pour pipeline production MVP

### 9.5 Étape 4 — Normalisation taxonomique

```python
from sentence_transformers import SentenceTransformer
import numpy as np

embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def normalize_skill(raw_skill: str, taxonomy: list[str]) -> tuple[str, float]:
    """Retourne (skill_canonique, similarité)."""
    raw_emb = embedder.encode([raw_skill])[0]
    tax_embs = embedder.encode(taxonomy)
    similarities = np.dot(tax_embs, raw_emb) / (
        np.linalg.norm(tax_embs, axis=1) * np.linalg.norm(raw_emb)
    )
    best_idx = int(np.argmax(similarities))
    return taxonomy[best_idx], float(similarities[best_idx])

# Si similarité ≥ 0.85 → alias automatique
# Si 0.70 ≤ similarité < 0.85 → quarantaine pour validation manuelle
# Si similarité < 0.70 → nouveau skill candidat (entrée taxonomy_review)
```

### 9.6 Mesure de qualité de l'extraction

| Métrique | Seuil cible MVP |
|---|---|
| % offres avec `extraction_confidence ≥ 0.75` | ≥ 90 % |
| % offres en quarantaine (validation) | ≤ 10 % |
| Temps moyen d'extraction (Claude Sonnet) | < 8 s / offre |
| Coût Claude pour 1 000 offres | < 15 $ |
| F1 NER (modèle champion) sur gold set | ≥ 0.80 micro |

### 9.7 LLM cloud vs Transformers locaux — discussion

Le projet utilise **les deux approches** côte à côte. Cette dualité est intentionnelle : elle alimente l'étude comparative et permet une discussion académique honnête.

| Critère | Pydantic AI + Claude (cloud) | HF Transformers (local) |
|---|---|---|
| **Qualité d'extraction structurée** | Excellente (Claude Sonnet 4.5 comprend le contexte) | Moyenne (NER seul, pas de structuration JSON) |
| **Latence** | 5–8 s / offre | 0.3–0.8 s / offre |
| **Coût** | ~$0.015 / offre | $0 (après téléchargement modèle) |
| **RGPD** | Données envoyées à Anthropic (DPA disponible) | Inférence locale, aucune donnée transférée |
| **Reproductibilité scientifique** | Modèle propriétaire, version peut changer | Version épinglée HF, reproductibilité totale |
| **Robustesse hors-ligne** | Nécessite API live | Fonctionne offline |

**Choix architectural SKILLNAV** : Claude pour l'extraction structurée (qualité + souplesse) ; Transformers pour la NER fine-grained (vitesse + reproductibilité scientifique). La comparaison NER est faite **uniquement** entre Transformers entre eux (cf. §N2.1) — pas entre Claude et Transformers, car ce n'est pas une comparaison équitable (Claude fait bien plus que de la NER).

---

## 10. RÈGLES MÉTIER

### 10.1 Règles d'extraction

| Code | Règle |
|---|---|
| RE-1 | Une offre dont `extraction_confidence < 0.75` est placée en quarantaine, jamais publiée |
| RE-2 | Une offre sans `skills_required` (≥ 3 items) est rejetée |
| RE-3 | Une offre dont `role_family` ne fait pas partie des 10 familles canoniques est rejetée |
| RE-4 | Les valeurs des champs `Literal` sont validées par Pydantic — aucune valeur libre acceptée |
| RE-5 | Les durées d'expérience absurdes (> 30 ans) sont normalisées à `None` |
| RE-6 | Le titre normalisé `title_normalized` doit avoir entre 3 et 80 caractères |
| RE-7 | Pas d'extraction de nom de candidat / contact RH / email : si présent dans le texte source, ne pas l'inclure dans la sortie (cf. §N4) |
| RE-8 | Toute extraction est tracée avec `extraction_model`, `extracted_at`, `extraction_version` |

### 10.2 Règles de normalisation

| Code | Règle |
|---|---|
| RN-1 | Aliases connus → forme canonique (`ML` → `Machine Learning`, `DL` → `Deep Learning`) |
| RN-2 | Casse normalisée (`pytorch` → `PyTorch`) via lookup dans `skills_taxonomy` |
| RN-3 | Cosine similarity sentence-transformers ≥ 0.85 → alias automatique |
| RN-4 | 0.70 ≤ cosine < 0.85 → entrée `taxonomy_review` pour validation manuelle |
| RN-5 | Cosine < 0.70 → nouveau skill candidat, validation manuelle requise avant publication |

### 10.3 Règles de classification (10 familles IA)

Une compétence est rattachée à une famille selon (i) une heuristique sur le nom (mapping pré-défini), (ii) confirmation par Claude Haiku si ambigu. Les 10 familles sont définies dans la **Charte SKILLNAV §02** et reprises ici :

ML Classique · Deep Learning · NLP · Computer Vision · Data Engineering · MLOps · Cloud & Big Data · AI Ethics · Statistiques · Outils & Soft Skills.

### 10.4 Compétences émergentes — comparaison de 3 méthodes

**Méthode 1 — Heuristique pondérée** :

```
emerging_score = (volume_normalisé      × 0.40)
              + (growth_rate_3m          × 0.40)
              + (présence_signaux_faibles × 0.20)

Émergente si emerging_score > 0.70  AND  volume_brut ≥ 5
```

`volume_normalisé` = volume du skill / volume du skill le plus fréquent (sur la période)
`growth_rate_3m` = (volume_M0 − volume_M-3) / max(volume_M-3, 1), clippé à [0, 2]
`présence_signaux_faibles` = 1 si le skill apparaît dans Google Trends OR GitHub Trending, sinon 0.5 sinon 0

**Méthode 2 — Supervisé XGBoost** :
- Jeu d'entraînement : 50 skills annotés manuellement (émergent / établi / déclinant)
- Features : `volume_normalisé`, `growth_rate_3m`, `growth_rate_6m`, `age_months`, `family_id`, `google_trends_score`, `github_mentions`
- Métriques : précision / rappel / F1 / matrice de confusion

**Méthode 3 — Clustering temporel** :
- Pour chaque skill, série mensuelle normalisée (z-score)
- KMeans `k=3` sur les vecteurs trajectoires
- Cluster identifié comme « émergent » = celui dont les profils ont la pente positive la plus marquée sur les 3 derniers mois

**Comparaison** (cf. §N2.4) sur précision / rappel / F1 vs jeu de validation indépendant.

### 10.5 Règles éthiques (RGPD)

Voir [§N4 RGPD](#n4-rgpd-robotstxt-et-anonymisation) pour le détail. Synthèse :

| Code | Règle |
|---|---|
| RE-RGPD-1 | Données personnelles candidates (nom, email, téléphone) : **jamais collectées** |
| RE-RGPD-2 | Données entreprises publiques (nom employeur, ville, secteur) : collectées sous base légale art. 6.1.f (intérêt légitime) |
| RE-RGPD-3 | Datasets exportés : anonymisation par hashage des noms d'entreprises < 10 offres |
| RE-RGPD-4 | Droit d'opposition : email `optout@skillnav.example` documenté, traitement < 30 jours |
| RE-RGPD-5 | Durée de conservation : `raw_html` ≤ 6 mois ; `extracted_jobs` ≤ 24 mois |
| RE-RGPD-6 | Respect strict de robots.txt : si Disallow, source désactivée |
| RE-RGPD-7 | User-Agent identifié : `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)` |
| RE-RGPD-8 | Rate limiting par défaut 5 s/requête, override prudent uniquement |

---

## N1. MAPPING PROJET ↔ 3 AXES WEB MINING

> **Cette section est lue en premier par le Pr. Sassi. Elle démontre que SKILLNAV couvre rigoureusement et équilibrément les trois axes canoniques du Web Mining.**

### N1.1 Définitions canoniques

| Axe | Définition (Liu, *Web Data Mining*, 2011) | Question canonique |
|---|---|---|
| **Web Content Mining** | Extraction d'information utile à partir du contenu textuel des pages (NLP appliqué au web) | « Quelle information est dans la page ? » |
| **Web Structure Mining** | Analyse de la structure des liens entre entités (graphes, hub/authority, communautés) | « Comment les entités sont-elles reliées ? » |
| **Web Usage Mining** | Analyse des patterns d'utilisation au cours du temps (séries temporelles, clickstream) | « Comment l'usage évolue-t-il ? » |

### N1.2 Couverture par SKILLNAV

| Axe | Technique appliquée | Modèle / algorithme | Livrable principal | Page dashboard | Section PRD |
|---|---|---|---|---|---|
| **Web Content Mining** | Extraction structurée + NER | Pydantic AI + Claude Sonnet 4.5 ; BERT-base-multilingual, CamemBERT-NER, DistilBERT-NER | Pipeline IA validé (livrable L3) | `/ner-explorer` | §9, §9.4bis |
| **Web Structure Mining** | Construction graphe + centralité + détection de communautés | PageRank, Louvain, Label Propagation, Leiden | Graphe Neo4j peuplé (livrable L2) | `/graph` | §6.3, §7.3, §F08–F10 |
| **Web Usage Mining** | Séries temporelles + forecasting + détection d'émergence | ARIMA, Prophet, LSTM ; Heuristique pondérée, XGBoost, KMeans temporel | Forecasts + KPIs (livrable L4) | `/forecasting`, `/skills` | §6.4, §10.4 |

### N1.3 Équilibre des trois axes

| Axe | % code source (estimation) | % temps binôme | Livrables associés |
|---|:---:|:---:|---|
| Content | 35 % | 35 % | L1 (scripts), L2 (MongoDB), L3 (pipeline NER), L5 (rapport partiel) |
| Structure | 30 % | 30 % | L2 (Neo4j), L4 (dashboard graphe), L5 (rapport partiel) |
| Usage | 30 % | 30 % | L2 (Elastic skills_timeseries), L4 (dashboard forecast), L5 (rapport partiel) |
| Transverse | 5 % | 5 % | L4 (dashboard pages méthodo), L6 (soutenance) |

**Garantie d'équilibre** : aucun axe ne représente moins de 25 % du code, du temps ou des livrables. Cet équilibre est démontrable et figurera dans l'introduction de la soutenance.

### N1.4 Étude comparative par axe (CRITIQUE)

Le sujet impose une étude comparative rigoureuse. SKILLNAV en fait **trois** (une par axe) :

| Axe | Comparaison | Modèles comparés |
|---|---|---|
| Content | NER multilingue | BERT-base-multilingual / CamemBERT-NER / DistilBERT (cf. §N2.1) |
| Structure | Détection de communautés | Louvain / Label Propagation / Leiden (cf. §N2.2) |
| Usage | Forecasting séries temporelles | ARIMA / Prophet / LSTM (cf. §N2.3) |
| Usage *(bonus)* | Détection compétences émergentes | Heuristique / XGBoost / KMeans temporel (cf. §N2.4) |

---

## N2. ÉTUDE COMPARATIVE ALGORITHMIQUE

> **Pour chaque comparaison : protocole, jeu test, métriques chiffrées, résultats, choix retenu, justification. Aucune comparaison qualitative seule — c'est une exigence du sujet.**

### N2.1 NER comparatif — BERT-multi / CamemBERT / DistilBERT

#### Protocole

- **Jeu test (gold set)** : 30 offres annotées manuellement par le binôme (15 FR + 15 EN), avec entités SKILL, TOOL, FRAMEWORK, MODEL, LANGUAGE, ROLE, ORGANIZATION
- **Annotation** : conventions BIO documentées dans `data/gold_set/annotation_guidelines.md`
- **Métriques** : F1-score micro et macro, précision, rappel, par type d'entité
- **Comparaison** : 3 modèles × 7 types d'entités × 4 métriques

#### Tableau attendu (template — chiffres à mesurer)

| Modèle | F1 micro | F1 macro | F1 SKILL | F1 FRAMEWORK | F1 MODEL | F1 LANGUAGE | Runtime / offre |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BERT-base-multilingual + tête NER | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| CamemBERT-NER (FR only) | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| DistilBERT-NER (EN only) | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

#### Choix retenu (cible)

Le modèle **champion** pour le pipeline production MVP sera celui qui maximise F1 macro **ET** garde un runtime ≤ 1 s / offre. Hypothèse préalable : CamemBERT-NER pour les offres FR, DistilBERT pour les EN, BERT-multi en fallback langue inconnue.

**Justification académique** : la routage par langue (langid avant NER) permet d'exploiter la spécialisation de chaque modèle. Le coût de cette routage est négligeable (langid < 5 ms).

### N2.2 Détection de communautés — Louvain / Label Propagation / Leiden

#### Protocole

- **Graphe test** : graphe complet SKILLNAV à fin de Sprint 2 (≥ 200 nœuds Skill, ≥ 800 arêtes CO_OCCURS_WITH)
- **Métriques** :
  - **Modularité Q** (Newman) : qualité de partitionnement (plus c'est haut, mieux c'est)
  - **Nombre de communautés détectées**
  - **Runtime**
  - **Stabilité** : 10 runs successifs, mesure du Variation of Information moyen

#### Tableau attendu

| Algorithme | Modularité Q | Nb communautés | Runtime | Stabilité (VI moyen) |
|---|:---:|:---:|:---:|:---:|
| Louvain (greedy modularity) | TBD | TBD | TBD | TBD |
| Label Propagation (asynchrone) | TBD | TBD | TBD | TBD |
| Leiden (résolution = 1.0) | TBD | TBD | TBD | TBD |

#### Choix retenu (cible)

**Louvain** est l'algorithme par défaut du dashboard (équilibre qualité/stabilité). **Leiden** est utilisé comme validateur (réputé plus stable). **Label Propagation** est documenté comme baseline rapide.

**Discussion académique** : Leiden corrige certains défauts de Louvain (communautés mal connectées) — pertinence ici dépend de la densité du graphe.

### N2.3 Forecasting — ARIMA / Prophet / LSTM

#### Protocole

- **Jeu test** : top 10 compétences par PageRank, séries mensuelles sur 12 mois minimum
- **Split** : 9 premiers mois en train, 3 derniers en test
- **Métriques** :
  - **MAPE** (mean absolute percentage error) — métrique principale, robuste aux ordres de grandeur
  - **RMSE** (root mean squared error)
  - **MAE** (mean absolute error)
  - **Runtime d'entraînement**
  - **Intervalle de confiance** (couverture à 95 %)

#### Tableau attendu

| Modèle | MAPE médian (10 skills) | RMSE médian | MAE médian | Runtime médian | Couverture IC 95% |
|---|:---:|:---:|:---:|:---:|:---:|
| ARIMA (auto via AIC) | TBD | TBD | TBD | TBD | TBD |
| Prophet | TBD | TBD | TBD | TBD | TBD |
| LSTM (neuralforecast) | TBD | TBD | TBD | TBD | TBD |

#### Choix retenu (cible)

**Prophet** est probablement le meilleur compromis qualité/explicabilité pour notre cas (séries < 36 mois, saisonnalité modérée). **ARIMA** est documenté comme baseline interprétable. **LSTM** est testé pour démontrer la capacité ML mais peut surpasser ou non Prophet selon la stationnarité.

**Discussion académique** : sur séries courtes (< 24 mois), les modèles statistiques (ARIMA, Prophet) tendent à battre les méthodes deep (LSTM) faute de données d'apprentissage suffisantes — point à confirmer/infirmer empiriquement.

### N2.4 Détection compétences émergentes — Heuristique / XGBoost / KMeans temporel

#### Protocole

- **Jeu de validation** : 30 skills annotés manuellement (émergent / établi / déclinant) — disjoint du jeu d'entraînement XGBoost
- **Métriques** : précision, rappel, F1 par classe, F1 macro, matrice de confusion 3×3

#### Tableau attendu

| Méthode | F1 macro | F1 émergent | F1 établi | F1 déclinant | Interprétabilité |
|---|:---:|:---:|:---:|:---:|:---:|
| Heuristique pondérée | TBD | TBD | TBD | TBD | Très haute |
| XGBoost supervisé | TBD | TBD | TBD | TBD | Haute (feature importance) |
| KMeans temporel | TBD | TBD | TBD | TBD | Moyenne |

#### Choix retenu (cible)

**Heuristique pondérée** comme méthode par défaut (interprétabilité + transparence), **XGBoost** comme amélioration justifiée si les chiffres le valident, **KMeans temporel** comme validation non-supervisée.

### N2.5 Synthèse — page dashboard `/comparative-study`

La page dashboard `/comparative-study` agrège les **quatre** tableaux ci-dessus, avec : (i) métriques chiffrées, (ii) graphique synthétique par tâche, (iii) choix retenu + justification, (iv) lien vers le notebook source. Cette page constitue la **preuve d'évaluation principale** pour le jury.

---

## N3. DATA QUALITY FRAMEWORK

> **Conformité au critère « qualité de la donnée » du sujet. Trois axes : complétude, bruit, biais. Affichage sur dashboard `/quality`.**

### N3.1 Complétude

| Champ Pydantic | % rempli | Seuil cible MVP |
|---|:---:|:---:|
| `title_normalized` | TBD | ≥ 99 % |
| `company` | TBD | ≥ 95 % |
| `country` | TBD | ≥ 99 % |
| `city` | TBD | ≥ 80 % |
| `contract_type` | TBD | ≥ 90 % |
| `seniority` | TBD | ≥ 85 % |
| `skills_required` (≥ 3) | TBD | ≥ 95 % |
| `responsibilities` (≥ 2) | TBD | ≥ 90 % |
| `ml_subdomains` | TBD | ≥ 85 % |
| `frameworks_used` | TBD | ≥ 70 % |
| `salary_min` | TBD | ≥ 30 % (donnée rare) |

Si la complétude est sous le seuil, une note est ajoutée dans le rapport de Data Quality et un disclaimer apparaît sur le dashboard.

### N3.2 Bruit

| Indicateur | Détection | Action |
|---|---|---|
| Doublons exacts | SHA-256 sur `(company + title + location + month)` | Suppression au moment de l'ingestion |
| Quasi-doublons | Cosine similarity titre + description ≥ 0.95 | Fusion (garde la plus récente, log) |
| Outliers (salaires aberrants) | Z-score > 3 par famille IA | Quarantaine, validation manuelle |
| Offres trop courtes | `len(raw_text) < 200` | Rejet, log |
| Offres trop longues | `len(raw_text) > 20 000` | Troncature, log |
| Caractères incohérents | Ratio caractères non-ASCII > 30 % avec lang FR/EN détecté | Re-detect lang, requalifier |

### N3.3 Biais

| Type de biais | Métrique | Visualisation |
|---|---|---|
| **Langue** | Ratio FR / EN / autres | Pie chart `/quality` |
| **Géographie** | Ratio Maroc / France / US / autres | Carte ou bar chart |
| **Taille employeur** | Distribution TPE / PME / ETI / GE | Histogram |
| **Sectoriel** | Top 10 secteurs représentés | Bar chart |
| **Plateforme source** | Ratio Rekrute / LinkedIn / Indeed / ... | Pie chart |
| **Genre lexical** | Présence de termes genrés (« il », « le candidat ») par offre | Histogram + alerte si > 60 % masculin |

**Disclaimer méthodologique** : tout biais détecté est rendu **visible** dans le rapport L5 et sur le dashboard — la transparence est la mesure de mitigation principale en cadre académique. Aucune correction n'est tentée en MVP (resampling, pondération) pour ne pas masquer les biais réels du marché observé.

### N3.4 Couverture temporelle

Le pipeline collecte des offres sur une fenêtre glissante. Le rapport indique : date min, date max, distribution mensuelle, mois sous-représentés (« attention : mois 2026-03 sous-représenté avec 8 offres seulement, à exclure des forecasts »).

### N3.5 Page dashboard `/quality`

```
┌─────────────────────────────────────────────────────┐
│  DATA QUALITY — SKILLNAV MVP                         │
│                                                      │
│  ┌──────────────────┬──────────────────┐             │
│  │ Volume total     │ Période couverte │             │
│  │ 1 247 offres     │ Jan – Mai 2026   │             │
│  └──────────────────┴──────────────────┘             │
│                                                      │
│  COMPLÉTUDE PAR CHAMP    [bar chart % rempli]        │
│  BRUIT                   [doublons supprimés: 87]    │
│  BIAIS LANGUE FR/EN      [pie chart 62 / 38 %]       │
│  BIAIS GÉOGRAPHIQUE      [bar MA 42 % / FR 30 %...]  │
│  COUVERTURE TEMPORELLE   [line chart offres/mois]    │
└─────────────────────────────────────────────────────┘
```

---

## N4. RGPD, ROBOTS.TXT ET ANONYMISATION

> **Section CRITIQUE pour l'évaluation. Voir aussi le document distinct `docs/RGPD_DPIA.md`.**

### N4.1 Base légale

SKILLNAV opère sous la base légale de **l'intérêt légitime** (RGPD art. 6.1.f), justifiée par :

- Finalité scientifique et académique (M242 ENSA-Tétouan, soutenance, rapport méthodologique)
- Pas de profilage de personnes physiques
- Données collectées : **uniquement des offres d'emploi publiques** (descriptions de postes, exigences de compétences, employeurs déclarés)
- Données **jamais** collectées : noms candidats, emails contacts RH, numéros de téléphone, photos, données personnelles sensibles

### N4.2 DPIA simplifiée

Voir document détaillé `docs/RGPD_DPIA.md`. Synthèse :

| Question DPIA | Réponse |
|---|---|
| Finalité du traitement | Recherche académique : observatoire compétences IA |
| Données traitées | Offres d'emploi publiques : titre, description, employeur (entité juridique), localisation, exigences |
| Données **exclues** | Toute donnée personnelle de candidat ou de contact RH |
| Sous-traitants | Anthropic (Claude API — DPA disponible), HuggingFace (modèles open source — inférence locale possible), MongoDB Atlas, Neo4j Aura, Elastic Cloud, Vercel, Apify, Firecrawl |
| Durée conservation | `raw_html` ≤ 6 mois ; `extracted_jobs` ≤ 24 mois ; logs ≤ 3 mois |
| Mesures techniques | TLS 1.2+ sur toutes les connexions DB ; secrets dans `.env` non versionné ; user-agent identifié |
| Droits personnes concernées | Droit d'opposition par email — traitement < 30 jours |

### N4.3 Robots.txt — protocole strict

```python
import urllib.robotparser

def check_robots(url: str, user_agent: str = "SkillnavBot/1.0") -> bool:
    """Retourne True si le scraping est autorisé."""
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{base_url(url)}/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)
```

**Règles strictes** :

- Si `Disallow: /` sur le chemin cible → **source désactivée** dans `sources/registry.yaml`
- Si `Crawl-delay: N` → rate limit respecté (jamais inférieur)
- User-Agent : `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)` — identifie clairement l'origine académique
- Log à chaque session : URL `robots.txt`, date lecture, décision (allow / deny)

### N4.4 Rate limiting

| Source | Rate limit |
|---|---|
| Rekrute, EmploiTIC | 5 s / requête (configurable par source) |
| LinkedIn (Apify) | Quota Apify natif (~ 200 / heure / acteur) |
| Indeed, builtin.com, WTTJ | 5 s / requête + respect User-Agent |
| Google Trends | 1 requête / 60 s (politique pytrends) |
| GitHub Trending | 5 s / requête (respect rate limit GitHub) |

### N4.5 Anonymisation des datasets publiés

Lors de l'export vers `data/exports/{date}/`, les transformations suivantes sont appliquées :

| Champ | Transformation |
|---|---|
| `company` si < 10 offres dans le mois | Remplacé par hash SHA-256[0:8] |
| `url` | Domaine conservé, chemin tronqué (`https://www.rekrute.com/.../`) |
| `raw_html` | **Exclu** des exports publics |
| `raw_text` | Tronqué à 500 caractères + ellipsis |
| `city` | Conservé seulement si > 10 offres (sinon `<masked>`) |
| Tous les champs `extraction_*` | Conservés (métadata méthodologique) |

### N4.6 Droit d'opposition

Email dédié : `optout@skillnav.example` (alias vers email Karamo). Procédure documentée :

1. Réception d'une demande mentionnant un domaine entreprise ou une URL d'offre
2. Vérification de la légitimité (entité juridique reconnaissable)
3. Suppression de la collection `extracted_jobs` + index Elasticsearch + nœud Neo4j (cascade)
4. Réponse écrite au demandeur sous 30 jours
5. Log de la suppression dans `data/audit/optout_log.jsonl`

### N4.7 Risque résiduel et mesures de mitigation

| Risque | Niveau | Mitigation |
|---|:---:|---|
| Une offre contient un nom de candidat dans le texte libre | Bas | RE-7 : prompt Pydantic AI instruisant explicitement de ne pas extraire les noms ; revue manuelle quarantaine |
| Profilage indirect d'un employeur petit (< 5 offres) | Moyen | Hashage sous seuil dans exports publics |
| Récupération automatisée pour usage commercial par un tiers | Faible | Datasets publiés sous licence académique non commerciale, mention en README |

---

## 11. UI / UX PAR PHASE

### 11.1 Phase notebook (Sprint 1–2, usage interne binôme)

Les notebooks Jupyter sont l'**outil d'exploration et de validation** avant toute publication sur le dashboard. Ils figurent dans le repository et sont mentionnés dans le rapport L5.

| Notebook | Contenu | Lead |
|---|---|---|
| `00_setup_dev.ipynb` | Connexion DBs + sanity checks | Binôme |
| `01_data_quality.ipynb` | Métriques complétude, bruit, biais (cf. §N3) | Bachirou Konaté |
| `02_ner_comparison.ipynb` | Étude comparative NER + tableaux F1 (cf. §N2.1) | Karamo |
| `03_graph_analysis.ipynb` | PageRank, Louvain, Label Propag., Leiden + tableau (cf. §N2.2) | Bachirou Konaté |
| `04_forecasting_comparison.ipynb` | ARIMA / Prophet / LSTM + tableau (cf. §N2.3) | Karamo |
| `05_dashboard_data_prep.ipynb` | Préparation JSON pré-calculés pour le dashboard | Karamo |

**Conventions** :
- Outputs sauvés dans le notebook (commit avec figures)
- Premier cell : description, auteur, dépendances
- Sections markdown explicatives entre les blocs de code
- Figures Plotly statiques + interactives quand pertinent

### 11.2 Phase dashboard (Sprint 2–3, livrable principal L4)

Le dashboard SKILLNAV est une application Next.js 15 déployée sur Vercel. Il comporte **7 pages principales** + 1 page Data Quality :

| Route | Page | Contenu | Lead |
|---|---|---|---|
| `/` | Overview | KPIs marché IA Maroc + International, top compétences, derniers signaux | Karamo |
| `/skills` | Skills explorer | Tableau filtrable, score émergence, family, growth | Karamo |
| `/graph` | Skill graph | Graphe interactif Neo4j (react-force-graph-2d), filtres communautés Louvain | Karamo (data Neo4j : Bachirou Konaté) |
| `/forecasting` | Forecasting | ARIMA + Prophet + LSTM superposés par skill, MAPE chiffré | Karamo |
| `/ner-explorer` | NER comparison | Texte annoté side-by-side 3 modèles, badges confidence | Karamo |
| `/methodology` | Méthodologie | Texte structuré : 3 axes, sources, RGPD, glossaire | Karamo (contenu : Bachirou Konaté) |
| `/comparative-study` | Comparative study | Tableaux N2.1–N2.4 chiffrés, choix justifiés | Karamo |
| `/quality` | Data Quality | Complétude, bruit, biais (cf. §N3.5) | Karamo (notebook source : Bachirou Konaté) |

### 11.3 Composants UI

Tous les composants UI sont documentés dans la **Charte SKILLNAV** (`docs/CHARTE_GRAPHIQUE_SKILLNAV.md`). Composants critiques :

- `<KPICard>` — KPI hero
- `<SkillBadge>` — 10 variantes couleurs familles IA
- `<EmergingScore>` — barre score émergence
- `<ConfidenceBadge>` — score 0-1 Pydantic AI / Transformers
- `<NERHighlight>` — texte annoté avec entités colorées (cf. Charte §06quater)
- `<SkillGraph>` — graphe force-directed (cf. Charte §06bis)
- `<TimeSeriesChart>` + `<ForecastComparisonChart>` (cf. Charte §06ter)
- `<ComparativeTable>` — tableau étude comparative

### 11.4 Responsive

Cible **desktop** prioritaire (laptop 1280–1920 px). Cible **tablet** acceptable. **Mobile** dégradé (consultation seulement, pas d'exploration interactive). Pas de temps gaspillé en MVP sur mobile-first.

### 11.5 Dark mode par défaut

Toutes les pages s'ouvrent en **dark mode** (Navy 1000) — cohérence avec la charte McKinsey. Toggle dark/light en haut à droite, persisté via `localStorage`.

---

## 12. AUTHENTIFICATION ET RÔLES

**Décision MVP** : **aucune authentification**. Le dashboard est public, en lecture seule.

**Raison** : SKILLNAV est un démonstrateur académique. L'auth introduirait une complexité technique et RGPD non justifiée en 18 jours. Le déploiement Vercel sur un sous-domaine `skillnav.vercel.app` suffit pour la démonstration de soutenance.

**V1.5+ (post-soutenance)** : auth Better Auth si déploiement public skillnav.ma, principalement pour : (i) tracking d'usage (privacy-respectful), (ii) éventuel accès admin pour relances de pipeline.

---

## 13. LIVRABLES

> **Alignement strict sur les 6 livrables imposés par le sujet du Pr. Sassi.**

### 13.1 Tableau de correspondance

| # | Livrable imposé | Forme livrée par SKILLNAV | Section PRD | Owner |
|---|---|---|---|---|
| **L1** | Scripts de collecte documentés | Repo GitHub `skillnav/` avec dossiers `scrapers/`, `pipelines/`, README détaillé | §8, §9 | Karamo |
| **L2** | Base de données hybride | MongoDB Atlas + Neo4j AuraDB + Elasticsearch Cloud, dumps fournis | §7 | Karamo + Bachirou Konaté |
| **L3** | Pipeline IA validé par métriques | Notebook `02_ner_comparison.ipynb` + page `/comparative-study` | §9, §N2.1 | Karamo |
| **L4** | Dashboard interactif | `skillnav.vercel.app` (7 pages + `/quality`) | §11 | Karamo |
| **L5** | Rapport méthodologique | `docs/RAPPORT_METHODOLOGIQUE.md` → PDF (25–40 pages) | dédié, §16, §N1–N4 | Bachirou Konaté |
| **L6** | Présentation soutenance | `docs/PLAN_SOUTENANCE.md` + deck PPTX + démo live | §22 | Bachirou Konaté + Karamo |

### 13.2 Détail L5 — Rapport méthodologique

Document distinct du PRD, format narratif académique :

```
1. Introduction (contexte, problème, contribution)
2. État de l'art (Web Mining, NER, graph mining, forecasting IA skills)
3. Méthodologie
   3.1 Sources et collecte
   3.2 Architecture polyglotte (MongoDB + Neo4j + Elasticsearch)
   3.3 Pipeline Content Mining (Pydantic AI + Transformers)
   3.4 Pipeline Structure Mining (Neo4j + PageRank + Louvain)
   3.5 Pipeline Usage Mining (ARIMA + Prophet + LSTM)
   3.6 Data Quality Framework
   3.7 RGPD et éthique
4. Résultats — Étude comparative
   4.1 NER comparé (tableau N2.1)
   4.2 Communautés comparées (tableau N2.2)
   4.3 Forecasting comparé (tableau N2.3)
   4.4 Émergence comparée (tableau N2.4)
5. Discussion (limites, biais, plans B)
6. Conclusion + perspectives V1.5 / V2
7. Bibliographie (Liu 2011, papiers HF, papiers Louvain/Leiden, OECD/WEF reports)
8. Annexes (schéma Pydantic, ADRs, captures dashboard)
```

Cible : 25–40 pages, généré via Markdown + Pandoc + WeasyPrint. **Auteur principal** : Bachirou Konaté (rédaction intégrale). **Contributions Karamo** : captures dashboard, schémas d'architecture, ADRs, données chiffrées des études comparatives.

### 13.3 Détail L6 — Soutenance

Voir [§22 Plan de soutenance](#22-plan-de-soutenance-25-min). Deck PPTX : 18–22 slides, durée 15 min, démo live 4 min, Q&A 10 min.

---

## 14. STACK TECHNIQUE

### 14.1 Stack consolidée par couche

| Couche | Outil | Version | Justification |
|---|---|---|---|
| **Language** | Python | 3.12 | Compatibilité pydantic-ai, transformers, neuralforecast |
| **Package mgr** | Poetry | 1.8+ | Lockfile reproductible |
| **Web scraping** | Scrapy | 2.11+ | Sources statiques (Rekrute, Indeed, builtin) |
| | Playwright | 1.40+ | Sources JS (EmploiTIC, WTTJ) |
| | Apify MCP | — | LinkedIn — pipeline reproductible et conforme |
| | Firecrawl MCP | — | Pages dynamiques diverses + fallback |
| **Extraction IA** | pydantic-ai | latest | Framework agentique typé |
| | anthropic | latest | Claude SDK officiel |
| | Modèles Claude | sonnet-4-5 + haiku-4-5 | Qualité + coût |
| **NLP** | transformers (HuggingFace) | 4.40+ | NER comparé multilingue |
| | sentence-transformers | 2.7+ | Normalisation taxonomique |
| | spacy | 3.7+ | Tokenization, sentence split |
| | fasttext-langdetect | 1.0+ | Détection de langue |
| **Graph** | neo4j-driver (Python) | 5.20+ | Connexion Neo4j AuraDB |
| | networkx | 3.3+ | Plan B + algos exotiques |
| | python-louvain / igraph | latest | Louvain + Leiden |
| | neo4j-graph-data-science | 2.6+ | PageRank + communautés natifs |
| **Time series** | statsmodels | 0.14+ | ARIMA, statistiques |
| | prophet | 1.1+ | Forecasting Meta |
| | neuralforecast (Nixtla) | latest | LSTM forecasting |
| | pytrends | 4.9+ | Google Trends |
| **Storage** | MongoDB Atlas | Free M0 | Source of truth |
| | Neo4j AuraDB | Free | Graphe |
| | Elasticsearch Cloud | Free 14j | Recherche + agrégations |
| | motor / pymongo | latest | Drivers Mongo |
| **API** | FastAPI | 0.110+ | API typée OpenAPI |
| | uvicorn | 0.27+ | Serveur ASGI |
| **Front** | Next.js | 15 | App router, RSC, fast |
| | TypeScript | 5.4+ | Type safety |
| | Tailwind CSS | v4 | Styling utility |
| | Shadcn/ui | latest | Composants base |
| | TanStack Query | 5+ | Fetch + cache |
| | openapi-typescript | latest | Types depuis OpenAPI |
| **Charts** | Recharts | 2.12+ | KPI cards, lignes |
| | Tremor | 3+ | Dashboards rapides |
| | react-force-graph-2d | latest | Graphe Neo4j |
| | Plotly | latest | Charts complexes |
| **DevOps** | GitHub | — | Repo + CI Actions |
| | Render | Free / starter | API FastAPI |
| | Vercel | Hobby | Front Next.js |
| **Quality** | ruff | 0.4+ | Linter Python |
| | mypy | 1.10+ | Type checker |
| | black | 24+ | Formatter |
| | pytest | 8+ | Tests |

### 14.2 `pyproject.toml` indicatif

```toml
[tool.poetry]
name = "skillnav"
version = "0.1.0"
description = "Skills Navigator — observatoire IA / DS par Web Mining (M242 ENSA-Tetouan)"
authors = ["Karamo Sylla", "Bachirou Konaté"]

[tool.poetry.dependencies]
python = "^3.12"
pydantic = "^2.7"
pydantic-ai = "^0.0.30"
anthropic = "^0.30"
transformers = "^4.40"
sentence-transformers = "^2.7"
torch = "^2.3"
spacy = "^3.7"
scrapy = "^2.11"
playwright = "^1.40"
motor = "^3.4"
neo4j = "^5.20"
networkx = "^3.3"
python-louvain = "^0.16"
igraph = "^0.11"
statsmodels = "^0.14"
prophet = "^1.1"
neuralforecast = "^1.6"
pytrends = "^4.9"
elasticsearch = "^8.13"
fastapi = "^0.110"
uvicorn = "^0.27"
typer = "^0.12"
rich = "^13.7"
beautifulsoup4 = "^4.12"
lxml = "^5.2"

[tool.poetry.group.dev.dependencies]
ruff = "^0.4"
mypy = "^1.10"
black = "^24.4"
pytest = "^8.2"
pytest-asyncio = "^0.23"
jupyter = "^1.0"
plotly = "^5.20"

[tool.poetry.scripts]
skillnav = "skillnav.cli:app"
```

### 14.3 `package.json` indicatif (web/)

```json
{
  "name": "skillnav-web",
  "version": "0.1.0",
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "generate-types": "openapi-typescript http://localhost:8000/openapi.json -o src/lib/api/types.ts"
  },
  "dependencies": {
    "next": "15.0.0",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "@tanstack/react-query": "^5.0.0",
    "recharts": "^2.12.0",
    "@tremor/react": "^3.18.0",
    "react-force-graph-2d": "^1.25.0",
    "react-plotly.js": "^2.6.0",
    "plotly.js": "^2.30.0",
    "lucide-react": "^0.400.0",
    "clsx": "^2.1.0"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "@types/react": "^19.0.0",
    "@types/node": "^20.10.0",
    "tailwindcss": "^4.0.0",
    "openapi-typescript": "^7.0.0"
  }
}
```

---

## 15. ESTIMATION DES COÛTS

### 15.1 Coûts MVP (18 jours)

| Poste | Estimation | Note |
|---|---|---|
| Apify (LinkedIn scraping) | $5–10 | ~ 500 offres LinkedIn |
| Anthropic Claude (extraction) | $10–20 | ~ 2 000 offres × $0.01 |
| MongoDB Atlas | $0 | Free tier M0 (512 MB) |
| Neo4j AuraDB | $0 | Free tier |
| Elastic Cloud | $0 | Free trial 14 jours (couvre la soutenance) |
| Vercel | $0 | Hobby |
| Render | $0–7 | Free tier suffit ; starter $7 si crash repeatedly |
| HuggingFace | $0 | Inférence locale, modèles ouverts |
| GitHub | $0 | Repo privé ou public |
| Domaine `.ma` (optionnel V1.5) | — | Reporté |
| **TOTAL MVP** | **< $50** | |

### 15.2 Coûts V1.5

| Poste | Estimation | Note |
|---|---|---|
| MongoDB Atlas M10 (si volume × 5) | $10–15 / mois | |
| Elastic Cloud Standard | $16 / mois | Si free trial expiré |
| Domaine `skillnav.ma` | ~$30 / an | |
| Anthropic Claude (volume × 5) | $50–100 | |
| **TOTAL mensuel V1.5** | **$80–130 / mois** | Si déploiement permanent |

### 15.3 Plans d'économies

- **Si budget tendu** : reporter Elasticsearch après la soutenance (MongoDB Atlas Search suffit), drop LSTM (ARIMA + Prophet suffisent), volume 500 offres au lieu de 2 000

---

## 16. MÉTHODOLOGIE DE DÉVELOPPEMENT

### 16.1 Approche binôme

- **Repository** : un seul repo GitHub `skillnav/` (privé pendant le dev, public pour soutenance)
- **Branches** : `main` (protégée), branches feature courtes par sprint
- **PR** : peer review systématique entre Karamo et Bachirou Konaté avant merge
- **Convention de commit** : Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`)
- **Communication** : daily 15 min en début de session, weekly retro fin de sprint

### 16.2 Structure du repository

```
skillnav/
├── pyproject.toml
├── README.md
├── CLAUDE.md                       # consignes pour Claude Code
├── .env.example
├── docs/
│   ├── PRD.md
│   ├── CHARTE_GRAPHIQUE_SKILLNAV.md
│   ├── CHARTE_GRAPHIQUE_SKILLNAV.pdf
│   ├── RAPPORT_METHODOLOGIQUE.md   # L5
│   ├── PLAN_SOUTENANCE.md          # L6
│   └── RGPD_DPIA.md
├── skillnav/
│   ├── schemas/                    # Pydantic models (source de vérité)
│   ├── db/
│   │   ├── mongodb/
│   │   ├── neo4j/
│   │   └── elasticsearch/
│   ├── pipelines/
│   │   ├── content_mining/         # NER + Pydantic AI
│   │   ├── structure_mining/       # Graph builder + algos
│   │   └── usage_mining/           # Time series + forecasting
│   ├── scrapers/
│   │   ├── rekrute/
│   │   ├── emploitic/
│   │   ├── apify/
│   │   ├── indeed/
│   │   ├── builtin/
│   │   └── weak_signals/
│   ├── comparative_studies/
│   │   ├── ner.py
│   │   ├── communities.py
│   │   ├── forecasting.py
│   │   └── emerging.py
│   ├── api/                        # FastAPI endpoints
│   └── cli.py                      # commande `skillnav`
├── notebooks/
│   ├── 00_setup_dev.ipynb
│   ├── 01_data_quality.ipynb
│   ├── 02_ner_comparison.ipynb
│   ├── 03_graph_analysis.ipynb
│   ├── 04_forecasting_comparison.ipynb
│   └── 05_dashboard_data_prep.ipynb
├── web/                            # Next.js 15
│   ├── package.json
│   ├── src/
│   │   ├── app/                    # App router pages
│   │   ├── components/
│   │   └── lib/api/types.ts        # généré
├── tests/
│   ├── fixtures/                   # 30 offres gold
│   ├── unit/
│   └── integration/
├── data/
│   ├── raw/                        # JSONL collectés (gitignored)
│   ├── gold_set/                   # annotations manuelles
│   ├── exports/                    # datasets publics
│   └── audit/                      # logs RGPD, optout
└── scripts/
    └── seed_taxonomy.py
```

### 16.3 Conventions de code

- **Python** : `ruff` (lint) + `black` (format) + `mypy` (strict)
- **TypeScript** : `tsc --strict`
- **Tests** : `pytest` avec fixtures sur 30 annonces gold
- **Couverture** : cible ≥ 70 % sur modules `schemas/`, `pipelines/`, `comparative_studies/`

### 16.4 Outillage IA (Claude Code)

Le projet livre :
- `CLAUDE.md` à la racine — consignes pour Claude Code (conventions, structure)
- `.claude/settings.json` — config MCP servers (Apify, Firecrawl, MongoDB)
- Slash commands courts (`/extract-batch`, `/refresh-graph`, `/dashboard-deploy`)

---

## 17. PHASAGE D'IMPLÉMENTATION

### 17.1 Vue d'ensemble — 3 sprints × 6 jours

```
Sprint 1 — Fondations         J1 → J6   (10-16 mai 2026)
Sprint 2 — Cœur Web Mining    J7 → J12  (17-22 mai 2026)
Sprint 3 — Forecasting + Finition J13 → J18 (23-28 mai 2026)
```

### 17.2 Sprint 1 — Fondations (J1–J6)

**Objectif** : finir la documentation, mettre en place les infra DBs, lancer les scrapers, peupler MongoDB ≥ 200 offres.

| Jour | Karamo | Bachirou Konaté |
|---|---|---|
| J1 | PRD finalisé, schémas Pydantic, repo init + Vercel setup | Charte SKILLNAV PDF, plan rapport L5 |
| J2 | MongoDB Atlas + Neo4j Aura + ES setup, drivers configurés + mock dashboard `/` (Tremor + Shadcn) | Lecture sources WEF / OECD / LinkedIn — chapitre 1 état de l'art (rapport L5) |
| J3 | Scrapers Rekrute + EmploiTIC, mock pages `/skills`, `/graph` (données factices) | Schémas Pydantic relus, page `/methodology` rédigée (contenu) |
| J4 | Scrapers Apify LinkedIn + Indeed, API FastAPI squelette + types générés | Charte PDF v2 livrée, démarrage notebook `01_data_quality` |
| J5 | Pydantic AI extraction sur 50 offres test | Notebook `01_data_quality` — tests complétude / bruit |
| J6 | Pipeline ingest stable, 200 offres extraites, page `/quality` shell | Notebook `01_data_quality` finalisé + chapitre 2 méthode (rapport L5) |

**Livrables fin Sprint 1** : MongoDB peuplée ≥ 200 offres extraites, charte PDF livrée, repo init, dashboard skeleton déployé Vercel.

### 17.3 Sprint 2 — Cœur Web Mining (J7–J12)

**Objectif** : pipelines NER + Structure complets, étude comparative NER chiffrée, dashboard `/graph` fonctionnel.

| Jour | Karamo | Bachirou Konaté |
|---|---|---|
| J7 | NER pipeline Transformers (3 modèles) | Graph builder MongoDB → Neo4j |
| J8 | Notebook `02_ner_comparison` + tableau F1 | PageRank + Louvain dans Neo4j |
| J9 | Annotation gold set 30 offres, page `/skills` | Notebook `03_graph_analysis` + tableau modularité |
| J10 | Normalisation sentence-transformers, page `/graph` interactive (react-force-graph-2d) | Label Propag. + Leiden, rédaction chapitres N1 + N2.2 (rapport L5) |
| J11 | Page `/ner-explorer` (composant NERHighlight) | Rédaction §N2.1 NER (rapport L5) + relecture §N3 Data Quality |
| J12 | Polish visuel dashboard, dark mode | Rédaction §N3 Data Quality + §N4 RGPD (rapport L5) |

**Livrables fin Sprint 2** : NER comparatif validé chiffré, Neo4j peuplée, 3 algos communautés comparés, dashboard 4 pages live.

### 17.4 Sprint 3 — Forecasting + Finition (J13–J18)

**Objectif** : pipeline Usage Mining, étude comparative forecasting + émergence, rapport L5 finalisé, deck répété.

| Jour | Karamo | Bachirou Konaté |
|---|---|---|
| J13 | Séries temporelles + ARIMA + Prophet, page `/forecasting` skeleton | Rédaction §N2.3 Forecasting (rapport L5) |
| J14 | LSTM (neuralforecast), page `/forecasting` graphiques superposés | Rédaction §N2.4 Détection émergence + chapitre Résultats (rapport L5) |
| J15 | Notebook `04_forecasting_comparison` + tableau MAPE, page `/comparative-study` (synthèse) | Rédaction Discussion + Conclusion (rapport L5) + deck PPTX 20 slides |
| J16 | Détection émergence (3 méthodes), polish final dashboard + revue accessibilité | Rédaction Annexes + Bibliographie + relecture rapport intégrale |
| J17 | Plans B testés, démo locale `pnpm dev` | Rapport L5 final + génération PDF + répétition 1 |
| J18 | Démo répétée, screenshots HD fallback | Répétition 2 + dry-run technique |

**Veille de soutenance (J17)** : répétition chronométrée 2 fois ; vérification dashboard live ; backup screenshots HD.

### 17.5 Soutenance — J19 (28 mai 2026)

15 min présentation + démo live + 10 min Q&A. Voir [§22](#22-plan-de-soutenance-25-min).

### 17.6 Plans B documentés par sprint

| Sprint | Si dérapage | Plan B |
|---|---|---|
| S1 | Scrapers cassent ou volume insuffisant | MVP « scrape direct → MongoDB sans pipeline complet » + utiliser dataset HuggingFace `jobs` pré-existant en backup |
| S2 | Neo4j AuraDB trop limité ou bug GDS | NetworkX en mémoire pour algos ; pas de Cypher, mais on garde les algos et les figures |
| S3 | LSTM trop long à entraîner | ARIMA + Prophet seulement, mention LSTM « évalué, non retenu pour MVP, raison X » |
| S3 | Dashboard Vercel HS le jour J | Screenshots HD préparés + démo locale `pnpm dev` projetée |

---

## 18. INDICATEURS DE SUCCÈS

### 18.1 KPIs techniques (mesurables sur le pipeline)

| KPI | Cible MVP | Mesure |
|---|:---:|---|
| Volume offres extraites | 500 – 2 000 | `mongo.extracted_jobs.count()` |
| Couverture langues | ≥ 90 % FR + EN | Pie chart `/quality` |
| F1 NER modèle champion | ≥ 0.80 | Notebook `02_ner_comparison` |
| Delta F1 entre modèles | ≥ 3 points | Comparable |
| Modularité Louvain | ≥ 0.40 | Notebook `03_graph_analysis` |
| MAPE forecasting médian | ≤ 15 % | Notebook `04_forecasting_comparison` |
| Couverture tests Python | ≥ 70 % | `pytest --cov` |
| Temps moyen extraction Claude | < 8 s / offre | Logs pipeline |
| Coût pipeline complet | < $50 | Récap §15 |

### 18.2 KPIs académiques (alignés sur les critères du sujet)

| KPI | Cible MVP | Mesure |
|---|:---:|---|
| Couverture des 3 axes Web Mining | ≥ 25 % chacun (code + temps) | §N1.3 |
| Étude comparative chiffrée | 4 comparaisons (NER, communautés, forecasting, émergence) | §N2 |
| 6 livrables prof remis | 6 / 6 | §13 |
| RGPD documentée | DPIA + log optout + protocole robots.txt | §N4 |
| Sources documentées avec TOS reviewed | 100 % | `sources/registry.yaml` |
| Rapport L5 finalisé | 25–40 pages | docs/RAPPORT_METHODOLOGIQUE.md |
| Soutenance répétée | ≥ 2 fois chronométrées | calendrier équipe |

### 18.3 KPIs produit (qualité du dashboard)

| KPI | Cible MVP | Mesure |
|---|:---:|---|
| Pages dashboard livrées | ≥ 7 | URL list |
| Temps de chargement page d'accueil | < 3 s | Lighthouse |
| Accessibilité Lighthouse | ≥ 90 | Lighthouse |
| Responsive desktop + tablet | OK | Tests manuels |
| Dashboard accessible publiquement | URL Vercel live | `curl -I` |
| Lien depuis README | Accessible | README.md |

---

## 19. ROADMAP POST-SOUTENANCE

### 19.1 V1.5 (juin–juillet 2026)

| Initiative | Effort | Valeur |
|---|---|---|
| Article Medium / DataTalks (méthodologie + résultats) | 1 semaine | Visibilité académique + portfolio |
| Fine-tuning CamemBERT sur dataset SKILLNAV (30–50 offres gold annotées) | 2 semaines | Gain F1 attendu +3–5 pts |
| Déploiement public skillnav.ma | 1 semaine | Démonstration permanente |
| Mise à jour mensuelle automatique | 1 semaine | Vivacité de la donnée |
| Open source repository public | 0.5 semaine | Contribution communautaire |

### 19.2 V2 (septembre 2026+)

- Extension géographique : Afrique francophone + Europe complète
- Pipeline live : Celery + APScheduler, scraping hebdomadaire
- Agents prospectifs : Claude Agent SDK pour investigation libre sur métiers émergents
- API publique versionnée
- Partenariats : observatoires académiques, écoles, médias data

---

## 20. CHECKLIST PRÉ-IMPLÉMENTATION

### 20.1 Académique

- [ ] Sujet du Pr. Sassi lu intégralement par chaque membre du binôme
- [ ] PRD validé par les deux auteurs
- [ ] Charte SKILLNAV validée
- [ ] Date de soutenance confirmée
- [ ] Salles / matériel de soutenance vérifiés J-3

### 20.2 Comptes et accès

- [ ] GitHub repo `skillnav/` créé (privé)
- [ ] MongoDB Atlas account + cluster M0 free créé
- [ ] Neo4j AuraDB account + free instance créée
- [ ] Elastic Cloud account + 14-day trial activé
- [ ] Anthropic API key configurée
- [ ] HuggingFace account + token (téléchargement modèles)
- [ ] Apify account + free credits ($5)
- [ ] Firecrawl account (free tier)
- [ ] Vercel account (Hobby)
- [ ] Render account (free)
- [ ] `.env.example` à jour

### 20.3 Préparation technique

- [ ] Python 3.12 + Poetry installés
- [ ] Node 20+ + pnpm installés
- [ ] Playwright browsers installés (`playwright install`)
- [ ] HF models téléchargés en local
- [ ] Schémas Pydantic figés
- [ ] Structure repo créée
- [ ] CI GitHub Actions minimal (lint + tests)

### 20.4 Préparation contenu

- [ ] Liste des 30 offres gold pour annotation NER pré-sélectionnée
- [ ] Sources/registry.yaml rempli avec TOS reviewed
- [ ] Glossaire IA / Web Mining démarré
- [ ] Plan deck soutenance esquissé

### 20.5 Validation pré-dev

- [ ] Premier scrape Rekrute réussi (10 offres)
- [ ] Première extraction Pydantic AI réussie (5 offres)
- [ ] Premier graphe Neo4j peuplé (10 nœuds)
- [ ] Première requête Elasticsearch ok
- [ ] Premier `pnpm dev` Next.js ok
- [ ] OpenAPI → types TS génération réussie

---

## 21. ANNEXES

### 21.1 Glossaire IA / Web Mining

| Terme | Définition |
|---|---|
| **NER** (Named Entity Recognition) | Tâche NLP visant à identifier et catégoriser des entités nommées (personnes, lieux, organisations, compétences) dans un texte |
| **BERT** | Bidirectional Encoder Representations from Transformers — modèle de langage pré-entraîné de Google (2018), base de nombreux dérivés |
| **CamemBERT** | Version française de BERT, fine-tunée sur corpus OSCAR français |
| **DistilBERT** | Version réduite (40 % paramètres en moins) de BERT, 60 % plus rapide, qualité ~97 % du modèle d'origine |
| **PageRank** | Algorithme de centralité de Google (Page & Brin, 1998), calcule l'importance d'un nœud dans un graphe orienté |
| **Louvain** | Algorithme de détection de communautés par modularité (Blondel et al., 2008), greedy hiérarchique |
| **Leiden** | Amélioration de Louvain (Traag et al., 2019) garantissant des communautés bien connectées |
| **Label Propagation** | Algorithme de communautés par propagation de labels (Raghavan et al., 2007), O(m) — très rapide |
| **ARIMA** | AutoRegressive Integrated Moving Average — modèle statistique classique pour séries temporelles univariées |
| **Prophet** | Modèle de forecasting de Meta (Taylor & Letham, 2018), additif (trend + seasonality + holidays) |
| **LSTM** | Long Short-Term Memory — RNN avec mécanisme de portes pour capturer dépendances long terme |
| **Modularité (Q)** | Métrique de qualité de partitionnement d'un graphe (Newman, 2006), Q ∈ [-0.5, 1] |
| **F1-score** | Moyenne harmonique précision/rappel ; F1 = 2·P·R/(P+R) |
| **MAPE** | Mean Absolute Percentage Error — métrique de forecasting normalisée |
| **Embeddings** | Représentation vectorielle dense d'un mot/phrase/document dans un espace continu |
| **Cosine similarity** | Similarité par cosinus entre deux vecteurs ; sim ∈ [-1, 1] |
| **RAG** | Retrieval-Augmented Generation — combinaison récupération + génération LLM |
| **MLOps** | Pratique d'industrialisation du ML (déploiement, monitoring, CI/CD) |

### 21.2 Inspirations méthodologiques

- **Liu, B.** — *Web Data Mining: Exploring Hyperlinks, Contents, and Usage Data* (Springer, 2011) — référence canonique des 3 axes Web Mining
- **Manning, C., Raghavan, P., Schütze, H.** — *Introduction to Information Retrieval* (Cambridge, 2008)
- **Devlin et al. (2018)** — *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding* (NAACL 2019)
- **Blondel, Guillaume, Lambiotte, Lefebvre (2008)** — *Fast unfolding of communities in large networks* (J. Stat. Mech.)
- **Taylor, S. J., Letham, B. (2018)** — *Forecasting at scale* (Prophet) — *American Statistician*
- **Grigorev, A.** — *DataTalks.Club* — méthodologie *Skills/Responsibilities/Use Cases* (transposée ici à l'IA)

### 21.3 Références institutionnelles

- **WEF** — *Future of Jobs Report 2025*
- **OECD** — *AI Skills Outlook 2024*
- **LinkedIn** — *Workforce Report MENA 2025*
- **Stack Overflow** — *Developer Survey 2025*
- **ESCO** (European Skills/Competences/Occupations) — taxonomie de référence
- **HuggingFace** — documentation `transformers`, `datasets`, `evaluate`
- **Neo4j GDS** — documentation algorithmes graphes

### 21.4 ADRs (Architecture Decision Records)

Chaque ADR suit le format : Contexte / Décision / Conséquences.

#### ADR-01 — Pydantic v2 comme source de vérité unique

**Contexte** : Trois stores (Mongo, Neo4j, ES) nécessitent chacun leur sérialisation. Risque de divergence des schémas.

**Décision** : Pydantic v2 définit le schéma central ; trois converters dédiés transforment vers chaque store. Pas de duplication.

**Conséquences** : Refactor cohérent (type-check global). Léger surcoût d'écriture des converters. Avantage net.

#### ADR-02 — Architecture NoSQL polyglotte vs PostgreSQL seul

**Contexte** : Le sujet impose NoSQL. PostgreSQL avec JSON natif + pgvector + pg_search aurait pu couvrir partiellement.

**Décision** : MongoDB + Neo4j + Elasticsearch — chaque store justifié (cf. §7.0). PostgreSQL exclu pour ne pas masquer la démonstration des 3 axes par un store généraliste.

**Conséquences** : Plus de DBs à gérer, plus de complexité opérationnelle. Mais démonstration scientifique solide.

#### ADR-03 — NER comparatif vs un seul modèle

**Contexte** : Un modèle NER mono-lingue ou un seul modèle pourrait suffire fonctionnellement.

**Décision** : Trois modèles comparés (BERT-multi, CamemBERT, DistilBERT). Justifié par l'exigence d'étude comparative du sujet.

**Conséquences** : Plus de code à maintenir. Mais matériel scientifique pour le rapport L5 et la soutenance.

#### ADR-04 — Claude pour extraction structurée vs Transformers locaux

**Contexte** : Faut-il utiliser Claude (cloud) ou des modèles ouverts (local) ?

**Décision** : Claude pour l'**extraction structurée Pydantic** (qualité supérieure) ; Transformers pour la **NER fine-grained** (vitesse + reproductibilité). Dualité documentée en §9.7.

**Conséquences** : Coût Claude (~$10–20 MVP) accepté. RGPD documentée (Anthropic DPA).

#### ADR-05 — Next.js 15 + Tailwind v4 + Shadcn

**Contexte** : Stack front pour le dashboard.

**Décision** : Next.js 15 (App Router, RSC, Turbopack). Tailwind v4 pour styling. Shadcn/ui pour composants base.

**Conséquences** : Stack moderne, performante, cohérente avec la charte McKinsey.

#### ADR-06 — react-force-graph-2d pour le graphe

**Contexte** : Plusieurs librairies graphes possibles (cytoscape, vis-network, d3-force).

**Décision** : `react-force-graph-2d` (Canvas, performant ≥ 1 000 nœuds, intégration React simple).

**Conséquences** : Pas d'algos hiérarchiques avancés (acceptable en MVP). Démo soutenance fluide garantie.

#### ADR-07 — Plotly + Recharts + Tremor — pourquoi trois

**Contexte** : Un seul outil de chart pourrait suffire.

**Décision** : Tremor pour les KPI cards rapides (productivité), Recharts pour les charts standards (line, bar) intégrés React, Plotly pour les charts complexes (treemap, heatmap, 3D scatter).

**Conséquences** : Bundle un peu plus gros. Acceptable.

#### ADR-08 — pas d'authentification en MVP

**Contexte** : Le dashboard pourrait être protégé.

**Décision** : Public, lecture seule, aucune auth en MVP (cf. §12).

**Conséquences** : Risque indexation Google négligeable (sous-domaine Vercel). Pas de tracking utilisateurs. Conformité RGPD simplifiée.

#### ADR-09 — Conventional Commits + branches courtes

**Contexte** : Convention git pour le binôme.

**Décision** : `feat:`, `fix:`, `docs:`, `refactor:` ; branches `feature/{nom-court}` ; merge via PR avec review du binôme.

**Conséquences** : Historique git lisible. Léger overhead de discipline.

#### ADR-10 — Notebooks Jupyter dans le repo (committed avec outputs)

**Contexte** : Faut-il versionner les notebooks avec ou sans outputs ?

**Décision** : **Avec outputs** — les figures de l'étude comparative sont des artefacts du livrable L3.

**Conséquences** : Diffs git lourds sur les notebooks. Convention : 1 commit = 1 cycle de run notebook.

### 21.5 Risques et mitigations (synthèse)

| # | Risque | Niveau | Mitigation |
|---|---|:---:|---|
| R1 | Scrapers cassent (changement HTML) | Moyen | Multi-sources + fallback Firecrawl + 30 % de marge dans les volumes cibles |
| R2 | Quotas API atteints (Claude, Apify) | Moyen | Budget surveillé + plan B Haiku pour réduire les coûts |
| R3 | Free tier DBs saturé | Faible-Moyen | Volumes cibles dimensionnés ; plans B documentés (§7.0) |
| R4 | NER faible qualité sur français | Moyen | 3 modèles testés ; routage par langue |
| R5 | LSTM ne converge pas (données insuffisantes) | Élevé | ARIMA + Prophet en filet de sécurité |
| R6 | Dashboard Vercel HS le jour J | Faible mais critique | Screenshots HD préparés ; démo locale projetable |
| R7 | Désalignement binôme | Moyen | Sections owners (§16.1) + daily 15 min |
| R8 | Sous-estimation rapport L5 | Élevé | Démarrer J7 dès premiers résultats ; cible 25–40 pages |
| R9 | Q&A soutenance sur point faible | Moyen | 15 questions probables préparées (§22.4) ; plan B humble assumé |
| R10 | Découverte RGPD à 48h de la soutenance | Faible | §N4 traitée dès Sprint 1 + document `RGPD_DPIA.md` séparé |

---

## 22. PLAN DE SOUTENANCE 25 MIN

> **Document distinct également exporté en `docs/PLAN_SOUTENANCE.md` pour répétition autonome.**

### 22.1 Format imposé

- **Durée totale** : 25 minutes
- **Présentation** : 15 minutes
- **Démo live** : intégrée dans la présentation
- **Q&A** : 10 minutes

### 22.2 Structure minute par minute (15 min présentation)

| Minute | Section | Contenu | Lead |
|:---:|---|---|:---:|
| M0–M1 | Ouverture | Titre, équipe, contexte M242, objectif soutenance | Karamo |
| M1–M2 | Sujet imposé + 3 axes | Reformulation sujet + tableau couverture 3 axes (§N1.2) | Karamo |
| M2–M4 | Architecture polyglotte | Schéma global + justification MongoDB + Neo4j + ES (§7.0) | Karamo |
| M4–M5 | Stack technique | Tableau §14 condensé + 3 décisions clés (ADR-02, ADR-03, ADR-04) | Karamo |
| M5–M9 | Démo live dashboard | `skillnav.vercel.app` — pages `/`, `/graph`, `/forecasting`, `/ner-explorer`, `/comparative-study` | Karamo |
| M9–M12 | Résultats étude comparative | 4 tableaux chiffrés (N2.1–N2.4) + interprétation | Karamo |
| M12–M13 | Data Quality + biais reconnus | Page `/quality` + transparence biais | Bachirou Konaté |
| M13–M14 | RGPD + robots.txt | Base légale + protocole + DPIA disponible | Bachirou Konaté |
| M14–M15 | Conclusion + roadmap | 6 livrables remis + roadmap V1.5 / V2 | Bachirou Konaté |

### 22.3 Démo live — script précis (4 minutes inclus)

1. **Page `/`** : pointer KPIs marché IA Maroc + International, volume 1 247 offres, top 5 compétences (15 s)
2. **Page `/graph`** : zoom sur cluster « NLP », montrer communauté Louvain colorée, hover top 5 PageRank (60 s)
3. **Page `/forecasting`** : sélectionner « Transformers » → afficher ARIMA + Prophet + LSTM superposés, lire MAPE chiffré (60 s)
4. **Page `/ner-explorer`** : afficher une offre annotée, basculer BERT-multi → CamemBERT → DistilBERT, montrer entités différentes (60 s)
5. **Page `/comparative-study`** : montrer les 4 tableaux récapitulatifs synthétiques (45 s)

**Plan B démo HS** : projeter `web/screenshots/{page}.png` (HD préparés) + verbaliser.

### 22.4 Q&A — 15 questions probables avec éléments de réponse

| # | Question probable | Élément de réponse clé |
|---|---|---|
| 1 | Pourquoi 3 DBs au lieu d'une seule ? | §7.0 : chaque store justifié, plans B documentés ; PostgreSQL aurait masqué la démo des 3 axes |
| 2 | Comment garantir la reproductibilité ? | MongoDB = source of truth, Neo4j et ES rederivables ; Pydantic figé ; modèles HF versionnés ; notebooks commités |
| 3 | Pourquoi 3 modèles NER au lieu d'un seul ? | Exigence d'étude comparative + routage par langue gain F1 réel |
| 4 | Quel volume de données ? Est-ce suffisant ? | 500–2 000 offres MVP ; suffisant pour démontrer 3 axes ; V1.5 monte à 10 000 |
| 5 | Biais reconnus ? | §N3.3 : langue (FR + EN), géographie (déséquilibre Maroc/International), employeurs taille variable. Affichés sur `/quality` |
| 6 | Pourquoi Claude (cloud) si on a Transformers locaux ? | §9.7 : Claude pour extraction structurée, Transformers pour NER fine ; complémentarité documentée |
| 7 | Pourquoi Louvain plutôt que Leiden ? | Comparés (§N2.2). Louvain retenu pour MVP + Leiden comme validateur. Pas idéologique, basé sur métriques |
| 8 | RGPD ? Données candidats ? | §N4 : aucune donnée candidat collectée, base légale art. 6.1.f, DPIA document séparé |
| 9 | Que se passe-t-il si Apify casse ? | Plan B : Firecrawl + sources statiques (Rekrute, Indeed, builtin) ; 200 offres LinkedIn maxi en MVP |
| 10 | Comment validez-vous le forecast ? | Train/test split 9-3 mois, MAPE médian sur top 10 skills, intervalles de confiance affichés |
| 11 | Différence avec LinkedIn Talent Insights ? | §1.5 : méthodologie ouverte, étude comparative reproductible, cible académique vs commerciale |
| 12 | Article 22 RGPD (décision automatisée) ? | Pas de décision automatisée individuelle ; analyse agrégée seulement (skills, marchés) |
| 13 | Combien de temps le pipeline complet ? | ~ 60 min pour 500 offres (extraction Claude limitante). Documenté §9.6 |
| 14 | Que feriez-vous différemment ? | Plus de gold set pour XGBoost, fine-tuner CamemBERT en V1.5, élargir géo |
| 15 | Pourquoi 18 jours seulement ? | Calendrier imposé M242. Plans B documentés ; cible MVP démontrable, pas V1 commerciale |

### 22.5 Répartition orale binôme

- **Karamo** prend M0–M12 (contexte, architecture, stack, démo live dashboard, résultats étude comparative)
- **Bachirou Konaté** prend M12–M15 (Data Quality, RGPD, conclusion + roadmap)
- Q&A : Karamo répond aux questions architecture / IA / dashboard / pipelines ; Bachirou Konaté aux questions méthodologie / Data Quality / RGPD / Structure Mining (Neo4j, communautés)

### 22.6 Répétitions

- **J17 (J-1)** : répétition 1 chronométrée à voix haute, avec mesures
- **J17 soir** : répétition 2, plan B démo testé
- **J18 (J-0) matin** : dry-run technique (projection, son, batterie, internet, dashboard live, fallback screenshots)

### 22.7 Matériel à apporter

- 2 laptops chargés (Karamo + Bachirou Konaté)
- Dongles HDMI / USB-C
- Clé USB avec backup (PDF + screenshots + repo zip)
- Document `PLAN_SOUTENANCE.md` imprimé
- Eau, papier, stylos

---

## ANNEXE RACI — Répartition Karamo / Bachirou Konaté

### Définitions RACI

- **R** = Responsible (fait le travail)
- **A** = Accountable (rend compte, valide)
- **C** = Consulted (consulté avant décision)
- **I** = Informed (informé du résultat)

### Matrice par section PRD

| Section PRD | Karamo | Bachirou Konaté |
|---|:---:|:---:|
| §0 Contexte académique | A R | C |
| §1 Contexte stratégique | A R | C |
| §2 Vision | C | A R |
| §3 Personas | A R | C |
| §4 Parcours utilisateur | R | A R |
| §5 Fonctionnalités | R | A R |
| §6 Architecture | A R | R |
| §7 Données NoSQL | A R | C |
| §8 Sources | A R | I |
| §9 Pipeline IA | A R | I |
| §10 Règles métier | R | A R |
| §11 UI/UX | A R | C |
| §12 Auth | A R | I |
| §13 Livrables | A | A |
| §14 Stack | A R | C |
| §15 Coûts | A R | I |
| §16 Méthodologie | A R | C |
| §17 Phasage | A R | A R |
| §18 KPIs | A R | C |
| §19 Roadmap | C | A R |
| §20 Checklist | A | A |
| §21 Annexes | A R | C |
| §22 Soutenance | C | A R |
| §N1 Mapping 3 axes | A R | R |
| §N2 Étude comparative | A R | R |
| §N3 Data Quality | C | A R |
| §N4 RGPD | A R | I |

### Matrice par livrable prof

| Livrable | Karamo | Bachirou Konaté |
|---|:---:|:---:|
| L1 — Scripts collecte | A R | I |
| L2 — Base hybride | A R | R |
| L3 — Pipeline IA validé | A R | C |
| L4 — Dashboard | A R | C |
| L5 — Rapport méthodologique | C | A R |
| L6 — Présentation | R | A R |

### Matrice par sprint

| Sprint | Karamo focus | Bachirou Konaté focus |
|---|---|---|
| S1 (J1–J6) | DBs, scrapers, schémas Pydantic, pipeline ingestion + extraction, **dashboard skeleton + Vercel** | Charte PDF, **notebook `01_data_quality`**, plan + chapitres 1–2 du rapport L5 |
| S2 (J7–J12) | NER + tableau F1, normalisation, **pages `/ner-explorer` + `/graph` + `/skills`**, dark mode | Graph builder, PageRank, Louvain, Leiden, **rédaction §N1 + §N2.1 + §N2.2 + §N3 + §N4** du rapport L5 |
| S3 (J13–J18) | Forecasting (ARIMA + Prophet + LSTM), **pages `/forecasting` + `/comparative-study`**, polish, démo | **Rapport L5 final (PDF)** + deck PPTX + répétitions |

---

**Référence officielle — SKILLNAV PRD v2.0**
Projet académique M242 — ENSA-Tétouan · Karamo Sylla & Bachirou Konaté · Mai 2026
