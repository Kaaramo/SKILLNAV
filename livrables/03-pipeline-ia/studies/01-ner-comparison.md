# Étude 01 — Reconnaissance d'entités nommées (NER)

> Axe Web Mining : **Content Mining**
> Pipeline correspondant : `skillnav/comparative_studies/ner/`
> Notebook : [`notebooks/02_ner_comparison.ipynb`](../../../notebooks/02_ner_comparison.ipynb)

---

## 1. Problème

Une fiche d'offre d'emploi est un texte non structuré. Pour exploiter le
corpus en aval (graphe Skill ↔ Skill, statistiques temporelles, gap
analysis), il faut **extraire les compétences mentionnées** de chaque
description. Cette tâche s'appelle *Named Entity Recognition* en NLP, ici
spécialisée sur les compétences techniques (skills, frameworks, outils).

L'enjeu : choisir un modèle NER pré-entraîné qui fonctionne sur un corpus
**bilingue français-anglais** (les fiches Maroc mélangent les deux), avec un
temps d'inférence acceptable pour traiter 3 467 fiches en batch.

---

## 2. Modèles testés

Trois modèles HuggingFace ont été comparés sur le même jeu de test.

| Modèle | Identifiant HuggingFace | Taille | Spécialité |
|---|---|:-:|---|
| BERT multilingual | `Davlan/bert-base-multilingual-cased-ner-hrl` | 110 M | NER multilingue (10 langues) |
| CamemBERT-NER | `Jean-Baptiste/camembert-ner` | 110 M | NER français pur |
| DistilBERT-NER | `dslim/distilbert-NER` | 66 M | NER anglais distillé |

Chaque modèle a été chargé via `transformers` en mode `pipeline("ner",
aggregation_strategy="simple")` pour fusionner automatiquement les sous-tokens.

---

## 3. Jeu de test

**30 fiches gold** annotées manuellement par le binôme, avec **543
compétences de référence** au total.

* Fichier source : `data/ner/ner_gold_set.json`
* Construction : `scripts/ner/01_build_gold_set.py`
* Sélection : tirage aléatoire stratifié par origine (Maroc / International)
  pour avoir un échantillon représentatif du corpus complet.
* Annotation : chaque compétence est marquée avec sa position dans le texte
  + son label canonique.

---

## 4. Méthodologie d'évaluation

| Métrique | Formule | Pourquoi |
|---|---|---|
| **Précision** | TP / (TP + FP) | Proportion d'entités prédites qui sont vraiment des compétences |
| **Rappel** | TP / (TP + FN) | Proportion des compétences gold qui ont été détectées |
| **F1** | 2 · P · R / (P + R) | Moyenne harmonique — métrique de référence pour départager |
| Temps moyen | sec/fiche en CPU | Coût opérationnel sur batch de 3 467 fiches |

Le matching entre prédiction et gold est fait par **chevauchement d'offsets**
(la prédiction `"PyTorch"` à la position 1240 matche la gold `"PyTorch"` à la
position 1238 si leur intervalle se chevauche).

Code d'évaluation : `scripts/ner/03_evaluate.py`.

---

## 5. Résultats détaillés

| Modèle | Précision | Rappel | **F1** | Entités prédites | Skills gold capturés | Temps |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| BERT multilingual | 0,308 | 0,029 | **0,054** | 49 | 16 / 543 | 0,29 s |
| CamemBERT-NER | 0,454 | 0,282 | **0,348** | 310 | 153 / 543 | 0,38 s |
| DistilBERT-NER | 0,443 | 0,484 | **0,463** | 532 | 263 / 543 | 0,15 s |

Source : `data/ner/evaluation_n2_1.json` (et copie dans
[`../metrics/ner_evaluation.json`](../metrics/ner_evaluation.json)).

---

## 6. Analyse

### Le modèle retenu : DistilBERT-NER (F1 = 0,463)

DistilBERT gagne sur deux axes simultanément :

1. **Meilleur F1** (0,463) — détecte presque la moitié des compétences gold,
   contre 28 % pour CamemBERT et 3 % pour BERT multilingual.
2. **Inférence 2× à 2,5× plus rapide** (0,15 s contre 0,29 s et 0,38 s) — ce
   qui ramène le batch complet (3 467 fiches) de ~25 minutes à ~9 minutes.

### Le paradoxe à discuter

> *« Pourquoi un modèle entraîné sur l'anglais bat-il un modèle entraîné sur
> le français, sur un corpus francophone ? »*

Trois facteurs convergent :

1. **Le corpus est en fait bilingue.** Les fiches Maroc et International
   contiennent toutes des termes techniques anglais (LLM, RAG, fine-tuning,
   Prompt Engineering, MLOps). CamemBERT, entraîné sur du français pur,
   ignore ces termes ou les classe en `O` (hors entité).
2. **Les compétences techniques sont en réalité des entités anglaises** la
   plupart du temps. `Python`, `TensorFlow`, `BigQuery` — ce sont des noms
   propres anglais. DistilBERT, qui les a vus à l'entraînement, les
   reconnaît.
3. **CamemBERT a été entraîné sur des textes journalistiques** (Le Monde,
   Wikipedia FR) qui ne contiennent pas le vocabulaire technique de notre
   domaine.

Le paradoxe disparaît dès qu'on regarde la nature réelle du corpus : on
n'évalue pas du français pur, on évalue du **français mêlé de jargon
technique anglais**. DistilBERT est le modèle adapté à cette mixité.

### Pourquoi BERT multilingual est si mauvais (F1 = 0,054)

Modèle généraliste, entraîné pour reconnaître `PERSON`, `LOCATION`,
`ORGANIZATION` — pas des compétences techniques. Il ne prédit que 49 entités
au total (vs 532 pour DistilBERT) parce qu'il ne sait pas quoi chercher.
C'est le bon rappel : il a servi de **baseline neutre** dans le comparatif.

---

## 7. Limites assumées

* **F1 = 0,463 reste perfectible.** En V2, deux pistes : (1) fine-tuner
  DistilBERT sur un corpus skills + (2) tester GLiNER (zero-shot sur
  taxonomie ouverte) — première inférence déjà collectée dans
  `data/ner/predictions/gliner.json`.
* **Le jeu de test est petit** (30 fiches). En V2, le passer à ~100 fiches
  pour réduire l'intervalle de confiance des métriques.
* **Pas de mesure de la latence GPU.** Tous les chiffres sont en CPU. Sur
  GPU, l'écart d'inférence entre les 3 modèles serait moins déterminant.

---

## 8. Verdict V1

**DistilBERT-NER retenu pour la production SKILLNAV V1.** Le modèle est
appelé en batch après chaque ingestion pour enrichir les fiches avec les
compétences détectées. Le score F1 et la liste exacte des compétences gold
manquées sont stockés dans MongoDB (`ner_annotations` collection) pour audit
ultérieur.
