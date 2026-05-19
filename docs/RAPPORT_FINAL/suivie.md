# Suivi de rédaction - Rapport Final SKILLNAV (L5)

> Fichier de pilotage de la rédaction du rapport. Cocher chaque case au fur et à mesure que l'étape est terminée.
> Cible : `docs/RAPPORT_FINAL/RAPPORT_FINAL_WEB_MINING.md` (Markdown) puis conversion en PDF LaTeX en toute dernière étape.
> Plan v3 validé le 18 mai 2026 : 6 chapitres, citations APA dispatchées au fil du texte, gap analysis curricula complet en section 5.1, discussion fusionnée avec conclusion.

**Auteurs :** Bachirou Konaté et Karamo Sylla
**Module :** M242 Analyse de Web, ENSA-Tétouan, Pr. Imad Sassi
**Soutenance :** 28 mai 2026
**Démarrage rédaction :** 18 mai 2026

---

## Légende de statut

- [ ] Pas commencé
- [~] En cours
- [x] Terminé
- [!] Bloqué (préciser pourquoi)

---

## Décisions structurantes actées

- [x] Plan v3 validé : 6 chapitres au lieu de 7 (suppression du chapitre état de l'art dédié)
- [x] Convention de citation : auteur-date APA, dispatchées au fil du texte plutôt que regroupées
- [x] Pagination cible : 30 à 49 pages (large pour ne pas brider le contenu)
- [x] Style éditorial : académique formel
- [x] Caractère "—" (em dash) interdit dans le rapport
- [x] Gap analysis curricula ENSA : étude complète sur les 8 ENSA, positionnée en section 5.1
- [x] Discussion fusionnée avec conclusion en chapitre 5
- [x] Chapitre 6 : annexes en premier, bibliographie à la fin
- [x] Toutes les images stockées dans `IMAGES_RAPPORT/` et référencées par chemin relatif
- [x] Squelette du rapport créé dans `RAPPORT_FINAL_WEB_MINING.md` (18 mai 2026)

---

## PHASE 1 - Chapitre 1 : Introduction et vue d'ensemble

> Cible : environ 5 pages. Présentation simplifiée mais complète des éléments importants du projet.

### 1.1 Contexte du projet
- [x] Cadre académique M242 et filière SDBIA ENSA-Tétouan
- [x] Explosion du marché IA / Data Science depuis ChatGPT (novembre 2022)
- [x] Citations WEF Future of Jobs 2025 et OECD AI Skills Outlook 2024
- [x] Question implicite : la formation Maroc prépare-t-elle au marché ?

### 1.2 Problématique et objectifs
- [x] Formuler les 3 questions structurantes Q1, Q2, Q3
- [x] Sous-questions opérationnelles pour chaque axe
- [x] Question dérivée gap analysis curricula

### 1.3 Les trois axes du Web Mining
- [x] Définition succincte (citation Liu, 2011)
- [x] Justifier l'unicité de SKILLNAV qui couvre les 3 axes
- [x] Pondération : 35 % Content, 30 % Structure, 30 % Usage, 5 % transverse

### 1.4 Architecture globale du projet
- [x] Description textuelle du pipeline en 7 étages
- [x] Stack technique (Python 3.12, Pydantic v2, MongoDB, Neo4j, OpenSearch, FastAPI, Next.js)
- [x] Mention du dashboard Next.js (8 pages) avec renvoi vers Annexe B
- [~] Image à produire : schéma architecture globale (à faire en Phase 8 conversion LaTeX)

### 1.5 Chiffres clés du projet
- [x] Tableau 1.1 récapitulatif (16 indicateurs)
- [x] Volume 3 467 fiches dépassant cible 2 000 (+73 %)
- [x] Volumétrie bases : 8 934 nœuds Neo4j, 40 899 relations, 17 indexes MongoDB
- [x] Coût total MVP : inférieur à 50 dollars

### 1.6 Organisation du rapport
- [x] Présenter brièvement les chapitres 2 à 6

### Validation chapitre 1
- [~] Relecture binôme à programmer
- [x] Cohérence avec PRD §1 vérifiée
- [~] Schéma architecture globale à produire avant conversion LaTeX

---

## PHASE 2 - Chapitre 2 : Méthodologie

> Cible : environ 12 pages. Explication détaillée et justifiée de la méthodologie de chaque partie avec schémas et images.

### 2.1 Collecte de données

#### 2.1.1 Périmètre métiers et géographique
- [x] Périmètre métiers (Data Analyst à LLM Engineer + cas frontière)
- [x] Périmètre géographique (Maroc prioritaire, International en complément)
- [x] Période d'observation (2023 à 2026, ancrage ChatGPT)

#### 2.1.2 Stratégie multi-sources
- [x] Tableau 2.1 récapitulatif des 7 sources collectées
- [x] Justification du choix de chaque source (tier, volume, méthode)

#### 2.1.3 Outils de scraping
- [x] Crawl4AI (HTML statique)
- [x] Playwright (pagination JavaScript)
- [x] Apify (LinkedIn via actor `cheap-advance-linkedin-jobs-scraper`)
- [x] Firecrawl (pages dynamiques)
- [x] Opérations de recovery détaillées (taux 84 % Indeed, 100 % Glassdoor)

#### 2.1.4 Architecture 3 couches
- [x] Présenter la structure data_raw vers data_structured vers postings (bloc code)
- [x] Justifier la symétrie scientifique Maroc / International
- [x] 4 avantages méthodologiques détaillés (alignement Bronze/Silver/Gold Databricks)
- [~] Schéma 3 couches visuel à produire en Phase 8 (option)

#### 2.1.5 Conformité RGPD et robots.txt
- [x] Base légale art. 6.1.f intérêt légitime
- [x] Données expressément exclues (nom, email, téléphone, photo)
- [x] User-Agent SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)
- [x] Rate limit 5 secondes minimum + respect Crawl-delay
- [x] Parsing robots.txt systématique + journalisation

