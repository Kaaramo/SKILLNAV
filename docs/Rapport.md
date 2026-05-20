# Rapport SKILLNAV — sections rédigées par Karamo Sylla

> Skills Navigator — observatoire des compétences en Data Science et Intelligence Artificielle, par Web Mining.
> M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi.
> Auteurs : Karamo Sylla & Bachirou Konaté.
>
> Ce document regroupe les sections du rapport dont je suis l'auteur principal : conception du système (en partie), implémentation, résultats observés sur le corpus, limites et perspectives. Les sections rédigées par Bachirou — état de l'art, RGPD et éthique du scraping, étude comparative NER/communautés/forecasting, biais reconnus, comparaison aux observatoires existants — figurent dans son propre fichier.

---

## §1.4 Plan du rapport

Le rapport est organisé en huit chapitres. Le premier pose le contexte du choc de l'IA générative grand public et la problématique de l'observabilité du marché des compétences au Maroc. Le deuxième propose un état de l'art ciblé sur les briques techniques que nous mobilisons : les trois axes du Web Mining selon Liu, le NER appliqué à l'extraction de compétences, les algorithmes de détection de communautés et les modèles de prévision de séries temporelles courtes. Le troisième présente la conception du système — périmètre, architecture polyglotte, modèle de données, stratégie de collecte, RGPD. Le quatrième détaille la réalisation effective : schémas Pydantic, pipelines Python, API FastAPI, frontend Next.js. Le cinquième concentre l'étude comparative §N2 demandée par l'énoncé, avec ses quatre tableaux chiffrés. Le sixième rapporte les résultats observés sur le corpus collecté, en contrastant explicitement marché marocain et marché international. Le septième discute les limites, les biais et la robustesse de l'étude. Le huitième conclut sur les perspectives à court et moyen terme.

---

## Chapitre 3 — Conception du système

### 3.1 Périmètre

Le périmètre du projet est volontairement étroit sur les métiers et large sur les sources.

Sur les métiers, nous nous concentrons sur l'ensemble des intitulés de la Data Science et de l'Intelligence Artificielle — du Data Analyst au LLM Engineer, en passant par le ML Engineer, le MLOps Engineer, l'AI Engineer, le NLP Engineer, le Computer Vision Engineer ou le Research Scientist. Sont exclus les profils Software Developer généralistes, les DevOps sans composante machine learning, les consultants IT sans spécialisation data. Cette frontière n'est pas toujours évidente — un "Architecte Cloud Big Data" entre-t-il dans le scope ? — et nous avons donc consigné une convention écrite dans le protocole de collecte, appliquée systématiquement lors de l'audit des fiches. Quand le doute persistait, nous tranchions plutôt vers l'inclusion : il est plus instructif d'avoir une fiche borderline annotée que de la perdre.

Sur la géographie, la priorité va au Maroc, et l'international vient en complément. Concrètement, six sources marocaines ont été mobilisées — Rekrute, LinkedIn MA, Indeed MA, Glassdoor MA, pages carrières et ANAPEC — et une source internationale, un corpus assemblé à partir de builtin.com couvrant six pays (États-Unis, Inde, Royaume-Uni, Allemagne, Pays-Bas, et une catégorie "international" résiduelle). L'idée n'est pas de prétendre à une couverture mondiale exhaustive — ce serait illusoire avec nos ressources — mais d'avoir de quoi contraster un marché émergent (le Maroc) à un marché mature et tech-centric pour situer notre observation.

Sur la période, nous couvrons trois ans, du début de la diffusion grand public des LLM jusqu'à aujourd'hui. Il faut être honnête sur un point : la densité réelle des données est très inégale dans cette fenêtre. Les fiches marocaines sont étalées sur l'ensemble de la période mais en faible volume mensuel ; le corpus international est massivement concentré sur la portion la plus récente, parce que c'est là que la collecte builtin.com a été conduite. Ce déséquilibre n'invalide pas l'analyse, mais il impose une lecture prudente des courbes temporelles, sujet que nous reprenons en §6.4.

### 3.2 Architecture polyglotte

Trois bases de données coexistent dans le système, chacune répondant à un besoin distinct.

MongoDB Atlas joue le rôle de source de vérité. C'est là que résident les 3 467 fiches collectées, dans une collection unique nommée `jobs`. Le choix d'une base documentaire pour le stockage primaire s'est imposé naturellement compte tenu de l'hétérogénéité des schémas entre sources : une fiche Rekrute ne ressemble pas à une fiche LinkedIn ni à une fiche builtin.com, et imposer un schéma relationnel rigide en amont aurait été contre-productif. Mongo nous permet de faire évoluer le modèle de document au fur et à mesure que nous comprenons mieux nos données, ce qui s'est révélé précieux pendant les phases de recovery.

Le deuxième store est Bonsai OpenSearch — choisi plutôt qu'Elastic Cloud pour son tier gratuit plus généreux et une mise en route plus simple, et pleinement compatible avec l'API Elastic au niveau des requêtes que nous utilisons. Bonsai héberge un index `skillnav_jobs` qui sert deux usages distincts. D'abord la recherche full-text via les champs `title`, `responsibilities`, `use_cases`, `focus` et `company`, avec une stratégie `multi_match` boostée sur les titres et une `fuzziness` automatique. Ensuite les agrégations rapides type "top 20 compétences par famille", qui seraient lentes en agrégation Mongo ou en SQL. Concrètement, Bonsai permet à la barre de recherche du dashboard de répondre en moins de cent millisecondes même quand l'utilisateur tape une requête approximative comme "machin lerning".

Le troisième store est Neo4j AuraDB, qui héberge le graphe de compétences. C'est ici que vivent les nœuds `Skill`, `Job`, `Company`, `SkillFamily` et les arêtes typées `REQUIRES`, `CO_OCCURS_WITH`, `POSTED_BY`, `BELONGS_TO`. Le graphe est entièrement dérivé du contenu Mongo — il est intégralement reconstructible — et il est mis à jour par un script `push_graph_to_neo4j.py` qui prend en entrée un snapshot `SkillGraph` Pydantic. Le free tier d'AuraDB ne donne pas accès à Neo4j GDS, donc tous les algorithmes que nous calculons (PageRank, Louvain, Leiden, Label Propagation) tournent côté Python avec `networkx`, `python-louvain` et `igraph` ; Neo4j est utilisé comme store de visualisation et de requêtage Cypher, pas comme moteur de calcul. Cette dissociation entre le calcul et la persistance graphe a un avantage non négligeable : nous n'avons pas à craindre les surcoûts d'un appel GDS, et le notebook 03 d'analyse graphe peut reprendre exactement les mêmes algorithmes que ceux exposés au dashboard.

