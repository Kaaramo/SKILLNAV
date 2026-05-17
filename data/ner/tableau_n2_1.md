# Tableau §N2.1 — Étude comparative NER sur 30 fiches gold

| Modèle | Paramètres | Précision | Rappel | F1 | Temps moyen (s/fiche) | Entités prédites | Skills gold détectés |
|---|---|---|---|---|---|---|---|
| **BERT multilingue** | 110M | 0.308 | 0.029 | **0.054** | 0.29 | 49 | 16 / 543 |
| **CamemBERT-NER** | 110M | 0.454 | 0.282 | **0.348** | 0.38 | 310 | 153 / 543 |
| **DistilBERT-NER** | 66M | 0.443 | 0.484 | **0.463** | 0.15 | 532 | 263 / 543 |

## Lecture du tableau

- **Précision** : proportion d'entités prédites qui correspondent à une compétence du gold set.
- **Rappel** : proportion des compétences gold qui ont été détectées par le modèle.
- **F1** : moyenne harmonique de la précision et du rappel (métrique synthétique).
- **Temps moyen** : secondes d'inférence par fiche (CPU, fiches de longueur moyenne ~1500 caractères).

## Choix retenu pour la V1 SKILLNAV

Le modèle retenu pour la pipeline de production est celui qui présente le meilleur F1
tout en gardant un temps d'inférence acceptable pour le traitement batch des 3 467 offres collectées.