### 2.2 Architecture des bases NoSQL polyglottes

#### 2.2.1 Justification du choix polyglotte
- [x] Principe de polyglot persistence (Sadalage & Fowler, 2012)
- [x] Exigence académique d'étude entre paradigmes NoSQL
- [x] Réalité industrielle (DB-Engines Ranking 2026, >80 % des archis prod)
- [x] Tableau 2.2 récapitulatif volumétrie 3 bases avec marges

#### 2.2.2 MongoDB Atlas comme source de vérité
- [x] 4 critères techniques justifiés (format, schéma souple, idempotence, hébergement EU)
- [x] Détail ingestion (190 docs/sec) et 17 indexes
- [x] Figure 2.1 mongodb_cluster_creation.png copiée
- [x] Figure 2.2 mongodb_ingestion.png copiée

#### 2.2.3 Neo4j AuraDB pour le graphe
- [x] Schéma graphe ASCII (4 types nœuds, 4 types arêtes)
- [x] Propriétés détaillées par type de nœud et d'arête
- [x] Volumétrie effective (8 934 nœuds, 40 899 relations, marges 4 % et 10 %)
- [~] Schéma visuel à produire en Phase 8 (option)

#### 2.2.4 OpenSearch Bonsai pour la recherche
- [x] Justifier OpenSearch via Bonsai (pérennité, licence Apache 2.0)
- [x] OpenSearch 2.19.5, index skillnav_jobs, analyzer fr_en_mixed, mapping multilingue
- [x] Ingestion 772 docs/sec via _bulk API

#### 2.2.5 Pipeline YAML vers JSON Lines vers bases
- [x] Justifier JSON Lines (standard de facto, streamable, mongoimport, _bulk, UNWIND)
- [x] Pipeline `scripts/build_dataset.py` (3 étapes, idempotent, 1 minute)

### 2.3 Pipeline Content Mining (axe 1)
- [x] 2.3.1 Cleaning (Crawl4AI markdown, fasttext-langdetect précision 98 %, spaCy fr/en/xx)
- [x] 2.3.2 Pydantic AI + Claude Sonnet 4.5, schéma JobExtraction, confidence threshold 0,75 + quarantaine
- [x] 2.3.3 NER comparatif 3 modèles HF (renvoi vers section 4.2)
- [x] 2.3.4 Canonicalisation 3 niveaux (190+ alias, 13 familles, réduction 27 %)

### 2.4 Pipeline Structure Mining (axe 2)
- [x] 2.4.1 Construction graphe Skill vers Skill par co-occurrence
- [x] 2.4.2 Justifier la projection (Cetin et al. 2023, Decorte et al. 2022)
- [x] 2.4.3 Filtrage min_cooccurrence=2 (justification chiffrée : 75k -> 10k arêtes)
- [x] 2.4.4 PageRank alpha=0.85 (Page et al., 1999)
- [x] 2.4.5 3 algorithmes communautés + bibliothèques (renvoi vers section 4.3)

### 2.5 Pipeline Usage Mining (axe 3)
- [x] 2.5.1 Construction séries hebdo ISO week, top_n compétences
- [x] 2.5.2 Justifier fenêtre janv-mai 2026, truncate 3 sem (artefact collecte)
- [x] 2.5.3 Split train 15 / test 4 / horizon 4
- [x] 2.5.4 ARIMA (Box & Jenkins 1976), Prophet (Taylor & Letham 2018), LSTM (Hochreiter & Schmidhuber 1997)
- [x] 2.5.5 Métriques (MAPE robuste, RMSE, MAE, couverture IC 95 %) + 3 raisons choix RMSE

