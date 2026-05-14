# PRD COMPLET — OCTAO

> **Observatoire des Compétences et Métiers d'Afrique de l'Ouest**
>
> **Version** : 1.2 — Collecte pilotée par Claude Code + MCP (Apify, Firecrawl)
> **Statut** : Validé — Prêt à implémenter
> **Date** : Mai 2026
> **Produit** : SYLI Technology
> **Auteur** : Karamo Sylla
> **Cible politique principale V1** : Dre Diaka Sidibé, Ministre de l'Enseignement Supérieur et de la Recherche Scientifique, République de Guinée

---

## CHANGELOG

### v1.1 → v1.2 (Mai 2026) — Collecte pilotée par Claude Code

| Changement | Détail |
|------------|--------|
| **Scraping abandonné côté Python** | Les scrapers Python orchestrés (Crawl4AI / Firecrawl SDK / Apify SDK avec `octao scrape`) sont remplacés par une collecte pilotée depuis Claude Code via les MCP servers Apify et Firecrawl. L'analyste copie-colle des prompts en langage naturel, source par source, et Claude Code persiste les données brutes en DB Neon |
| **Catalogue de prompts en annexe** | Le PRD intègre désormais un catalogue de prompts prêts à l'emploi (Annexe A) — un prompt par source (job board guinéen, page carrière entreprise, ONG, LinkedIn via Apify). Chaque prompt est dimensionné pour produire un fichier `data/raw/{source}_{date}.jsonl` ingérable par le pipeline Python d'extraction |
| **Pipeline Python recentré sur l'extraction** | Le code Python conserve : extraction Pydantic AI, normalisation taxonomique, ghost skills, génération PDF/PPTX/DOCX, exports GitHub. Il perd toute la couche scraping. Gain : ~40 % de code en moins, dépendances Crawl4AI / Apify SDK / Firecrawl SDK retirées |
| **Stack MCP officialisée** | Apify MCP et Firecrawl MCP deviennent des dépendances de premier plan, configurées dans `.claude/settings.json` du projet. Le setup Claude Code (CLAUDE.md + sous-agents + slash commands) est livré avec le projet |
| **Phasage V1 raccourci** | V1 passe de 3-4 semaines à 2-3 semaines — le scraping ne nécessite plus de développer 5 scrapers Python, juste de rédiger les prompts et de tester la connexion MCP |

### v1.0 → v1.1 (Mai 2026)

