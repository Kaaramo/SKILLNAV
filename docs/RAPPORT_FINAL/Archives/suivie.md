# Suivi de rédaction - Rapport Final SKILLNAV (L5)

> Fichier de pilotage de la rédaction du rapport méthodologique final.
> Cocher chaque case au fur et à mesure que l'étape est terminée.
> Cible : `docs/RAPPORT_FINAL/RAPPORT_FINAL_WEB_MINING.md` (Markdown) puis conversion en PDF LaTeX.

**Auteur** : Bachirou Konaté
**Contributions techniques** : Karamo Sylla
**Module** : M242 Analyse de Web, ENSA-Tétouan, Pr. Imad Sassi
**Soutenance** : 28 mai 2026
**Démarrage rédaction** : 18 mai 2026

---

## Légende de statut

- [ ] Pas commencé
- [~] En cours
- [x] Terminé
- [!] Bloqué (préciser pourquoi)

---

## PHASE 0 - Préparation et cadrage

### 0.1 Cadre de travail
- [x] Confirmer le plan global du rapport (8 chapitres + annexes) avec l'utilisateur
- [x] Confirmer la cible de pagination (30 à 40 pages, validé)
- [x] Confirmer le style éditorial (académique formel, validé)
- [x] Valider la convention de citation bibliographique (auteur-date APA, validé)

### 0.2 Page de garde et front-matter
- [x] Rédiger la page de garde (titre, auteurs, ENSA-Tétouan, M242, Pr. Sassi, soutenance 28 mai 2026)
- [x] Rédiger les remerciements (encadrant, binôme, ressources)
- [~] Rédiger le résumé exécutif (placeholder en place, à finaliser après chapitre 4)
- [x] Préparer la table des matières (sommaire prévisionnel + bloc YAML `toc: true` pour génération auto LaTeX)
- [x] Préparer la liste des figures (sommaire prévisionnel + bloc YAML `lof: true`)
- [x] Préparer la liste des tableaux (sommaire prévisionnel + bloc YAML `lot: true`)
- [x] Préparer la liste des acronymes (62 entrées : NER, MAPE, RMSE, NoSQL, etc.)

### 0.3 Outillage technique
- [x] Créer la structure de section du fichier `RAPPORT_FINAL_WEB_MINING.md` (7 chapitres + 6 annexes + front-matter)
- [x] Préparer le dossier `IMAGES_RAPPORT/` (créé, vide, à peupler progressivement)
- [x] Définir la convention de nommage des images dans le rapport (réutilisation des noms existants : `fXX_*.png` marché, `n21_*.png` NER, `forecast_*.png`, `community_*.png`, `pagerank_*.png`)
- [x] Bloc YAML metadata Pandoc en tête du fichier (titre, auteurs, doc class report, A4 11pt, marges 2.5cm, biblio APA via `references.bib` + `apa.csl`)

---

## PHASE 1 - Chapitre 1 : Introduction