### 2.6 Data Quality Framework
- [x] 2.6.1 Complétude par champ Pydantic (chiffres 100 %, 98 %, 92 %, 87 %, 65 %)
- [x] 2.6.2 Détection bruit (SHA-256, titres courts, descriptions <200 chars, 17 fiches éliminées)
- [x] 2.6.3 5 biais reconnus (linguistique, géographique, plateforme, sectoriel, lexical genre)
- [x] 2.6.4 Stratégie de transparence (pas de correction artificielle, page /quality)

### Validation chapitre 2
- [~] Relecture binôme à programmer
- [x] Cohérence avec implémentation Python vérifiée (sources : schémas Pydantic, pipelines, notebooks)
- [x] Toutes les images du chapitre 2 disponibles dans `IMAGES_RAPPORT/`

---

## PHASE 3 - Chapitre 3 : Analyse exploratoire du corpus

> Cible : environ 8 pages. Illustrer les tendances et commenter les graphiques importants, en se basant sur notebook `01_visualisations.ipynb`.

### 3.0 Préparation des images du chapitre
- [x] Copier 16 figures depuis `docs/figures/` vers `IMAGES_RAPPORT/`
  - [x] f01_bascule_marche.png
  - [x] f02_top_employeurs_maroc.png
  - [x] f03_top_employeurs_intl.png
  - [x] f04_top_intitules.png
  - [x] f05_frameworks_genai.png
  - [x] f06_grand_ecart_intl_vs_ma.png
  - [x] f07_skills_typiques_maroc.png
  - [x] f08_recherche_vs_applied.png
  - [x] f09_distribution_types_maroc.png
  - [x] f10_top_intitules_maroc.png
  - [x] f11_top_skills_maroc.png
  - [x] f12_competences_par_famille_maroc.png
  - [x] f13_distribution_types_intl.png
  - [x] f14_top_skills_intl.png
  - [x] f15_competences_par_famille_intl.png
  - [x] f16_comparaison_top20_ma_vs_intl.png

### 3.1 Bascule structurelle du marché après ChatGPT
- [x] Rédiger l'analyse de la figure f01
- [x] Insérer image et légende

### 3.2 Volumes et distribution
- [x] Tableau récapitulatif volumes par origine et par source (Tableau 3.1)
- [x] Sous-section 3.2.2 profils accessoires (managériaux, interface client)

### 3.3 Distribution AI type Maroc vs International
- [x] Tableau 3.2 : AI-First / AI-Support / ML-First / Data Analytics par origine
- [x] Insight clé : 73,1 % vs 12,1 % AI-First, écart 61 points

### 3.4 Top employeurs et intitulés
- [x] 3.4.1 Top employeurs Maroc (figure 3.4 = f02)
- [x] 3.4.2 Top employeurs International (figure 3.5 = f03)
- [x] 3.4.3 Top intitulés Maroc (figure 3.6 = f10)
- [x] 3.4.4 Top intitulés International (figure 3.7 = f04)

### 3.5 Top compétences par famille
- [x] 3.5.1 Compétences Maroc (figures 3.8 et 3.9 = f11, f12)
- [x] 3.5.2 Compétences International (figures 3.10 et 3.11 = f14, f15)

### 3.6 Frameworks GenAI dominants
- [x] Analyse f05 (figure 3.12) avec écosystème LangChain, LangGraph, LlamaIndex, CrewAI, AutoGen

### 3.7 Grand écart marché Maroc vs International
- [x] Analyse f06 (figure 3.13) avec top 10 écarts INTL vs MA
- [x] Quantification : LLM +47,9 pts, RAG +40,6 pts, Prompt Engineering +37,1 pts

### 3.8 Compétences typiques du marché marocain
- [x] Analyse f07 (figure 3.14) avec SQL, Spark, Power BI, Airflow

### 3.9 Profils recherche vs applied
- [x] Analyse f08 (figure 3.15) avec heuristique scoring keyword
- [x] Constat : 18,4 % recherche au MA contre 3,0 % à l'INTL

### 3.10 Comparaison top 20 MA vs INTL
- [x] Analyse f16 (figure 3.16) avec trois groupes : universelles, GenAI, Data Engineering classique

### 3.11 Synthèse : portrait du marché observé
- [x] Conclusion descriptive : INTL ai-first dominant, MA ML classique + BI traditionnel
- [x] Pont vers chapitre 4 (études comparatives) et chapitre 5.1 (gap analysis)

### Validation chapitre 3
- [~] Toutes les figures intégrées avec légende (à valider en relecture)
- [~] Cohérence des chiffres avec notebooks `00_market_analysis.ipynb` et `01_visualisations.ipynb` (chiffres extraits du notebook 00, à valider)

---

## PHASE 4 - Chapitre 4 : Études comparatives et choix justifiés

> Cible : environ 10 pages. Exposer tous les résultats et comparaisons d'algorithmes pour chaque phase (NER, communautés, forecasting).