| Changement | Détail |
|------------|--------|
| **V1 mode local** | V1 abandonne l'infra live (Render + Celery + APScheduler) au profit de scripts CLI Python + Jupyter notebooks exécutés localement par l'analyste. Gain : time-to-market divisé par 2, coûts divisés par 2 |
| **Stack frontend hybride V2+** | V1 sans frontend (Jupyter suffit pour l'analyste) ; V2 introduit Next.js 15 + Shadcn + Better Auth comme dashboard premium et portail universités |
| **Architecture Option 3 confirmée** | Aucun accès direct à PostgreSQL depuis Next.js. Toute la communication passe par l'API FastAPI typée OpenAPI (apparaît en V2). Type-safety end-to-end via codegen `openapi-typescript` |
| **Framework IA = Pydantic AI** | Confirmé pour V1 et V2. Claude Agent SDK introduit en V3 uniquement pour les tâches agentiques prospectives (recherche métiers d'avenir) |
| **DB Neon dès V1** | Plutôt que SQLite local — pour permettre le partage entre toi et tes futurs collaborateurs AI5D, et éviter une migration plus tard |
| **Suppression de Streamlit** | V1 utilise Jupyter pour l'exploration analytique ; V2 passe directement à Next.js. Gain : pas de double effort UI |
| **Phasage révisé** | V1 = 3-4 semaines (au lieu de 6). V2 = 6-7 semaines (intègre Next.js + FastAPI). V3 = 8-10 semaines (inchangé) |
| **Coûts V1** | ~$15-20/mois (au lieu de ~$30) |

### v0.1 → v1.0 (rappel)

| Changement | Détail |
|------------|--------|
| Repositionnement multi-secteurs | OCTAO couvre TOUS les métiers (santé, droit, gestion, ingénierie, agro, éducation, etc.) |
| Repositionnement outil interne | Pas de dashboard public — outil interne produisant des livrables |
| Marque produit | OCTAO = premier produit B2G de SYLI Technology (AI5D opérateur initial) |
| 13 familles de métiers définies | Taxonomie macro de référence |
| 5 enrichissements méthodologiques Alexey Grigorev | Skills + responsibilities + use cases, Reality vs Curriculum, Job Type, transparence radicale, open data GitHub |
| Vision V1/V2/V3 affinée | Miroir intérieur (Guinée) → régional (UEMOA) → mondial (métiers d'avenir) |

---

## TABLE DES MATIÈRES

1. [Contexte stratégique](#1-contexte-stratégique)
2. [Vision produit](#2-vision-produit)
3. [Audience et personas](#3-audience-et-personas)
4. [Parcours utilisateur](#4-parcours-utilisateur)
5. [Fonctionnalités V1 → V2 → V3](#5-fonctionnalités-v1--v2--v3)
6. [Architecture technique](#6-architecture-technique)
7. [Architecture des données](#7-architecture-des-données)
8. [Sources de données](#8-sources-de-données)
9. [Pipeline d'extraction IA (Pydantic AI)](#9-pipeline-dextraction-ia-pydantic-ai)
10. [Règles métier](#10-règles-métier)
11. [UI/UX par phase (Jupyter V1, Next.js V2+)](#11-uiux-par-phase)
12. [Authentification et rôles](#12-authentification-et-rôles)
13. [Livrables politiques](#13-livrables-politiques)
14. [Stack technique](#14-stack-technique)
15. [Estimation des coûts](#15-estimation-des-coûts)
16. [Méthodologie de développement](#16-méthodologie-de-développement)
17. [Phasage d'implémentation](#17-phasage-dimplémentation)
18. [Indicateurs de succès](#18-indicateurs-de-succès)
19. [Roadmap V2+](#19-roadmap-v2)
20. [Checklist pré-implémentation](#20-checklist-pré-implémentation)
21. [Annexes](#annexes)

---

## 1. CONTEXTE STRATÉGIQUE

### 1.1 Genèse — la réforme MPS-30 du MESRS

Le 27 avril 2026, le Ministère de l'Enseignement Supérieur et de la Recherche Scientifique de la République de Guinée a officiellement lancé deux mégaprojets structurants dans le cadre du Programme Simandou 2040 :

- **MPS-30** : Projet de Cartographie des compétences et besoins métiers sur le marché du travail et intégration de ces données à un système d'information dynamique
- **MPS-32** : Projet de Révision des contenus pédagogiques afin de les aligner avec les besoins identifiés du marché du travail

Ces deux projets sont indissociables : le MPS-30 mesure ce que veut l'économie guinéenne, le MPS-32 adapte les programmes universitaires en conséquence. La ministre Diaka Sidibé a explicitement formulé la philosophie : « réformer des programmes sans mesurer leur impact sur l'insertion des diplômés serait avancer à l'aveugle ».

Pour piloter cette réforme, 51 équipes encadrées par 8 comités scientifiques travaillent pendant 5 mois (avril-septembre 2026) à concrétiser ces projets.

### 1.2 Diagnostic posé par le MESRS

Les chiffres officiels présentés par la ministre Sidibé sont sans appel :

- **48 institutions** d'enseignement supérieur en Guinée
- **Plus de 15 000 diplômés** produits chaque année
- **Seulement 30,96%** d'entre eux ont un emploi 12 mois après la fin de leurs études
- Une situation qualifiée d'« inacceptable » et d'« inadéquation structurelle » entre formation et emploi

### 1.3 Le problème politique à résoudre

Aujourd'hui, le MESRS guinéen ne dispose d'aucun **instrument de mesure objectif** lui permettant de répondre à des questions critiques pour piloter ses arbitrages :

| Question stratégique | Données disponibles aujourd'hui |
|---|---|
| Quels métiers les entreprises guinéennes recherchent-elles réellement ? | Aucune |
| Quelles compétences sont systématiquement exigées dans chaque secteur ? | Aucune |
| Quels diplômes/niveaux d'études sont demandés ? | Aucune |
| Où sont les écarts les plus criants entre les programmes universitaires et les besoins réels ? | Intuitions et anecdotes |
| Comment la Guinée se compare-t-elle à ses voisins UEMOA ? | Aucune |
| Quels métiers émergents la Guinée doit-elle anticiper pour 2030-2040 ? | Aucune |

Sans ces données, **chaque arbitrage budgétaire et pédagogique est arbitraire**. Le MPS-30 vise précisément à combler ce vide. **OCTAO se positionne comme l'outil opérationnel qui permet de produire ces données dès maintenant**, en avance sur les 5 mois de travail des 51 équipes officielles.

### 1.4 L'opportunité stratégique

Le contexte est unique : la ministre cherche activement des contributions techniques pour structurer la cartographie. Disposer d'un outil et d'un livrable opérationnel **avant que les 51 équipes ne produisent leurs propres résultats** crée une fenêtre stratégique exceptionnelle pour :

- Établir un standard méthodologique de référence
- Devenir un contributeur technique reconnu de la réforme
- Positionner SYLI Technology comme acteur B2G de référence sur l'enseignement supérieur en Afrique de l'Ouest
- Ouvrir un parcours de contribution pluriannuel auprès du MESRS et des ministères équivalents UEMOA

### 1.5 Positionnement OCTAO

> **OCTAO est un instrument d'intelligence économique et pédagogique conçu pour les décideurs publics et académiques d'Afrique de l'Ouest francophone. Il cartographie en continu le marché de l'emploi pour révéler les écarts entre la formation universitaire et les besoins réels de l'économie.**

OCTAO se distingue de toutes les approches existantes :

| Approche existante | Limite | Réponse OCTAO |
|---|---|---|
| Études manuelles cabinets de conseil | Coûteuses, datées, biais déclaratif | Données réelles, mises à jour régulièrement |
| Statistiques INS / observatoires officiels | Décalées (3-5 ans), peu granulaires | Données fraîches, granularité métier/compétence |
| Sondages employeurs | Biais déclaratif, taux de réponse faible | Observation directe des annonces publiées |
| Plateformes internationales (LinkedIn Talent Insights) | Inexistantes en Guinée, prix prohibitifs | Approche locale, gratuite pour l'État |

### 1.6 Vision long terme — l'escalier V1/V2/V3

OCTAO n'est pas un outil monolithique. C'est un **escalier de crédibilité politique** structuré en trois versions, chacune apportant un angle d'analyse différent à la même question fondamentale : « comment aligner la formation universitaire guinéenne sur les besoins de l'économie ? »

```
┌──────────────────────────────────────────────────────────────────┐
│  V1 — MIROIR INTÉRIEUR (mode LOCAL)                              │
│  Géographie : Guinée                                             │
│  Mode opératoire : Collecte pilotée Claude Code (MCP Apify       │
│                    + Firecrawl) → extraction Python (Pydantic AI)│
│                    → notebooks Jupyter pour QC et exploration    │
│  Question : "Que demande NOTRE marché aujourd'hui ?"             │
│  Sources : Sites d'emploi guinéens + ONG locales + grands employ.│
│  Méthode : Prompts en langage naturel, source par source         │
│  Livrable : État des lieux du marché de l'emploi national        │
│  Audience : Ministre Sidibé (cabinet, MESRS)                     │
│                                                                  │
│  → Argument politique : "Voici ce qu'il manque dans la formation │
│    universitaire pour répondre aux besoins des entreprises       │
│    présentes en Guinée."                                         │
└──────────────────────────────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  V2 — MIROIR RÉGIONAL (passage en LIVE)                          │
│  Géographie : + Sénégal, Côte d'Ivoire, Mali (cœur UEMOA)        │
│  Mode opératoire : FastAPI + Next.js dashboard + portail univ.   │
│  Question : "Comment se positionne la Guinée par rapport à ses   │
│              voisins directs ?"                                  │
│  Sources : Sites d'emploi régionaux + LinkedIn (Apify)           │
│  Méthode : Scraping élargi + analyses comparatives               │
│  Livrable : Benchmark régional Guinée vs UEMOA                   │
│  Audience : Ministre + ministres UEMOA (MESRS Sénégal, CI, Mali) │
│                                                                  │
│  → Argument politique : "La Guinée est en retard de X années sur │
│    l'écosystème data du Sénégal — voici comment combler le gap." │
└──────────────────────────────────────────────────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  V3 — MIROIR MONDIAL (PRODUCTION + AGENTS IA)                    │
│  Géographie : Top pays africains + références internationales    │
│  Mode opératoire : Pipeline Celery + agents Claude Agent SDK     │
│                    pour la recherche prospective                 │
│  Question : "Quels métiers d'avenir la Guinée doit-elle intégrer │
│              dans ses cursus pour préparer 2030-2040 ?"          │
│  Sources : LinkedIn international, Indeed, builtin.com, etc.     │
│  Méthode : Approche inspirée Alexey Grigorev + investigation     │
│            agentique sur métiers émergents                       │
│  Livrable : Rapport "Métiers d'avenir 2030 — Implications pour   │
│             l'enseignement supérieur guinéen" (100-150 pages)    │
│  Audience : Ministre + Présidence + bailleurs (BM, BAD, AFD)     │
│                                                                  │
│  → Argument politique : "Voici les métiers que la Guinée doit    │
│    intégrer dans son programme Simandou 2040 dès maintenant pour │
│    être compétitive en 2040."                                    │
└──────────────────────────────────────────────────────────────────┘
```

Cette progression crée un **parcours narratif politique sur 12 mois** :

| Mois | Version | Pitch à la ministre |
|---|---|---|
| Mois 1-2 | V1 livrée | « Madame, voici ce qui se passe dans VOTRE pays » |
| Mois 4-5 | V2 livrée | « Madame, voici comment la Guinée se compare à ses VOISINS » |
| Mois 9-10 | V3 livrée | « Madame, voici les métiers du FUTUR que la Guinée doit anticiper » |

### 1.7 Inscription dans Simandou 2040

OCTAO s'inscrit naturellement dans le **Pilier 2 du Programme Simandou 2040** (Capital humain et Attractivité), doté de 49 milliards USD sur l'enveloppe globale de 200 milliards. Sa vocation prospective (V3) en fait un instrument de pilotage adapté à l'horizon 2040 du programme.

---

## 2. VISION PRODUIT

### 2.1 Mission OCTAO

> **Donner aux décideurs publics et académiques d'Afrique de l'Ouest francophone un instrument d'intelligence économique permettant d'aligner la formation universitaire sur les besoins réels et émergents du marché de l'emploi — par la donnée, l'analyse continue et la transparence méthodologique.**

### 2.2 Trois principes fondateurs

| # | Principe | Conséquence concrète |
|---|---|---|
| 1 | **Données réelles, jamais déclaratives** | Aucun sondage ; extraction directe d'annonces publiées par les employeurs |
| 2 | **Multi-secteurs par défaut** | Tous les métiers, toutes les filières — pas de biais sectoriel |
| 3 | **Transparence méthodologique radicale** | Méthodologie publiée, datasets ouverts sur GitHub, chaque chiffre traçable jusqu'à l'annonce source |

### 2.3 Différenciation par version

| Dimension | V1 (LOCAL) | V2 (LIVE) | V3 (PRODUCTION + AGENTS) |
|---|---|---|---|
| Géographie | 🇬🇳 Guinée | + 🇸🇳 🇨🇮 🇲🇱 (UEMOA) | + Top Afrique + International |
| Volume offres analysées (cible) | 800-1 500 / mois | 3 000-5 000 / mois | 15 000-30 000 / mois |
| Mode d'exécution | Scripts CLI + Jupyter local | Pipeline FastAPI + Next.js | Pipeline live Celery + agents IA |
| Algorithme phare | Cartographie + ghost skills | Benchmark régional | **Métiers d'avenir** |
| Livrable principal | Rapport État du marché Guinée 2026 | Rapport Benchmark UEMOA 2026 | Rapport Métiers d'avenir 2030 |
| Audience principale | Ministre + cabinet MESRS | Ministres UEMOA + doyens | Présidence + bailleurs |

### 2.4 Promesses politiques par cible

**Pour la ministre de l'Enseignement Supérieur (Guinée puis UEMOA)** :
> « Vous allez enfin pouvoir piloter vos arbitrages pédagogiques sur des données réelles, non sur des intuitions. Vous saurez quels cursus créer, lesquels renforcer, lesquels fermer. »

**Pour les doyens d'université** :
> « Vous saurez exactement quelles compétences ajouter à vos programmes pour que vos diplômés soient employables, et où vos étudiants trouvent un emploi après leur diplôme. »

**Pour la Présidence et les bailleurs internationaux (V3)** :
> « Vous avez la photographie objective des métiers d'avenir sur lesquels investir dans le cadre de Simandou 2040 — un alignement pédagogique-économique mesurable et défendable internationalement. »

### 2.5 Anti-positionnement

OCTAO n'est délibérément PAS :

- ❌ Un job board (pas d'agrégation d'offres pour les candidats)
- ❌ Un service de matching candidats-employeurs
- ❌ Une plateforme grand public destinée à la recherche d'emploi individuelle
- ❌ Un outil de marketing RH pour les entreprises
- ❌ Un produit SaaS public concurrent de LinkedIn ou Indeed

OCTAO **utilise les annonces** comme matière première statistique, mais sa mission est uniquement l'**aide à la décision pédagogique et politique**.

---

## 3. AUDIENCE ET PERSONAS

### 3.1 Persona principal V1 — Dre Diaka Sidibé

| Dimension | Description |
|---|---|
| **Rôle** | Ministre de l'Enseignement Supérieur et de la Recherche Scientifique |
| **Contexte** | Pilote la réforme MPS-30/MPS-32 dans le cadre de Simandou 2040 |
| **Pression politique** | Doit produire des résultats visibles dans 5 mois (51 équipes mobilisées) |
| **Contraintes** | Agenda surchargé, doit défendre ses arbitrages devant la Présidence |
| **Niveau technique** | Non-technicien — attend de la donnée digérée, lisible, défendable |
| **Format préféré** | Documents PDF lisibles, présentations claires, chiffres mémorables |
| **Critère d'adoption** | Crédibilité scientifique + utilité politique immédiate |
| **Phrase qu'elle veut pouvoir dire en conseil des ministres** | « Selon la cartographie OCTAO, X% des entreprises guinéennes recherchent Y compétences que nos cursus ne forment pas » |

**Ce qu'elle ne veut PAS** : un dashboard à explorer elle-même, des données brutes sans interprétation, des recommandations vagues.

### 3.2 Persona secondaire V1 — Conseiller technique du MESRS

| Dimension | Description |
|---|---|
| **Rôle** | Conseiller au cabinet, ou Directeur Général de l'Enseignement Supérieur |
| **Contexte** | Prépare les notes pour la ministre, instruit les dossiers |
| **Niveau technique** | Cadre supérieur — peut lire un rapport de 30 pages, comprend les nuances |
| **Critère d'adoption** | Méthodologie défendable + données granulaires + comparabilité dans le temps |
| **Format préféré** | Rapport approfondi avec annexes méthodologiques + datasets exportables |

### 3.3 Persona V2 — Doyens et responsables de filière universitaire

| Dimension | Description |
|---|---|
| **Rôle** | Doyens d'UFR, responsables de filière, directeurs d'école |
| **Institution cible** | UGANC, ISSEG, ISIM, UTG, UMLK et autres établissements top 10 |
| **Contexte** | Doivent justifier l'évolution de leurs maquettes pédagogiques |
| **Niveau technique** | Académique — confortable avec données et statistiques |
| **Critère d'adoption** | Données spécifiques à leur filière + comparaison avec les besoins du marché |
| **Format préféré** | Portail web léger filtrable par institution + rapports filière |

### 3.4 Persona V3 — Stratèges de la planification nationale

| Dimension | Description |
|---|---|
| **Rôle** | Délégation Simandou, Ministère du Plan, conseillers Présidence |
| **Contexte** | Pilotent Simandou 2040 sur 15 ans |
| **Niveau technique** | Hauts cadres — manient les références internationales (BAD, BM, OCDE) |
| **Critère d'adoption** | Vision prospective + standards internationaux + projections |
| **Format préféré** | Rapport stratégique 100-150 pages + executive summary |

### 3.5 Persona interne — Analyste OCTAO (toi + équipe AI5D)

| Dimension | Description |
|---|---|
| **Rôle** | Analyste data + responsable production des livrables |
| **Niveau technique** | Confirmé Python, SQL, Jupyter, prompt engineering |
| **Besoin principal V1** | Scripts CLI rapides + notebooks Jupyter pour explorer les données |
| **Besoin principal V2+** | Dashboard Next.js + portail multi-utilisateurs |
| **Format préféré V1** | Notebooks Jupyter avec visualisations Plotly + accès direct à la DB Neon |

### 3.6 Cartographie des besoins par persona

| Besoin | Ministre | Conseiller | Doyen | Stratège | Analyste |
|---|:---:|:---:|:---:|:---:|:---:|
| Synthèse exécutive | ✅✅✅ | ✅ | ✅ | ✅✅✅ | — |
| Rapport approfondi | ✅ | ✅✅✅ | ✅✅ | ✅✅✅ | — |
| Données filière-spécifiques | ✅ | ✅✅ | ✅✅✅ | ✅ | ✅✅ |
| Comparaisons régionales | — | ✅ | ✅ | ✅✅✅ | ✅ |
| Métiers d'avenir | — | ✅ | ✅✅ | ✅✅✅ | ✅✅ |
| Datasets exportables | — | ✅ | ✅ | ✅✅ | ✅✅✅ |
| Dashboard exploratoire | — | — | ✅ | — | ✅✅✅ |
| Méthodologie détaillée | — | ✅✅ | ✅ | ✅✅ | ✅✅✅ |

---
## 4. PARCOURS UTILISATEUR

### 4.1 Parcours interne V1 — Analyste OCTAO (toi, en mode local)

C'est le parcours le plus important à optimiser puisque c'est celui qui s'exécute en boucle pour produire les livrables. **En V1, tout se passe sur ton MacBook**.

```
┌─────────────────────────────────────────────────────────────────┐
│  LUNDI MATIN — Tu démarres ta semaine OCTAO sur ton Mac         │
│  Tu ouvres VS Code dans le dossier ~/projects/octao             │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 — Collecte (Claude Code + MCP Apify/Firecrawl)         │
│  Tu ouvres Claude Code dans ~/projects/octao                    │
│                                                                 │
│  → Tu copies-colles successivement les prompts du catalogue     │
│    (Annexe A du PRD) — un prompt par source :                   │
│      Prompt 01 : EmploiGuinee.com                               │
│      Prompt 02 : 224jobs.com                                    │
│      Prompt 03 : LinkedIn Guinée (via Apify)                    │
│      Prompt 04 : PNUD / UNICEF / OMS                            │
│      Prompt 05 : Pages carrières mines/banques/télécoms         │
│      ... etc.                                                   │
│  → Claude Code utilise Firecrawl MCP / Apify MCP pour fetch     │
│  → Chaque prompt produit data/raw/{source}_{date}.jsonl         │
│  → Persistence en DB Neon via $ poetry run octao ingest         │
│  Durée : ~30-60 minutes pour ~500 offres (toi en pilote actif)  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 — Extraction IA (CLI)                                  │
│  $ poetry run octao extract --batch=last --confidence-min=0.75  │
│                                                                 │
│  → Le script appelle Pydantic AI + Claude Sonnet 4.5            │
│  → Progress bar avec rich (1/500, 2/500...)                     │
│  → Quarantaine automatique offres confidence < 0.75             │
│  Durée : ~30-60 minutes pour 500 offres                         │
│  Coût : ~5-10€ Claude API                                       │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 — Quality Control (Notebook)                           │
│  Tu ouvres notebooks/01_quality_control.ipynb                   │
│                                                                 │
│  → Cellule 1 : nb offres scrapées vs semaine précédente         │
│  → Cellule 2 : sources qui ont échoué                           │
│  → Cellule 3 : distribution des confidences                     │
│  → Cellule 4 : offres en quarantaine à vérifier                 │
│  Durée : 10-15 minutes                                          │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 4 — Taxonomy Review (CLI)                                │
│  $ poetry run octao taxonomy review                             │
│                                                                 │
│  → Affiche les nouveaux skills/tools détectés                   │
│  → Mode interactif : valider [V] / mapper [M] / rejeter [R]     │
│  → Mise à jour de la taxonomie en DB                            │
│  Durée : 15-20 minutes                                          │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 5 — Exploration (Notebook)                               │
│  Tu ouvres notebooks/02_insights_exploration.ipynb              │
│                                                                 │
│  → Top métiers de la semaine                                    │
│  → Évolution mois sur mois                                      │
│  → Compétences ghost émergentes                                 │
│  → Visualisations Plotly                                        │
│  → Identification des storylines pour le prochain rapport       │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 6 — Génération de livrables (CLI)                        │
│  $ poetry run octao report --type=synthesis --period=30d        │
│  $ poetry run octao report --type=deep --period=30d             │
│  $ poetry run octao deck --period=30d                           │
│  $ poetry run octao briefing --period=30d                       │
│                                                                 │
│  → Génère PDF synthèse 4p + PDF approfondi 25-30p +             │
│    PPTX deck 15-20 slides + DOCX briefing 4p                    │
│  → Stockage local dans output/2026-05-04/                       │
│  Durée : 5-10 minutes                                           │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 7 — Export datasets ouverts (CLI)                        │
│  $ poetry run octao export --month=2026-05 --push-github        │
│                                                                 │
│  → Génère JSON Lines + CSV anonymisés                           │
│  → Push automatique sur syli-technology/octao-datasets          │
│  → Met à jour le README et le notebook Jupyter d'analyse        │
│  Durée : 5 minutes                                              │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 8 — Envoi des livrables                                  │
│  Tu envoies par email au cabinet ministériel :                  │
│   - Note de briefing 4p (DOCX)                                  │
│   - Lien vers rapport approfondi (Google Drive ou similaire)    │
│   - Lien vers datasets GitHub                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Moment AHA principal pour l'analyste V1** : voir apparaître en quelques minutes une compétence ghost détectée par l'algorithme, et pouvoir générer en 2 minutes un PDF qui la contextualise pour la ministre. **Pas besoin d'infra live, pas besoin de dashboard — juste des outils Python qui s'enchaînent proprement.**

### 4.2 Parcours interne V2+ — Analyste OCTAO (mode dashboard Next.js)

À partir de V2, le parcours évolue vers une UI premium :

```
Login Better Auth sur dashboard.octao.africa
   ↓
Dashboard global (KPIs en temps réel depuis API FastAPI)
   ↓
Navigation par onglets (Insights, Ghost Skills, Reports, etc.)
   ↓
Bouton "Générer rapport" → appel à l'API → PDF disponible en téléchargement
```

Mais le **moteur reste identique** : Python + Pydantic AI + Claude. Seule l'UI change.

### 4.3 Parcours décideur — Ministre Sidibé (consommatrice de livrables)

```
Cabinet reçoit l'email de Karamo Sylla / SYLI Technology
avec en pièce jointe note briefing 4p + lien rapport approfondi
   ↓
Conseiller technique lit la note de briefing en 5 minutes
   ↓
Conseiller prépare une note interne 1 page pour la ministre
   ↓
La ministre lit en 90 secondes pendant un trajet en voiture
   ↓
Si intérêt → Demande de rendez-vous avec Karamo
   ↓
Si validation politique → Premier contrat / convention SYLI Technology
```

### 4.4 Parcours bénéficiaire V2 — Doyen d'université

```
Doyen reçoit invitation par email (magic link Better Auth)
   ↓
Connexion au portail (login restreint sur whitelist .edu)
   ↓
Sélection de son institution + sa filière
   ↓
Consultation des données spécifiques :
   - Top métiers occupés par les diplômés de cette filière
   - Compétences exigées non couvertes par le cursus
   - Comparaison avec institutions équivalentes UEMOA
   ↓
Téléchargement du rapport filière personnalisé (PDF)
```

### 4.5 Parcours stratège national V3

```
Le Délégué Simandou reçoit le rapport "Métiers d'avenir 2030"
   ↓
Lecture de l'executive summary (5 pages)
   ↓
Identification des 3-5 recommandations stratégiques majeures
   ↓
Inscription à l'agenda d'un comité de pilotage Simandou
   ↓
Décision d'allouer un budget pour la création de nouvelles filières
```

---

## 5. FONCTIONNALITÉS V1 → V2 → V3

### 5.1 Tableau de phasage des fonctionnalités

| # | Fonctionnalité | V1 (LOCAL) | V2 (LIVE) | V3 (PROD+AGENTS) |
|---|---|:---:|:---:|:---:|
| F01 | Catalogue de prompts de collecte Guinée (Claude Code + MCP Apify/Firecrawl) | ✅ | ✅ | ✅ |
| F01b | CLI `octao ingest` — ingestion JSONL → DB Neon | ✅ | ✅ | ✅ |
| F02 | Catalogue de prompts UEMOA (Sénégal, CI, Mali) | — | ✅ | ✅ |
| F03 | Catalogue de prompts internationaux (top Afrique + monde) | — | — | ✅ |
| F04 | Extraction IA Pydantic AI (skills + responsibilities + use cases) | ✅ | ✅ | ✅ |
| F05 | Normalisation taxonomique avec aliases | ✅ | ✅ | ✅ |
| F06 | Classification automatique par 13 familles de métiers | ✅ | ✅ | ✅ |
| F07 | Notebooks Jupyter exploratoires (Insights, QC, Trends) | ✅ | ✅ | ✅ |
| F08 | Dashboard Next.js — vue Guinée | — | ✅ | ✅ |
| F09 | Dashboard Next.js — vue régionale UEMOA | — | ✅ | ✅ |
| F10 | Dashboard Next.js — vue internationale | — | — | ✅ |
| F11 | Algorithme « Compétences ghost » (Reality vs Curriculum) | ✅ | ✅ | ✅ |
| F12 | Algorithme « Métiers d'avenir » | — | — | ✅ |
| F13 | Comparaisons régionales et benchmarks | — | ✅ | ✅ |
| F14 | Génération rapport PDF synthèse 4 pages (CLI puis dashboard) | ✅ | ✅ | ✅ |
| F15 | Génération rapport PDF approfondi 25-30 pages | ✅ | ✅ | ✅ |
| F16 | Génération rapport PDF prospectif 100-150 pages | — | — | ✅ |
| F17 | Export deck de présentation 15-20 slides (PPTX) | ✅ | ✅ | ✅ |
| F18 | Export note de briefing 4 pages (DOCX) | ✅ | ✅ | ✅ |
| F19 | Export datasets JSON/CSV pour GitHub | ✅ | ✅ | ✅ |
| F20 | Page méthodologie publique | — | ✅ | ✅ |
| F21 | API REST FastAPI typée OpenAPI | — | ✅ | ✅ |
| F22 | Auth Better Auth (V1 interne + V2 portail) | — | ✅ | ✅ |
| F23 | Quality Control (notebook V1, dashboard V2) | ✅ | ✅ | ✅ |
| F24 | Taxonomy Review (CLI V1, dashboard V2) | ✅ | ✅ | ✅ |
| F25 | Portail universités (accès restreint par institution) | — | ✅ | ✅ |
| F26 | API privée pour ministères/bailleurs | — | — | ✅ (étude) |
| F27 | Pipeline live (Celery + APScheduler) | — | — | ✅ |
| F28 | Agents prospectifs (Claude Agent SDK) | — | — | ✅ |
| F29 | Système d'alertes hebdomadaires | — | ✅ | ✅ |

### 5.2 V1 — Détail des fonctionnalités prioritaires

#### F01 — Catalogue de prompts de collecte (Claude Code + MCP Apify/Firecrawl)

**Description :** L'analyste ouvre Claude Code dans le dossier projet et copie-colle des prompts en langage naturel — un prompt par source. Claude Code utilise les MCP servers Apify et Firecrawl pour récupérer les données, puis écrit le résultat dans `data/raw/{source}_{date}.jsonl`. **Aucun scraper Python n'est codé pour V1.**

**Pourquoi ce choix :**
- Time-to-value immédiat : pas de scraper Python à coder, déboguer, maintenir
- Adaptabilité : si une source change de structure HTML, on adapte le prompt en 30 secondes
- Traçabilité : chaque collecte produit un transcript Claude Code archivable
- Coût : Apify (~3-5€/mois Guinée) + Firecrawl (free tier suffisant V1)

**Workflow type pour une session de collecte :**

```
1. Ouvrir Claude Code dans ~/projects/octao
2. Copier le Prompt 01 du catalogue (Annexe A)
3. Coller dans Claude Code → exécution Firecrawl MCP / Apify MCP
4. Vérifier le résultat dans data/raw/emploiguinee_2026-05-06.jsonl
5. Passer au Prompt 02, 03, ... jusqu'à épuisement du catalogue
6. Lancer $ poetry run octao ingest data/raw/*.jsonl
   → ingestion en table job_offer_raw de la DB Neon
```

**Acceptance criteria :**
- Le catalogue couvre les 5 catégories de sources Guinée (cf. §8.1)
- Chaque prompt produit un fichier JSONL au format normalisé (cf. F01b)
- Une session complète Guinée (toutes sources) prend moins de 60 minutes en mode actif
- Aucune dépendance Python liée au scraping dans `pyproject.toml`

#### F01b — CLI `octao ingest` (ingestion JSONL → DB Neon)

**Description :** Petit utilitaire Python (Typer) qui lit les fichiers JSONL produits par Claude Code et insère les offres brutes dans la table `job_offer_raw` de Neon, avec déduplication par hash d'URL canonique.

**Commande :**

```bash
# Ingère tous les fichiers JSONL d'aujourd'hui
poetry run octao ingest data/raw/*.jsonl

# Mode dry-run : compte les offres sans écrire en DB
poetry run octao ingest data/raw/*.jsonl --dry-run

# Ingère un seul fichier
poetry run octao ingest data/raw/linkedin_2026-05-06.jsonl
```

**Acceptance criteria :**
- Déduplication par `hash(url_canonical)` — réingérer un fichier = no-op
- Logs : nb offres lues / insérées / dédupliquées par fichier
- Validation Pydantic du schéma JSONL avant insertion (rejette les lignes malformées)

#### F04 — Extraction IA Pydantic AI

**Description :** Pour chaque offre brute non encore traitée, Pydantic AI + Claude API extrait un objet structuré contenant 3 niveaux d'information : skills required, responsibilities, use cases.

**Schéma de sortie Pydantic (JSON validé) :**

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class JobExtraction(BaseModel):
    title: str = Field(..., description="Titre normalisé du poste")
    company: str = Field(..., description="Nom de l'entreprise tel quel")
    company_size_estimate: Literal["TPE", "PME", "ETI", "GE", "Unknown"]
    sector: str = Field(..., description="Secteur, mappé sur taxonomie Sector")

    country: str = Field(..., min_length=2, max_length=2)
    city: Optional[str] = None
    contract_type: Literal["CDI", "CDD", "Stage", "Alternance", "Freelance", "Autre"]
    remote_type: Literal["On-site", "Hybrid", "Remote", "Unspecified"]

    seniority: Literal["Débutant", "Junior", "Confirmé", "Senior", "Expert", "Direction"]
    education_required: Optional[str] = None
    experience_years_min: Optional[int] = None
    experience_years_max: Optional[int] = None

    skills_required: List[str] = Field(..., min_length=3, max_length=20)
    responsibilities: List[str] = Field(..., min_length=2, max_length=10)
    use_cases: List[str] = Field(default_factory=list, max_length=5)

    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None

    role_family: Literal[
        "Santé", "Droit & Conformité", "Gestion & Management",
        "Finance & Comptabilité", "Marketing & Commerce",
        "Ingénierie & Technique", "IT & Numérique", "RH & Formation",
        "Agriculture & Agroalimentaire", "Éducation & Recherche",
        "Social & Humanitaire", "Logistique & Supply Chain",
        "Support & Service"
    ]
    job_type: Literal["Tech-Core", "Tech-Adjacent", "Tech-Enabled", "Non-Tech"]

    extraction_confidence: float = Field(..., ge=0.0, le=1.0)
    extraction_notes: Optional[str] = None
```

**Modèles utilisés :**
- **Claude Sonnet 4.5** pour l'extraction principale (qualité maximale)
- **Claude Haiku 4.5** pour la normalisation taxonomique secondaire (rapide, moins cher)

**Acceptance criteria :**
- Confidence ≥ 0.75 sur ≥ 90% des offres traitées
- Temps moyen d'extraction < 8 secondes par offre
- Coût total extraction < 15€ pour 1000 offres

#### F07 — Notebooks Jupyter exploratoires

**Liste des notebooks :**

```
notebooks/
├── 00_setup_dev.ipynb              # Bootstrap connection DB + tests
├── 01_quality_control.ipynb        # Vérifs hebdo : sources, confidence, errors
├── 02_insights_exploration.ipynb   # Top métiers/skills/tools, exploration libre
├── 03_ghost_skills_analysis.ipynb  # Algorithme + visualisations ghost
├── 04_taxonomy_review.ipynb        # Validation des nouveaux skills/tools
├── 05_reports_preview.ipynb        # Aperçu des rapports avant génération
└── 06_datasets_export.ipynb        # Préparation des exports GitHub
```

#### F11 — Algorithme « Compétences ghost »

**Formule :**

```
ghost_score = (frequency_in_market × 0.5)
            + (growth_rate_3m × 0.3)
            - (presence_in_known_curricula × 0.2)

Une compétence est marquée "ghost" si :
   ghost_score > 0.7
   AND occurrences ≥ 5 dans le marché
```

**Implémentation :** module Python `app/algorithms/ghost_skills.py`, exécutable depuis CLI ou notebook.

#### F14 + F15 — Génération de rapports PDF (CLI)

**Commande CLI :**

```bash
poetry run octao report --type=synthesis --period=30d --country=GN
poetry run octao report --type=deep --period=30d --country=GN --output=output/2026-05/
```

**Stack technique :**
- Templates HTML avec Jinja2
- Conversion HTML → PDF avec WeasyPrint
- Charte graphique OCTAO appliquée
- Visualisations Plotly converties en PNG embarqués

**Rapport synthèse 4 pages :**
- Page 1 : Couverture + 5 chiffres clés du marché
- Page 2 : Top 10 métiers les plus recherchés en Guinée
- Page 3 : Top 5 compétences ghost prioritaires
- Page 4 : 3 recommandations actionnables + appel à approfondir

#### F19 — Export datasets JSON/CSV pour GitHub

**Commande CLI :**

```bash
poetry run octao export --month=2026-05 --push-github
```

**Format des fichiers générés :**
- `2026-05-guinea-jobs.jsonl` : offres complètes anonymisées
- `2026-05-guinea-skills.csv` : agrégat skills par fréquence
- `2026-05-guinea-roles.csv` : agrégat roles par fréquence
- `2026-05-methodology.md` : méthodologie de cette extraction
- `notebook-analysis.ipynb` : notebook Jupyter d'exemple d'analyse
- `README.md` : mise à jour automatique avec dernières stats

### 5.3 V2 — Élargissement régional + introduction du LIVE

V2 marque le passage en **mode live** avec FastAPI + Next.js. Les fonctionnalités V1 restent **toutes accessibles** (CLI + notebooks), mais s'enrichissent :

- **F02** : Pipelines scraping Sénégal, Côte d'Ivoire, Mali
- **F08-F09** : Dashboards Next.js premium
- **F13** : Module benchmark régional automatique
- **F20** : Page méthodologie publique sur `octao.africa/methode`
- **F21** : API REST FastAPI typée OpenAPI
- **F22** : Auth Better Auth
- **F25** : Portail universités à accès restreint
- **F29** : Système d'alertes hebdomadaires par email (Resend)

### 5.4 V3 — Standards internationaux + métiers d'avenir + agents IA

#### F12 — Algorithme « Métiers d'avenir »

```
metier_avenir_score =
    (presence_marches_matures × 0.35)
  + (croissance_12_mois × 0.30)
  + (presence_secteurs_tech_strategiques × 0.20)
  - (presence_marche_guineen × 0.15)

Si metier_avenir_score > 0.65
   AND occurrences_marches_matures ≥ 50
   AND presence_marche_guineen < 5%
   → "Métier d'avenir prioritaire pour la Guinée" 🚀
```

#### F28 — Agents prospectifs (Claude Agent SDK)

V3 introduit Claude Agent SDK **uniquement** pour les tâches **vraiment agentiques** :
- Investigation libre sur un métier émergent
- Synthèse multi-sources hétérogènes
- Comparaison de tendances entre marchés

**Pydantic AI reste pour l'extraction** des offres individuelles. Claude Agent SDK arrive **en complément**, pas en remplacement.

---

## 6. ARCHITECTURE TECHNIQUE

### 6.1 Diagramme général V1 (mode local)

V1 est intentionnellement minimaliste. **Tout tourne sur ton MacBook**, sauf la base de données (Neon cloud, partageable).

```
   ┌──────────────────────────────────────┐
   │  TON MAC (MacBook Karamo)            │
   │                                      │
   │  ┌────────────────────────────────┐  │
   │  │  Claude Code (collecte)        │  │
   │  │  MCP servers :                 │  │
   │  │   - Apify MCP (LinkedIn etc.)  │  │
   │  │   - Firecrawl MCP (sites web)  │  │
   │  │   - Postgres MCP (lecture DB)  │  │
   │  │  Catalogue de prompts (PRD §A) │  │
   │  │   → data/raw/{source}.jsonl    │  │
   │  └────────────┬───────────────────┘  │
   │               │                      │
   │  ┌────────────▼───────────────────┐  │
   │  │  CLI Python (octao)            │  │
   │  │  Commands :                    │  │
   │  │   - octao ingest               │  │
   │  │   - octao extract              │  │
   │  │   - octao taxonomy review      │  │
   │  │   - octao report               │  │
   │  │   - octao deck                 │  │
   │  │   - octao briefing             │  │
   │  │   - octao export               │  │
   │  └────────────┬───────────────────┘  │
   │               │                      │
   │  ┌────────────▼───────────────────┐  │
   │  │  Modules Python                │  │
   │  │   - ingest/ (JSONL → Neon)     │  │
   │  │   - extraction/ (Pydantic AI   │  │
   │  │      + Claude API)             │  │
   │  │   - normalization/             │  │
   │  │   - algorithms/ (ghost skills) │  │
   │  │   - reports/ (WeasyPrint,      │  │
   │  │      python-docx, pptx)        │  │
   │  │   - exports/ (GitHub publisher)│  │
   │  └────────────┬───────────────────┘  │
   │               │                      │
   │  ┌────────────▼───────────────────┐  │
   │  │  Jupyter Lab                   │  │
   │  │   - notebooks/ (analyse)       │  │
   │  │   - Plotly + Pandas            │  │
   │  │   - SQLAlchemy                 │  │
   │  └────────────┬───────────────────┘  │
   │               │                      │
   │  ┌────────────▼───────────────────┐  │
   │  │  output/                       │  │
   │  │   - rapports PDF générés       │  │
   │  │   - decks PPTX                 │  │
   │  │   - briefings DOCX             │  │
   │  │   - datasets JSON/CSV          │  │
   │  └────────────────────────────────┘  │
   │                                      │
   └────────┬─────────────────────────────┘
            │ asyncpg (TLS)
            ▼
   ┌──────────────────────────────────────┐
   │  PostgreSQL (Neon Cloud Frankfurt)   │
   │  - Free tier (3 GB suffisant V1)     │
   │  - Tables OCTAO + materialized views │
   │  - Branching pour expérimentation    │
   └──────────────────────────────────────┘
            ▲
            │ asyncpg (TLS) — accès partagé en lecture
            │
   ┌────────┴─────────────────────────────┐
   │  MAC futur collaborateur AI5D        │
   │  (lecture seule depuis notebooks)    │
   └──────────────────────────────────────┘


   ┌──────────────────────────────────────┐
   │  GitHub                              │
   │  - syli-technology/octao-app (privé) │
   │  - syli-technology/octao-datasets    │
   │    (public, push depuis CLI)         │
   └──────────────────────────────────────┘

   ┌──────────────────────────────────────┐
   │  APIs externes                       │
   │  - Anthropic API (Claude Sonnet 4.5  │
   │    + Haiku) pour extraction          │
   │  - Apify (LinkedIn scraping)         │
   │  - Firecrawl (sites JS)              │
   └──────────────────────────────────────┘
```

**Lecture rapide :** zéro infra cloud "live" en V1. La seule dépendance cloud = Neon (gratuit) + APIs externes (pay-as-you-go). Pas de Render, pas de Vercel, pas de Celery.

### 6.2 Diagramme général V2 (passage en LIVE hybride)

V2 introduit l'API FastAPI et le frontend Next.js. **Le moteur Python V1 reste identique** — on ajoute juste une couche d'exposition.

```
                    ┌─────────────────────────────┐
                    │  ANALYSTE (toi + équipe)    │
                    │  Toujours scripts CLI       │
                    │  + notebooks Jupyter        │
                    │  pour les tâches batch      │
                    └──────────────┬──────────────┘
                                   │ accès direct DB
                                   ▼
   ┌─────────────────────────────────────────────────────────┐
   │  PostgreSQL (Neon Frankfurt)                            │
   │  Schéma partagé, source unique de vérité                │
   └────────────────────────────┬────────────────────────────┘
                                ▲
                                │ SQL (asyncpg)
                                │
                ┌───────────────┴───────────────┐
                │                               │
   ┌────────────▼─────────────┐   ┌─────────────▼─────────────┐
   │  CLI Python + Jupyter    │   │  FastAPI (Render)         │
   │  (jobs batch comme V1)   │   │  - REST API typée OpenAPI │
   │   - Scrapers             │   │  - Endpoints /api/*       │
   │   - Extraction           │   │  - JWT internal auth      │
   │   - Génération PDF/DOCX  │   │  - Hosted Frankfurt       │
   └──────────────────────────┘   └─────────────┬─────────────┘
                                                │ HTTPS REST
                                                │ (types via openapi-typescript)
                                                ▼
                                  ┌─────────────────────────────┐
                                  │  Next.js 15 (Vercel)        │
                                  │  - Dashboard interne (V2)   │
                                  │  - Portail universités (V2) │
                                  │  - Better Auth              │
                                  │  - Shadcn + Tailwind v4     │
                                  │  - TanStack Query           │
                                  └──────────────┬──────────────┘
                                                 ▲
                          ┌──────────────────────┼──────────────────────┐
                          │                                             │
                ┌─────────┴─────────┐                          ┌────────┴─────────┐
                │  Toi + équipe     │                          │  Doyens (V2)     │
                │  AI5D             │                          │  Magic links     │
                │  Sessions Better  │                          │  Better Auth     │
                │  Auth             │                          │                  │
                └───────────────────┘                          └──────────────────┘
```

### 6.3 Diagramme général V3 (PRODUCTION + agents)

V3 ajoute le **pipeline live** (Celery + APScheduler) et les **agents prospectifs** (Claude Agent SDK) au pipeline V2.

```
   ┌──────────────────────────────────────┐
   │  APScheduler (Render)                │
   │  Cron : Lundi 03h00 UTC              │
   └──────────────┬───────────────────────┘
                  │ trigger
                  ▼
   ┌──────────────────────────────────────┐
   │  Celery Workers (Render)             │
   │  - Scraping multi-pays               │
   │  - Extraction Pydantic AI batch      │
   │  - Recalcul agrégats                 │
   └──────────────┬───────────────────────┘
                  │
                  ▼
   ┌──────────────────────────────────────┐
   │  PostgreSQL Neon (Scale tier)        │
   └──────────────────────────────────────┘
                  ▲
                  │
   ┌──────────────┴───────────────────────┐
   │  Agents prospectifs (Claude Agent    │
   │  SDK) — déclenchés à la demande      │
   │  pour V3 :                           │
   │   - Investigation métiers émergents  │
   │   - Synthèses multi-sources          │
   │   - Comparaisons de tendances        │
   │  Lancés depuis CLI ou dashboard V3   │
   └──────────────────────────────────────┘
```

### 6.4 Process de collecte — Claude Code + MCP (V1)

**Principe** : V1 abandonne tout scraper Python. La collecte est pilotée depuis **Claude Code** via deux serveurs MCP, en mode prompt-driven.

| Outil | MCP server | Sources cibles V1 | Coût |
|---|---|---|---|
| **Firecrawl** | `firecrawl-mcp` | Sites web simples + JS (job boards Guinée, ONG, pages carrières mines/banques/télécoms, sites institutionnels publics) | 0–5 €/mois (free tier souvent suffisant) |
| **Apify** | `@apify/actors-mcp-server` | LinkedIn (filtre Guinée), plateformes verrouillées | ~3–5 €/mois |
| **Postgres** | `postgres-mcp` (optionnel) | Lecture de l'état DB depuis Claude Code (offres déjà collectées, dédoublonnage en amont) | 0 € |

**Workflow type — session de collecte hebdomadaire :**

```
1. L'analyste ouvre Claude Code dans ~/projects/octao
2. Il copie successivement les prompts du catalogue Annexe A
   (un prompt = une source)
3. Pour chaque prompt :
     a. Claude Code interprète le prompt
     b. Claude Code appelle Firecrawl MCP ou Apify MCP
     c. Claude Code normalise la réponse au schéma JSONL OCTAO
     d. Claude Code écrit data/raw/{source}_{YYYY-MM-DD}.jsonl
4. À la fin de la session :
     $ poetry run octao ingest data/raw/*.jsonl
   → insertion en table job_offer_raw de Neon, dédoublonnage par
     hash d'URL canonique
5. Pipeline classique reprend la main :
     $ poetry run octao extract --batch=last
     $ poetry run octao report ...
```

**Schéma JSONL de référence (sortie Claude Code, entrée `octao ingest`) :**

```jsonl
{"source":"emploiguinee","collected_at":"2026-05-06T08:30:00Z","url":"https://www.emploiguinee.com/offres/123","title":"Ingénieur génie civil","company":"SMB-Winning","location":"Conakry, Guinée","contract_type":"CDI","posted_at":"2026-05-04","raw_html":"<div>...</div>","raw_text":"Description complète..."}
{"source":"emploiguinee","collected_at":"2026-05-06T08:30:00Z","url":"https://www.emploiguinee.com/offres/124","title":"Comptable senior","company":"Ecobank Guinée","location":"Conakry","contract_type":"CDI","posted_at":"2026-05-05","raw_html":"...","raw_text":"..."}
```

**Champs obligatoires** : `source`, `collected_at` (ISO 8601 UTC), `url`, `title`, `raw_text`. Tous les autres sont optionnels — l'extraction Pydantic AI les retrouvera dans `raw_text`.

**Pourquoi cette architecture (par rapport à des scrapers Python codés)** :

| Critère | Scrapers Python (ancien V1) | Claude Code + MCP (V1.2) |
|---|---|---|
| Time to first data | 1-2 semaines (coder 5 scrapers) | 1-2 jours (rédiger les prompts) |
| Maintenance si HTML change | Refactoriser le scraper | Ajuster une phrase du prompt |
| Volume de code projet | ~3 000 lignes scrapers + tests | 0 ligne scraper Python |
| Lisibilité de la collecte | Code spécialisé | Prompts en français, lisibles par tous |
| Coût récurrent | Infra orchestrator | Abonnements Apify + Firecrawl identiques |
| Dépendance forte | Crawl4AI, Apify SDK, Firecrawl SDK | Apify MCP + Firecrawl MCP |

**Limites assumées** :
- L'analyste doit être présent pendant la collecte (pas de cron). Pour V1 (1 session / semaine), c'est acceptable. V3 réintroduit l'automatisation via Celery + APScheduler si besoin.
- Le débit dépend de la rate limit MCP. Pour ~500-1 000 offres / session, c'est largement suffisant.

### 6.5 Communication Python ↔ Next.js (V2+)

**Principe : Option 3 — zéro accès direct à PostgreSQL depuis Next.js.**

```
┌──────────────────────────────────────────────────────────┐
│  FastAPI (Python)                                        │
│  Génère openapi.json automatiquement                     │
└──────────────────────────────────────────────────────────┘
                         │ Téléchargé par Next.js au build
                         ▼
┌──────────────────────────────────────────────────────────┐
│  openapi-typescript (npm package)                        │
│  $ npm run generate-types                                │
│  Génère src/lib/api/types.ts                             │
│  Tous les types TypeScript = miroir des Pydantic models  │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│  Composants React utilisent l'API                        │
│  const { data } = useQuery(['ghost-skills'], ...)        │
│  → data est typé automatiquement                         │
│  → Si Pydantic change, TypeScript hurle au build         │
└──────────────────────────────────────────────────────────┘
```

**Conventions API REST V2 :**

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/aggregates/top-roles` | Top métiers (filtré par pays/période/famille) |
| GET | `/api/aggregates/top-skills` | Top compétences |
| GET | `/api/aggregates/ghost-skills` | Compétences ghost |
| GET | `/api/offers` | Liste des offres (paginée, filtrée) |
| GET | `/api/offers/{id}` | Détail d'une offre |
| POST | `/api/reports/generate` | Génère un rapport, retourne un job_id |
| GET | `/api/reports/{job_id}/status` | Statut de génération |
| GET | `/api/reports/{job_id}/download` | Téléchargement du PDF |
| POST | `/api/datasets/export` | Lance un export GitHub |
| GET | `/api/quality/scraping-report` | Dernier rapport de scraping |
| GET | `/api/quality/extraction-stats` | Stats d'extraction |
| POST | `/api/taxonomy/skills/{id}/validate` | Valide un skill |
| POST | `/api/taxonomy/skills/{id}/map` | Map un skill sur un existant |

---

## 7. ARCHITECTURE DES DONNÉES

### 7.1 Modèle conceptuel

```
┌─────────────────┐         ┌──────────────────┐
│  JobSource      │1───────*│  JobOffer        │
│ (sites scrapés) │         │ (offres brutes)  │
└─────────────────┘         └──────────────────┘
                                     │1
                                     │
                                     │1
                            ┌────────▼─────────┐
                            │ ExtractionResult │
                            │ (données IA)     │
                            └──────────────────┘
                  ┌──────────┬───┼───┬───────────┐
                  │*         │*  │*  │*          │*
            ┌─────▼────┐ ┌──▼─┐ │ ┌─▼────┐ ┌────▼────┐
            │  Skill   │ │Tool│ │ │Sector│ │Education│
            └────┬─────┘ └────┘ │ └──┬───┘ │Required │
                 │*             │    │*    └─────────┘
            ┌────▼──────┐ ┌────▼───┐ ┌▼────────────┐
            │SkillCateg.│ │JobRole │ │SectorFamily │
            └───────────┘ └───┬────┘ └─────────────┘
                              │*
                              │
                              │1
                         ┌────▼──────┐
                         │RoleFamily │
                         │(13 fam.)  │
                         └───────────┘

┌──────────────────┐         ┌──────────────────┐
│  University      │1───────*│  CurriculumSkill │
│  (institution    │         │  (skills couverts│
│   univ. réf.)    │         │   par cursus)    │
└──────────────────┘         └──────────────────┘
```

### 7.2 Entités principales

#### `JobSource` — Catalogue des sites scrapés

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | PK |
| `name` | str | Ex: "EmploiGuinee", "LinkedIn-Guinea" |
| `base_url` | str | URL de base à scraper |
| `country` | str(2) | ISO 3166-1 alpha-2 ("GN", "SN", "CI", "ML"...) |
| `scraper_type` | enum | "firecrawl-mcp" \| "apify-mcp" \| "manual" |
| `apify_actor_id` | str? | Pour Apify uniquement |
| `is_active` | bool | Active/désactivable depuis config |
| `last_scraped_at` | datetime? | Dernier scraping réussi |
| `last_offers_count` | int? | Nb offres au dernier run |

#### `JobOffer` — Offre brute collectée

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | PK |
| `source_id` | UUID FK | → JobSource |
| `external_id` | str? | ID natif sur le site source |
| `country` | str(2) | Dénormalisé pour perf |
| `url` | str | URL de l'annonce originale |
| `raw_html` | text | HTML brut conservé |
| `raw_text` | text | Texte nettoyé pour extraction IA |
| `title_raw` | str | Titre tel que scrapé |
| `dedup_hash` | str(64) | SHA-256 (company+title+location+month) |
| `published_at` | date? | Date de publication estimée |
| `scraped_at` | datetime | Quand scrapé la 1ère fois |
| `last_seen_at` | datetime | Dernière fois vue |
| `is_expired` | bool | True si non vue depuis 60j |
| `extraction_status` | enum | "pending" \| "success" \| "quarantine" \| "failed" |

#### `ExtractionResult` — Résultat structuré IA

Champs clés (issus directement du schéma `JobExtraction` Pydantic AI) :

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | PK |
| `offer_id` | UUID FK unique | → JobOffer (1-1) |
| `extraction_version` | str | Version du prompt (ex "v1.2") |
| `extracted_at` | datetime | Timestamp extraction |
| `extraction_confidence` | float | 0.0 à 1.0 |
| `title` | str | Titre normalisé |
| `company` | str | Entreprise |
| `country` | str(2) | |
| `city` | str? | |
| `contract_type` | enum | CDI/CDD/Stage/... |
| `seniority` | enum | Débutant/Junior/... |
| `role_family` | enum | 1 des 13 familles |
| `job_type` | enum | Tech-Core/Adjacent/Enabled/Non-Tech |
| `sector_id` | UUID FK | → Sector |
| `responsibilities` | jsonb | Array de strings |
| `use_cases` | jsonb | Array de strings |

**Tables de jonction many-to-many :**

```sql
-- Relation ExtractionResult ↔ Skill
CREATE TABLE extraction_skills (
    extraction_id UUID REFERENCES extraction_result(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skill(id),
    PRIMARY KEY (extraction_id, skill_id)
);

-- Relation ExtractionResult ↔ Tool
CREATE TABLE extraction_tools (
    extraction_id UUID REFERENCES extraction_result(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES tool(id),
    PRIMARY KEY (extraction_id, tool_id)
);
```

### 7.3 Entités taxonomiques

#### `Skill` — Compétence normalisée

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | PK |
| `name` | str unique | Nom canonique ("Machine Learning") |
| `aliases` | jsonb | Array d'aliases ["ML", "machine learning"...] |
| `category_id` | UUID FK | → SkillCategory |
| `is_validated` | bool | Validé manuellement |

#### `RoleFamily` — Les 13 familles canoniques

| Famille | Exemples de métiers |
|---|---|
| 🏥 **Santé** | Médecin, infirmier, pharmacien, sage-femme, biologiste |
| ⚖️ **Droit & Conformité** | Juriste, avocat, conseiller juridique, compliance officer |
| 💼 **Gestion & Management** | Chef de projet, manager, DAF, directeur opérationnel |
| 💰 **Finance & Comptabilité** | Comptable, contrôleur de gestion, auditeur, analyste financier |
| 📈 **Marketing & Commerce** | Commercial, marketeur, business developer, account manager |
| 🛠️ **Ingénierie & Technique** | Ingénieur civil, électrique, mécanique, BTP, mines |
| 💻 **IT & Numérique** | Développeur, data analyst, devops, sysadmin, IA |
| 👥 **RH & Formation** | RRH, recruteur, formateur, gestionnaire de paie |
| 🌾 **Agriculture & Agroalimentaire** | Agronome, technicien agricole, ingénieur agro |
| 🎓 **Éducation & Recherche** | Enseignant, chercheur, formateur, ingénieur pédagogique |
| 🤝 **Social & Humanitaire** | Travailleur social, coordinateur projet ONG |
| 🏗️ **Logistique & Supply Chain** | Logisticien, supply chain manager, acheteur |
| 📞 **Support & Service** | Assistant, secrétaire, customer service |

### 7.4 Entités cursus (pour algorithme ghost)

#### `University` — Top 10 institutions guinéennes V1

1. UGANC — Université Gamal Abdel Nasser de Conakry
2. ISSEG — Institut Supérieur des Sciences de l'Éducation de Guinée
3. ISIM — Institut Supérieur d'Informatique et de Management
4. UTG — Université de Thierno Mamadou Saïdou Bah de Guinée
5. UMLK — Université Mohamed Lamine Kaba de Kankan
6. ISMG — Institut Supérieur des Mines et Géologie de Boké
7. USTG — Université Saadou-Sourya Touré de Guinée
8. IST — Institut Supérieur de Technologie de Mamou
9. IFRSAG — Institut de Formation et de Recherche en Santé
10. UJNK — Université Julius Nyerere de Kankan

#### `CurriculumSkill` — Skill couverte par cursus

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | PK |
| `university_id` | UUID FK | → University |
| `field_of_study` | str | "Médecine", "Génie informatique", "Droit"... |
| `degree_level` | enum | "Licence", "Master", "Doctorat" |
| `skill_id` | UUID FK | → Skill |
| `coverage_depth` | enum | "Mention", "Module", "Spécialisation" |
| `source_document` | str? | URL du syllabus officiel |

Cette table permet la jointure avec les `Skill` extraites du marché pour calculer le `presence_in_known_curricula` de l'algorithme ghost.

---

## 8. SOURCES DE DONNÉES

### 8.1 V1 — Sources Guinée (multi-secteurs, tous métiers)

L'objectif V1 est de couvrir **tous les secteurs économiques** présents en Guinée, pas seulement le tech. Les sources sont classées en 5 catégories complémentaires.

> **Note depuis v1.2** : la colonne « Outil » des tableaux ci-dessous indique le **MCP server** utilisé depuis Claude Code (cf. §6.4). « Crawl4AI » correspond désormais à **Firecrawl MCP** (mode markdown rapide), « Firecrawl » au **Firecrawl MCP** (mode rendu JS), « Apify » au **Apify MCP**. Le catalogue de prompts associé est livré en **Annexe A**.

#### Catégorie 1 — Job boards généralistes guinéens

| Source | URL (à confirmer au lancement) | Couverture sectorielle | Outil scraping | Volume estimé / mois |
|---|---|---|---|---|
| **EmploiGuinee.com** | À confirmer | Tous secteurs (top citation) | Crawl4AI | 200-400 |
| **224jobs.com** | À confirmer | Tous secteurs | Crawl4AI | 100-300 |
| **GuineeJob.com** | À confirmer | Tous secteurs | Crawl4AI | 80-200 |
| **EmploisGuinee.org** | À vérifier | Humanitaire, ONG, dev | Crawl4AI | 30-100 |

> **Action préalable** : valider les URLs et l'activité de ces sites au lancement du projet.

#### Catégorie 2 — Pages carrières grandes entreprises (multi-industries)

| Secteur | Entreprise | Outil |
|---|---|---|
| **Mines** | SMB-Winning Consortium | Firecrawl |
| **Mines** | Compagnie des Bauxites de Guinée (CBG) | Firecrawl |
| **Mines** | Rio Tinto Simfer | Firecrawl |
| **Mines** | MMG Limited | Firecrawl |
| **Banque** | BCRG (Banque Centrale) | Firecrawl |
| **Banque** | BICIGUI | Firecrawl |
| **Banque** | Société Générale Guinée | Firecrawl |
| **Banque** | Ecobank Guinée | Firecrawl |
| **Banque** | Orabank Guinée | Firecrawl |
| **Télécoms** | Orange Guinée | Firecrawl |
| **Télécoms** | MTN Guinée | Firecrawl |
| **Télécoms** | Cellcom Guinée | Firecrawl |
| **Énergie** | EDG (Électricité de Guinée) | Firecrawl |
| **Énergie** | TotalEnergies Guinée | Firecrawl |
| **Brasseries** | Brasseries de Guinée (SOBRAGUI) | Crawl4AI |
| **Industrie** | Société Industrielle des Sodas de Guinée | Crawl4AI |
| **Construction/BTP** | Top 3 entreprises BTP guinéennes | Firecrawl |
| **Hôtellerie** | Sheraton Conakry, Noom Hotel, etc. | Crawl4AI |

#### Catégorie 3 — ONG internationales et organisations multilatérales en Guinée

Cette catégorie couvre **plus de 25% du marché de l'emploi qualifié en Guinée** — elle est cruciale.

| Organisation | Type | Outil |
|---|---|---|
| **PNUD Guinée** | Multilatéral | Crawl4AI |
| **UNICEF Guinée** | Multilatéral | Crawl4AI |
| **OMS Guinée** | Multilatéral | Crawl4AI |
| **Banque Mondiale Guinée** | Multilatéral | Crawl4AI |
| **BAD Guinée** | Multilatéral | Crawl4AI |
| **AFD Guinée** | Bilatéral | Crawl4AI |
| **USAID Guinée** | Bilatéral | Crawl4AI |
| **MSF (Médecins Sans Frontières)** | ONG | Crawl4AI |
| **Croix-Rouge Guinéenne** | ONG | Crawl4AI |
| **Plan International Guinée** | ONG | Crawl4AI |
| **Action Contre la Faim Guinée** | ONG | Crawl4AI |
| **ReliefWeb (filtre Guinée)** | Agrégateur ONG mondial | Crawl4AI |

#### Catégorie 4 — Sites institutionnels publics

| Source | Type | Outil |
|---|---|---|
| **Fonction publique guinéenne** | Recrutement État | Crawl4AI |
| **Concours administratifs** | Public | Crawl4AI |
| **Universités publiques** (recrutement enseignants/personnel) | Public | Crawl4AI |

#### Catégorie 5 — LinkedIn (filtre Guinée) via Apify

Volume estimé : 200-500 offres pertinentes par mois.

| Acteur Apify | Rôle | Coût estimé |
|---|---|---|
| `bebity/linkedin-jobs-scraper` (ou équivalent maintenu) | Scraping offres LinkedIn par localisation + mots-clés génériques tous secteurs | ~$0,40/1000 résultats |

**Configuration de scraping LinkedIn V1 :**
- Localisation : "Guinée" (Conakry et autres villes)
- Mots-clés rotatifs (tous secteurs) : "ingénieur", "manager", "comptable", "infirmier", "juriste", "responsable", "chargé", "directeur", "coordinateur", "agent", "technicien", "consultant", "analyste", "développeur", "chef de projet"
- Période : 7 derniers jours par run

### 8.2 Volume cible V1

| Catégorie | Volume estimé / mois | Outil principal |
|---|---|---|
| Job boards généralistes | 400-1 000 | Crawl4AI |
| Pages carrières grandes entreprises | 50-150 | Firecrawl |
| ONG et multilatéraux | 100-250 | Crawl4AI |
| Sites institutionnels publics | 30-80 | Crawl4AI |
| LinkedIn Guinée | 200-500 | Apify |
| **Total brut V1 / mois** | **780-1 980** | |
| **Total après dédoublonnage** | **600-1 500** | |

### 8.3 V2 — Sources UEMOA

Réplication de la stratégie V1 sur 3 nouveaux pays.

**Job boards de référence par pays (à valider) :**

| Pays | Job boards principaux |
|---|---|
| 🇸🇳 Sénégal | Senjob, EmploiSenegal, Novojob, JobBoss |
| 🇨🇮 Côte d'Ivoire | EducarrierEs, Yokojob, Côte d'Ivoire Emploi |
| 🇲🇱 Mali | EmploiMali, JobMali, MaliJobs |

### 8.4 V3 — Sources internationales (inspirées Alexey Grigorev)

#### Marchés africains de référence

| Pays | Sources principales | Pourquoi |
|---|---|---|
| 🇲🇦 Maroc | ReKrute, Bayt Maroc, Anapec, EmploiMaroc | Marché francophone le plus mature d'Afrique |
| 🇪🇬 Égypte | Wuzzuf, Naukrigulf | Hub d'innovation Afrique du Nord |
| 🇰🇪 Kenya | BrighterMonday, MyJobMag Kenya | Hub tech Afrique de l'Est ("Silicon Savannah") |
| 🇳🇬 Nigeria | MyJobMag Nigeria, Jobberman | Plus grand marché africain |
| 🇿🇦 Afrique du Sud | PNet, Careers24 | Économie continentale dominante |
| 🇬🇭 Ghana | Jobberman Ghana, Jobsearchgh | Voisin anglophone direct |

#### Marchés internationaux de référence

| Pays | Sources principales | Pourquoi |
|---|---|---|
| 🇺🇸 USA | LinkedIn US, Indeed US, builtin.com (réf. Alexey), Wellfound | Standards mondiaux, métiers émergents |
| 🇬🇧 UK | LinkedIn UK, Indeed UK, Otta | Marché tech européen mature |
| 🇫🇷 France | LinkedIn FR, Indeed FR, Welcome to the Jungle, APEC | Référence francophone européenne |
| 🇩🇪 Allemagne | LinkedIn DE, StepStone | Industrie 4.0, métiers ingénierie d'avenir |
| 🇸🇬 Singapour | LinkedIn SG | Hub innovation Asie, smart city |

**Volume cible V3 : 15 000 - 30 000 offres internationales analysées en continu.**

---

## 9. PIPELINE D'EXTRACTION IA (PYDANTIC AI)

### 9.1 Pourquoi Pydantic AI

Le pipeline d'extraction est le cœur intellectuel d'OCTAO. **Pydantic AI** a été retenu après analyse comparative de 6 frameworks (Pydantic AI, Claude Agent SDK, Instructor, BAML, LangGraph, CrewAI).

**Justification** :
- Stack référence IA5D (cohérence avec Miratti et autres projets)
- Validation Pydantic native — type-safety garantie sur le `JobExtraction`
- Multi-LLM (Claude, GPT, Gemini, Mistral, Ollama) — flexibilité future
- Maintenu par l'équipe Pydantic = pérennité
- Si besoin agentique en V3, Pydantic AI sait le faire aussi (`Agent` class avec tools)
- Adapté pour de l'**extraction** (≠ orchestration agentique complexe)

**Frameworks rejetés et pourquoi :**

| Framework | Pourquoi rejeté |
|---|---|
| LangGraph | Sur-engineering pour un pipeline linéaire (non-conditionnel) |
| CrewAI | Anti-pattern d'extraction (faire débattre N agents pour extraire 1 JSON) |
| Instructor | Pydantic AI fait pareil + meilleure évolutivité |
| BAML | Ajoute un nouveau langage à la stack — overhead injustifié |
| Claude Agent SDK seul (V1) | Surdimensionné pour de la simple extraction structurée |

**Note V3** : Claude Agent SDK arrivera en V3 **en complément** de Pydantic AI, uniquement pour les vraies tâches agentiques (recherche prospective).

### 9.2 Schéma d'extraction complet

Le schéma `JobExtraction` (déjà décrit en section 5.2 F04) garantit :
- Validation automatique (Pydantic rejette tout JSON mal formé)
- Trois niveaux d'analyse (skills + responsibilities + use cases) — innovation Alexey
- Score de confiance honnête pour filtrage qualité
- Classification multi-axes (famille métier + type tech + secteur + diplôme)

### 9.3 Système de confidence scoring

Chaque extraction porte un `extraction_confidence` entre 0.0 et 1.0 attribué par Claude lui-même.

| Seuil | Action |
|---|---|
| `confidence >= 0.85` | ✅ Intégration directe en base curated |
| `0.75 <= confidence < 0.85` | ✅ Intégration mais flagged pour review qualité |
| `0.5 <= confidence < 0.75` | ⚠️ Quarantaine — review manuelle hebdomadaire requise |
| `confidence < 0.5` | ❌ Rejet — offre marquée comme inintelligible |

**Méthodologie d'attribution de la confidence (instruction au modèle) :**

Le prompt système précise à Claude qu'il doit baisser la confidence si :
- L'offre est trop courte (< 100 mots de description)
- Les sections sont mal délimitées (pas de structure claire)
- La langue n'est pas le français (occasionnellement anglais)
- Plusieurs postes semblent décrits dans une seule annonce
- Des informations critiques manquent (titre, entreprise)

### 9.4 Normalisation taxonomique

Après l'extraction principale, un second pipeline (Claude Haiku 4.5, plus rapide et moins cher) normalise les skills/tools/roles extraits.

**Flux de normalisation :**

```
Extraction Skill brute : "ML"
        ↓
Recherche dans la table Skill par nom et aliases
        ↓
   ┌────┴────┐
   ▼         ▼
TROUVÉ    NON TROUVÉ
   │         │
   │         ▼
   │    Claude Haiku : "Ce skill 'ML' est-il un alias d'un skill existant
   │    dans cette liste : [Machine Learning, MLOps, Marketing Manager, ...]"
   │         │
   │         ▼
   │    Si oui → ajouter "ML" aux aliases du skill matché
   │    Si non → créer nouveau skill EN STATUT "à valider"
   │         │
   └─────────┘
        ▼
Liaison ExtractionResult ↔ Skill
        ▼
Si skill nouvellement créé → apparaît dans la commande CLI
"octao taxonomy review" pour validation manuelle hebdomadaire
```

**Bénéfice :** la taxonomie s'auto-enrichit sans explosion de doublons. Le coût de validation manuelle hebdomadaire est limité à ~10-20 nouveaux items par semaine après stabilisation.

### 9.5 Code complet de l'agent Pydantic AI (V1)

```python
# app/services/extraction/extraction_agent.py
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from app.schemas.extraction import JobExtraction
from app.config import settings
import logging

logger = logging.getLogger(__name__)

EXTRACTION_SYSTEM_PROMPT = """
Tu es un expert en analyse du marché de l'emploi en Afrique de l'Ouest
francophone. Ta mission est d'extraire de manière structurée les
informations clés d'une offre d'emploi pour alimenter un observatoire
gouvernemental utilisé par le Ministère de l'Enseignement Supérieur.

CONTEXTE :
- Les données extraites alimentent des rapports lus par des ministres et
  des doyens d'université
- Chaque erreur d'extraction peut fausser des décisions politiques
- La rigueur prime sur l'exhaustivité

INSTRUCTIONS STRICTES :

Tu DOIS :
- Extraire les compétences EXPLICITEMENT mentionnées dans l'offre (jamais
  inférer ou supposer)
- Extraire 3 à 8 responsabilités/missions concrètes (pas les avantages
  comme "salaire attractif" ou "bonne ambiance")
- Extraire 1 à 3 use cases business (pourquoi l'entreprise recrute, quel
  problème elle résout)
- Classifier dans une famille de métiers parmi les 13 listées strictement
- Fournir un score de confiance honnête (0-1) sur la qualité d'extraction
- Si l'offre est inintelligible ou incomplète, mettre confidence < 0.5

Tu NE DOIS PAS :
- Inventer des compétences non mentionnées dans l'offre
- Standardiser ou corriger les noms d'entreprise (les laisser tels quels)
- Extraire des données personnelles (noms candidats, contacts directs)
- Mélanger plusieurs postes même si l'annonce semble en contenir plusieurs
  (extraire seulement le poste principal)

CALIBRATION DE LA CONFIDENCE :
- 0.95+ : extraction parfaite, toutes les sections claires
- 0.85-0.95 : extraction très bonne, quelques zones grises mineures
- 0.75-0.85 : extraction correcte mais quelques infos approximatives
- 0.5-0.75 : extraction difficile, beaucoup d'inférences
- < 0.5 : offre trop dégradée, mieux vaut rejeter

Réponds STRICTEMENT au format JSON correspondant au schéma JobExtraction.
"""

extraction_agent = Agent(
    model=AnthropicModel(settings.EXTRACTION_MODEL),
    output_type=JobExtraction,
    system_prompt=EXTRACTION_SYSTEM_PROMPT,
    retries=2,
)


def build_extraction_prompt(offer_text: str, source_name: str, country: str) -> str:
    """Construit le prompt user pour une offre."""
    return f"""
Voici une offre d'emploi à extraire.

SOURCE : {source_name}
PAYS : {country}

CONTENU DE L'OFFRE :
---
{offer_text}
---

Extrait toutes les informations selon le schéma JobExtraction.
"""


async def extract_offer(offer_text: str, source_name: str, country: str) -> JobExtraction:
    """Extrait une offre d'emploi vers un objet structuré."""
    user_prompt = build_extraction_prompt(offer_text, source_name, country)
    try:
        result = await extraction_agent.run(user_prompt)
        return result.output
    except Exception as e:
        logger.error(f"Extraction failed for offer from {source_name}: {e}")
        raise
```

### 9.6 Coûts d'extraction estimés

Pour 1000 offres extraites (V1 mensuel typique) :

| Étape | Modèle | Tokens moyens (in/out) | Coût/offre | Coût total 1000 |
|---|---|---|---|---|
| Extraction principale | Claude Sonnet 4.5 | ~3000 in / ~1500 out | ~$0.018 | ~$18 |
| Normalisation skills/tools | Claude Haiku 4.5 | ~500 in / ~200 out | ~$0.0008 | ~$0.80 |
| **TOTAL pour 1000 offres** | | | | **~$19** |

V1 budget IA : ~$15-20/mois pour ~1000 offres extraites.

---

## 10. RÈGLES MÉTIER

### 10.1 Règles de qualité des données (RD)

| # | Règle | Justification |
|---|---|---|
| RD-1 | Une offre n'est intégrée à la base curated que si l'extraction a une `confidence ≥ 0.75` | Préserver la crédibilité scientifique. Les offres mal parsées vont en quarantaine pour révision manuelle |
| RD-2 | Une offre est marquée `expired` après 60 jours sans réapparition dans les scrapings | Le marché bouge ; on ne pollue pas les statistiques avec des offres mortes |
| RD-3 | Dédoublonnage cross-sources via hash SHA-256 `(company + title + location + month)` | Une même offre publiée sur 3 sites différents ne compte qu'une fois |
| RD-4 | Toute offre antérieure à 12 mois est exclue des agrégats par défaut | Les rapports reflètent le marché actuel, pas l'historique |
| RD-5 | Les offres sans titre extractible OU sans entreprise identifiable sont rejetées | Standards minimum d'intégrité |
| RD-6 | Une offre dont `country` ne peut pas être déterminé est rejetée | Évite la pollution des analyses pays |

### 10.2 Règles de normalisation taxonomique (RT)

| # | Règle | Exemple |
|---|---|---|
| RT-1 | Les compétences sont normalisées via une table d'aliases | `"ML"`, `"machine learning"`, `"apprentissage automatique"` → `Skill: "Machine Learning"` |
| RT-2 | Les outils sont catégorisés (langage / framework / cloud / db / ai-tool / office / industry-tool / autre) | `"Python"` → `category: "language"` ; `"AWS"` → `category: "cloud"` |
| RT-3 | Les métiers sont mappés vers une taxonomie inspirée du ROME | `"Dev fullstack"`, `"Développeur web"` → `JobRole: "Full-Stack Developer"` (famille `IT & Numérique`) |
| RT-4 | Toute nouvelle compétence détectée mais non mappée déclenche une review hebdomadaire | Empêche l'explosion de doublons |
| RT-5 | Le seuil minimum d'occurrences pour qu'une compétence apparaisse dans les rapports est de 3 | Évite les compétences anecdotiques qui faussent les analyses |
| RT-6 | La classification dans une des 13 familles de métiers est obligatoire | Si Claude ne peut pas classer, l'offre est rejetée |
| RT-7 | La taxonomie est versionnée — chaque changement majeur incrémente une version | Permet de retraiter rétroactivement les données si la taxonomie évolue |

### 10.3 Algorithme « Compétences ghost » (RA-Ghost)

C'est le cœur politique de l'outil. Une compétence est qualifiée de **« ghost »** si elle satisfait les critères de la formule :

```
ghost_score = (frequency_in_market × 0.5)
            + (growth_rate_3m × 0.3)
            - (presence_in_known_curricula × 0.2)

Si ghost_score > 0.7
   AND occurrences_in_market ≥ 5
   → Marquée "compétence ghost" 🚨
```

**Variables et calcul :**

| Variable | Calcul | Plage |
|---|---|---|
| `frequency_in_market` | (nb offres demandant cette compétence dans la famille) / (nb total offres dans la famille) | 0-1 |
| `growth_rate_3m` | (occ_mois_courant - occ_mois_T-3) / max(1, occ_mois_T-3) clampé entre -1 et +1 | -1 à 1 |
| `presence_in_known_curricula` | 1 si la compétence existe dans CurriculumSkill pour ≥1 institution, 0 sinon | 0 ou 1 |

**Exemple de sortie politique :**

> *« La compétence 'gestion de projet Agile' apparaît dans 47% des offres en Ingénierie & Technique en Guinée (croissance de +18% sur 3 mois), mais n'est enseignée dans aucun cursus d'ingénierie listé parmi les 10 institutions de référence. Score ghost : 0.85. Recommandation : intégration prioritaire dans les Bac+5 ingénierie. »*

### 10.4 Algorithme « Métiers d'avenir » (RA-Avenir, V3)

L'algorithme phare V3, défini par :

```
metier_avenir_score =
    (presence_marches_matures × 0.35)
  + (croissance_12_mois × 0.30)
  + (presence_secteurs_tech_strategiques × 0.20)
  - (presence_marche_guineen × 0.15)

Si metier_avenir_score > 0.65
   AND occurrences_marches_matures ≥ 50
   AND presence_marche_guineen < 5%
   → "Métier d'avenir prioritaire pour la Guinée" 🚀
```

**Variables :**

| Variable | Calcul | Plage |
|---|---|---|
| `presence_marches_matures` | % d'apparition du métier dans les marchés USA + UK + FR + DE + Singapour | 0-1 |
| `croissance_12_mois` | Croissance des occurrences sur 12 mois sur les marchés matures | 0-1 (clampé) |
| `presence_secteurs_tech_strategiques` | Bonus si le métier touche IA, énergie verte, biotech, climat, semiconducteurs | 0-1 |
| `presence_marche_guineen` | % d'apparition du métier dans les offres scrapées en Guinée | 0-1 |

**Livrable typique V3 :** *Top 30 métiers d'avenir prioritaires pour la Guinée, avec pour chacun : description du métier, compétences associées, secteurs porteurs, recommandations de filière universitaire à créer ou à enrichir, exemples internationaux d'institutions de référence formant à ce métier.*

### 10.5 Règles éthiques et conformité (RE)

| # | Règle | Justification |
|---|---|---|
| RE-1 | Aucune donnée personnelle (nom de candidat, contact direct) n'est jamais collectée ou stockée | Conformité RGPD et éthique professionnelle |
| RE-2 | Le nom des entreprises qui recrutent est public (déjà sur les job boards) — on ne l'anonymise pas | Transparence totale sur "qui demande quoi" — c'est ce qui rend les insights actionnables |
| RE-3 | Respect du `robots.txt` de chaque site scrapé | Bonne citoyenneté web, évite blocages et conflits juridiques |
| RE-4 | User-Agent identifié comme `OCTAO-Bot/1.0 (Observatoire des Compétences et Métiers AFO — contact@syli.technology)` | Transparence sur qui scrape |
| RE-5 | Rate limiting strict : max 1 requête / 3 secondes par site scrapé | Ne pas surcharger les serveurs locaux |
| RE-6 | Page « Méthodologie & Sources » publique exposant comment les données sont collectées et traitées (à partir de V2) | Crédibilité scientifique |
| RE-7 | Datasets publiés sur GitHub anonymisés (suppression e-mails, téléphones, noms de personnes) | RGPD by design + bien commun |
| RE-8 | Aucune retransmission ou revente de la base brute d'offres à des tiers | Évite tout conflit avec les sources scrapées |

### 10.6 Règles de fraîcheur (RF)

| # | Règle |
|---|---|
| RF-1 | Tous les rapports affichent systématiquement la date du dernier scraping |
| RF-2 | V1 : les agrégats sont calculés à la demande (notebooks ou CLI) |
| RF-3 | V2+ : les vues matérialisées sont rafraîchies une fois par jour à 07h UTC |
| RF-4 | Les filtres « période » disponibles : 7 jours / 30 jours / 90 jours / 12 mois / Tout |
| RF-5 | Si une période contient moins de 50 offres, un disclaimer « Échantillon limité, à interpréter avec prudence » s'affiche dans les rapports |
| RF-6 | Les rapports PDF sont datés et versionnés (ex : `OCTAO_Guinee_Synthese_2026-05.pdf`) pour traçabilité |

---

## 11. UI/UX PAR PHASE

### 11.1 V1 — UI = Jupyter notebooks + CLI

V1 n'a **pas de dashboard**. L'analyste OCTAO (toi) interagit avec le système via :
1. **Une CLI** pour les actions (scrape, extract, report, export)
2. **Des notebooks Jupyter** pour l'exploration et l'analyse

C'est intentionnel : V1 valide la méthodologie sans investir dans une UI complexe.

#### CLI OCTAO — commandes de référence

```bash
# Scraping
octao scrape --country=GN --sources=all
octao scrape --source=emploi-guinee
octao scrape --country=GN --tier=free  # exclut Apify (payant)

# Extraction IA
octao extract --batch=last
octao extract --batch=last --confidence-min=0.75
octao extract --offer-id=<uuid>  # une seule offre

# Quality control
octao quality --report-last-week
octao quality --quarantine-list

# Taxonomy
octao taxonomy review                # mode interactif
octao taxonomy stats                 # stats sur skills/tools
octao taxonomy export --format=csv

# Reports
octao report --type=synthesis --period=30d --country=GN
octao report --type=deep --period=30d --country=GN
octao briefing --period=30d --country=GN  # DOCX
octao deck --period=30d --country=GN      # PPTX

# Datasets export
octao export --month=2026-05
octao export --month=2026-05 --push-github

# Database
octao db migrate          # Alembic upgrade
octao db seed             # Seed initial (13 familles, 5 sectors, etc.)
octao db status
```

#### Liste des notebooks Jupyter

```
notebooks/
├── 00_setup_dev.ipynb              # Bootstrap + tests connection DB
├── 01_quality_control.ipynb        # Vérifs hebdo des extractions
├── 02_insights_exploration.ipynb   # Top métiers/skills/tools
├── 03_ghost_skills_analysis.ipynb  # Analyse des compétences ghost
├── 04_taxonomy_review.ipynb        # Review taxonomique alternatif à CLI
├── 05_reports_preview.ipynb        # Preview des rapports avant génération
└── 06_datasets_export.ipynb        # Préparation des exports GitHub
```

**Stack notebooks :**
- `jupyterlab` + `ipykernel`
- `pandas` ou `polars` pour manipulation
- `plotly` pour visualisations interactives
- `sqlalchemy` + `asyncpg` pour accès DB
- `rich` pour outputs formatés

### 11.2 V2+ — Dashboard Next.js premium

V2 introduit le **dashboard Next.js** comme UI principale, avec un design adapté aux deux audiences :
- **Dashboard interne** : pour toi et l'équipe AI5D
- **Portail universités** : pour les doyens (V2)

#### Direction visuelle

OCTAO doit fonctionner sur deux registres :
1. **Dashboard interne** : sobre, fonctionnel, dense, productif
2. **Livrables PDF/PPTX + Portail universités** : registre éditorial gouvernemental — sérieux, institutionnel

La même charte est utilisée dans les deux contextes pour maintenir la cohérence de marque.

#### Charte graphique OCTAO (résumé — détail dans document Charte séparé)

| Rôle | Couleur | Hex | Usage principal |
|---|---|---|---|
| **Primary — Bleu nuit** | Bleu nuit | `#0F2A44` | Headers, navigation, titres |
| **Secondary — Or institutionnel** | Or sobre | `#C9A961` | Accents, KPI hero, badges |
| **Accent positif** | Émeraude data | `#10B981` | Tendances positives, croissance |
| **Accent alerte** | Rouille | `#C6613F` | Tendances négatives, alertes ghost |
| **Background light** | Crème chaud | `#FAF8F3` | Fond principal mode clair |
| **Background dark** | Bleu très foncé | `#0A1628` | Fond principal mode sombre |
| **Surface light** | Blanc pur | `#FFFFFF` | Cards, panels mode clair |
| **Surface dark** | Bleu foncé | `#13243D` | Cards, panels mode sombre |
| **Text primary light** | Anthracite | `#1A1A1A` | Texte principal mode clair |
| **Text primary dark** | Crème | `#FAF8F3` | Texte principal mode sombre |
| **Text muted** | Gris doux | `#6B7280` | Texte secondaire, légendes |

**Typographies :**
- **Titres et data hero** : DM Serif Display (cohérent avec AI5D)
- **Corps de texte** : DM Sans (lisibilité optimale)
- **Chiffres et data viz** : DM Mono (tabular figures)

**Iconographie :** Lucide React.

**Modes :** Light + Dark via `next-themes`.

#### Routes Next.js V2 (dashboard interne)

| Route | Page | Audience |
|---|---|---|
| `/login` | Connexion Better Auth | Toi + équipe |
| `/dashboard` | Vue d'ensemble + KPIs | Toi + équipe |
| `/insights` | Exploration libre + filtres | Toi + équipe |
| `/ghost-skills` | Compétences ghost détaillées | Toi + équipe |
| `/reports` | Génération de rapports | Toi + équipe |
| `/quality` | Quality control | Toi + équipe |
| `/taxonomy` | Taxonomy review | Toi + équipe |
| `/datasets` | Export datasets | Toi + équipe |
| `/settings` | Paramètres + utilisateurs | Admin uniquement |

#### Routes Next.js V2 (portail universités)

| Route | Page | Audience |
|---|---|---|
| `/portail/login` | Magic link Better Auth | Doyens whitelistés |
| `/portail/[universityId]` | Vue institution | Doyen de cette institution |
| `/portail/[universityId]/filieres` | Liste des filières | Doyen |
| `/portail/[universityId]/filieres/[id]` | Vue filière + recommandations | Doyen |
| `/methode` | Page méthodologie publique | Public (SEO) |

#### Composants principaux (Shadcn customisés)

| Composant | Rôle |
|---|---|
| `<KPICard>` | KPI hero avec chiffre + tendance |
| `<FiltersBar>` | Barre de filtres globaux (pays, période, famille) |
| `<DataTable>` | TanStack Table pour QC, taxonomy, datasets |
| `<PlotlyChart>` | Wrapper pour graphiques (bar, treemap, heatmap) |
| `<TremorChart>` | Charts data rapides via Tremor |
| `<ReportCard>` | Card de rapport généré (preview + download) |
| `<SkillBadge>` | Badge skill avec famille couleur |
| `<GhostScore>` | Score ghost avec barre visuelle |
| `<SourceStatus>` | Status d'une source (last scraped, count) |
| `<ConfidenceBadge>` | Badge de confiance d'extraction (couleur selon seuil) |

### 11.3 Principes UX appliqués (V2+)

| Principe | Application |
|---|---|
| **Densité d'information assumée côté dashboard interne** | Outil pour analyste — pas de souci d'overload |
| **Sobriété côté portail universités** | Audience doyens — clarté, pas de fonctionnalités cachées |
| **Pas de gradients ni d'ombres marquées** | Direction éditoriale sobre, cohérent avec le rendu PDF |
| **Tabular figures** dans tous les chiffres | Alignement vertical impeccable |
| **Toujours afficher la date du dernier refresh** | Confiance + transparence |
| **Disclaimers automatiques sur faibles échantillons** | Honnêteté méthodologique |
| **Tooltip explicatif sur chaque indicateur complexe** | Auto-documentation |
| **Aucune photo, aucune illustration décorative** | Le sérieux d'un rapport institutionnel |

---

## 12. AUTHENTIFICATION ET RÔLES

### 12.1 V1 — Pas d'auth (mode local)

V1 ne nécessite aucune authentification. Tu travailles en local sur ton Mac, la DB Neon a son propre mot de passe stocké dans `.env`.

**Sécurité V1 :**
- `.env` jamais commité (gitignored)
- Connection string Neon avec rôle limité à OCTAO (pas postgres root)
- Backup régulier via Neon (point-in-time recovery natif)

### 12.2 V2 — Better Auth pour dashboard interne + portail universités

À partir de V2, **Better Auth** gère deux contextes d'authentification distincts :

#### Contexte 1 : Sessions internes (toi + équipe AI5D)

**Configuration :**
- Authentification email + mot de passe
- Sessions persistantes 30 jours
- Whitelist d'emails (max 5-10 utilisateurs internes)

**Rôles internes :**

| Rôle | Permissions |
|---|---|
| **Admin** (toi) | Tout : générer rapports, exporter datasets, modifier taxonomie, gérer users |
| **Analyst** (équipe AI5D) | Tout sauf gestion utilisateurs et modification prompts |
| **Viewer** | Lecture seule sur dashboards |

#### Contexte 2 : Portail universités (doyens)

**Configuration :**
- Authentification par **magic link** (pas de mot de passe)
- Whitelist d'emails institutionnels (`@uganc.edu.gn`, `@isseg.gn`, etc.)
- Liaison email ↔ University via table `UniversityUser`
- Sessions 7 jours

**Rôles portail :**

| Rôle | Permissions |
|---|---|
| **University Admin** (doyen) | Vue complète de SON institution, télécharger rapports filière |
| **University Viewer** (responsable filière) | Vue limitée à SA filière |

### 12.3 Matrice des rôles V2

| Action | Viewer interne | Analyst interne | Admin interne | Univ. Admin | Univ. Viewer |
|---|:---:|:---:|:---:|:---:|:---:|
| Consulter dashboards globaux | ✅ | ✅ | ✅ | ❌ | ❌ |
| Consulter dashboard sa propre institution | — | — | — | ✅ | ✅ |
| Filtrer/explorer | ✅ | ✅ | ✅ | ✅ | ✅ |
| Générer rapports PDF (toutes options) | ❌ | ✅ | ✅ | ❌ | ❌ |
| Télécharger rapport filière préparé | ❌ | ✅ | ✅ | ✅ | ✅ |
| Exporter datasets | ❌ | ✅ | ✅ | ❌ | ❌ |
| Valider taxonomie | ❌ | ✅ | ✅ | ❌ | ❌ |
| Relancer scraping manuel | ❌ | ✅ | ✅ | ❌ | ❌ |
| Modifier prompt extraction | ❌ | ❌ | ✅ | ❌ | ❌ |
| Gérer utilisateurs | ❌ | ❌ | ✅ | ❌ | ❌ |

### 12.4 V3 — API privée éventuelle

Si demande effective des ministères ou bailleurs : exposition d'une API REST FastAPI privée avec auth par clé API (rate limited). Décision déclenchée par les retours V1 et V2 — **non engagée à ce stade**.

---
## 13. LIVRABLES POLITIQUES

### 13.1 Cinq livrables produits par OCTAO V1

L'objectif V1 est de produire **cinq livrables complémentaires** que l'analyste génère depuis la CLI et envoie au cabinet ministériel. Chaque livrable répond à un cas d'usage politique précis.

| # | Livrable | Format | Pages | Audience principale | Cas d'usage |
|---|---|---|:---:|---|---|
| L1 | **Note de briefing exécutive** | DOCX | 4 | Conseiller technique → Ministre | Lecture express, prise de décision en 5 min |
| L2 | **Rapport synthèse** | PDF | 4 | Ministre + Conseiller | Vision panoramique avec 5 chiffres clés |
| L3 | **Rapport approfondi** | PDF | 25-30 | Conseiller + DGES | Document de référence avec méthodologie |
| L4 | **Deck de présentation** | PPTX | 15-20 | Karamo (présentation orale) | Présentation rendez-vous ou conseil |
| L5 | **Datasets ouverts** | JSON/CSV | — | Communauté tech, chercheurs | Transparence + crédibilité scientifique |

### 13.2 L1 — Note de briefing exécutive (DOCX, 4 pages)

**Commande :** `poetry run octao briefing --period=30d --country=GN`

**Structure :**
- **Page 1** — Synthèse en 1 paragraphe + 3 chiffres clés mis en avant
- **Page 2** — Top 5 compétences ghost prioritaires (avec contexte secteurs)
- **Page 3** — 3 recommandations actionnables (« Si vous deviez agir aujourd'hui... »)
- **Page 4** — Liens vers rapport approfondi + datasets + méthodologie

**Format :** DOCX (modifiable par le cabinet pour intégrer leurs propres notes)

**Charte appliquée :** police DM Sans, en-tête bleu nuit + or, logo OCTAO discret, marges aérées.

### 13.3 L2 — Rapport synthèse (PDF, 4 pages)

**Commande :** `poetry run octao report --type=synthesis --period=30d --country=GN`

**Structure :**
- **Page 1** — Couverture + executive summary 1 paragraphe + 5 chiffres clés
- **Page 2** — Top 10 métiers les plus recherchés en Guinée (graphique + tableau)
- **Page 3** — Top 5 compétences ghost prioritaires + score ghost
- **Page 4** — 3 recommandations + appel à approfondir + crédits méthodologiques

**Stack technique :** Jinja2 + WeasyPrint, charte OCTAO appliquée, visualisations Plotly converties en PNG embarqués.

### 13.4 L3 — Rapport approfondi (PDF, 25-30 pages)

**Commande :** `poetry run octao report --type=deep --period=30d --country=GN`

**Structure type :**

```
1. Couverture + Executive Summary (2 pages)
2. Méthodologie (3 pages)
   - Sources scrapées et volumes
   - Pipeline d'extraction Pydantic AI
   - Calibration de la confidence
   - Algorithme ghost expliqué
3. Vue d'ensemble du marché de l'emploi guinéen (3 pages)
   - Volume total + évolution
   - Répartition par famille de métiers
   - Répartition géographique
   - Répartition par taille d'entreprise
4. Analyse par famille de métiers (13 sections × 1-2 pages)
5. Compétences ghost — analyse détaillée (3-4 pages)
6. Recommandations stratégiques par filière (3-4 pages)
7. Annexes (3-4 pages)
   - Limites méthodologiques
   - Sources et fréquence de scraping
   - Glossaire
   - Lien vers datasets
```

### 13.5 L4 — Deck de présentation (PPTX, 15-20 slides)

**Commande :** `poetry run octao deck --period=30d --country=GN`

**Stack technique :** `python-pptx` avec template OCTAO (charte appliquée).

**Structure :**

```
Slide 1   — Couverture (logo + titre + date)
Slide 2   — Le problème en 1 chiffre (30,96% d'employabilité)
Slide 3   — Notre approche en 1 schéma (V1/V2/V3)
Slide 4   — Volume total scrapé + sources
Slide 5   — Top 5 chiffres clés
Slide 6   — Répartition par famille de métiers (camembert)
Slide 7-9 — Focus 3 familles porteuses (1 slide chacune)
Slide 10  — Compétences ghost — concept (1 schéma explicatif)
Slide 11  — Top 5 compétences ghost détectées
Slide 12-14 — Zoom sur 3 compétences ghost (1 slide chacune)
Slide 15  — Recommandation 1 (avec impact estimé)
Slide 16  — Recommandation 2
Slide 17  — Recommandation 3
Slide 18  — Roadmap V2/V3 (continuité narrative)
Slide 19  — Méthodologie en 1 slide + crédits
Slide 20  — Contact + remerciements
```

### 13.6 L5 — Datasets ouverts (JSON/CSV)

**Commande :** `poetry run octao export --month=2026-05 --push-github`

**Repo :** `github.com/syli-technology/octao-datasets` (public)

**Structure du repo après le push :**

```
octao-datasets/
├── README.md                          # Auto-généré, avec stats à jour
├── methodology/
│   └── methodology-2026-05.md         # Méthodologie de cette extraction
├── data/
│   └── 2026-05/
│       ├── guinea-jobs.jsonl          # Offres complètes anonymisées
│       ├── guinea-skills.csv          # Agrégat skills par fréquence
│       ├── guinea-roles.csv           # Agrégat roles par fréquence
│       └── guinea-ghost-skills.csv    # Liste des skills ghost détectées
├── notebooks/
│   └── analysis-example.ipynb         # Notebook Jupyter d'exemple
└── LICENSE                            # CC-BY 4.0 (datasets + code)
```

**Anonymisation appliquée :**
- Suppression des emails, téléphones, noms de personnes
- Conservation des noms d'entreprises (publics par nature)
- Conservation des fourchettes salariales sans personne identifiable

---

## 14. STACK TECHNIQUE

### 14.1 Vue d'ensemble par couche (V1 / V2 / V3)

| Couche | V1 (LOCAL) | V2 (LIVE) | V3 (PRODUCTION + AGENTS) |
|---|---|---|---|
| **Langage backend** | Python 3.12 | Python 3.12 | Python 3.12 |
| **Gestion deps backend** | Poetry | Poetry | Poetry |
| **CLI framework** | **Typer** | Typer | Typer |
| **Output terminal** | **Rich** | Rich | Rich |
| **Notebooks** | **JupyterLab** | JupyterLab | JupyterLab |
| **Framework IA** | **Pydantic AI** | Pydantic AI | Pydantic AI **+ Claude Agent SDK** |
| **Modèles LLM** | Claude Sonnet 4.5 + Haiku 4.5 | Claude Sonnet 4.5 + Haiku 4.5 | Claude Sonnet 4.5 + Opus 4.7 (V3 prospectif) |
| **Validation** | Pydantic v2 | Pydantic v2 | Pydantic v2 |
| **API Web** | — | **FastAPI** | FastAPI |
| **ORM** | SQLAlchemy 2.0 + asyncpg | SQLAlchemy 2.0 + asyncpg | SQLAlchemy 2.0 + asyncpg |
| **Migrations** | Alembic | Alembic | Alembic |
| **DB** | PostgreSQL Neon (free tier) | PostgreSQL Neon (paid tier) | PostgreSQL Neon (Scale tier) |
| **Collecte** | **Claude Code + MCP Apify/Firecrawl** (prompts catalogue) | idem (catalogue UEMOA étendu) | idem + Celery pour batchs nocturnes |
| **Ingestion JSONL → DB** | CLI Python `octao ingest` | idem | idem |
| **Manipulation data** | Pandas + Polars | Pandas + Polars | Pandas + Polars |
| **Viz notebook** | Plotly + Seaborn | Plotly + Seaborn | Plotly + Seaborn |
| **Génération PDF** | WeasyPrint + Jinja2 | WeasyPrint + Jinja2 | WeasyPrint + Jinja2 |
| **Génération DOCX** | python-docx | python-docx | python-docx |
| **Génération PPTX** | python-pptx | python-pptx | python-pptx |
| **Frontend** | — | **Next.js 15 + TypeScript** | Next.js 15 + TypeScript |
| **Styling** | — | Tailwind v4 + Shadcn/ui | Tailwind v4 + Shadcn/ui |
| **Auth** | — | **Better Auth** | Better Auth |
| **Codegen types API** | — | openapi-typescript | openapi-typescript |
| **Data fetching** | — | TanStack Query | TanStack Query |
| **Charts dashboard** | — | Recharts + Tremor | Recharts + Tremor |
| **Hosting Python** | Local Mac | Render (FastAPI) | Render (FastAPI + workers) |
| **Hosting Frontend** | — | Vercel (Hobby) | Vercel (Pro) |
| **File storage** | Local (`output/`) | Cloudflare R2 | Cloudflare R2 |
| **Job queue** | — | — | **Celery** |
| **Scheduler** | — | — | **APScheduler** |
| **Cache/Broker** | — | — | Upstash Redis |
| **Email transactionnel** | — | Resend | Resend |
| **Monitoring** | — | Sentry | Sentry + custom dashboards |
| **CI/CD** | GitHub Actions (lint + tests) | GitHub Actions + Render auto-deploy + Vercel auto-deploy | idem |

### 14.2 Détail Python V1 — `pyproject.toml` indicatif

```toml
[tool.poetry]
name = "octao"
version = "0.1.0"
description = "Observatoire des Compétences et Métiers d'Afrique de l'Ouest"
authors = ["Karamo Sylla <karamo@ai5d.technology>"]

[tool.poetry.dependencies]
python = "^3.12"

# Core
pydantic = "^2.9"
pydantic-settings = "^2.6"

# CLI + outputs
typer = {extras = ["all"], version = "^0.13"}
rich = "^13.9"

# IA Framework
pydantic-ai = "^0.0.14"
anthropic = "^0.40"

# Database
sqlalchemy = {extras = ["asyncio"], version = "^2.0.36"}
asyncpg = "^0.30"
alembic = "^1.14"

# NB : aucune dépendance scraping côté Python depuis V1.2 — la collecte
# se fait via Claude Code + MCP Apify/Firecrawl (cf. §6.4 et Annexe A)
# Seule l'ingestion JSONL est codée côté Python (orjson, pydantic).
orjson = "^3.10"

# Data analysis (notebooks)
pandas = "^2.2"
polars = "^1.13"
plotly = "^5.24"
seaborn = "^0.13"
jupyterlab = "^4.3"

# Génération de livrables
weasyprint = "^63.0"
jinja2 = "^3.1"
python-docx = "^1.1"
python-pptx = "^1.0"
matplotlib = "^3.9"   # pour conversion Plotly → PNG embarqué

# Utilitaires
python-dotenv = "^1.0"
tenacity = "^9.0"     # retries
loguru = "^0.7"       # logging structuré

[tool.poetry.group.dev.dependencies]
pytest = "^8.3"
pytest-asyncio = "^0.24"
pytest-cov = "^6.0"
ruff = "^0.7"
black = "^24.10"
mypy = "^1.13"

[tool.poetry.scripts]
octao = "app.cli:app"
```

### 14.3 Détail Frontend V2 — `package.json` indicatif

```json
{
  "name": "octao-web",
  "version": "0.2.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "generate-types": "openapi-typescript http://localhost:8000/openapi.json -o src/lib/api/types.ts"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "typescript": "^5.6.0",
    "tailwindcss": "^4.0.0",
    "better-auth": "^1.0.0",
    "@tanstack/react-query": "^5.62.0",
    "@tanstack/react-table": "^8.20.0",
    "react-hook-form": "^7.54.0",
    "zod": "^3.24.0",
    "recharts": "^2.13.0",
    "@tremor/react": "^3.18.0",
    "lucide-react": "^0.468.0",
    "next-themes": "^0.4.0",
    "openapi-fetch": "^0.13.0"
  },
  "devDependencies": {
    "openapi-typescript": "^7.5.0"
  }
}
```

---

## 15. ESTIMATION DES COÛTS

### 15.1 Coûts V1 (mode local) — détaillé

| Poste | Coût mensuel | Note |
|---|---|---|
| Render (FastAPI) | **$0** | NON utilisé en V1 |
| Vercel (Next.js) | **$0** | NON utilisé en V1 |
| Neon PostgreSQL | **$0** | Free tier (3 GB suffisant) |
| Upstash Redis | **$0** | NON utilisé en V1 |
| Cloudflare R2 | **$0** | PDFs en local |
| Apify (LinkedIn) | $3-5 | ~3 runs/mois × ~$1 |
| Firecrawl | $0-5 | Free tier 500 crédits/mois suffisant |
| Anthropic API (Claude) | $10-15 | ~1000 offres extraites/mois |
| Sentry | $0 | NON utilisé en V1 |
| Domaine octao.africa | $2 | $24/an amorti |
| **TOTAL V1 / mois** | **~$15-20** | |

**Coût annuel V1 ≈ $200-250.**

### 15.2 Coûts V2 (passage en LIVE) — détaillé

| Poste | Coût mensuel | Note |
|---|---|---|
| Render (FastAPI Starter) | $7 | 1 service web Python |
| Vercel (Hobby) | $0 | Suffisant pour début V2 |
| Neon (Launch tier) | $19 | Connexion partagée + plus de stockage |
| Upstash Redis | $0 | Pas encore en V2 (optionnel) |
| Cloudflare R2 | $0-5 | Storage PDFs cloud |
| Apify | $5-10 | Volume UEMOA × 4 pays |
| Firecrawl | $5-10 | Plus de pages JS |
| Anthropic API | $30-50 | Volume × 3-4 |
| Resend (emails alertes) | $0 | Free tier 3000 emails/mois |
| Sentry | $0 | Free tier suffit |
| **TOTAL V2 / mois** | **~$70-100** | |

### 15.3 Coûts V3 (PRODUCTION) — détaillé

| Poste | Coût mensuel | Note |
|---|---|---|
| Render (FastAPI + Workers Celery) | $35-50 | Service web + workers |
| Vercel (Pro) | $20 | Volume utilisateurs accru |
| Neon (Scale tier) | $69 | Volume international |
| Upstash Redis | $10 | Broker Celery |
| Cloudflare R2 | $5-10 | Storage rapports volumineux |
| Apify | $30-50 | Scraping international |
| Firecrawl | $30-50 | Volume international |
| Anthropic API | $150-300 | 15-30K offres + agents prospectifs V3 |
| Resend | $20 | Plan Pro |
| Sentry | $26 | Plan Team |
| **TOTAL V3 / mois** | **~$400-600** | |

### 15.4 Synthèse coûts par phase

| Phase | Coût mensuel | Coût total cumulé |
|---|---|---|
| V1 (3-4 semaines + 2 mois exploitation) | $15-20 | ~$50-70 |
| V2 (6-7 semaines + 3 mois exploitation) | $70-100 | ~$300-450 cumulé |
| V3 (8-10 semaines + 6 mois exploitation) | $400-600 | ~$2,800-4,000 cumulé |

**Investissement total 12 mois pour développer + exploiter V1 + V2 + V3 ≈ $3,000-4,500** (hors temps Karamo). Très accessible compte tenu du potentiel B2G.

---

## 16. MÉTHODOLOGIE DE DÉVELOPPEMENT

### 16.1 Approche — vibe coding piloté avec Claude Code

OCTAO sera développé avec **Claude Code** comme outil principal de développement, en mode pair-programming avec Karamo.

**Principes :**
- Spec-driven : chaque feature commence par une spec écrite (extension du PRD)
- Tests d'abord pour les algorithmes critiques (ghost score, métiers d'avenir)
- Code review systématique par Claude Code avant merge
- Refactoring continu (pas de dette technique tolérée plus de 2 sprints)

### 16.2 Structure du repo `octao-app` (privé)

```
octao-app/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── alembic.ini
├── alembic/                       # Migrations DB
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── cli.py                     # Entry point Typer
│   ├── config.py                  # Settings via pydantic-settings
│   ├── database.py                # SQLAlchemy engine + session
│   ├── models/                    # Modèles ORM
│   │   ├── job_source.py
│   │   ├── job_offer.py
│   │   ├── extraction_result.py
│   │   ├── skill.py
│   │   ├── tool.py
│   │   ├── job_role.py
│   │   ├── role_family.py
│   │   ├── sector.py
│   │   ├── education_required.py
│   │   ├── university.py
│   │   └── curriculum_skill.py
│   ├── schemas/                   # Schémas Pydantic
│   │   ├── extraction.py
│   │   ├── reports.py
│   │   └── exports.py
│   ├── services/
│   │   ├── scrapers/
│   │   │   ├── orchestrator.py
│   │   │   ├── base.py
│   │   │   ├── crawl4ai_scraper.py
│   │   │   ├── firecrawl_scraper.py
│   │   │   └── apify_scraper.py
│   │   ├── extraction/
│   │   │   ├── extraction_agent.py
│   │   │   ├── extraction_prompts.py
│   │   │   └── batch_extractor.py
│   │   ├── normalization/
│   │   │   ├── skill_normalizer.py
│   │   │   ├── tool_normalizer.py
│   │   │   └── role_normalizer.py
│   │   ├── algorithms/
│   │   │   ├── ghost_skills.py
│   │   │   └── metier_avenir.py    # V3 only
│   │   ├── reports/
│   │   │   ├── synthesis_builder.py
│   │   │   ├── deep_report_builder.py
│   │   │   ├── briefing_builder.py
│   │   │   ├── deck_builder.py
│   │   │   └── templates/         # Jinja2 + assets PPTX
│   │   └── exports/
│   │       └── github_publisher.py
│   ├── algorithms/                # Algos critiques avec tests
│   │   ├── ghost_skills.py
│   │   └── tests/
│   └── utils/
│       ├── logging.py
│       └── retries.py
├── notebooks/
│   ├── 00_setup_dev.ipynb
│   ├── 01_quality_control.ipynb
│   ├── 02_insights_exploration.ipynb
│   ├── 03_ghost_skills_analysis.ipynb
│   ├── 04_taxonomy_review.ipynb
│   ├── 05_reports_preview.ipynb
│   └── 06_datasets_export.ipynb
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── output/                        # Livrables générés (gitignored)
└── docs/
    ├── PRD-OCTAO-v1.1.md
    ├── CHARTE-GRAPHIQUE.md
    └── METHODOLOGY.md
```

### 16.3 Conventions de code

| Aspect | Convention |
|---|---|
| Linter | Ruff (config stricte) |
| Formateur | Black + Ruff format |
| Type checker | mypy strict |
| Style commits | Conventional commits (`feat:`, `fix:`, `docs:`...) |
| Branches | `feat/`, `fix/`, `chore/`, `docs/` |
| PR mergeables si | tous tests passent + review Claude Code OK |
| Tests obligatoires sur | `app/algorithms/*` (ghost score, métier_avenir) |
| Tests recommandés sur | `app/services/*` |
| Couverture cible | >70% sur algorithms, >50% global |

### 16.4 Stratégie de tests

**V1 — pyramide de tests :**

```
                 ┌─────────────┐
                 │  E2E (3-5)  │   Tests CLI complets sur fixtures
                 └─────────────┘
              ┌─────────────────┐
              │ Integration (~15)│  Test scraper + extraction sur HTML réel
              └─────────────────┘
        ┌──────────────────────────┐
        │   Unit tests (~50-80)    │  Algorithmes, normalizers, schemas
        └──────────────────────────┘
```

**Fixtures critiques :**
- `tests/fixtures/offers/` — 20-30 offres réelles anonymisées (HTML brut)
- `tests/fixtures/extractions/` — JobExtraction attendus pour ces offres
- `tests/fixtures/curricula/` — Cursus universitaires de référence pour ghost

**Test critique algorithme ghost :**

```python
# tests/unit/test_ghost_skills.py
def test_ghost_skill_detected_when_high_market_low_curriculum():
    """Une skill avec 60% du marché et 0 cursus doit être ghost."""
    result = compute_ghost_score(
        frequency_in_market=0.6,
        growth_rate_3m=0.2,
        presence_in_known_curricula=0,
    )
    assert result > 0.7
    assert result <= 1.0

def test_ghost_skill_not_detected_when_present_in_curricula():
    """Une skill très demandée mais déjà enseignée n'est pas ghost."""
    result = compute_ghost_score(
        frequency_in_market=0.8,
        growth_rate_3m=0.1,
        presence_in_known_curricula=1,
    )
    assert result < 0.7
```

---

## 17. PHASAGE D'IMPLÉMENTATION

### 17.1 V1 — Mode local (3-4 semaines)

#### Sprint 0 — Setup (1 jour)
- [ ] Créer repo `syli-technology/octao-app` (privé) sur GitHub
- [ ] Init Poetry + structure du projet
- [ ] Setup `.env.example` + `.gitignore`
- [ ] Setup pre-commit hooks (ruff + black + mypy)
- [ ] Compte Neon créé + DB `octao_v1` provisionnée
- [ ] Config Alembic + première migration vide
- [ ] Setup Claude Code dans le repo

#### Sprint 1 — Modèles + Scraping infra (3 jours)
- [ ] Modèles SQLAlchemy : JobSource, JobOffer, ExtractionResult, Skill, Tool, RoleFamily, JobRole, Sector, EducationRequired, University, CurriculumSkill
- [ ] Migrations Alembic complètes
- [ ] Seed initial : 13 RoleFamily + 5 SectorFamily + 10 University guinéennes
- [ ] Base scrapers (`base.py`) + abstraction commune
- [ ] CLI Typer skeleton (`octao --help`)

#### Sprint 2 — Extraction Pydantic AI (1 semaine)
- [ ] Schéma `JobExtraction` Pydantic (validation stricte)
- [ ] Prompt système d'extraction calibré
- [ ] Agent Pydantic AI fonctionnel
- [ ] Tests unitaires sur 10 offres fixtures
- [ ] Pipeline batch d'extraction (`octao extract`)
- [ ] Confidence scoring + quarantaine

#### Sprint 3 — Toutes les sources + premier scraping réel (5 jours)
- [ ] Scrapers Crawl4AI (4 job boards guinéens + ONG)
- [ ] Scraper Firecrawl (5 grandes entreprises)
- [ ] Scraper Apify LinkedIn Guinée
- [ ] Orchestrator unifié (`octao scrape`)
- [ ] Premier scraping complet en réel → ~500-1000 offres
- [ ] Première extraction batch complète
- [ ] Notebook `01_quality_control.ipynb` opérationnel

#### Sprint 4 — Algorithmes + Génération livrables (1 semaine)
- [ ] Module `algorithms/ghost_skills.py` + tests
- [ ] Notebook `02_insights_exploration.ipynb`
- [ ] Notebook `03_ghost_skills_analysis.ipynb`
- [ ] Templates Jinja2 + WeasyPrint pour PDF synthèse + PDF approfondi
- [ ] Module python-docx pour briefing
- [ ] Module python-pptx pour deck (template OCTAO)
- [ ] Génération du premier rapport réel pour validation visuelle

#### Sprint 5 — Datasets + finitions (3 jours)
- [ ] Module `exports/github_publisher.py`
- [ ] Création repo public `syli-technology/octao-datasets` avec template
- [ ] Première publication datasets sur GitHub
- [ ] Documentation README projet
- [ ] Documentation METHODOLOGY.md
- [ ] Premier livrable complet envoyé à un testeur (interne AI5D)

**Livrable de fin V1 :** rapport synthèse + briefing + deck pour la **première présentation à la ministre**.

### 17.2 V2 — Passage en LIVE (6-7 semaines)

#### Sprint 1 V2 — Migration vers FastAPI (1 semaine)
- [ ] Wrapper FastAPI autour des services existants
- [ ] Endpoints REST principaux (top-roles, top-skills, ghost-skills, offers, reports)
- [ ] Génération `openapi.json` automatique
- [ ] Déploiement initial Render (FastAPI Starter)
- [ ] Migration DB Neon Free → Launch tier

#### Sprint 2 V2 — Setup Next.js + Auth (1 semaine)
- [ ] Setup Next.js 15 + TypeScript + Tailwind v4 + Shadcn
- [ ] Better Auth configuré (sessions internes)
- [ ] Codegen `openapi-typescript`
- [ ] Couches API client (TanStack Query)
- [ ] Layouts + thème OCTAO appliqué (DM Serif + DM Sans + DM Mono)
- [ ] Login + dashboard layout

#### Sprint 3 V2 — Pages dashboard interne (1.5 semaines)
- [ ] Page dashboard global (KPIs hero + graphiques)
- [ ] Page Insights (filtres + tables Plotly)
- [ ] Page Ghost Skills (visualisations dédiées)
- [ ] Page Reports (génération + téléchargement)
- [ ] Page Quality (QC live)
- [ ] Page Taxonomy (validation interactive)

#### Sprint 4 V2 — Scraping UEMOA (1 semaine)
- [ ] Sources Sénégal configurées
- [ ] Sources Côte d'Ivoire configurées
- [ ] Sources Mali configurées
- [ ] Premier scraping UEMOA complet
- [ ] Module benchmark régional

#### Sprint 5 V2 — Portail universités (1.5 semaines)
- [ ] Magic link Better Auth pour doyens
- [ ] Whitelist par institution
- [ ] Vue institution (dashboard restreint)
- [ ] Vue filière + recommandations
- [ ] Téléchargement rapport filière personnalisé

#### Sprint 6 V2 — Page méthodologie publique + alertes (3 jours)
- [ ] Page `/methode` publique (SEO friendly)
- [ ] Système d'alertes hebdomadaires Resend
- [ ] Templates email institutionnels

#### Sprint 7 V2 — Tests + déploiement final (5 jours)
- [ ] Tests E2E Playwright sur dashboard
- [ ] Tests d'intégration FastAPI
- [ ] Déploiement Vercel Hobby
- [ ] Domaine `dashboard.octao.africa` configuré
- [ ] Onboarding 2-3 doyens pilotes

### 17.3 V3 — Production + agents prospectifs (8-10 semaines)

#### Sprint 1-2 V3 — Pipeline live (2 semaines)
- [ ] Migration scripts CLI vers tâches Celery
- [ ] APScheduler hebdomadaire configuré
- [ ] Upstash Redis broker
- [ ] Workers Render dédiés
- [ ] Tests de charge sur 5K offres/run

#### Sprint 3-4 V3 — Scraping international (2 semaines)
- [ ] 6 sources africaines (Maroc, Égypte, Kenya, Nigeria, ZA, Ghana)
- [ ] 5 sources internationales (USA, UK, FR, DE, SG)
- [ ] Volume cible 15-30K offres/mois validé
- [ ] Page dashboard internationale Next.js

#### Sprint 5-6 V3 — Algorithme métiers d'avenir (2 semaines)
- [ ] Module `algorithms/metier_avenir.py` + tests
- [ ] Calibration sur données réelles
- [ ] Module benchmarks internationaux
- [ ] Visualisations dédiées (heatmap, treemap)

#### Sprint 7-8 V3 — Agents prospectifs Claude Agent SDK (2 semaines)
- [ ] Setup Claude Agent SDK
- [ ] Agent investigation métier émergent (avec tools : web search, code exec)
- [ ] Agent synthèse multi-sources
- [ ] Endpoint API pour déclencher agents depuis dashboard
- [ ] Documentation use cases V3

#### Sprint 9-10 V3 — Rapport prospectif 100-150 pages (2 semaines)
- [ ] Builder rapport approfondi V3 (prospectif)
- [ ] Templates dédiés (livrable Présidence + bailleurs)
- [ ] Génération du premier rapport complet pour livraison
- [ ] Migration Neon Scale tier
- [ ] Migration Vercel Pro

---

## 18. INDICATEURS DE SUCCÈS

### 18.1 KPIs techniques

| KPI | Cible V1 | Cible V2 | Cible V3 |
|---|---|---|---|
| Volume offres scrapées / mois | 800-1500 | 3000-5000 | 15-30K |
| Volume offres extraites / mois | 700-1300 | 2500-4500 | 13-27K |
| Taux confidence ≥ 0.75 | ≥ 90% | ≥ 92% | ≥ 95% |
| Coût IA / 1000 offres | < $20 | < $18 | < $15 |
| Temps total pipeline scrape + extract | < 2h | < 6h auto | < 12h auto |
| Couverture tests algorithmes | > 70% | > 80% | > 85% |
| Taux d'erreur sources | < 10% | < 8% | < 5% |
| Uptime API FastAPI | — | > 99% | > 99.5% |

### 18.2 KPIs politiques (les plus importants)

| KPI | Cible mois 1-3 | Cible mois 4-6 | Cible mois 7-12 |
|---|---|---|---|
| Présentation OCTAO V1 à la ministre | ✅ Mois 1-2 | — | — |
| Citations OCTAO dans documents officiels MESRS | 0 | 1-2 | 5+ |
| Doyens onboardés sur portail V2 | — | 5 | 15+ |
| Ministres UEMOA touchés (au-delà GN) | — | 1 | 3 |
| Première convention/contrat SYLI ↔ MESRS | Espéré | Cible | Idéal signé |
| Couverture presse / événements (GITEX, etc.) | 1 mention | 3 mentions | 10+ mentions |
| Téléchargements datasets GitHub | 50 | 500 | 2000+ |
| Stars GitHub `octao-datasets` | 10 | 100 | 500+ |

### 18.3 KPIs business SYLI Technology

| KPI | Mois 6 | Mois 12 |
|---|---|---|
| Pipeline opportunités B2G identifiées | 3 ministères | 8 ministères |
| Devis envoyés | 2 | 6 |
| Contrats signés | 0-1 | 1-3 |
| Revenus annuels OCTAO B2G | $0 (phase démonstration) | $50-200K (premiers contrats) |

---

## 19. ROADMAP V2+

### 19.1 Vision 24 mois

```
Mois 1-2     │ V1 LOCAL livrée → Première présentation Ministre Sidibé
Mois 3       │ Itérations V1 selon retours cabinet
Mois 4-5     │ V2 LIVE livrée → Onboarding 5 doyens guinéens
Mois 6       │ Présentation V2 ministres UEMOA (Sénégal en priorité)
Mois 7-8     │ V3 PRODUCTION + agents en développement
Mois 9-10    │ V3 livrée → Rapport "Métiers d'avenir 2030"
Mois 11-12   │ Premier contrat institutionnel signé (cible)
Mois 13-18   │ Extension à 4 pays UEMOA actifs
Mois 19-24   │ Ouverture B2G hors UEMOA (Maroc, Sénégal, Tunisie)
```

### 19.2 Pistes d'évolution post-V3

| # | Évolution | Justification |
|---|---|---|
| E1 | API privée pour ministères/bailleurs | Si demande effective lors V2/V3 |
| E2 | Module "Adéquation diplômes-emploi" | Alimenter directement le MPS-32 |
| E3 | Module "Salaires & Compensation" | Indicateur d'inflation des compétences |
| E4 | Comparaison historique 2026-2030 | Mesurer impact des réformes Simandou |
| E5 | Intégration ROME français + ESCO européen | Standards internationaux comparables |
| E6 | Module "Pénuries critiques" | Alerte rouge sur métiers en sous-effectif |
| E7 | Module multilingue (anglais, arabe) | Élargissement marchés africains |
| E8 | OCTAO White Label | Vente à d'autres pays africains |

### 19.3 Stratégie SYLI Technology

OCTAO est le **produit phare V1** de SYLI Technology, mais pas le seul. Roadmap produits SYLI :

| Produit SYLI | Audience B2G | Statut |
|---|---|---|
| **OCTAO** | MESRS Guinée + UEMOA | V1 en cours |
| **SYLI Pulse** (à concevoir) | Présidence — KPIs Simandou 2040 | Roadmap 2027 |
| **SYLI Compass** (à concevoir) | Universités — accompagnement réforme curricula | Roadmap 2027 |
| **SYLI Beacon** (à concevoir) | Étudiants — orientation métiers d'avenir | Roadmap 2028 |

---

## 20. CHECKLIST PRÉ-IMPLÉMENTATION

### 20.1 Préparation administrative et juridique

- [ ] Confirmer la structure juridique d'opération (SYLI Technology vs AI5D Consulting initial)
- [ ] Statuts SYLI Technology déposés (Ltd UK ou Guinée — décision pragmatique)
- [ ] Domaines réservés : `octao.africa`, `syli.technology`, `syli.tech`
- [ ] Compte GitHub Organization `syli-technology` créé
- [ ] Compte Neon créé avec email `karamo@ai5d.technology`
- [ ] Compte Anthropic API + budget mensuel de sécurité fixé
- [ ] Compte Apify créé
- [ ] Compte Firecrawl créé (free tier suffit V1)
- [ ] Compte Render créé (V2)
- [ ] Compte Vercel créé (V2)

### 20.2 Préparation politique et relationnelle

- [ ] Liste finalisée des contacts MESRS (cabinet, DGES, comités scientifiques)
- [ ] Email professionnel `karamo@syli.technology` ou similaire configuré
- [ ] Brief 1-pager OCTAO préparé pour pitch initial
- [ ] Carnet d'adresses doyens top 10 universités guinéennes (V2)
- [ ] Veille active sur communications MESRS et Délégation Simandou

### 20.3 Préparation technique

- [ ] Mac de développement à jour (Python 3.12 installé via pyenv)
- [ ] Poetry installé globalement
- [ ] Claude Code configuré et connecté au compte Anthropic
- [ ] VS Code avec extensions Python, Pylance, Ruff
- [ ] Docker Desktop (pour Crawl4AI si besoin de containerisation)
- [ ] Compte de test sur les 4 job boards guinéens cibles
- [ ] Validation que les sites cibles sont scrapables (test manuel BeautifulSoup)
- [ ] Robots.txt vérifiés sur les 4 job boards
- [ ] User-Agent OCTAO décidé : `OCTAO-Bot/1.0 (contact@syli.technology)`

### 20.4 Préparation contenu

- [ ] Charte graphique OCTAO finalisée (document séparé)
- [ ] Logo OCTAO designé (identité visuelle distincte d'AI5D)
- [ ] Templates PPTX OCTAO créés (cohérent avec charte)
- [ ] Templates DOCX OCTAO créés (briefing)
- [ ] Template HTML/CSS OCTAO créé (rapports PDF)
- [ ] Méthodologie OCTAO rédigée (4-5 pages, document public)
- [ ] FAQ anticipée pour les questions ministre/cabinet

### 20.5 Validation pré-développement

- [ ] PRD v1.1 lu et validé par Karamo (ce document)
- [ ] Charte graphique OCTAO validée (à produire après ce PRD)
- [ ] Stack technique confirmée (✅ fait dans ce PRD)
- [ ] Phasage 3-4 semaines V1 validé
- [ ] Budget V1 ($15-20/mois) confirmé
- [ ] Stratégie de pitch ministériel V1 préparée

---

## 21. ANNEXES

### 21.1 Glossaire

| Terme | Définition |
|---|---|
| **MPS-30** | Projet de cartographie des compétences et métiers — réforme MESRS Guinée |
| **MPS-32** | Projet de révision des contenus pédagogiques — réforme MESRS Guinée |
| **MESRS** | Ministère de l'Enseignement Supérieur et de la Recherche Scientifique |
| **DGES** | Direction Générale de l'Enseignement Supérieur |
| **Simandou 2040** | Programme stratégique national guinéen de transformation économique |
| **UEMOA** | Union Économique et Monétaire Ouest-Africaine |
| **Compétence ghost** | Compétence demandée par le marché mais absente des cursus universitaires |
| **Métier d'avenir** | Métier émergent dans les marchés matures, peu présent dans le marché guinéen, à anticiper |
| **JobExtraction** | Schéma Pydantic structuré décrivant une offre d'emploi extraite par IA |
| **Pydantic AI** | Framework Python d'extraction structurée par LLM (équipe Pydantic) |
| **Claude Agent SDK** | SDK Anthropic pour construire des agents Claude autonomes (V3 OCTAO) |
| **Crawl4AI** | Bibliothèque Python OSS de scraping pour sites HTML simples |
| **Firecrawl** | Service cloud de scraping pour sites JS complexes |
| **Apify** | Plateforme cloud d'acteurs de scraping (LinkedIn, etc.) |
| **Better Auth** | Bibliothèque d'auth moderne pour applications JavaScript/TypeScript |
| **OpenAPI** | Standard de spécification d'API REST permettant codegen automatique |
| **Job Type (Tech-Core/Adjacent/Enabled/Non-Tech)** | Classification d'Alexey Grigorev sur le degré d'intensité tech d'un métier |

### 21.2 Inspirations méthodologiques

#### Alexey Grigorev — DataTalks.Club

OCTAO s'inspire fortement de la méthodologie d'Alexey Grigorev sur l'analyse du marché de l'emploi data/AI :

| Apport Alexey Grigorev | Application dans OCTAO |
|---|---|
| Skills + Responsibilities + Use Cases | Trois listes extraites séparément par Pydantic AI |
| Reality vs Curriculum | Algorithme `ghost_skills` |
| Job Type classification (Tech-Core/Adjacent/Enabled/Non-Tech) | Champ `job_type` du JobExtraction |
| Transparence radicale | Méthodologie publique + datasets ouverts GitHub |
| Open data community | Repo `syli-technology/octao-datasets` public, CC-BY 4.0 |

**Différences clés OCTAO vs Alexey :**
- Alexey est centré data/AI ; OCTAO est multi-secteurs (toutes les 13 familles)
- Alexey est mondial ; OCTAO commence par la Guinée puis UEMOA
- Alexey vise la communauté ; OCTAO vise les décideurs publics
- Alexey publie sur LinkedIn ; OCTAO produit des livrables institutionnels formels

### 21.3 Références externes utiles

| Référence | URL / Source | Usage |
|---|---|---|
| ROME (Pôle Emploi) | francetravail.io | Référentiel français des métiers (mapping `JobRole.rome_code`) |
| ESCO (UE) | ec.europa.eu/esco | Référentiel européen des compétences |
| ISCO-08 (OIT) | ilo.org/isco | Classification internationale type des professions |
| O*NET (USA) | onetonline.org | Référentiel américain des métiers + compétences |
| Communiqué MESRS du 27 avril 2026 | Site officiel MESRS Guinée | Genèse politique d'OCTAO |
| Programme Simandou 2040 | Délégation Simandou | Cadre stratégique de référence |
| Pydantic AI | ai.pydantic.dev | Documentation framework |
| Claude Agent SDK | docs.claude.com | Documentation pour V3 |

### 21.4 Décisions architecturales clés (Architecture Decision Records — ADR résumés)

| ADR # | Décision | Justification |
|---|---|---|
| ADR-1 | V1 mode local (pas de live) | Réduit time-to-market de 50%, coûts de 50% |
| ADR-2 | Neon dès V1 (pas SQLite) | Évite migration future, partage facile, gratuit |
| ADR-3 | Pydantic AI (pas LangGraph/CrewAI) | Adapté à l'extraction, pas sur-dimensionné |
| ADR-4 | Claude Agent SDK différé en V3 | Pas nécessaire en V1/V2 pour l'extraction |
| ADR-5 | FastAPI typed OpenAPI (pas tRPC) | Stack hybride Python+TS, OpenAPI standard B2G |
| ADR-6 | Pas d'ORM côté Next.js (Option 3) | DB credentials jamais sur Vercel, source unique vérité |
| ADR-7 | Better Auth (pas NextAuth) | Cohérence Miratti, OSS, magic links V2 |
| ADR-8 | Jupyter en V1 (pas Streamlit) | Suffit pour l'analyste, évite UI à jeter en V2 |
| ADR-9 | Hébergement DB Neon Frankfurt | Conformité RGPD UE, latence acceptable Afrique |
| ADR-10 | Datasets publics CC-BY 4.0 | Crédibilité scientifique + bien commun |

### 21.5 Risques identifiés et mitigations

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Sites guinéens scrapables changent leur structure | Élevée | Moyen | Tests automatiques sources, alertes en cas d'échec, scrapers résilients |
| Volume insuffisant de données en Guinée | Moyenne | Élevé | Diversification des sources (5 catégories), inclusion ONG/multilatéraux |
| Qualité d'extraction insuffisante | Faible | Élevé | Confidence scoring strict, quarantaine, tests unitaires sur fixtures |
| Coûts API Claude qui explosent | Faible | Moyen | Plafond mensuel paramétré, fallback Haiku pour normalisation |
| Refus politique de la ministre Sidibé | Moyenne | Critique | Approche méthodologique solide + livrables impeccables, plan B doyens |
| Concurrence cabinet conseil avec mandat MPS-30 | Moyenne | Moyen | Positionnement complémentaire, transparence radicale (datasets ouverts) |
| Difficulté à scrapper LinkedIn (anti-bot) | Élevée | Moyen | Délégation à Apify (acteur spécialisé maintenu), volume cible modeste |
| Attaque sur les datasets ouverts (utilisation détournée) | Faible | Faible | Licence CC-BY 4.0, anonymisation stricte, anti-spam des annonceurs |
| Dépendance Apify ou Firecrawl qui ferment | Faible | Élevé | Architecture orchestrator agnostique, possibilité de remplacement |
| Burnout solo Karamo | Moyenne | Élevé | Onboarding 1 collaborateur AI5D dès V1 stabilisée, scopes courts |

---

## ANNEXE A — CATALOGUE DE PROMPTS DE COLLECTE (V1 GUINÉE)

> Ces prompts sont conçus pour être copiés-collés dans **Claude Code** lancé depuis `~/projects/octao`. Pré-requis : MCP servers `firecrawl-mcp` et `@apify/actors-mcp-server` configurés dans `.claude/settings.json`. Chaque prompt produit un fichier `data/raw/{source}_{YYYY-MM-DD}.jsonl` au schéma de référence (cf. §6.4).

### Règles communes à tous les prompts

- **Date de collecte** : aujourd'hui en ISO 8601 UTC (ex: `2026-05-06T08:30:00Z`)
- **Schéma JSONL** : un objet par ligne, champs `source, collected_at, url, title, company?, location?, contract_type?, posted_at?, raw_html?, raw_text` (les `?` sont optionnels)
- **Encodage** : UTF-8 strict, accents français préservés
- **Idempotence** : si le fichier existe, l'écraser (l'ingestion Python dédoublonne par hash d'URL canonique)
- **Limite raisonnable** : 200 offres maximum par source par session — au-delà, paginer ou découper en plusieurs prompts thématiques

### Prompt 01 — EmploiGuinee.com (Firecrawl)

```
Utilise le MCP Firecrawl pour scraper https://www.emploiguinee.com (vérifie l'URL active au préalable). Récupère toutes les offres d'emploi des 7 derniers jours, sur la première page de résultats puis paginée jusqu'à 5 pages maximum.

Pour chaque offre, capture : titre du poste, nom de l'entreprise, ville, type de contrat, date de publication, URL canonique de l'annonce, et le texte brut complet (raw_text) de la description du poste.

Persiste le résultat dans data/raw/emploiguinee_{date_du_jour}.jsonl au schéma JSONL OCTAO (cf. §6.4 du PRD). Champ source = "emploiguinee".

À la fin, donne-moi : le nombre d'offres collectées, les éventuels échecs, et le top 5 des entreprises les plus présentes.
```

### Prompt 02 — 224jobs.com (Firecrawl)

```
Utilise Firecrawl pour scraper https://www.224jobs.com (vérifie l'URL active). Récupère les offres publiées dans les 7 derniers jours.

Schéma de sortie : data/raw/224jobs_{date_du_jour}.jsonl, champ source = "224jobs". Mêmes règles que Prompt 01.

Pagine jusqu'à 5 pages. Indique-moi le nombre total et la répartition par secteur si tu peux la déduire des intitulés.
```

### Prompt 03 — GuineeJob.com (Firecrawl)

```
Firecrawl sur https://www.guineejob.com (à valider). Offres des 7 derniers jours, 5 pages max.

Sortie : data/raw/guineejob_{date_du_jour}.jsonl, source = "guineejob". Schéma standard.
```

### Prompt 04 — LinkedIn Guinée (Apify)

```
Utilise le MCP Apify avec l'acteur `bebity/linkedin-jobs-scraper` (ou un acteur LinkedIn jobs maintenu équivalent — vérifie d'abord la liste).

Configuration :
- Localisation : "Guinée" (ajouter Conakry si l'acteur le permet)
- Mots-clés rotatifs (lance des recherches successives) : "ingénieur", "manager", "comptable", "infirmier", "juriste", "responsable", "chargé", "directeur", "coordinateur", "agent", "technicien", "consultant", "analyste", "développeur", "chef de projet"
- Période : 7 derniers jours
- Limite : 30 offres par mot-clé (soit ~450 offres au total max)

Pour chaque offre, capture les champs standards (titre, entreprise, lieu, contrat, date, URL canonique, raw_text).

Sortie : data/raw/linkedin_guinea_{date_du_jour}.jsonl, source = "linkedin". Dédoublonne par URL canonique avant l'écriture (LinkedIn renvoie souvent les mêmes offres sur plusieurs mots-clés).

Indique-moi le coût Apify estimé de la session et la répartition par mot-clé.
```

### Prompt 05 — ONG et multilatéraux (PNUD, UNICEF, OMS, BM, BAD, AFD, USAID)

```
Utilise Firecrawl pour collecter les offres "Guinée" sur les pages carrières des organisations suivantes (vérifie l'URL active de chaque) :
- PNUD Guinée (UN Jobs / UN Careers filtre Guinea)
- UNICEF Guinée (unicef.org/careers)
- OMS Guinée (who.int/careers, filtre Guinée)
- Banque Mondiale Guinée (worldbank.org/en/careers)
- BAD Guinée (afdb.org)
- AFD Guinée (afd.fr)
- USAID Guinée (usaid.gov/careers)

Pour chaque organisation, scrape les 20 dernières offres publiées localisées en Guinée. Si une organisation n'a pas d'offre Guinée active, le mentionner dans le résumé final mais ne pas écrire de ligne dans le JSONL.

Sortie unique consolidée : data/raw/ong_multi_{date_du_jour}.jsonl, source = nom de l'organisation en kebab-case (ex: "pnud", "unicef", "oms").

Donne-moi un résumé : nombre d'offres par organisation, secteurs dominants, profils les plus recherchés.
```

### Prompt 06 — ONG locales et opérationnelles (MSF, Croix-Rouge, Plan, Action Contre la Faim, ReliefWeb)

```
Firecrawl sur les pages emploi de :
- MSF (Médecins Sans Frontières) — filtre Guinée
- Croix-Rouge Guinéenne
- Plan International Guinée
- Action Contre la Faim Guinée
- ReliefWeb (reliefweb.int/jobs?country=guinea)

Schéma identique. Sortie : data/raw/ong_locales_{date_du_jour}.jsonl, source = nom kebab-case ("msf", "croix-rouge", "plan", "acf", "reliefweb").

Limite 30 offres par organisation. Mentionne les ONG inactives en commentaire (résumé final).
```

### Prompt 07 — Pages carrières mines (SMB-Winning, CBG, Rio Tinto Simfer, MMG)

```
Firecrawl sur les pages carrières des sociétés minières opérant en Guinée :
- SMB-Winning Consortium (smb-winning.com/careers ou équivalent)
- Compagnie des Bauxites de Guinée — CBG (cbg-guinee.com)
- Rio Tinto Simfer (riotinto.com/careers, filtre Guinée)
- MMG Limited (mmg.com/careers, filtre Guinée)

Cherche toutes les offres actives localisées en Guinée. Si aucune offre active, mentionne-le dans le résumé.

Sortie : data/raw/mines_{date_du_jour}.jsonl, source = nom de la société en kebab-case.
```

### Prompt 08 — Pages carrières banques (BCRG, BICIGUI, SGGuinée, Ecobank, Orabank)

```
Firecrawl sur les pages carrières / espaces RH des banques opérant en Guinée :
- BCRG (Banque Centrale)
- BICIGUI
- Société Générale Guinée
- Ecobank Guinée
- Orabank Guinée

Sortie : data/raw/banques_{date_du_jour}.jsonl, source = nom kebab-case (bcrg, bicigui, sg-guinee, ecobank, orabank).

Mêmes règles : 7 derniers jours, max 30 offres par banque.
```

### Prompt 09 — Pages carrières télécoms et énergie (Orange, MTN, Cellcom, EDG, TotalEnergies)

```
Firecrawl sur les pages carrières :
- Orange Guinée
- MTN Guinée
- Cellcom Guinée
- EDG (Électricité de Guinée)
- TotalEnergies Guinée

Sortie : data/raw/telecoms_energie_{date_du_jour}.jsonl, source kebab-case (orange-gn, mtn-gn, cellcom, edg, totalenergies-gn).
```

### Prompt 10 — Industrie et hôtellerie (SOBRAGUI, Sodas Guinée, BTP top 3, hôtels)

```
Firecrawl sur :
- Brasseries de Guinée (SOBRAGUI)
- Société Industrielle des Sodas de Guinée
- Top 3 entreprises BTP guinéennes (à identifier au préalable, par exemple via une recherche web)
- Sheraton Conakry, Noom Hotel Conakry, Kaloum Hôtel

Sortie : data/raw/industrie_hotellerie_{date_du_jour}.jsonl. Source = kebab-case par société.

Si une page carrière est absente, scrappe la page "Contact" ou la racine du site et signale-le dans le résumé.
```

### Prompt 11 — Fonction publique et institutionnel

```
Firecrawl sur :
- Site officiel de la Fonction publique guinéenne
- Portails de concours administratifs guinéens
- Pages recrutement enseignants/personnel des universités publiques (UGANC, ISSEG, ISIM, UTG, UMLK)

Sortie : data/raw/fonction_publique_{date_du_jour}.jsonl. Source = "fonction-publique" ou "concours-{nom-organisme}".

Limite : 7 derniers jours, max 30 offres par site.
```

### Prompt master — Session complète Guinée

```
Lance les Prompts 01 à 11 du catalogue OCTAO Annexe A en séquence.

Avant de commencer, crée le dossier data/raw/ s'il n'existe pas et purge les fichiers de la session précédente datant de plus de 7 jours.

Entre chaque prompt, fais un point d'étape : nombre d'offres collectées sur la session, temps écoulé, coût Apify cumulé.

À la fin, génère data/raw/_session_summary_{date_du_jour}.md avec :
- Total offres collectées par source
- Sources en échec (et raison)
- Coût Apify total
- Suggestions de prompts à ajouter ou ajuster pour la prochaine session
```

---

## FIN DU PRD v1.2

**Document validé pour implémentation.**

**Prochaines étapes :**
1. ✅ PRD v1.2 livré (ce document)
2. ✅ Charte graphique OCTAO détaillée (`Docs/Charte/CHARTE_GRAPHIQUE_OCTAO.{pdf,md}`)
3. ⏭️ Setup environnement Claude Code (PROMPT-CLAUDE-CODE-SETUP-OCTAO.md)
4. ⏭️ Configuration MCP servers Apify + Firecrawl
5. ⏭️ Première session de collecte test (Prompts 01-04 en mode dry)
6. ⏭️ Lancement Sprint 1 (modèles + ingestion + extraction)

**Contacts :**
- Karamo Sylla — `karamo@ai5d.technology` — `karamo@syli.technology` (à activer)
- SYLI Technology — `contact@syli.technology` (à activer)
- Repo développement — `github.com/syli-technology/octao-app` (privé — à créer)
- Repo datasets — `github.com/syli-technology/octao-datasets` (public — à créer)