Cette répartition à trois stores peut sembler luxueuse pour un projet académique. Elle s'explique par la pédagogie de l'énoncé qui demande explicitement une "architecture NoSQL hybride justifiée", et par le fait que chaque store correspond à un usage que nous avons réellement déployé. Aucune des trois bases n'est là pour la décoration.

### 3.3 Modèle de données

Le modèle de données s'organise en trois couches successives, présentes dans l'arborescence `sources/collected/`.

La première couche, `data_raw/{YYYY-MM}/*.yaml`, contient le résultat brut de l'extraction HTML → YAML pour chaque fiche. C'est la trace fidèle du signal source, conservée pour pouvoir rejouer en cas de bug d'extraction sans relancer le scraping.

La deuxième couche, `data_structured/{YYYY-MM}/*.yaml`, enrichit chaque fiche brute via Claude (modèle déterministe Opus, prompt fixé) qui produit une vingtaine de champs structurés : compétences regroupées en dix familles (`genai`, `ml`, `web`, `databases`, `data`, `cloud`, `ops`, `languages`, `domains`, `other`), classification `ai_type` à quatre valeurs (`ai-first`, `ai-support`, `ml-first`, `non-ai`), `job_family`, séniorité estimée, intitulé canonique normalisé, etc.

La troisième couche, `postings/NNNN.json`, est le pivot final, validé contre un schéma Pydantic, prêt à être ingéré dans les bases de données. C'est ce qu'on appelle dans le repo le format "DB-ready".

Cette discipline en trois couches a un coût en stockage — chaque fiche existe trois fois sur disque — mais elle a un bénéfice majeur. Si nous changeons d'avis sur une règle de classification, il suffit de relancer la couche 2 ou la couche 3 sans relancer le scraping, qui est l'étape la plus longue et la plus coûteuse. Concrètement, le passage de "non-ai" à "data-analytics" comme libellé public, ou la fusion de deux familles de compétences, se fait en quelques minutes au lieu de quelques heures.

Au-dessus de cette organisation fichiers, les schémas Pydantic v2 jouent le rôle de source de vérité unique. Les modèles principaux sont `RawJob` et `JobExtraction` côté offre, `Entity` et `NerAnnotation` côté NER, `SkillNode`, `JobNode`, `CompanyNode` et leurs arêtes côté graphe, et `SkillTimeSeries` côté séries temporelles. Tous résident dans `skillnav/schemas/` et tous les converters vers les bases de données en dérivent. Un converter explicite vers Neo4j, dans `schemas/converters/to_neo4j.py`, encapsule les sept requêtes Cypher `MERGE` paramétrées en `UNWIND` batch ; les converters vers Mongo et OpenSearch sont implicites dans les scripts d'ingestion qui transforment directement les dicts Pydantic en documents BSON ou en docs indexés.

Le contrat avec ces schémas est strict : toute modification d'un champ doit casser au type-check le converter correspondant. C'est précisément ce que nous voulons. Cela permet à Bachirou de travailler sur le pipeline graphe et à moi sur le frontend sans craindre une dérive silencieuse du modèle de données entre les deux. Quand un type bouge, mypy nous le dit avant la prod.

### 3.4 Stratégie de collecte hybride MCP

Le repo contient un sous-package `skillnav/scrapers/` avec des dossiers Rekrute, EmploiTIC, Indeed, Apify, builtin et weak_signals — mais ces dossiers ne contiennent que des fichiers `__init__.py` vides. Nous avons rapidement compris qu'écrire des scrapers Python automatisés pour chaque source consommerait à elle seule l'essentiel du temps du projet, sans rien apporter à la dimension analytique demandée par l'énoncé. Nous avons donc fait un choix méthodologique assumé : la collecte est conduite par des sessions Claude Code distinctes, pilotées par un protocole versionné (`sources/collected/COLLECTION_PROTOCOL.md` v1.0), qui mobilisent l'écosystème MCP plutôt qu'un package Python maison.

Concrètement, chaque source est attaquée avec l'outil le plus adapté à sa nature technique.

Pour les pages dynamiques avec du JavaScript lourd ou des défis anti-bot, nous utilisons **Firecrawl MCP** — c'est ce qui a permis de récupérer 72 fiches Glassdoor MA et les pages carrières du Crédit du Maroc et de Stellantis. Pour LinkedIn, nous passons par **Apify MCP** avec l'actor `linkedin-jobs-scraper` officiel ; huit runs d'Apify ont produit 207 fiches LinkedIn marocaines pour un coût d'environ quatre dollars. Pour Indeed MA, nous avons d'abord récupéré 73 URLs candidates puis lancé `misceres/indeed-scraper`, qui en a converti 67 en fiches exploitables (le reste correspondait à des offres expirées). Le statique — Rekrute — est traité par `curl` et regex Python directement, sans tooling lourd. EmploiTIC, initialement prévu dans le périmètre, a été retiré après vérification : c'est un job board algérien, hors scope MA prioritaire.

Cette stratégie hybride a une qualité essentielle qu'un package automatisé n'aurait pas : la **traçabilité humaine**. Chaque session de collecte produit un log lisible, chaque écart de qualité est immédiatement signalé, et lorsque nous avons réalisé qu'un tiers du corpus marocain initial était mal extrait (descriptions vides ou trop courtes), nous avons pu organiser une phase de recovery ciblée. Cette recovery a remonté le taux d'exploitabilité du corpus marocain de 67 % à 100 %, en réinjectant les URLs problématiques dans Apify pour Indeed et dans Firecrawl pour Glassdoor, et en éliminant 17 fiches définitivement perdues (offres expirées ou descriptions structurellement trop courtes).

Côté international, la stratégie a été différente. Plutôt que d'attaquer LinkedIn US/UK avec Apify, ce qui aurait été très coûteux à grande échelle, nous avons intégré un corpus tech existant collecté sur builtin.com et couvrant six pays. Ce corpus apporte 3 087 fiches Data/IA — ce qui change radicalement la dimensionalité du projet. Avec 381 fiches marocaines et 3 086 fiches internationales, nous pouvons faire de la comparaison entre marchés avec une base statistique correcte, là où nous aurions été coincés à quelques centaines de fiches au total si nous étions restés sur la stratégie initiale.

L'ensemble de ce protocole respecte les règles RGPD inviolables : aucune donnée personnelle de candidat n'est jamais collectée, le user-agent identifie explicitement le bot académique, le rate limit minimum est de cinq secondes sur les sources statiques, et chaque source est vérifiée robots.txt + TOS avant intégration. Les détails relèvent de §3.5, rédigée par Bachirou.

---