### 4.0 Préparation des images du chapitre
- [x] Copier 4 figures NER depuis `docs/figures/` vers `IMAGES_RAPPORT/`
  - [x] n21_comparaison_ner.png
  - [x] n21_temps_inference.png
  - [x] n21_amelioration_A_seuil.png
  - [x] n21_amelioration_recap.png
- [x] Copier 2 figures graphe depuis `data/exports/` vers `IMAGES_RAPPORT/`
  - [x] community_comparison.png
  - [x] pagerank_top20.png
- [x] Copier 3 figures forecasting depuis `data/exports/` vers `IMAGES_RAPPORT/`
  - [x] forecast_comparison.png
  - [x] forecast_series_top10.png
  - [x] forecast_test_predictions.png

### 4.1 Protocole expérimental commun
- [x] Reproductibilité (seeds, versions Python et bibliothèques)
- [x] Métriques explicites par étude
- [x] Partitionnement train / test
- [x] Exécutions multiples pour algos non déterministes (Label Propagation)

### 4.2 NER : BERT-multi vs CamemBERT vs DistilBERT (§N2.1)

#### 4.2.1 Modèles comparés (motivation stratégique)
- [x] BERT-multilingual = option universelle
- [x] CamemBERT-NER = optimisée FR marché Maroc
- [x] DistilBERT-NER = légère et rapide pour corpus INTL

#### 4.2.2 Protocole
- [x] Gold set 30 fiches (8 MA + 22 INTL)
- [x] Distant supervision (Hovy et al., 2014)
- [x] Matching par sous-chaîne case-insensitive

