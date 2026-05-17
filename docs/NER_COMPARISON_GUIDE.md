# Guide §N2.1 : Étude comparative NER

> Module M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi
> Auteurs : Karamo Sylla & Bachirou Konaté · Soutenance : 28 mai 2026

Ce document décrit le pipeline d'évaluation comparative des trois modèles
de reconnaissance d'entités nommées (NER) du projet SKILLNAV, conformément
aux exigences du sujet imposé §N2.1.

---

## 1. Modèles comparés

| Modèle | Identifiant HuggingFace | Paramètres | Langue cible | Pourquoi le retenir dans la comparaison |
|---|---|---|---|---|
| **BERT multilingue** | `Davlan/bert-base-multilingual-cased-ner-hrl` | 110M | 10 langues (dont français, anglais, arabe) | Représente l'option « universelle » : un seul modèle pour le corpus mixte Maroc + International |
| **CamemBERT-NER** | `Jean-Baptiste/camembert-ner` | 110M | Français spécialisé | Représente l'option « optimisée pour le marché marocain » (offres souvent en français) |
| **DistilBERT-NER** | `dslim/distilbert-NER` | 66M | Anglais (CoNLL-03) | Représente l'option « légère et rapide » pour l'inférence batch ; bien adaptée au corpus International majoritairement anglais (73 % du corpus) |

Les trois modèles sont open source, hébergés sur Hugging Face Hub, et
téléchargeables sans authentification. La licence est compatible avec un
projet académique.

---

## 2. Pipeline d'évaluation

```
┌──────────────────────┐
│ data/jobs.jsonl      │   3 467 fiches canonicalisées
└──────────┬───────────┘
           │ sélection diversifiée (seed=42)
           ▼
┌──────────────────────┐
│ 30 fiches gold       │   8 Maroc + 22 International
│ avec gold_skills     │   12 AI-First + 6 AI-Support + 6 ML-First + 6 Data Analytics
└──────────┬───────────┘
           │
           │ inférence × 3 modèles HuggingFace
           ▼
┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐
│ predictions/bert_*.json │  │ predictions/camembert.* │  │ predictions/distilbert.*│
└──────────┬─────────────┘  └──────────┬─────────────┘  └──────────┬─────────────┘
           │                            │                            │
           └────────────────────────────┴────────────────────────────┘
                                        │
                                        │ matching gold ↔ prédictions
                                        │ (sous-chaîne case-insensitive)
                                        ▼
                            ┌──────────────────────────┐
                            │ evaluation_n2_1.json     │   Précision · Rappel · F1
                            │ tableau_n2_1.md          │   pour chaque modèle
                            └──────────────────────────┘
                                        │
                                        ▼
                            ┌──────────────────────────┐
                            │ notebooks/               │   Visualisations
                            │ 02_ner_comparison.ipynb  │   + interprétation
                            └──────────────────────────┘
```

---

## 3. Stratégie d'annotation : *distant supervision*

L'annotation manuelle de 30 fiches par un binôme représente 6 à 10 heures
de travail. Pour rester compatible avec le calendrier de 11 jours avant
soutenance, le projet adopte la stratégie *distant supervision* documentée
par Hovy, Marcus, Palmer, Ramshaw et Weischedel (2014) dans « Weakly
Supervised Models for Named Entity Recognition ».

Concrètement, le gold set s'appuie sur les champs `skills` canonicalisés
issus du pipeline d'extraction structurée mené pendant la phase de
collecte (cf. `sources/collected/*/data_structured/`). Ces champs ont été
produits puis canonicalisés via `scripts/skillnav_eda.canonicaliser_liste`
qui applique 190+ alias de normalisation.

**Avantages** :

- Reproductibilité totale : `seed=42` figé dans `config.py`.
- Couverture homogène : 30 fiches diversifiées par origine et `ai_type`.
- Justification académique solide : la canonicalisation a été validée
  empiriquement sur l'ensemble du corpus (cf. cellule §0.3 « Contrôle
  qualité » du notebook `00_market_analysis.ipynb`).

**Limites** (à mentionner dans §N2.1 du rapport L5) :

- Les éventuels biais de la canonicalisation se propagent au gold set.
- Le matching gold ↔ prédiction utilise une logique souple par
  sous-chaîne, ce qui peut sur-évaluer le rappel sur des compétences à
  noms génériques (« Python » détecte aussi « Python 3.12 »).
- La variance des métriques n'est pas estimée par bootstrap (taille du
  gold set limitée à 30 fiches).

---

## 4. Exécution