### 1.1 Contexte académique et scientifique
- [ ] Cadre M242 et filière SDBIA (s'appuyer sur PRD §0 et §1.1)
- [ ] Contexte explosion marché IA / Data Science depuis ChatGPT (nov. 2022)
- [ ] Désalignement formation et marché (chiffres OECD, WEF, LinkedIn)
- [ ] Image : figure de bascule du marché (f01_bascule_marche.png)

### 1.2 Problème scientifique
- [ ] Formuler les 3 questions structurantes Q1 (Content), Q2 (Structure), Q3 (Usage)
- [ ] Lier chaque question aux 3 axes Web Mining

### 1.3 Contribution
- [ ] Démonstration empirique couverture équilibrée des 3 axes sur IA / DS
- [ ] Étude comparative chiffrée par tâche (NER, communautés, forecasting)
- [ ] Particularité Maroc vs International (insight scientifique unique)

### 1.4 Plan du rapport
- [ ] Présenter la structure des 8 chapitres + annexes

### Validation chapitre 1
- [ ] Relecture binôme
- [ ] Cohérence avec PRD §1 vérifiée

---

## PHASE 2 - Chapitre 2 : État de l'art

### 2.1 Les trois axes du Web Mining
- [ ] Définitions canoniques (Liu, 2011) avec exemples historiques
- [ ] Justifier l'unicité de SKILLNAV qui couvre les trois axes

### 2.2 NER pour l'extraction de compétences
- [ ] BERT (Devlin et al., 2018)
- [ ] CamemBERT (Martin et al., 2019)
- [ ] DistilBERT (Sanh et al., 2019)
- [ ] Travaux skill extraction (SkillSpan, ESCO embeddings)

### 2.3 Détection de communautés dans les graphes
- [ ] Modularité de Newman (2006)
- [ ] Louvain (Blondel et al., 2008)
- [ ] Label Propagation (Raghavan et al., 2007)
- [ ] Leiden (Traag et al., 2019)

### 2.4 Forecasting de séries temporelles courtes
- [ ] ARIMA (Box and Jenkins)
- [ ] Prophet (Taylor and Letham, 2018)
- [ ] LSTM (Hochreiter and Schmidhuber, 1997)

### 2.5 Observatoires de compétences existants
- [ ] LinkedIn Talent Insights
- [ ] ESCO
- [ ] Lightcast (Burning Glass)
- [ ] Positionnement SKILLNAV

### Validation chapitre 2
- [ ] Relecture binôme
- [ ] Bibliographie cohérente

---

## PHASE 3 - Chapitre 3 : Méthodologie

### 3.1 Sources et collecte
- [ ] Stratégie triplet (Wayback + live + signaux faibles)
- [ ] Sources Maroc (Anapec, Rekrute, Indeed MA, LinkedIn MA, Pages carrières, Glassdoor MA)
- [ ] Sources International (intl-ai-corpus, 6 pays)
- [ ] Tableau récapitulatif volumes par source (381 MA + 3 087 INTL = 3 468)
- [ ] Architecture 3 couches uniforme (data_raw, data_structured, postings)
- [ ] Conformité robots.txt + TOS
- [ ] Source : `sources/collected/README.md` et `COLLECTION_PROTOCOL.md`

### 3.2 Architecture polyglotte NoSQL
- [ ] Justifier MongoDB comme source of truth
- [ ] Justifier Neo4j pour Structure Mining
- [ ] Justifier Elasticsearch / OpenSearch pour la recherche
- [ ] Pipeline de transmission YAML vers JSON Lines vers bases cibles
- [ ] Image : diagramme architecture (à produire ou réutiliser PRD §6.A)
- [ ] Image : capture création cluster MongoDB (`La creation du cluster MongoBB.png`)
- [ ] Image : capture ingestion MongoDB (`iungestion des données sur MongoDB.png`)
- [ ] Source principale : `docs/for Rapport/Justification_Architecture_NoSQL.md`

### 3.3 Pipeline Content Mining
- [ ] Cleaning (Crawl4AI vers markdown, langdetect, spaCy)
- [ ] Extraction Pydantic AI + Claude Sonnet 4.5
- [ ] NER comparative HF Transformers x 3
- [ ] Normalisation taxonomique (sentence-transformers, cosine >= 0.85)
- [ ] Schémas Pydantic v2 (job.py, ner.py)
- [ ] Source : `docs/NER_COMPARISON_GUIDE.md` et `skillnav/schemas/job.py`

### 3.4 Pipeline Structure Mining
- [ ] Construction du graphe Skill <-> Skill (projection co-occurrence)
- [ ] Justifier le seuil min_cooccurrence=2
- [ ] Justifier la projection plutôt qu'un graphe bipartite
- [ ] Schéma graphe Neo4j (Skill, Job, Company, SkillFamily + arcs)
- [ ] PageRank (alpha=0.85)
- [ ] Louvain, Leiden, Label Propagation
- [ ] Volumétrie Neo4j (8 934 nœuds, 40 899 relations)
- [ ] Source principale : `docs/MODELISATION_GUIDE.md`

### 3.5 Pipeline Usage Mining
- [ ] Construction séries hebdomadaires top 10 skills
- [ ] Justifier la fenêtre janv-mai 2026 et la troncature 3 dernières semaines
- [ ] Split train 15 / test 4 / horizon 4
- [ ] Modèles ARIMA, Prophet, LSTM
- [ ] Métriques RMSE, MAE, MAPE, couverture IC 95%
- [ ] Source : `skillnav/pipelines/usage_mining/comparison.py` et notebook 04

### 3.6 Data Quality Framework
- [ ] Complétude par champ Pydantic
- [ ] Bruit (titres anormalement courts, doublons SHA-256)
- [ ] Biais (langue, géo, taille employeur, plateforme)
- [ ] Approche : transparence plutôt que correction
- [ ] Note : dépend du notebook 01_data_quality (à finaliser, cf. `bachirou.md`)

### 3.7 RGPD et éthique
- [ ] Base légale art. 6.1.f intérêt légitime
- [ ] Données exclues (nom, email, téléphone, photo, profil)
- [ ] Protocole robots.txt + User-Agent identifié + rate limit 5s
- [ ] Anonymisation des exports
- [ ] Source : `docs/RGPD_DPIA.md`

### Validation chapitre 3
- [ ] Relecture binôme
- [ ] Cohérence avec implémentation vérifiée
- [ ] Images intégrées dans `IMAGES_RAPPORT/`

---

## PHASE 4 - Chapitre 4 : Résultats et étude comparative

### 4.0 Introduction du chapitre
- [ ] Annoncer les 4 études comparatives (NER, communautés, forecasting, émergence si traitée)
- [ ] Rappeler le protocole expérimental commun

### 4.1 EDA descriptive du corpus (Karamo, notebook 00 et 01)
- [ ] Volumes par origine et par source
- [ ] Distribution AI type Maroc vs International (insight ai-first 73.2% vs 10%)
- [ ] Top intitulés Maroc (f10_top_intitules_maroc.png)
- [ ] Top intitulés International (f04_top_intitules.png)
- [ ] Top compétences Maroc par famille (f11, f12)
- [ ] Top compétences International par famille (f14, f15)
- [ ] Comparaison top 20 MA vs INTL (f16_comparaison_top20_ma_vs_intl.png)
- [ ] Frameworks GenAI dominants (f05_frameworks_genai.png)
- [ ] Grand écart INTL vs MA (f06_grand_ecart_intl_vs_ma.png)
- [ ] Skills typiques Maroc (f07_skills_typiques_maroc.png)
- [ ] Recherche vs Applied (f08_recherche_vs_applied.png)
- [ ] Top employeurs Maroc (f02) et International (f03)

### 4.2 NER comparé (§N2.1)
- [ ] Protocole : gold set 30 fiches, distant supervision (Hovy et al. 2014)
- [ ] Tableau §N2.1 : BERT-multi vs CamemBERT vs DistilBERT (P, R, F1, temps)
- [ ] Image : `n21_comparaison_ner.png`
- [ ] Image : `n21_temps_inference.png`
- [ ] Discussion : pourquoi DistilBERT gagne en F1 et en vitesse
- [ ] Choix retenu V1 : DistilBERT-NER (F1 0.463, 0.15s/fiche)
- [ ] Itération GLiNER zero-shot (notebook 03_ner_improvement)
- [ ] Image : `n21_amelioration_A_seuil.png` et `n21_amelioration_recap.png`
- [ ] Source : `docs/NER_COMPARISON_GUIDE.md` et `data/ner/tableau_n2_1.md`

### 4.3 Communautés comparées (§N2.2)
- [ ] Protocole : graphe Skill <-> Skill, 3 937 nœuds, 10 324 arêtes
- [ ] Tableau §N2.2 : Louvain Q=0.295 / Leiden Q=0.298 / Label Propagation Q=0.148
- [ ] Image : `community_comparison.png` (à copier depuis `data/exports/`)
- [ ] Stabilité Label Propagation (5 runs, σ=0.0012)
- [ ] Discussion : Leiden meilleur, Louvain référence narrative
- [ ] PageRank top 20 skills centrales
- [ ] Image : `pagerank_top20.png` (à copier depuis `data/exports/`)
- [ ] Source : `docs/MODELISATION_GUIDE.md` §6 et notebook 03_graph_analysis

### 4.4 Forecasting comparé (§N2.3)
- [ ] Protocole : top 10 skills, séries hebdo, split 15/4/4
- [ ] Tableau §N2.3 : ARIMA RMSE 17.21 (5 victoires) / Prophet 17.96 (3) / LSTM 21.51 (2)
- [ ] Image : `forecast_comparison.png`
- [ ] Image : `forecast_series_top10.png`
- [ ] Image : `forecast_test_predictions.png`
- [ ] Discussion : sur séries courtes, modèles statistiques battent le deep learning
- [ ] Prédictions à 4 semaines pour les compétences pivot (RAG, Prompt engineering, etc.)
- [ ] Source : notebook 04_forecasting_comparison et `data/exports/forecast_top10.json`

### 4.5 Détection d'émergence (§N2.4)
- [ ] Statut : à confirmer (heuristique vs XGBoost vs KMeans temporel)
- [ ] Tableau §N2.4 si traité
- [ ] Sinon mentionner en "perspectives V1.5"

### Validation chapitre 4
- [ ] Tous les tableaux chiffrés, aucun TBD restant
- [ ] Toutes les figures dans `IMAGES_RAPPORT/`
- [ ] Discussion narrative ajoutée à chaque tableau

---

## PHASE 5 - Chapitres 5, 6, 7 : Discussion, Conclusion, Bibliographie

### 5. Discussion
- [ ] 5.1 Limites de l'étude (volume 3 468, biais géo, période 5 mois denses)
- [ ] 5.2 Biais reconnus (langue FR/EN, plateforme, sectoriel, genre lexical)
- [ ] 5.3 Robustesse des résultats (stabilité PageRank, sensibilité forecasts)
- [ ] 5.4 Comparaison aux travaux antérieurs (LinkedIn Talent Insights, Lightcast)

### 6. Conclusion et perspectives
- [ ] 6.1 Synthèse des contributions (couverture 3 axes, 4 études comparatives, NoSQL polyglotte, RGPD)
- [ ] 6.2 Perspectives V1.5 (fine-tuning CamemBERT, déploiement skillnav.ma, mise à jour mensuelle)
- [ ] 6.3 Perspectives V2 (extension géo, pipeline live, agents prospectifs, API publique)
- [ ] 6.4 Gap analysis curricula ENSA Maroc (si traité)

### 7. Bibliographie
- [ ] Compiler la liste finale (Liu 2011, Devlin 2018, Martin 2019, Sanh 2019, Blondel 2008, Traag 2019, etc.)
- [ ] Format de citation cohérent
- [ ] Ajouter sources web (OECD, WEF, LinkedIn Workforce, Stack Overflow Dev Survey)
- [ ] Ajouter standards techniques (MongoDB, Neo4j, Elastic docs)

### Validation chapitres 5-7
- [ ] Cohérence des limites annoncées avec les résultats du chapitre 4
- [ ] Bibliographie complète sans référence orpheline

---

## PHASE 6 - Annexes

### Annexe A - Schéma Pydantic complet
- [ ] Bloc `JobExtraction` (skillnav/schemas/job.py)
- [ ] Bloc `NerAnnotation` (skillnav/schemas/ner.py)
- [ ] Bloc `SkillGraph` (skillnav/schemas/graph.py)
- [ ] Bloc `SkillTimeSeries` + `Forecast` (skillnav/schemas/timeseries.py)

### Annexe B - ADRs (Architecture Decision Records)
- [ ] Reproduire les 10 ADRs du PRD §21.4

### Annexe C - Captures du dashboard
- [ ] À récupérer auprès de Karamo si dashboard fonctionnel
- [ ] Plan B : mentionner que le dashboard est en cours de finalisation

### Annexe D - Extraits de code représentatifs
- [ ] Pipeline NER comparatif (`scripts/ner/03_evaluate.py`)
- [ ] Builder de graphe (`skillnav/pipelines/structure_mining/graph_builder.py`)
- [ ] Calcul des communautés (`skillnav/pipelines/structure_mining/communities.py`)
- [ ] Pipeline forecasting (`skillnav/pipelines/usage_mining/comparison.py`)

### Annexe E - Liste exhaustive des sources
- [ ] Tableau récapitulatif 7 sources + protocoles
- [ ] Référence à `sources/collected/README.md`

### Annexe F - DPIA simplifiée
- [ ] Référence vers `docs/RGPD_DPIA.md`
- [ ] Synthèse en 1 page intégrée au rapport

### Validation annexes
- [ ] Chaque annexe est référencée au moins une fois dans le corps du rapport
- [ ] Pagination des annexes vérifiée

---

## PHASE 7 - Relectures et finitions

### 7.1 Relecture binôme
- [ ] Karamo relit chapitres 1, 2, 4 (parties Content Mining)
- [ ] Bachirou relit tout

### 7.2 Cohérence finale
- [ ] Vérifier qu'aucun chiffre n'est en TBD
- [ ] Vérifier que tous les figures référencées existent dans `IMAGES_RAPPORT/`
- [ ] Vérifier que toutes les références internes (vers chapitres, annexes) sont correctes
- [ ] Vérifier l'absence du caractère "—" (em dash) dans le fichier final

### 7.3 Résumé exécutif
- [ ] Rédiger en dernier (1 page, contexte + contribution + méthode + résultats + conclusion)

### 7.4 Métriques du rapport
- [ ] Compter les pages (cible 25 à 40)
- [ ] Compter les figures (cible >= 15)
- [ ] Compter les tableaux (cible >= 10)
- [ ] Compter les références bibliographiques (cible >= 20)

---

## PHASE 8 - Conversion PDF LaTeX

### 8.1 Préparation
- [ ] Choisir le template LaTeX (Pandoc + WeasyPrint, ou LaTeX direct avec classe `article` / `report`)
- [ ] Personnaliser la page de garde (logo ENSA, charte Navy + Royal Blue)
- [ ] Configurer les polices (Fraunces titres, Inter corps, JetBrains Mono code)

### 8.2 Conversion
- [ ] Conversion Markdown vers LaTeX
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
| 2026-05-18 | Phase 0 démarrée | Création du fichier de suivi |
| 2026-05-18 | Phase 0 conventions validées | Citations APA, pagination 30-40 p., style académique formel |
| 2026-05-18 | Phase 0 terminée | Squelette `RAPPORT_FINAL_WEB_MINING.md` créé : front-matter YAML Pandoc + page de garde + remerciements + résumé exécutif (placeholder) + TOC + LOF + LOT + 62 acronymes + 7 chapitres + 6 annexes en placeholders. Pages estimées : ~10 pages pour le front-matter. Le résumé exécutif sera finalisé après chapitre 4. |

---

## Points en suspens (questions à valider)

- [ ] Cible exacte de pagination (25 ou 40 pages ?)
- [ ] Inclure ou non la §N2.4 émergence dans le chapitre 4 ?
- [ ] Inclure ou non le volet curricula ENSA dans la conclusion ?
- [ ] Convention de citation : auteur-date type APA, ou numérique type IEEE ?
- [ ] Captures dashboard disponibles à la date de rédaction (statut Karamo) ?
- [ ] Notebook 01 data quality finalisé ou à intégrer "en l'état" ?

---

**Mai 2026 - Bachirou Konaté - M242 ENSA-Tétouan**
