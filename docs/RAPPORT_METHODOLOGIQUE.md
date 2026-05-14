# Rapport méthodologique SKILLNAV

> **Livrable L5 — M242 Analyse de Web · ENSA-Tétouan**
> Document académique distinct du PRD. Format narratif, cible 25–40 pages PDF.

**Auteur** : Bachirou Konaté
**Contributions techniques** : Karamo Sylla (captures dashboard, schémas d'architecture, ADRs, données chiffrées des études comparatives)
**Encadrement** : Pr. Imad Sassi
**Cursus** : Diplôme d'Ingénieur — filière SDBIA (Sciences des Données, Big Data et Intelligence Artificielle)
**Date de rendu** : 28 mai 2026
**Statut** : Squelette à compléter au fur et à mesure des résultats (Sprint 2 → Sprint 3)

---

## Comment utiliser ce document

Ce squelette est rédigé pour être **rempli progressivement** dès l'arrivée des premiers résultats expérimentaux (J7 environ). Chaque section comporte :

- **Plan détaillé** : sous-sections imposées par la cohérence académique
- **Pointers PRD** : référence vers la section du PRD où trouver le contenu source à transposer en ton narratif
- **TBD** : valeurs chiffrées à insérer après mesure dans les notebooks correspondants

Le document final sera converti en PDF via Pandoc + WeasyPrint en respectant la charte SKILLNAV (Navy + Royal Blue + Fraunces / Inter / JetBrains Mono).

---

## Résumé

> *(à rédiger en dernier, ~ 1 page)*

Synthèse en français : contexte, contribution, méthode, résultats principaux chiffrés, conclusion.

---

## 1. Introduction

### 1.1 Contexte académique et scientifique
*(s'appuyer sur PRD §0 + §1.1–1.2)*

Cadre du module M242 ; explosion du marché IA / DS ; désalignement formation / marché ; chiffres OECD, WEF, LinkedIn.

### 1.2 Problème scientifique
*(PRD §1.3)*

Trois questions structurantes Q1 (Content), Q2 (Structure), Q3 (Usage), reliées aux trois axes Web Mining.

### 1.3 Contribution
*(PRD §1.5)*

Démonstration empirique de la couverture équilibrée des 3 axes sur le domaine IA / DS, avec étude comparative chiffrée pour chaque tâche.

### 1.4 Plan du rapport

Brève présentation de la structure des 8 chapitres + annexes.

---

## 2. État de l'art

### 2.1 Les trois axes du Web Mining

S'appuyer sur **Liu (2011)** : définitions canoniques de Content / Structure / Usage Mining, avec exemples historiques. Insister sur l'unicité de SKILLNAV qui couvre les trois en parallèle.

### 2.2 NER pour l'extraction de compétences

État de l'art rapide :
- BERT (Devlin et al., 2018) — base de tous les modèles dérivés
- CamemBERT (Martin et al., 2019) — adaptation française
- DistilBERT (Sanh et al., 2019) — version compressée
- Travaux spécifiques skill extraction (ex. *SkillSpan*, *ESCO embeddings*)

### 2.3 Détection de communautés dans les graphes

Brève revue :
- Modularité de Newman (2006)
- Louvain (Blondel et al., 2008)
- Label Propagation (Raghavan et al., 2007)
- Leiden (Traag et al., 2019) — corrige les communautés mal connectées de Louvain

### 2.4 Forecasting de séries temporelles courtes

- ARIMA (Box & Jenkins, classique)
- Prophet (Taylor & Letham, 2018) — saisonnalité robuste
- LSTM (Hochreiter & Schmidhuber, 1997 ; popularisé pour séries temporelles dans les années 2015+)

### 2.5 Observatoires de compétences existants

Discussion comparative : LinkedIn Talent Insights, ESCO, Lightcast (Burning Glass), études cabinets. Limites de chacun. Position SKILLNAV.

---

## 3. Méthodologie

### 3.1 Sources et collecte
*(PRD §8)*

- Maroc : Rekrute, EmploiTIC, LinkedIn MA via Apify, pages carrières
- International : LinkedIn, Indeed, builtin.com, Welcome to the Jungle
- Signaux faibles : Google Trends, GitHub Trending, HuggingFace Trending
- Volume cible : 500–2 000 offres
- Conformité robots.txt + TOS reviewed (cf. `sources/registry.yaml`)

### 3.2 Architecture polyglotte
*(PRD §7.0 + §6.1)*

Justification détaillée : pourquoi MongoDB + Neo4j + Elasticsearch et non un seul store. Diagramme du pipeline global. Stratégie : MongoDB = source of truth, Neo4j et ES dérivés (rejouables).

### 3.3 Pipeline Content Mining
*(PRD §6.2 + §9)*

Étapes : cleaning, extraction Pydantic AI + Claude Sonnet, NER comparative HF Transformers, normalisation sentence-transformers. Schémas Pydantic v2 comme source de vérité unique.

### 3.4 Pipeline Structure Mining
*(PRD §6.3 + §F08–F10)*

Construction du graphe Skill ↔ Job ↔ Family. Algos exécutés via Neo4j GDS : PageRank, Louvain, Label Propagation, Leiden (via igraph).

### 3.5 Pipeline Usage Mining
*(PRD §6.4 + §F11–F13)*

Séries temporelles skill_count(time) — agrégation mensuelle. Forecasting comparatif ARIMA / Prophet / LSTM. Détection compétences émergentes (3 méthodes comparées).

### 3.6 Data Quality Framework
*(PRD §N3)*

Trois axes : complétude, bruit, biais. Métriques par champ Pydantic. Visualisations sur dashboard `/quality`. Approche **transparence** plutôt que correction des biais.

### 3.7 RGPD et éthique
*(PRD §N4 + document `RGPD_DPIA.md`)*

Base légale art. 6.1.f. Données exclues. Protocole robots.txt strict. Anonymisation des exports publics. Droit d'opposition.

---

## 4. Résultats — Étude comparative

> **Cœur scientifique du rapport. Chaque tableau doit être chiffré, pas qualitatif.**
> Source : notebooks `02_ner_comparison`, `03_graph_analysis`, `04_forecasting_comparison`.

### 4.1 NER comparé — BERT-multi / CamemBERT / DistilBERT

#### Protocole
- Jeu test (gold set) : 30 offres annotées BIO (15 FR + 15 EN)
- 7 types d'entités : SKILL, TOOL, FRAMEWORK, MODEL, LANGUAGE, ROLE, ORGANIZATION
- Métriques : F1 micro, F1 macro, F1 par type, runtime / offre

#### Résultats

| Modèle | F1 micro | F1 macro | F1 SKILL | F1 FRAMEWORK | F1 MODEL | Runtime / offre |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| BERT-base-multilingual + tête NER | TBD | TBD | TBD | TBD | TBD | TBD |
| CamemBERT-NER (FR only) | TBD | TBD | TBD | TBD | TBD | TBD |
| DistilBERT-NER (EN only) | TBD | TBD | TBD | TBD | TBD | TBD |

#### Discussion

À rédiger après mesure : analyser les écarts par type d'entité, justifier le choix du modèle champion (routage par langue + meilleur compromis F1 / runtime).

### 4.2 Communautés comparées — Louvain / Label Propagation / Leiden

#### Protocole
- Graphe complet SKILLNAV à fin Sprint 2 (≥ 200 nœuds, ≥ 800 arêtes)
- Métriques : Modularité Q, nombre de communautés, runtime, stabilité (VI moyen sur 10 runs)

#### Résultats

| Algorithme | Modularité Q | Nb communautés | Runtime | Stabilité (VI moyen) |
|---|:---:|:---:|:---:|:---:|
| Louvain (greedy modularity) | TBD | TBD | TBD | TBD |
| Label Propagation (asynchrone) | TBD | TBD | TBD | TBD |
| Leiden (résolution = 1.0) | TBD | TBD | TBD | TBD |

#### Discussion

À rédiger après mesure : Louvain équilibre qualité/stabilité, Leiden corrige les communautés mal connectées, Label Propagation rapide mais instable.

### 4.3 Forecasting comparé — ARIMA / Prophet / LSTM

#### Protocole
- Top 10 compétences par PageRank, séries mensuelles 12 mois
- Train/test : 9 mois / 3 mois
- Métriques : MAPE, RMSE, MAE, runtime, couverture IC 95 %

#### Résultats

| Modèle | MAPE médian | RMSE médian | MAE médian | Runtime médian | Couverture IC 95% |
|---|:---:|:---:|:---:|:---:|:---:|
| ARIMA (auto via AIC) | TBD | TBD | TBD | TBD | TBD |
| Prophet | TBD | TBD | TBD | TBD | TBD |
| LSTM (neuralforecast) | TBD | TBD | TBD | TBD | TBD |

#### Discussion

À rédiger : sur séries courtes, modèles statistiques (ARIMA, Prophet) battent souvent les deep models. Hypothèse à confirmer empiriquement.

### 4.4 Émergence comparée — Heuristique / XGBoost / KMeans temporel

#### Protocole
- Jeu de validation : 30 skills annotés (émergent / établi / déclinant)
- Métriques : précision, rappel, F1 par classe, F1 macro, matrice de confusion 3×3

#### Résultats

| Méthode | F1 macro | F1 émergent | F1 établi | F1 déclinant | Interprétabilité |
|---|:---:|:---:|:---:|:---:|:---:|
| Heuristique pondérée | TBD | TBD | TBD | TBD | Très haute |
| XGBoost supervisé | TBD | TBD | TBD | TBD | Haute (feature importance) |
| KMeans temporel | TBD | TBD | TBD | TBD | Moyenne |

#### Discussion

À rédiger : trade-off interprétabilité vs performance. Heuristique recommandée pour MVP académique (transparence) ; XGBoost si gain F1 substantiel.

---

## 5. Discussion

### 5.1 Limites de l'étude

- Volume modeste (500–2 000 offres) — résultats indicatifs, pas définitifs
- Biais géographique (sur-représentation de certaines plateformes)
- Annotation gold set par 2 personnes (pas d'inter-annotator agreement formel)
- Période courte (3–6 mois) — saisonnalité non capturée

### 5.2 Biais reconnus
*(PRD §N3.3)*

Biais langue, géographie, taille employeur, plateforme source, sectoriel, genre lexical. Approche : transparence (visualisation sur `/quality`) plutôt que correction.

### 5.3 Robustesse des résultats

Discussion sur la stabilité des classements PageRank, la sensibilité des forecasts aux outliers, la généralisabilité des modèles NER au-delà du gold set.

### 5.4 Comparaison aux travaux antérieurs

À rédiger : positionnement vs LinkedIn Talent Insights, vs études Lightcast, vs travaux académiques sur skill extraction.

---

## 6. Conclusion et perspectives

### 6.1 Synthèse des contributions

- Couverture équilibrée des 3 axes Web Mining (~ 30 % chacun)
- 4 études comparatives chiffrées et reproductibles
- Architecture polyglotte justifiée
- RGPD intégrée dès la conception
- Dashboard public + datasets ouverts

### 6.2 Perspectives V1.5
*(PRD §19.1)*

Article Medium, fine-tuning CamemBERT, déploiement skillnav.ma, mise à jour mensuelle automatique, repository open source.

### 6.3 Perspectives V2
*(PRD §19.2)*

Extension géographique, pipeline live (Celery + APScheduler), agents prospectifs (Claude Agent SDK), API publique versionnée, partenariats.

---

## 7. Bibliographie

| Référence | |
|---|---|
| Liu, B. | *Web Data Mining: Exploring Hyperlinks, Contents, and Usage Data*. Springer, 2011. |
| Manning, C., Raghavan, P., Schütze, H. | *Introduction to Information Retrieval*. Cambridge University Press, 2008. |
| Devlin, J., Chang, M.-W., Lee, K., Toutanova, K. | « BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding ». NAACL 2019. |
| Martin, L. et al. | « CamemBERT: a Tasty French Language Model ». ACL 2020. |
| Sanh, V., Debut, L., Chaumond, J., Wolf, T. | « DistilBERT, a distilled version of BERT ». NeurIPS Workshop 2019. |
| Blondel, V., Guillaume, J.-L., Lambiotte, R., Lefebvre, E. | « Fast unfolding of communities in large networks ». J. Stat. Mech. 2008. |
| Traag, V. A., Waltman, L., van Eck, N. J. | « From Louvain to Leiden: guaranteeing well-connected communities ». Scientific Reports 9, 2019. |
| Raghavan, U. N., Albert, R., Kumara, S. | « Near linear time algorithm to detect community structures in large-scale networks ». Phys. Rev. E 76, 2007. |
| Newman, M. E. J. | « Modularity and community structure in networks ». PNAS 103(23), 2006. |
| Taylor, S. J., Letham, B. | « Forecasting at scale ». The American Statistician 72(1), 2018. |
| Hochreiter, S., Schmidhuber, J. | « Long Short-Term Memory ». Neural Computation 9(8), 1997. |
| WEF | *Future of Jobs Report 2025*. World Economic Forum, 2025. |
| OECD | *AI Skills Outlook 2024*. OECD Publishing, 2024. |
| LinkedIn | *Workforce Report MENA 2025*. LinkedIn Economic Graph, 2025. |
| Stack Overflow | *Developer Survey 2025*. |

---

## 8. Annexes

### Annexe A — Schéma Pydantic complet

Reproduire le bloc `JobExtraction` du PRD §5.2 F04 + `NerAnnotation` + `SkillTimeSeries` + `Forecast`.

### Annexe B — ADRs (Architecture Decision Records)

Reproduire les 10 ADRs du PRD §21.4.

### Annexe C — Captures du dashboard

5–10 captures HD des pages clés : `/`, `/skills`, `/graph`, `/forecasting`, `/ner-explorer`, `/comparative-study`, `/quality`.

### Annexe D — Extraits de code représentatifs

Pipeline NER comparatif, builder de graphe, calcul de scores d'émergence — extraits commentés.

### Annexe E — Liste exhaustive des sources

Reproduction de `sources/registry.yaml` avec TOS reviewed dates.

### Annexe F — DPIA simplifiée

Référence vers `docs/RGPD_DPIA.md`.

---

**Mai 2026 · Bachirou Konaté (auteur) — avec Karamo Sylla (contributions techniques) · ENSA-Tétouan**