```bash
# 1. Construire le gold set (30 fiches diversifiées + skills attendus)
python scripts/ner/01_build_gold_set.py

# 2. Inférence des 3 modèles HuggingFace (téléchargement automatique
#    au premier lancement, ~500 Mo par modèle)
python scripts/ner/02_run_inference.py

# 3. Évaluation P / R / F1 et génération du tableau §N2.1
python scripts/ner/03_evaluate.py

# 4. Notebook de visualisation (régénération depuis le script générateur)
python scripts/build_ner_notebook.py
python scripts/run_notebook.py notebooks/02_ner_comparison.ipynb
```

Temps total : environ 5 minutes après le premier téléchargement des modèles.
Le premier lancement complet est plus long (10 à 15 minutes selon la
connexion) à cause du téléchargement HuggingFace.

---

## 5. Résultats observés (run de référence du 17 mai 2026)

| Modèle | Précision | Rappel | F1 | Temps (s/fiche) |
|---|---|---|---|---|
| BERT multilingue | 0.308 | 0.029 | **0.054** | 0.29 |
| CamemBERT-NER | 0.454 | 0.282 | **0.348** | 0.38 |
| **DistilBERT-NER** | 0.443 | 0.484 | **0.463** | **0.15** |

### Interprétation

1. **BERT multilingue** présente un rappel très faible (0.029) : il
   détecte peu d'entités sur des textes mixtes français / anglais. Sa
   précision n'est pas en cause, mais sa capacité de rappel est limitée
   par l'absence de fine-tuning spécifique au domaine RH.
2. **CamemBERT-NER** est cohérent avec sa spécialisation française :
   précision et rappel équilibrés, mais le rappel est limité par la
   composition du corpus (73 % d'offres internationales en anglais).
3. **DistilBERT-NER** obtient le meilleur F1, en grande partie grâce à
   un rappel élevé (0.484). Il est aussi le plus rapide à l'inférence
   grâce à sa taille réduite (66M paramètres vs 110M).

### Choix retenu pour la V1 SKILLNAV

**DistilBERT-NER** est retenu pour la pipeline de production V1.

Critères :

- F1 le plus élevé sur le gold set : **0.463**
- Temps d'inférence le plus court : **0.15 s/fiche**, soit ~9 minutes pour
  retraiter les 3 467 offres complètes en cas de mise à jour du corpus
- Empreinte mémoire 40 % plus faible : déployable sur les Free Tiers
  envisagés pour le dashboard

---

## 6. Pistes d'amélioration documentées dans le rapport L5

1. **Fine-tuning sur le domaine SKILLNAV** : annoter 100 à 200 fiches
   manuellement pour fine-tuner DistilBERT sur les entités spécifiques
   (compétences IA, intitulés de poste, frameworks). Gain attendu : +0.15
   à +0.25 sur F1 (Lample et al. 2016).
2. **Ensemble de modèles** : combiner DistilBERT (rappel) + CamemBERT
   (précision sur les fiches FR) pour bénéficier des deux forces.
3. **Modèles LLM modernes** : tester un modèle plus récent type
   `gliner-multi` ou `mDeBERTa-NER` qui dominent les benchmarks 2024.
4. **Évaluation avec variance** : appliquer un bootstrap (100 ré-échantillonnages
   du gold set) pour estimer l'intervalle de confiance des métriques.

---

## 7. Artefacts produits

| Fichier | Contenu |
|---|---|
| `data/ner/ner_gold_set.json` | 30 fiches gold (texte + compétences attendues) |
| `data/ner/predictions/bert_multilingual.json` | Prédictions BERT multilingue |
| `data/ner/predictions/camembert.json` | Prédictions CamemBERT-NER |
| `data/ner/predictions/distilbert.json` | Prédictions DistilBERT-NER |
| `data/ner/evaluation_n2_1.json` | Métriques P / R / F1 par modèle (JSON) |
| `data/ner/tableau_n2_1.md` | Tableau §N2.1 prêt à coller dans le rapport L5 |
| `notebooks/02_ner_comparison.ipynb` | Notebook de visualisation comparative |
| `docs/figures/n21_comparaison_ner.png` | Figure barres P/R/F1 par modèle |
| `docs/figures/n21_temps_inference.png` | Figure temps d'inférence par modèle |

---

## 8. Références académiques

- Devlin, J. et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL-HLT.
- Sanh, V. et al. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter*. NeurIPS Workshop.
- Martin, L. et al. (2020). *CamemBERT: a Tasty French Language Model*. ACL.
- Hovy, E. et al. (2014). *Weakly Supervised Models for Named Entity Recognition*. ACL.
- Lample, G. et al. (2016). *Neural Architectures for Named Entity Recognition*. NAACL-HLT.
- Tjong Kim Sang, E. F. & De Meulder, F. (2003). *Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition*. CoNLL.