## Chapitre 4 — Implémentation

### 4.1 Vue d'ensemble du repository

Le repository SKILLNAV s'organise en six dossiers principaux, qui reflètent une séparation explicite des préoccupations.

Le package Python `skillnav/` (~7 000 lignes effectives) héberge les schémas Pydantic, les clients de bases de données et les pipelines de `structure_mining` et `usage_mining`. C'est la logique métier réutilisable et testable.

Le dossier `api/`, situé à la racine et distinct du package, contient l'application FastAPI avec ses routers, ses clients de bases et son pipeline NER live. C'est la couche d'exposition HTTP — elle dépend du package, mais elle a ses propres dépendances et son propre cycle de vie. Cette dualité n'est pas dogmatique, elle évite simplement que l'API devienne un fourre-tout qui mélange métier et plomberie HTTP.

Le dossier `web/` est l'application Next.js 15 avec ses neuf pages, ses composants partagés et ses données JSON pré-calculées dans `web/src/lib/`. Côté front, nous consommons soit ces JSON statiques (rapide, fiable), soit l'API directement (pour les fonctions live comme la recherche ou l'extraction NER).

Le dossier `notebooks/` regroupe sept notebooks Jupyter numérotés, qui sont à la fois le banc d'essai des pipelines et la source des figures du rapport. Le plus gros (`01_visualisations.ipynb`, 1.8 MB) est régénéré par script depuis `scripts/build_visualisations_notebook.py` — pratique "notebooks as code" que je détaille en §4.4.

Le dossier `scripts/` contient les utilitaires d'orchestration : assemblage des datasets, génération des JSON dashboard, ingestion vers Mongo et OpenSearch, push du graphe vers Neo4j, chaîne NER, génération de notebooks. Ces scripts sont volontairement courts et explicites, chacun fait une chose et la fait bien.

Le dossier `sources/collected/` matérialise les trois couches du modèle de données (`data_raw`, `data_structured`, `postings`), avec un sous-dossier par source. C'est la zone de travail "données brutes" du repo. Enfin, `data/` rassemble les exports binaires consommables : `jobs.jsonl` (6.3 MB) qui est l'export principal, `graph_nodes.csv` et `graph_edges.csv` qui sortent du pipeline structure_mining, et `data/ner/` qui stocke le gold set d'évaluation, les prédictions de chaque modèle NER, et le tableau §N2.1 chiffré.

### 4.2 Schémas Pydantic — source de vérité unique

Tous les schémas du système descendent de `pydantic.BaseModel` v2 et résident dans `skillnav/schemas/`.

Le fichier `job.py` définit `RawJob`, la fiche brute avant extraction structurée, et `JobExtraction`, la fiche après traitement IA. `JobExtraction` porte les listes `skills`, `tools`, `frameworks` et `programming_languages` séparées (et non un seul fourre-tout `skills`), une `confidence` entre 0 et 1, et un statut `extracted` ou `quarantined` selon que la confidence dépasse le seuil de 0.75. Une propriété calculée `all_technical_terms` produit l'union dédoublonnée des quatre listes, ce qui est pratique côté analyse.

Le fichier `ner.py` modélise les entités extraites. `Entity` représente un span avec son texte, son `entity_type` parmi sept valeurs canoniques (`SKILL`, `TOOL`, `FRAMEWORK`, `LANGUAGE`, `ROLE`, `MODEL`, `OTHER`), sa position dans le texte source, sa confidence, et son nom normalisé après alignement taxonomique. `NerAnnotation` représente le résultat complet d'un modèle sur une fiche, avec une propriété `technical_entities` qui filtre automatiquement les `ROLE` et `OTHER` quand on veut juste les compétences techniques. `NerComparison` est un quadruplet bert-multi / camembert / distilbert / baseline pour une même offre — c'est le pivot de l'étude §N2.1.

Le fichier `graph.py` formalise le graphe. `SkillNode` porte son nom, sa famille parmi 14 valeurs, son score PageRank, son `community_id` et son `occurrence_count`. `JobNode` représente une offre côté graphe. `CompanyNode` a été introduit après que nous nous soyons rendus compte que la dimension "qui recrute" était insuffisamment représentée — sans `CompanyNode`, il n'est pas possible de répondre à des requêtes comme "quelles compétences Capgemini cherche-t-il au Maroc". `SkillFamilyNode` et les arêtes typées `CoOccursWithEdge`, `RequiresEdge`, `BelongsToEdge`, `PostedByEdge` complètent le modèle. Le tout se compose en un `SkillGraph` qui est le snapshot complet et sérialisable du graphe en mémoire, sortie typée du pipeline structure_mining.

Le fichier `timeseries.py` traite des séries temporelles. `DataPoint` est un couple période/count, `ForecastPoint` une prédiction avec son intervalle de confiance à 95 %, `SkillTimeSeries` la trajectoire hebdomadaire d'une compétence (avec un filtre `source_filter` qui distingue "all", "morocco" et "international"), `Forecast` le résultat d'un modèle (avec son MAPE), et `ForecastComparison` les trois modèles côte à côte avec une `best_method` désignée.

Le converter `to_neo4j.py` encapsule les sept requêtes Cypher `MERGE` paramétrées, et une fonction `push_graph_to_neo4j` pousse l'intégralité du `SkillGraph` en un batch unique via `UNWIND`. C'est court — environ 140 lignes — et délibérément ennuyeux : la complexité métier est dans les schémas, pas dans la sérialisation.

### 4.3 Pipelines Python — structure_mining et usage_mining

Le sous-package `skillnav/pipelines/structure_mining/` implémente la construction et l'analyse du graphe de compétences.

Le module `graph_builder.py`, qui fait à peu près 500 lignes, est le cœur du pipeline. Il charge les postings via `analysis/loaders.py`, extrait pour chaque fiche la liste `skills_required + skills_optional` dédoublonnée, compte les co-occurrences entre paires de compétences (avec un seuil minimum de deux co-occurrences pour filtrer le bruit), dédoublonne les entreprises par leur nom canonique en minuscules, et émet à la fois un `SkillGraph` Pydantic et un `networkx.Graph` pondéré. Une particularité importante : l'inférence des 14 familles de compétences s'appuie sur un dictionnaire ordonné de mots-clés, `_FAMILY_KEYWORDS`. L'ordre compte. La famille `Agents AI` est testée avant `GenAI`, qui est testée avant `NLP` ; cela permet de bien classer "RAG" et "LangGraph" comme agents plutôt que comme NLP générique, et de ne pas voir "openai" capturé par "ai" qui aurait été trop large. Ce détail nous a coûté plusieurs allers-retours d'itération — un mot-clé "go" pour Golang capturait "google", ce qui faisait basculer toutes les fiches Google ADK/Gemini en famille `Programming`. Le commentaire dans le code mentionne explicitement cette correction.

Le module `pagerank.py` est minimal — une trentaine de lignes — il appelle `networkx.pagerank` avec un alpha de 0.85 pondéré par les co-occurrences, et écrit le score sur chaque `SkillNode` en plus de remplir le top 20 dans `GraphMetrics`.

Le module `communities.py` (environ 200 lignes) implémente les trois algorithmes de détection de communautés étudiés au §5.2 : Louvain via `python-louvain.best_partition`, Leiden via `igraph.community_leiden` (avec dix itérations et la fonction objectif `modularity`), et Label Propagation via `networkx.community.asyn_lpa_communities` avec une seed fixe pour stabiliser. La fonction `compute_all_communities` exécute les trois et écrit dans `GraphMetrics` les trois modularités ainsi que le nom de la méthode gagnante — ce qui alimente directement le tableau §N2.2.

Le sous-package `usage_mining/` est plus volumineux, cinq fichiers totalisant une trentaine de kilo-octets.

Le module `series_builder.py` construit les séries temporelles hebdomadaires des `top_n` compétences les plus fréquentes. Le choix de la granularité hebdomadaire — lundi ISO — plutôt que mensuelle s'est imposé après une première tentative en mensuel qui produisait des séries trop courtes pour le forecasting : avec quatre à cinq mois de données denses, nous n'avions qu'une poignée de points par compétence, ce qui rendait toute prévision absurde. En semaines, nous obtenons environ dix-neuf points exploitables après troncature des trois dernières semaines partiellement incomplètes, ce qui suffit à un découpage train/test de quinze contre quatre. C'est court, mais c'est ce que les données réelles permettent.

Les trois modèles de forecasting sont implémentés dans `arima_model.py`, `prophet_model.py` et `lstm_model.py` selon une interface commune `fit_<model>_auto(series, train_periods, test_periods) -> (Forecast, runtime)` et `fit_<model>_and_forecast(series, horizon) -> (Forecast, runtime)`. ARIMA s'auto-paramètre par grid search sur les triplets `(p, d, q) ∈ {0,1,2} × {0,1} × {0,1,2}`, en minimisant l'AIC sur le train ; Prophet désactive les saisonnalités annuelle et hebdomadaire (la série est déjà agrégée par semaine) et utilise un `changepoint_prior_scale` faible pour limiter le sur-ajustement ; LSTM passe par `neuralforecast` (Nixtla) avec une seule couche récurrente de seize unités, un `input_size` de six semaines et deux cents itérations — paramètres conservateurs calibrés pour des séries courtes, où un modèle plus gros ne ferait que sur-apprendre.

Le module `comparison.py` orchestre l'étude comparative §N2.3. Pour chaque compétence, il exécute en deux phases : d'abord la séquence "fit sur le train, prédire le test, calculer les métriques" pour les trois modèles, puis "refit sur toute la série, projeter quatre semaines dans le futur". La sélection du modèle gagnant par compétence se fait sur **RMSE** plutôt que sur MAPE, et c'est un choix délibéré : MAPE explose sur les zéros, qui sont fréquents dans nos séries — une compétence rare a beaucoup de semaines à zéro, et un MAPE classique devient inutilisable. MAPE reste calculé en version robuste (il ignore les `actual < 5`) mais il sert d'indicateur de lecture, pas de critère de tri.

### 4.4 Scripts d'orchestration

Le dossier `scripts/` regroupe les utilitaires qui transforment le repo en pipeline reproductible. Plutôt que d'enterrer toute la logique dans des fonctions de package, j'ai choisi d'extraire chaque étape opérationnelle en un script appelable directement, ce qui rend l'enchaînement explicite et facile à déboguer.

Le script `build_dataset.py` agrège les `postings/NNNN.json` de toutes les sources en un unique `data/jobs.jsonl` de 6.3 MB, prêt à être lu par les notebooks et par les scripts d'ingestion. Les scripts `build_dashboard_overview.py` et `build_skills_distribution.py` produisent les deux fichiers JSON consommés directement par le frontend : `dashboard_overview.json` (8.6 KB) alimente la page d'accueil avec les donuts AI-type, les top intitulés, les top employeurs et la bascule temporelle ; `skills_distribution.json` (138 KB) alimente la page `/skills` avec le catalogue de plus de 8 000 compétences indexées par origine et par famille. Ces deux fichiers sont régénérés à chaque snapshot, ce qui permet au frontend de tourner sans dépendre de l'API en lecture seule.

Côté ingestion, `scripts/ingestion/ingest_mongodb.py` pousse les fiches dans la collection `jobs` de MongoDB Atlas en gérant l'upsert sur `_id`. `scripts/ingestion/ingest_elasticsearch.py` indexe les mêmes fiches dans Bonsai OpenSearch avec les mappings adaptés : champs `keyword` pour les agrégations exactes (`origine.keyword`, `ai_type.keyword`, `job_family.keyword`) et analyseur par défaut sur les champs texte pour la recherche full-text. `scripts/push_graph_to_neo4j.py` consomme le `SkillGraph` produit par le pipeline structure_mining et le pousse via les requêtes Cypher batch du converter `to_neo4j.py`.

Une chaîne dédiée vit dans `scripts/ner/`. Le script `01_build_gold_set.py` matérialise les annotations manuelles des trente fiches du gold set (quinze françaises, quinze anglaises) sur les sept types d'entités, dans `data/ner/ner_gold_set.json`. Le script `02_run_inference.py` lance les trois modèles BERT plus GLiNER sur chaque fiche du gold set et écrit les prédictions dans `data/ner/predictions/`. Le script `03_evaluate.py` calcule les métriques de précision, rappel et F1 par modèle et produit le tableau `data/ner/tableau_n2_1.md` plus le JSON `evaluation_n2_1.json` consommé par l'endpoint `GET /api/v1/ner/comparison`. Cette chaîne est entièrement reproductible : trois commandes, dans cet ordre, et le tableau §N2.1 du rapport est régénéré déterministiquement.

Enfin, un script atypique mais précieux : `build_visualisations_notebook.py`, qui pèse 33 KB et régénère par programme le notebook `01_visualisations.ipynb`. Cette pratique — "notebooks as code" — évite l'enfer de la maintenance manuelle d'un notebook devenu trop gros pour être édité confortablement à la main (1.8 MB dans notre cas). Toute modification d'une figure passe par une mise à jour du script Python, et le notebook est régénéré déterministiquement. C'est plus disciplinant et plus reproductible que d'ouvrir Jupyter et de tripoter les cellules.

### 4.5 API FastAPI — quinze endpoints sur huit routers

L'API FastAPI vit dans le dossier `api/` à la racine du repo, distinct du package `skillnav/`. Le fichier d'entrée est `api/main.py`, lancé par `uvicorn api.main:app --reload --port 8000`, exposant la documentation interactive sur `localhost:8000/docs`. L'application est structurée autour de huit routers — `health`, `overview`, `jobs`, `skills`, `companies`, `search`, `ner`, `comparative` — tous montés sous le préfixe `/api/v1`. Au total, quinze endpoints répondent aux besoins du dashboard.

Le router `health` expose `GET /health` qui ping les trois bases (Mongo, OpenSearch, NER chargé) et renvoie un statut global `ok` ou `degraded`. C'est un endpoint trivial mais essentiel : c'est ce qui permet à un système de monitoring extérieur de vérifier la vie de l'API sans charger les modèles BERT.

Le router `overview` expose un seul endpoint `GET /overview` qui calcule en live les KPIs de la page d'accueil via trois agrégations Mongo (`$group` sur `ai_type`, sur `origine`, sur `job_family`). C'est l'endpoint le plus appelé en pratique parce que le dashboard l'utilise pour son rafraîchissement.

Le router `jobs` expose la liste paginée des offres et le détail par identifiant. La liste accepte les filtres `origine`, `ai_type`, `job_family`, `company`, plus la pagination `limit` (1 à 100) et `skip`. Le détail (`GET /jobs/{job_id}`) renvoie toutes les listes de compétences par famille, les responsabilités, les use cases, le focus et l'origine.

Le router `skills` expose deux endpoints. `GET /skills/top` agrège les compétences par famille — les dix codes `genai`, `ml`, `web`, `databases`, `data`, `cloud`, `ops`, `languages`, `domains`, `other` — via un pipeline Mongo qui utilise `$reduce` et `$concatArrays` pour aplatir les listes par famille avant le `$group`. `GET /skills/{name}/jobs` retourne les offres qui mentionnent une compétence donnée via une regex insensible à la casse sur toutes les familles.

Le router `companies` expose les tops employeurs et les tops intitulés. Le router `search` s'appuie exclusivement sur Bonsai OpenSearch et propose une recherche full-text avec `multi_match` boosté sur `title^2` et `title_canonical^2`, une fuzziness automatique, et un highlight HTML qui sert directement aux mises en évidence dans le frontend (balises `<mark>` autour des termes matchés).

Le router `ner` est le plus inhabituel. Il charge en mémoire les trois modèles BERT (BERT multilingue, CamemBERT, DistilBERT) — soit environ vingt secondes au démarrage si `LOAD_NER_AT_STARTUP=true`, ou bien en lazy au premier appel — et expose `POST /ner/extract` qui prend un texte en entrée et applique la stratégie Union avec dédoublonnage case-insensitive. Le résultat liste chaque entité avec la liste des modèles qui l'ont détectée, ce qui permet au frontend d'afficher pourquoi telle entité a été retenue (par exemple "détectée par CamemBERT et DistilBERT, manquée par BERT-multi"). Une variable d'environnement `DISABLE_NER` permet de couper proprement cet endpoint sur les déploiements à faible RAM (typiquement Vercel) — les modèles BERT prennent à eux trois environ 1.5 GB de mémoire, ce qui dépasse le quota gratuit. Sur Render, où l'API tourne par défaut, ils tiennent.

Le router `comparative` sert le contenu des études §N2.1 à §N2.4. L'endpoint `GET /comparative/{section}` renvoie le JSON correspondant. Seul `n21` (NER) est branché à un fichier de données concret pour l'instant ; les sections N2.2 (communautés) et N2.3 (forecasting) attendent leur tableau définitif de Bachirou pour être branchées, et N2.4 (émergence) renvoie pour l'instant vers le notebook `01_visualisations`.

### 4.6 Frontend Next.js — neuf pages

Le frontend est construit avec Next.js 15 en App Router, TypeScript strict, et un système de composants maison plutôt que Shadcn/ui ou Tremor.

Ce choix s'est imposé pour une raison esthétique : la charte SKILLNAV — Navy 1000, Royal Blue 600, Ocre 700, typographies Fraunces serif display / Inter sans / JetBrains Mono — demande un rendu typographique éditorial qu'aucune librairie de composants génériques ne donne par défaut. J'ai préféré construire une douzaine de composants custom — `AppShell`, `KPICard`, `DonutChart`, `SkillFamilyCard`, `LineChart`, `DivergingBars`, `GapBars`, `ForceGraphMock`, `Segmented`, `ContextStrip`, `SectionRule`, `MethodFooter` — que combattre les styles par défaut d'une librairie tierce. Le poids total des composants tient en environ 30 KB côté `web/src/components/`, ce qui reste très raisonnable.

Neuf pages composent l'application.

La page d'accueil `/` est la vitrine principale du dashboard. Elle affiche quatre KPI en bandeau supérieur (offres MA, offres INTL, compétences uniques recensées, taux AI-First), deux donuts AI-type pour Maroc et International côte à côte, deux blocs top intitulés et top employeurs en pair MA/INTL, et une courbe LineChart de la bascule temporelle sur quarante-et-un mois. Toutes les données viennent de `dashboard_overview.json`, lui-même généré par `scripts/build_dashboard_overview.py`.

La page `/skills` est le catalogue exhaustif. Une colonne de filtres à gauche permet de cocher individuellement les dix familles de compétences, de sélectionner l'origine (Maroc, International, Tous), de voir les sources avec leurs proportions exactes et la période réelle de chaque sous-corpus. Le tableau central liste les compétences filtrées avec pagination, et un volet rétractable en bas affiche le top 8 par famille en pair MA/INTL — soit dix blocs comparatifs si toutes les familles sont activées.

Les sept autres pages — `/methodology`, `/forecasting`, `/graph`, `/ner`, `/quality`, `/comparative`, `/gap` — sont en place côté UI mais affichent encore des données fictives stockées dans `web/src/lib/mockData.ts`. Cette dichotomie n'est pas un défaut de conception : c'est une étape volontaire qui a permis de valider la maquette graphique complète, avec la charte SKILLNAV appliquée, avant de brancher les vraies données. Le wiring de ces pages sur les endpoints existants ou à créer est l'un des chantiers prioritaires de la suite (cf. §8.2). À titre d'exemple, la page `/forecasting` actuelle parle de "LSTM retenu MAPE 6.7 %" — ce sont des chiffres mock. Quand l'endpoint `/comparative/n23` sera branché à la sortie réelle de `comparison.py`, la page affichera le vrai vainqueur par RMSE et les vrais MAPE par compétence.

Le rendu est intégralement client-side (`"use client"` sur chaque page) — le SSR n'aurait apporté que de la complexité pour un dashboard analytique consulté depuis un poste fixe. La cible est explicitement desktop, le dark mode est activé par défaut, et chaque page se termine par un `MethodFooter` qui rappelle les paramètres méthodologiques (méthode de calcul, snapshot, taille de corpus). Cette discipline éditoriale — toute valeur affichée doit être sourcée — est inspirée des standards de la presse data plutôt que des dashboards SaaS génériques.

---

## §5.4 N2.4 Émergence de compétences — préfiguration

La quatrième sous-section de l'étude comparative §N2 porte sur la détection de compétences émergentes. Il faut être franc : nous n'avons pas conduit une étude comparative complète comme pour le NER ou le forecasting, avec trois algorithmes confrontés sur un protocole partagé.

À la place, nous avons préfiguré l'analyse via une **heuristique pondérée**, implémentée dans le notebook `01_visualisations.ipynb` à la section IV.10. Le score d'émergence d'une compétence combine trois signaux : la pente de la régression linéaire sur les volumes hebdomadaires (composante de tendance), le rapport entre les volumes des trois derniers mois et la moyenne historique (composante de récence), et le volume total brut (composante de poids, qui pénalise les compétences anecdotiques). Les coefficients de la combinaison sont calibrés à la main sur une liste de quinze compétences manifestement émergentes (LangChain, vLLM, MLflow Models Serving, Pinecone, MCP, DSPy, Cursor, etc.) et quinze compétences manifestement stables (Python, SQL, pandas, scikit-learn, Docker).

Les deux autres approches qu'envisageait initialement le projet — un classifieur supervisé XGBoost entraîné sur des annotations émergent/établi/déclinant, et un clustering KMeans sur les trajectoires temporelles normalisées — n'ont pas été développées dans le temps imparti. Elles restent des pistes pour la V1.5.

Cette honnêteté coûte un peu en ambition affichée, mais elle est préférable à une étude comparative fantôme dont les chiffres ne seraient pas tracés à un notebook. Le score d'émergence heuristique reste utile pour la lecture marché : il classe sans ambiguïté LangChain, RAG, MCP, vLLM en tête, et confirme que Python et SQL ne sont pas "émergents" même si leur volume absolu est massif.

---

## Chapitre 6 — Résultats observés

### 6.1 Volumétrie et qualité de la collecte

Le corpus exposé sur le dashboard contient **3 467 fiches** d'offres d'emploi, dont 381 marocaines et 3 086 internationales.

Sept sources ont contribué. Côté Maroc : LinkedIn MA (207 fiches), Glassdoor MA (72), Indeed MA (67), Rekrute (27), pages carrières marocaines (6), ANAPEC (2). Côté international : un corpus tech assemblé à partir de builtin.com (3 087 fiches) couvrant six pays — États-Unis avec 1 381 fiches, Inde 835, Royaume-Uni 283, Allemagne 53, Pays-Bas 40, et une catégorie internationale résiduelle de 495 fiches.

Au total, 1 522 entreprises distinctes apparaissent comme employeurs — 147 marocaines et 1 378 internationales — ce qui montre que la concentration sur quelques grands groupes est modérée des deux côtés. Le nombre de compétences uniques recensées est de 8 082, dont 252 spécifiques au Maroc et 7 951 spécifiques à l'international. Cet écart d'un ordre de grandeur reflète à la fois la taille des corpus et la diversification du vocabulaire technique : un Data Scientist marocain mentionne typiquement Python, SQL, Power BI, scikit-learn ; un AI Engineer américain mentionne LangChain, vLLM, MCP, Pinecone, DSPy, RAG, fine-tuning, RLHF, MLOps Models Serving... La sur-représentation lexicale du corpus international est aussi une observation, pas un biais à corriger.

Onze intitulés de poste canoniques sont identifiés au total dans le corpus : Data Analyst, Business Analyst, Data Scientist, Data Engineer, ML Engineer, MLOps Engineer, AI Engineer, NLP Engineer, CV Engineer, LLM Engineer, Research Scientist. La couverture est inégale selon l'origine — dix sur onze côté Maroc, huit sur onze côté international (le corpus builtin étant focalisé "AI Engineer" au sens large, il manque mécaniquement quelques intitulés Data Science classiques).

Sur la qualité de l'extraction, une métrique pratique mérite d'être soulignée : après la phase de recovery décrite en §3.4, **100 %** des 381 fiches marocaines ont une description textuelle exploitable d'au moins 200 caractères significatifs, contre 67 % avant recovery. Sur l'international, la qualité est nativement haute parce que builtin.com ne publie pas de fiches stubs sans description.

### 6.2 Distribution AI-type Maroc vs International

L'observation la plus marquante du projet tient en quelques chiffres. Le champ `ai_type`, attribué par Claude lors de la phase 2 de structuration, classe chaque offre dans une de quatre catégories : `ai-first` (l'offre est centrée sur des modèles IA, typiquement LLM ou modèles avancés), `ai-support` (l'offre soutient un produit IA sans être centrée sur les modèles, par exemple un AI Solutions Architect ou un Customer Engineer AI), `ml-first` (l'offre concerne du Machine Learning classique en production), et `non-ai` (l'offre relève en réalité du Data Analytics, BI, ou Data Engineering sans composante IA). La distribution est radicalement différente entre les deux marchés.

Au Maroc, sur 381 offres : **54.1 %** classées Data Analytics, **33.9 %** ML-First, **12.1 %** AI-First. Pas une seule offre AI-Support. Autrement dit, plus d'une offre sur deux qui se présente comme une offre "Data/IA" est en réalité une offre de Business Intelligence ou d'Analyse de données traditionnelle ; un tiers concerne du Machine Learning classique (scikit-learn, XGBoost, régression, scoring) ; et seul un peu plus d'un dixième concerne réellement de l'IA générative ou de la mise en production de modèles IA.

À l'international, sur 3 086 offres : **73.1 %** AI-First, **24.0 %** AI-Support, **2.1 %** ML-First, zéro Data Analytics. La quasi-totalité du corpus est donc directement liée à l'IA générative ou à son écosystème immédiat.

L'écart sur la catégorie AI-First est de **61 points** entre les deux marchés. C'est un chiffre considérable, et il a une lecture qualitative claire : **le marché marocain n'a pas, à ce jour, basculé sur la GenAI**. Les emplois Data/IA proposés au Maroc relèvent encore très majoritairement du monde pré-LLM — Power BI, Tableau, dashboards, ML classique en production, ETL. Cette différence n'est pas un défaut de collecte : elle est l'observation principale du projet, et elle motive à elle seule la valeur d'un observatoire dédié au marché marocain.

### 6.3 Top compétences et top employeurs par origine

Les classements de tête confirment cette lecture.

Côté intitulés de poste, le marché marocain est dominé par **Data Analyst** (37 offres), **Data Scientist** (30) et **Data Engineer** (23), avec à peine quatre offres d'AI Engineer. Le marché international au contraire est massivement piloté par les rôles AI : AI Engineer (148), Senior AI Engineer (98), Applied AI Engineer (45), AI/ML Engineer (32), Lead AI Engineer (29), Staff AI Engineer (27), Senior AI/ML Engineer (25), Principal AI Engineer (22). Le mot "AI" apparaît dans les huit premiers intitulés du marché international ; il n'apparaît qu'en quatrième position au Maroc, et encore très marginalement.

Côté employeurs au Maroc, le tableau est dominé par des sociétés de service et des banques : BROME Consulting & Technology (23 offres), Capgemini (20), ALTEN (18), CIH Bank (14), Agoda (12), ALTEN Maroc (9), Odixcity Consulting (8). Les sociétés tech pure-play et les scale-ups sont sous-représentées, ce qui correspond à la structure réelle de l'écosystème tech marocain — où l'essentiel de l'embauche tech transite par les SSII et les grandes entreprises bancaires ou télécom. Côté international, on retrouve des employeurs caractéristiques du marché AI américain : Capital One (56), Citi (39), Jack & Jill AI (37), Optum (32), Thomson Reuters (29), G2i (28), NVIDIA (24), Wolters Kluwer (20). Le mélange entre grandes financières, scale-ups AI (G2i, Jack & Jill) et infrastructure hardware (NVIDIA) est révélateur de la maturité du marché.

Côté compétences, la divergence par famille est elle aussi parlante. Sur le top 5 de la famille GenAI, le Maroc cite Python, Hugging Face, LangChain, prompt engineering et OpenAI ; l'international cite LangChain, RAG, GPT, prompt engineering et embedding. Sur le top 5 MLOps, le Maroc cite Docker, Git, Kubernetes, MLflow, CI/CD ; l'international cite Kubernetes, Docker, MLflow, model deployment et model monitoring. Sur le top 5 BI & Analytics, le Maroc cite Power BI, Tableau, Excel, SAS — l'international ne cite quasiment rien dans cette famille, qui y est marginale.

### 6.4 Bascule temporelle — lecture critique

La courbe de bascule temporelle exposée sur la page d'accueil du dashboard montre une explosion de la catégorie AI-First à partir de la portion la plus récente de la période d'observation : 494, 729, 583, 469 puis 21 offres sur cinq mois consécutifs. Il serait tentant d'y voir le signe d'une bascule brutale du marché vers la GenAI. La réalité est plus nuancée, et il faut le dire clairement.

Le corpus international, qui représente l'essentiel des offres AI-First (2 257 sur 2 303 au total), provient d'une collecte concentrée sur les mois les plus récents — il a été assemblé en une opération unique sur builtin.com. Avant cette fenêtre, le corpus est dominé par les 381 fiches marocaines réparties sur l'intégralité des trois ans, soit environ une dizaine d'offres marocaines par mois en moyenne. La courbe qui semble plate puis qui explose ne reflète donc pas tant une bascule du marché qu'un changement de **composition du corpus** dans le temps.

Cette précision est essentielle et elle figure explicitement sur le dashboard lui-même, en mention sous le graphique. Il aurait été facile de présenter cette courbe comme une preuve de bascule structurelle ; nous préférons être honnêtes sur ses limites. Cela ne supprime pas la valeur de l'observation §6.2 — la distribution AI-type contrastée entre marchés est, elle, indiscutable parce qu'elle compare des distributions à corpus comparables — mais cela invalide l'usage de la courbe temporelle comme preuve indépendante d'une accélération récente.

Une V1.5 du projet, avec une collecte rétrospective équilibrée par mois et par origine, permettrait de produire une vraie courbe temporelle interprétable. Pour l'instant, la courbe doit être lue comme une illustration de la composition du corpus, pas comme une mesure d'évolution réelle du marché.

### 6.5 Communautés de compétences et PageRank

Le pipeline `structure_mining` produit le graphe Skill ↔ Skill complet et calcule sur ce graphe le PageRank ainsi que les trois partitionnements en communautés. Les résultats sont accessibles en CSV dans `data/graph_nodes.csv` (1.1 MB) et `data/graph_edges.csv` (3.5 MB), et sont reproductibles par la commande `python -m skillnav.pipelines.structure_mining`.

Les vingt compétences au plus haut PageRank émergent comme les **pivots** du marché : ce sont les compétences qui se co-occurrent le plus avec d'autres compétences importantes. Sans surprise, Python, SQL, machine learning, deep learning et les services cloud (AWS, GCP, Azure) dominent ce classement, parce qu'elles sont mentionnées dans la quasi-totalité des offres tech. Plus intéressant : LangChain, PyTorch et Hugging Face apparaissent dans le top 20, ce qui confirme leur statut d'écosystème central de la GenAI moderne. Et plus parlant encore, Power BI et Tableau entrent dans le top 20 — non pas parce qu'ils sont centraux à l'IA générative, mais parce qu'ils sont massivement présents dans le corpus marocain ML/Analytics qui contribue lourdement aux co-occurrences via les fiches MA.

Du côté des communautés détectées par Louvain (le partitionnement retenu pour l'affichage côté dashboard), la lecture qualitative est cohérente avec les 14 familles inférées par le dictionnaire de mots-clés du `graph_builder`. On distingue clairement un cluster GenAI/Agents (LangChain, RAG, LLM, OpenAI, embedding, prompt engineering), un cluster MLOps (Docker, Kubernetes, MLflow, CI/CD, model deployment), un cluster Data Engineering (Spark, Airflow, dbt, Kafka, Snowflake), un cluster ML classique (scikit-learn, XGBoost, random forest, supervised learning), un cluster Cloud (AWS, GCP, Azure, S3, SageMaker, Vertex AI) et un cluster BI & Analytics dominé par les outils marocains (Power BI, Tableau, Excel, SAS, dashboards).

La séparation entre ce dernier cluster et le cluster GenAI est particulièrement nette : les compétences BI marocaines ne se co-occurrent quasiment jamais avec les compétences GenAI internationales, ce qui matérialise géométriquement la dichotomie observée en §6.2. Vu autrement, la modularité du graphe est en partie le reflet géographique du gap AI-First.

Les valeurs chiffrées de la modularité Louvain ainsi que le tableau §N2.2 complet, qui compare Louvain, Leiden et Label Propagation sur ce même graphe, sont rédigés par Bachirou en §5.2.

---

## §7.1 Limites assumées

Plusieurs limites doivent être assumées en toute transparence.

La première est la **volumétrie marocaine modeste**. Trois cent quatre-vingt-une fiches sont un échantillon utile mais réduit. Les pourcentages et trajectoires affichés pour le marché marocain doivent être lus comme indicatifs et non comme représentatifs de l'ensemble du marché national. Cette limite est partiellement compensée par la diversité des six sources mobilisées, qui évite la mono-source — mais elle reste réelle, et elle se traduit notamment par une vulnérabilité aux variations échantillonnales sur les classements de tête (un employeur qui poste deux ou trois offres de plus modifie significativement son rang).

La deuxième est l'**asymétrie temporelle du corpus**. Comme expliqué en §6.4, les trois mille fiches internationales viennent quasi-exclusivement d'une fenêtre courte de quatre à cinq mois sur builtin.com. Lorsque le rapport mentionne une "période d'observation de trois ans", il faut garder à l'esprit que le poids des données est très inégalement réparti dans cette fenêtre. Toute lecture longitudinale de l'évolution INTL est donc à manier avec prudence, et la courbe de bascule temporelle est explicitement annotée comme une lecture de composition du corpus plutôt que d'évolution du marché.

La troisième concerne le **gold set NER** : trente fiches annotées par deux personnes, sans calcul de Cohen's kappa formel pour mesurer l'accord inter-annotateurs. Une convention écrite a été suivie (sept types d'entités, schéma BIO strict) et les désaccords ont été résolus par discussion ; mais le volume est trop faible pour produire une mesure d'IAA fiable. Cette limite affecte la précision des F1 reportés au tableau §N2.1 — il faut considérer ces chiffres comme des ordres de grandeur, pas comme des mesures à 0.01 près.

La quatrième est l'**absence d'implémentation du volet curricula ENSA**. Le projet avait prévu un deuxième axe analytique — comparer les compétences demandées par le marché aux compétences enseignées par les huit ENSA marocaines proposant une filière Data/IA — et un pipeline `curriculum_mining` correspondant. Ce pipeline n'a pas été développé dans le temps imparti. La page `/gap` du dashboard affiche actuellement des valeurs fictives ; la véritable étude est repoussée en V1.5. Cette limite est d'autant plus regrettable que le volet curricula aurait fourni un récit complémentaire fort : non seulement le marché marocain ne bascule pas sur la GenAI, mais en plus la formation marocaine prépare-t-elle à ce qu'on observe ailleurs ?

La cinquième concerne le **wiring partiel du frontend**. Sur les neuf pages déployées, sept utilisent encore des données fictives pour leurs visualisations principales. Les pages `/`, `/skills` et l'endpoint live `POST /ner/extract` sont opérationnelles avec les vraies données. Les pages `/graph`, `/forecasting`, `/quality`, `/comparative`, `/methodology` et `/gap` restent à brancher sur les endpoints existants ou à créer. Le dashboard public actuel donne donc une impression de complétude qui n'est pas entièrement honnête — c'est un point sur lequel nous travaillons activement et qui figure en tête des perspectives V1.5.

Ces limites ne sont pas anecdotiques. Elles forment ensemble le périmètre réel de ce qui peut être affirmé sans réserve sur la base du travail conduit. Le reste relève de l'extrapolation et doit être présenté comme tel.

---

## §8.2 Perspectives V1.5

La V1.5 du projet vise à transformer SKILLNAV d'un démonstrateur académique en un observatoire utilisable au-delà du jury de soutenance. Quatre chantiers prioritaires sont identifiés.

Le premier est le **wiring complet du frontend**. Les sept pages encore en mock data — forecasting, graph, ner-explorer, quality, comparative, methodology, gap — doivent être branchées soit sur les endpoints API existants soit sur de nouveaux endpoints à créer. Pour `/forecasting`, il s'agit de créer un endpoint qui sert les `ForecastComparison` calculés par le notebook 04 — c'est conceptuellement immédiat. Pour `/graph`, il faut un endpoint qui sert le `SkillGraph` calculé par le pipeline structure_mining, avec une projection compacte pour ne pas envoyer 100 000 arêtes côté front (idée : top 200 nœuds par PageRank, top 500 arêtes par weight). Pour `/quality`, il faut un endpoint qui sert les métriques NER (déjà calculées) et forecasting (à exporter du notebook 04). Pour `/comparative`, l'endpoint existant est à étendre aux sections N2.2 et N2.3. Pour `/methodology` et `/gap`, ce sont des endpoints nouveaux.

Le deuxième est l'**augmentation du corpus marocain**. La cible raisonnable est de doubler le volume actuel, soit atteindre environ 800 à 1 000 fiches marocaines exploitables. Les sources identifiées et non encore exploitées sont l'AI Movement de l'UM6P (l'université Mohammed VI Polytechnique à Benguérir, qui est un foyer tech identifié), des extractions LinkedIn Casablanca plus profondes au-delà du plafond Apify, et les pages carrière des grandes entreprises tech marocaines (Inwi, Maroc Telecom, OCP, et les scale-ups). La méthodologie reste la même — collecte MCP suivant le protocole, intégration en trois couches.

Le troisième est le **pipeline `curriculum_mining`**. Concrètement, il s'agit de finir d'extraire les filières Data/IA des huit ENSA recensées (deux sur huit sont déjà entièrement extraites), de modéliser le schéma `CurriculumExtraction` Pydantic, et de produire un notebook `06_gap_analysis` qui croise le top marché et le top enseigné. Le livrable final est la page `/gap` du dashboard alimentée par de vraies données et une table des "manques critiques" — compétences fortement demandées mais peu enseignées. Cette analyse a une vraie utilité pour les directions d'écoles et c'est probablement le sous-projet à plus fort potentiel d'impact réel.

Le quatrième est un **article Medium** et un **déploiement public** sur `skillnav.ma`. L'observation centrale du projet — le gap AI-First entre marchés — mérite d'être publiée avec un récit qui rende justice aux chiffres et qui assume les limites méthodologiques. Le déploiement public, lui, est essentiellement un travail d'industrialisation (variables d'environnement, monitoring basique, sauvegarde des snapshots) qui ne pose pas de difficulté technique majeure.

Les pistes V2 — pipeline live mensuel, fine-tuning CamemBERT sur gold set étendu, agents prospectifs, extension géographique MENA — sont traitées par Bachirou en §8.3.

---

**Karamo Sylla · M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi**
