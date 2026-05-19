# Notebooks d'expérimentation

Les notebooks Jupyter qui ont produit les résultats du livrable 3 sont à la
racine du repo dans [`notebooks/`](../../../notebooks/). Ce fichier en sert
de table des matières — ne pas dupliquer les notebooks ici.

| Notebook | Étude | Contenu |
|---|---|---|
| [`02_ner_comparison.ipynb`](../../../notebooks/02_ner_comparison.ipynb) | 01 — NER | Chargement des 3 modèles HuggingFace, inférence sur les 30 fiches gold, calcul des métriques précision/rappel/F1, génération du tableau comparatif |
| [`03_ner_improvement.ipynb`](../../../notebooks/03_ner_improvement.ipynb) | 01 — NER (extension) | Première itération GLiNER zero-shot pour viser une V2 |
| [`03_graph_analysis.ipynb`](../../../notebooks/03_graph_analysis.ipynb) | 02 — Communautés | Construction du graphe Skill ↔ Skill, comparaison Label Propagation vs Louvain vs Leiden, calcul modularité Q + temps + stabilité |
| [`04_forecasting_comparison.ipynb`](../../../notebooks/04_forecasting_comparison.ipynb) | 03 — Forecasting | Séries temporelles top 10 PageRank, entraînement ARIMA + Prophet + LSTM avec hold-out 4 semaines, sélection du gagnant par RMSE |

## Reproductibilité

Chaque notebook est **complètement exécutable de bout en bout** depuis un
environnement Poetry à jour :

```bash
poetry install
poetry run jupyter nbconvert --to notebook --execute notebooks/04_forecasting_comparison.ipynb
```

Les cellules de chargement de modèles (NER) et d'entraînement (LSTM) peuvent
prendre quelques minutes au premier run. Les modèles HuggingFace sont
ensuite mis en cache local (`~/.cache/huggingface/`).
