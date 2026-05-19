# Étude 03 — Prévision temporelle de la demande en compétences

> Axe Web Mining : **Usage Mining**
> Pipeline correspondant : `skillnav/pipelines/usage_mining/`
> Notebook : [`notebooks/04_forecasting_comparison.ipynb`](../../../notebooks/04_forecasting_comparison.ipynb)

---

## 1. Problème

Pour chaque compétence du top 10 PageRank (les plus centrales du graphe), on
dispose d'une **série temporelle hebdomadaire** : combien d'offres l'ont
mentionnée chaque semaine entre janvier 2026 et mai 2026.

Question :

> *Quel modèle de prévision donne les estimations les plus fiables à
> l'horizon 4 semaines (1 mois) ?*

Réponse attendue : pour chaque skill, prévoir les 4 prochains points avec un
intervalle de confiance, et identifier le modèle qui minimise l'erreur de
prévision en moyenne.

---

## 2. Modèles testés

Trois familles d'approches, choisies pour couvrir 50 ans d'histoire de la
prévision :

| Modèle | Famille | Implémentation | Année |
|---|---|---|:-:|
| ARIMA | statistique Box-Jenkins | `statsmodels.tsa.arima.model.ARIMA` | 1970 |
| Prophet | additif décomposable | `prophet` (Facebook) | 2017 |
| LSTM | réseau récurrent | `torch.nn.LSTM` + `pytorch-lightning` | 2014 |

Hyperparamètres :

* ARIMA : auto-fit sur grille `(p, d, q)` ∈ {0,1,2} × {0,1} × {0,1,2},
  sélection par AIC minimum
* Prophet : changepoints automatiques, mode `additive`, sans seasonality
  hebdomadaire (séries trop courtes pour la détecter)
* LSTM : 1 couche, hidden=32, séquence d'entrée=8 semaines, 200 epochs,
  early stopping sur validation

Code source : `skillnav/pipelines/usage_mining/{arima,prophet,lstm}_model.py`,
orchestration dans `comparison.py`.

---

## 3. Jeu de test

* **10 compétences** = top 10 PageRank du graphe Skill ↔ Skill
* Période : **17 semaines** par série (janvier → début mai 2026)
* Hold-out : **les 4 dernières semaines** servent de jeu de test, les 13
  premières sont l'entraînement
* Source des séries : `skillnav/pipelines/usage_mining/series_builder.py`
  agrège les fiches MongoDB par semaine
* Snapshot complet : `data/exports/forecast_top10.json`

Les 10 compétences testées :

| Rang | Skill | Famille |
|:-:|---|---|
| 1 | Prompt engineering | GenAI |
| 2 | RAG | Agents AI |
| 3 | LangChain | GenAI |
| 4 | PyTorch | Deep Learning |
| 5 | LLMs | GenAI |
| 6 | TensorFlow | Deep Learning |
| 7 | LangGraph | Agents AI |
| 8 | Fine-tuning | GenAI |
| 9 | OpenAI API | GenAI |
| 10 | embeddings | GenAI |

---

## 4. Métriques d'évaluation

| Métrique | Formule | Pourquoi |
|---|---|---|
| **RMSE** | √(mean((ŷ - y)²)) | Pénalise les grosses erreurs, plus robuste que MAPE en présence de zéros |
| Victoires | argmin du RMSE par skill | Compte combien de fois chaque modèle gagne |
| Couverture IC95 | proportion de points y dans [ŷ-1,96σ, ŷ+1,96σ] | Honnêteté de l'intervalle de confiance |

Le **RMSE moyen sur les 10 skills** est la métrique principale de décision.

---

## 5. Résultats détaillés

| Skill | ARIMA | Prophet | LSTM | Gagnant |
|---|:-:|:-:|:-:|---|
| Prompt engineering | **17,24** | 17,60 | 50,74 | ARIMA |
| RAG | **21,85** | 22,65 | 45,25 | ARIMA |
| LangChain | 19,98 | 30,18 | **18,93** | LSTM |
| PyTorch | **17,18** | 23,14 | 22,42 | ARIMA |
| LLMs | 23,77 | 18,31 | **17,96** | LSTM |
| TensorFlow | 22,52 | 22,25 | **19,15** | LSTM |
| LangGraph | 7,00 | 17,27 | **5,77** | LSTM |
| Fine-tuning | 10,30 | **5,45** | 8,38 | Prophet |
| OpenAI API | 13,64 | 9,12 | **3,77** | LSTM |
| embeddings | **8,71** | 9,25 | 10,32 | ARIMA |
| **RMSE moyen** | **16,22** | 17,52 | 20,27 | — |
| **Victoires** | **4** | **1** | **5** | — |

Source : [`../metrics/forecast_top10.json`](../metrics/forecast_top10.json).

---

## 6. Analyse — le paradoxe LSTM

> *LSTM gagne plus souvent (5/10) mais perd sur le RMSE moyen (20,27 vs
> 16,22 pour ARIMA). Que faut-il en conclure ?*

C'est exactement le piège classique d'un comparatif naïf : **« qui gagne le
plus souvent ? »** n'est pas la bonne question.

### Le diagnostic

LSTM a une **variance extrême** sur sa précision :

* Skills où LSTM **excelle** : OpenAI API (3,77), LangGraph (5,77), LLMs (17,96)
* Skills où LSTM **dérive** : Prompt engineering (50,74), RAG (45,25),
  LangChain (18,93)

Sur les séries où les données sont stables et nombreuses, LSTM capture des
patterns que ARIMA ne voit pas. Sur les séries irrégulières ou courtes, il
**overfite** ou diverge.

ARIMA, en revanche, dégrade gracieusement : son pire score (RMSE 23,77 sur
LLMs) reste raisonnable. C'est un modèle **prévisible dans sa
prévisibilité**.

### Le choix retenu

Pour une V1 livrée à des utilisateurs (jury, recruteurs, étudiants), la
**prévisibilité** vaut plus que le **pic de performance**. Mieux vaut un
modèle qui rate jamais catastrophiquement, qu'un modèle qui parfois excelle
mais parfois sort des prévisions absurdes.

**ARIMA est donc retenu pour la V1**, sur la base du RMSE moyen.

### Une nuance importante

Si on disposait de **séries plus longues** (24-36 mois au lieu de 4 mois),
LSTM pourrait basculer en sa faveur. Le pipeline est conçu pour permettre
ce basculement automatique : la fonction `comparison.select_best_model()`
retourne le modèle gagnant par RMSE, on changera de modèle V2 le jour où le
LSTM cesse de diverger sur les séries irrégulières.

---

## 7. Limites assumées

* **Séries courtes** (17 semaines). LSTM a besoin de plus de données pour
  exprimer son potentiel. ARIMA est mieux adapté aux séries courtes par
  construction (modèle statistique paramétrique).
* **Pas de variables exogènes.** ARIMA pourrait être amélioré en ARIMAX
  (ajout de variables comme « nombre total d'offres publiées la semaine
  N ») — non testé pour cette V1.
* **Évaluation sur 10 séries seulement.** Le RMSE moyen est lui-même une
  variable aléatoire. Un test de Wilcoxon entre ARIMA et Prophet
  donnerait une p-value plus rigoureuse.

---

## 8. Verdict V1

**ARIMA retenu pour la production SKILLNAV V1.** Le pipeline
`scripts/build_forecast_top10.py` exécute les trois modèles, sélectionne le
gagnant par skill (`best_method` dans le JSON), et écrit les prévisions dans
`web/src/lib/forecast_top10.json` pour la page Prévisions du dashboard.