#### 4.2.3 Résultats chiffrés
- [x] Tableau 4.1 §N2.1 (P, R, F1, temps d'inférence)
- [x] Figure 4.1 n21_comparaison_ner.png
- [x] Figure 4.2 n21_temps_inference.png

#### 4.2.4 Discussion
- [x] BERT-multi rappel très faible (0.029)
- [x] CamemBERT limité par corpus 73 % anglophone
- [x] DistilBERT gagne en F1 et vitesse

#### 4.2.5 Itération GLiNER zero-shot
- [x] Présenter l'amélioration (notebook `03_ner_improvement.ipynb`)
- [x] Figure 4.3 n21_amelioration_A_seuil.png
- [x] Figure 4.4 n21_amelioration_recap.png

#### 4.2.6 Choix retenu pour la V1
- [x] DistilBERT-NER (F1 0.463, 0.15 s/fiche)
- [x] Pistes d'amélioration (fine-tuning, ensemble, mDeBERTa)

### 4.3 Communautés : Louvain vs Leiden vs Label Propagation (§N2.2)

#### 4.3.1 Protocole
- [x] Graphe Skill <-> Skill (3 937 nœuds, 10 324 arêtes, densité 0,0013, 2 768 composantes connexes)
- [x] Seuil min_cooccurrence=2
- [x] Métrique : modularité Q de Newman (2006)

#### 4.3.2 Résultats chiffrés
- [x] Tableau 4.2 §N2.2 (Louvain 0,2943 / Leiden 0,2988 / LP 0,1476)
- [x] Figure 4.5 community_comparison.png
- [x] Note pédagogique sur les 2 782 communautés (effet des composantes isolées)

#### 4.3.3 Stabilité Label Propagation
- [x] Tableau 4.3 - 5 runs (Q moyen 0,1487, écart-type 0,0004)
- [x] Comparaison déterminisme Louvain / Leiden

#### 4.3.4 Centralité PageRank
- [x] Top 20 compétences pivot (1. prompt engineering 0,0473)
- [x] Tableau 4.4 top 10 avec score et famille
- [x] Figure 4.6 pagerank_top20.png
- [x] Insight : 7/10 compétences pivot relèvent du GenAI/Agents

#### 4.3.5 Analyse qualitative top 5 communautés Louvain
- [x] Communauté 1 GenAI (542 skills) : prompt engineering, RAG, LangChain
- [x] Communauté 2 DL/ML (291 skills) : PyTorch, TensorFlow, scikit-learn
- [x] Communauté 3 IDE-AI (146 skills) : Cursor, Copilot, Claude Code
- [x] Communauté 4 Data classique (83 skills) : Python, SQL, Power BI
- [x] Communauté 5 LLMs+compliance (23 skills) : Llama, Mistral, GDPR

#### 4.3.6 Choix retenu et perspectives
- [x] Leiden (Q max 0,2988, connexité garantie, temps 0,383s)
- [x] Louvain conservé comme référence narrative

### 4.4 Forecasting : ARIMA vs Prophet vs LSTM (§N2.3)

#### 4.4.1 Protocole
- [x] Top 10 skills, séries hebdo, split 15/4/4
- [x] RMSE comme métrique de sélection (robuste aux zéros)
- [x] MAPE robuste (mask actual >= 5), MAE, couverture IC 95 %

#### 4.4.2 Résultats agrégés
- [x] Tableau 4.5 §N2.3 (ARIMA 17,21 / Prophet 17,96 / LSTM 21,51)
- [x] Figure 4.7 forecast_comparison.png

#### 4.4.3 Détail par compétence
- [x] Tableau 4.6 RMSE par compétence pour les 10 skills
- [x] Modèle gagnant par compétence (5 ARIMA, 3 Prophet, 2 LSTM)
- [x] Figure 4.8 forecast_series_top10.png
- [x] Figure 4.9 forecast_test_predictions.png

#### 4.4.4 Discussion
- [x] Constat conforme à la littérature séries courtes
- [x] LSTM remarquable sur LangGraph et OpenAI API
- [x] Pistes d'ensembles (ARIMA + Prophet, ARIMA + LSTM ciblé)

#### 4.4.5 Choix retenu et perspectives
- [x] ARIMA en V1 (5/10 victoires, RMSE 17,21)
- [x] Perspective V1.5 : ensemble ARIMA + Prophet + LSTM ciblé

### 4.5 Synthèse comparative globale
- [x] Tableau 4.7 : axe, étude, algorithmes, métrique, choix retenu V1
- [x] Cohérence des choix pour le déploiement V1 (DistilBERT léger, Leiden rapide, ARIMA peu gourmand)

### Validation chapitre 4
- [x] Tous les tableaux chiffrés (aucun TBD)
- [x] Toutes les figures intégrées (4.1 à 4.9, 9 figures)
- [x] Discussion narrative par étude

---

## PHASE 5 - Chapitre 5 : Conclusion et perspectives

> Cible : environ 6 pages (augmenté pour intégrer le gap analysis).

### 5a - Chantier préalable : Curriculum mining ENSA Maroc

> Cette étape est bloquante pour la rédaction de la section 5.1. Volume de travail estimé : 4 à 7 jours.
> **Note importante (18 mai 2026)** : le dossier `sources/curricula/` n'existe pas encore sur disque malgré ce que dit la documentation. Tout est à construire de zéro pour les 8 ENSA.

#### Bootstrap de la structure curricula
- [x] Créer le dossier `sources/curricula/`
- [x] Créer `sources/curricula/REGISTRY.md` (index humain des 8 ENSA)
- [x] Créer `sources/curricula/registry.yaml` (index machine-lisible)
- [x] Définir le template `source.yaml` et `filiere.md` (à dupliquer pour chaque ENSA)

#### Extraction des 8 programmes ENSA
- [x] ENSA Tétouan - filière SDBIA (PDF fourni par utilisateur, complete)
- [!] ENSA Berrechid - filière ISIBD (placeholder, programme non public en mai 2026)
- [x] ENSA Khouribga - filière IID (dépliant IID 2025-2026, complete)
- [x] ENSA Oujda - filière IDSCC (page officielle ensao.ump.ma, complete)
- [x] ENSA Agadir - filière SDBDIA (page officielle ensa-agadir.ac.ma, complete)
- [x] ENSA Fès - filière ISDIA (page officielle ensaf.ac.ma, slug corrigé ISDIA au lieu de ILIA, complete)
- [!] ENSA El Jadida - filière 2ITE (placeholder, programme non public en mai 2026)
- [x] ENSA Safi - filière IDIA (PDF officiel ensas.uca.ma, complete)

#### Pipeline de mining curriculum
- [x] Créer le schéma `skillnav/schemas/curriculum.py` (CurriculumExtraction, Semester, Module) - S6 PFE exclu du Literal
- [x] Créer `skillnav/pipelines/curriculum_mining/__init__.py`
- [x] Créer `skillnav/pipelines/curriculum_mining/parser.py` (parse filiere.md vers CurriculumExtraction)
- [x] Créer `skillnav/pipelines/curriculum_mining/skill_extractor.py` (LLM Claude Sonnet 4.5 + fallback rules)
- [x] Créer `skillnav/pipelines/curriculum_mining/normalizer.py` (sentence-transformers cosine >= 0.85 + fallback substring)
- [x] Créer `skillnav/pipelines/curriculum_mining/orchestrator.py` (entry point mode auto / llm / rules)
- [x] 40 tests unitaires (schema 14 + parser 10 + extractor 16), 100 % réussite

#### Notebook 06 d'analyse comparative
- [x] Créer `notebooks/06_gap_analysis_market_vs_curriculum.ipynb` (7 cellules + synthèse markdown)
- [x] Charger les 8 CurriculumExtraction + 3 468 postings marché via `load_postings()`
- [x] Produire figure : diagramme de Venn skills enseignées vs demandées (`IMAGES_RAPPORT/gap_venn_skills.png`)
- [x] Produire figure : heatmap recouvrement par famille (`IMAGES_RAPPORT/gap_heatmap_familles.png`)
- [x] Produire tableau : top 15 compétences sous-enseignées prioritaires (`data/exports/gap_top15_sous_enseignees.csv`)
- [x] Produire tableau : top 10 compétences enseignées non demandées (`data/exports/gap_top10_sur_enseignees.csv`)
- [x] Notebook exécuté en place (178 KB avec outputs embarqués)

#### Constats chiffrés clés (Phase 5a, 2026-05-19)

- **Périmètre exploitable** : 6 ENSA sur 8 (Berrechid et El Jadida en placeholder)
- **Set A** (enseignées par >= 3 ENSA sur 6) : 46 compétences
- **Set B** (top 100 marché ET >= 10 % offres) : 7 compétences
- **Set C** (alignement A inter B) : 2 compétences
- **Set E** (sous-enseignement prioritaire) : 5 compétences, toutes GenAI ou Agents
  - RAG (30,19 % offres, 0 ENSA)
  - LangChain (20,91 % offres, 0 ENSA)
  - LLMs (17,19 % offres, 0 ENSA)
  - prompt engineering (12,57 % offres, 0 ENSA)
  - LangGraph (11,25 % offres, 0 ENSA)
- **Écart par famille (heatmap)** :
  - GenAI : 0,9 % ENSA contre 34,0 % marché (écart 33 points)
  - Agents AI : 1,9 % ENSA contre 20,5 % marché (écart 18 points)
  - Statistics : 7,4 % ENSA contre 1,0 % marché (sur-représentation académique)

### 5.1 Gap analysis ENSA Maroc vs marché

#### 5.1.1 Périmètre des 8 filières
- [ ] Présenter les 8 ENSA et leurs filières Data / IA

#### 5.1.2 Méthodologie d'extraction
- [ ] Présenter le pipeline curriculum_mining
- [ ] Justifier l'extraction manuelle vs scraping (sites web hétérogènes)

#### 5.1.3 Schéma Pydantic CurriculumExtraction
- [ ] Présenter le schéma

#### 5.1.4 Top compétences enseignées vs demandées
- [ ] Rédiger analyse du Venn
- [ ] Insérer image `IMAGES_RAPPORT/gap_venn_skills.png`

#### 5.1.5 Matrice de recouvrement par famille
- [ ] Rédiger analyse de la heatmap
- [ ] Insérer image `IMAGES_RAPPORT/gap_heatmap_familles.png`

#### 5.1.6 Compétences sous-enseignées prioritaires
- [ ] Top 15 compétences fortement demandées mais quasi absentes ENSA
- [ ] Recommandations d'évolution des maquettes

#### 5.1.7 Discussion et implications pédagogiques
- [ ] Réponse à la question : la formation prépare-t-elle au marché ?
- [ ] Limites du gap analysis (snapshot 2026, biais d'extraction, pondération horaire absente)

### 5.2 Limites de l'étude
- [ ] 5.2.1 Volume et représentativité (3 468 fiches, asymétrie MA/INTL)
- [ ] 5.2.2 Limites du gold set NER (30 fiches, distant supervision)
- [ ] 5.2.3 Limites du forecasting (séries courtes 22 semaines)
- [ ] 5.2.4 Limites du gap analysis curricula (extraction manuelle, pondération absente)

### 5.3 Synthèse des contributions
- [ ] Couverture équilibrée des 3 axes Web Mining
- [ ] 3 études comparatives chiffrées
- [ ] Architecture polyglotte NoSQL opérationnelle
- [ ] RGPD intégré dès la conception
- [ ] Gap analysis ENSA inédit dans l'écosystème francophone

### 5.4 Perspectives V1.5
- [ ] Fine-tuning CamemBERT sur gold set étendu
- [ ] Notebook 01 data quality finalisé
- [ ] Déploiement skillnav.ma
- [ ] Ensemble ARIMA + Prophet pour forecasting
- [ ] Mise à jour mensuelle automatique

### 5.5 Perspectives V2
- [ ] Extension géographique MENA
- [ ] Pipeline live (Celery + APScheduler)
- [ ] Agents prospectifs (Claude Agent SDK)
- [ ] API publique versionnée
- [ ] Partenariats avec les ENSA pour mise à jour annuelle

### Validation chapitre 5
- [x] Chantier curriculum mining terminé (6 ENSA exploitables + 2 placeholder + notebook 06)
- [ ] Cohérence des limites avec les résultats du chapitre 4
- [x] Figures gap analysis dans `IMAGES_RAPPORT/` (gap_venn_skills.png, gap_heatmap_familles.png)

---

## PHASE 6 - Chapitre 6 : Annexes et bibliographie

> Cible : environ 7 à 8 pages. Annexes en premier, bibliographie à la fin.

### Annexe A - Schémas Pydantic v2
- [x] A.1 Bloc `JobExtraction` (`skillnav/schemas/job.py`) avec enums ContractType, SeniorityLevel, JobStatus
- [x] A.2 Bloc `NerAnnotation` + `Entity` + `EntityType` + `NerComparison` (`skillnav/schemas/ner.py`)
- [x] A.3 Bloc `SkillGraph` complet avec `SkillFamily`, `SkillNode`, `CoOccursWithEdge`, `GraphMetrics`
- [x] A.4 Bloc `SkillTimeSeries` + `Forecast` + `ForecastComparison` (`skillnav/schemas/timeseries.py`)
- [x] A.5 Mention `CurriculumExtraction` (renvoi vers section 5.1.3, à créer en Phase 5a)

### Annexe B - Captures du dashboard SKILLNAV
- [~] À récupérer auprès de Karamo (statut conditionnel)
- [x] Mention de l'état de finalisation avec renvoi vers le journal de suivi Git

### Annexe C - Extraits de code représentatifs
- [x] C.1 `graph_builder.build_graph()` commenté (extraction et co-occurrence)
- [x] C.2 `communities.compute_all_communities()` commenté
- [x] C.3 `comparison.run_forecast_comparison()` commenté
- [x] C.4 `scripts/ner/03_evaluate.py` commenté

### Annexe D - Liste exhaustive des sources collectées
- [x] Tableau D.1 récapitulatif des 7 sources avec dates TOS, méthode, conformité robots.txt
- [x] Mention User-Agent SkillnavBot/1.0 et journalisation `data/audit/`

### Annexe E - DPIA simplifiée RGPD
- [x] E.1 Description du traitement (finalités, responsables)
- [x] E.2 Base légale art. 6.1.f intérêt légitime
- [x] E.3 Tableau données traitées vs données exclues
- [x] E.4 Durée de conservation (HTML 6 mois, fiches durée projet + 6 mois)
- [x] E.5 Droits des personnes (non applicables car aucune donnée personnelle), point de contact

### Annexe F - Architecture Decision Records (ADR)
- [x] 12 ADRs documentés : MongoDB, Neo4j, OpenSearch, Pydantic v2, Pydantic AI, stack scraping, Apify, projection graphe, seuil min_cooccurrence, RMSE, transparence biais, architecture 3 couches

### Annexe G - Liste des curricula ENSA extraits
- [~] Tableau à compléter à l'issue du chantier curriculum mining (Phase 5a en cours)
- [x] Structure du tableau définie et renvoi vers `sources/curricula/REGISTRY.md`

### Bibliographie
- [x] Compiler toutes les références citées au fil du texte (style APA)
- [x] 25 références au total
- [x] Articles scientifiques (Liu, Newman, Blondel, Traag, Raghavan, Devlin, Sanh, Martin, Hovy, Lample, Box & Jenkins, Taylor & Letham, Hochreiter & Schmidhuber, Cetin, Decorte, Akaike, Tjong Kim Sang)
- [x] Ouvrages (Sadalage & Fowler)
- [x] Rapports sectoriels (WEF Future of Jobs 2025, OECD AI Skills Outlook 2024)
- [x] Documentations techniques (MongoDB, Neo4j GDS, OpenSearch, Elastic NV)
- [x] Cadres réglementaires (RGPD UE 2016/679)
- [~] Vérification finale d'orphelines à effectuer en Phase 7

### Validation chapitre 6
- [~] Vérification que chaque annexe est référencée au moins une fois dans le corps du rapport (Phase 7)
- [x] Bibliographie cohérente et complète (25 références)

---

## PHASE 7 - Relectures et finitions

### 7.1 Relecture binôme
- [ ] Karamo relit chapitres 1, 2 (parties Content Mining + ingestion DB), 4 (NER), 6 (Annexes B, C dashboard et code)
- [ ] Bachirou relit tout

### 7.2 Cohérence finale
- [ ] Aucun chiffre en TBD
- [ ] Toutes les figures référencées présentes dans `IMAGES_RAPPORT/`
- [ ] Toutes les références internes (chapitres, sections, annexes) correctes
- [ ] Aucune occurrence du caractère "—" (em dash) dans le rapport
- [ ] Toutes les citations APA ont leur entrée bibliographique correspondante

### 7.3 Métriques du rapport
- [ ] Comptage des pages (cible 30 à 49)
- [ ] Comptage des figures (cible supérieur à 20)
- [ ] Comptage des tableaux (cible supérieur à 12)
- [ ] Comptage des références bibliographiques (cible supérieur à 25)

---

## PHASE 8 - Conversion PDF LaTeX

> Cette phase démarre uniquement après validation complète du contenu Markdown.

### 8.1 Préparation
- [ ] Page de garde institutionnelle finalisée (logos ENSA si disponibles)
- [ ] Front-matter (table des matières auto, liste figures, liste tableaux, liste acronymes)
- [ ] Choix du template LaTeX (classe `report`, polices charte Navy + Royal Blue)
- [ ] Configuration polices (Fraunces titres, Inter corps, JetBrains Mono code)

### 8.2 Conversion
- [ ] Conversion Markdown vers LaTeX via Pandoc
- [ ] Compilation PDF
- [ ] Vérification rendu (images, tableaux, code, références croisées)

### 8.3 Itérations
- [ ] Corrections typographiques (orphelines, veuves, alignements)
- [ ] Optimisation tailles d'images
- [ ] Pagination finale propre

### 8.4 Livraison
- [ ] Export PDF final dans `docs/RAPPORT_FINAL/RAPPORT_FINAL_WEB_MINING.pdf`
- [ ] Sauvegarde source LaTeX dans `docs/RAPPORT_FINAL/latex/`
- [ ] Commit Git avec tag de version

---

## Journal d'avancement (à remplir au fil de l'eau)

| Date | Étape | Notes |
|---|---|---|
| 2026-05-18 | Phase 0 démarrée | Création du fichier de suivi initial |
| 2026-05-18 | Plan v1 critiqué et refondu | Passage de 7 à 6 chapitres, fusion discussion/conclusion, état de l'art dispatché |
| 2026-05-18 | Plan v3 validé | 6 chapitres, citations APA dispatchées, gap analysis complet section 5.1 |
| 2026-05-18 | Squelette du rapport créé | `RAPPORT_FINAL_WEB_MINING.md` propre, focus contenu, page de garde reportée en Phase 8 |
| 2026-05-18 | Nouveau suivi créé | Ancien fichier déplacé dans `Archives/` |
| 2026-05-18 | Phase 3 terminée | Chapitre 3 (12 sections) rédigé, 16 figures copiées dans `IMAGES_RAPPORT/`, chiffres extraits du notebook 00 (3 467 fiches, AI-First 73,1 % INTL vs 12,1 % MA, écart LLM 47,9 pts). Enchaînement sur Phase 4. |
| 2026-05-18 | Phase 4 terminée | Chapitre 4 (5 sections, 7 tableaux, 9 figures) rédigé. Études comparatives §N2.1 NER (DistilBERT F1 0,463), §N2.2 Communautés (Leiden Q 0,2988), §N2.3 Forecasting (ARIMA RMSE 17,21). Chiffres recalés sur les notebooks réels (03_graph_analysis et 04_forecasting). Enchaînement sur Phase 1. |
| 2026-05-19 | Phase 5a terminée | 6 ENSA extraites sur 8 (Berrechid + El Jadida en placeholder car programmes non publics). Pipeline `skillnav/pipelines/curriculum_mining/` opérationnel (parser, skill_extractor LLM/rules, normalizer sentence-transformers, orchestrator). 8 JSON produits dans `data/curricula/`. Notebook 06 exécuté, 2 figures produites (gap_venn_skills.png, gap_heatmap_familles.png), 2 CSV exportés. Constat majeur : 5 compétences GenAI/Agents (RAG, LangChain, LLMs, prompt engineering, LangGraph) demandées par 11 à 30 % du marché mais enseignées par 0 ENSA sur 6. Écart GenAI 33 points, Agents AI 18 points. 40 tests unitaires verts. |
| 2026-05-18 | Phase 1 terminée | Chapitre 1 (6 sections, 1 tableau de chiffres clés) rédigé. Contexte M242, problématique 3 axes Q1/Q2/Q3, citation Liu (2011), architecture en 7 étages, tableau 1.1 avec 16 indicateurs clés. Enchaînement sur Phase 2. |
| 2026-05-18 | Phase 2 terminée | Chapitre 2 (6 sections, 2 tableaux, 2 figures MongoDB) rédigé. Méthodologie complète : collecte (7 sources, 3 couches, RGPD art. 6.1.f), architecture NoSQL polyglotte (Sadalage & Fowler 2012, MongoDB + Neo4j + OpenSearch), 3 pipelines axes (Content/Structure/Usage), Data Quality Framework (5 biais transparents). Toutes les références APA dispatchées (Page 1999, Box & Jenkins 1976, Cetin 2023, Decorte 2022). |
| 2026-05-18 | Phase 6 terminée | Chapitre 6 (7 annexes + bibliographie) rédigé. Annexe A schémas Pydantic v2 (4 modules), Annexe B captures dashboard (placeholder), Annexe C 4 extraits de code commentés, Annexe D tableau 7 sources avec TOS, Annexe E DPIA simplifié 5 sections, Annexe F 12 ADRs, Annexe G placeholder curricula (Phase 5a en cours). Bibliographie : 25 références APA complètes. |

---

## Points en suspens

- [ ] Statut Karamo : captures dashboard disponibles à la date de rédaction du chapitre 6 ?
- [ ] Notebook 01 data quality : finalisé en parallèle ou intégré "en l'état" en section 2.6 ?

---

**Mai 2026 - Bachirou Konaté et Karamo Sylla - M242 ENSA-Tétouan**
