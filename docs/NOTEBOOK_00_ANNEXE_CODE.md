# Annexe : Comprendre le code (notebook `00_market_analysis.ipynb`)

> Pour Karamo / Bachirou : explications pédagogiques des blocs principaux du
> notebook d'EDA descriptive. Cette annexe accompagne le notebook
> `notebooks/00_market_analysis.ipynb` ; elle en a été extraite pour alléger
> la lecture du notebook lui-même.

---

## A.1 `load_corpus(racines, origine)` (cellule §0.2)

Cette fonction est le **point d'entrée des données**. Elle :

1. Reçoit une liste de chemins racines (un par source : `rekrute/data_structured/`, `linkedin-ma/data_structured/`, etc.)
2. Pour chaque racine, fait un `rglob('*.yaml')` qui parcourt récursivement tous les sous-dossiers (organisés par mois de publication `YYYY-MM/`)
3. Ouvre chaque YAML avec `yaml.safe_load()` (sécurisé : ne désérialise pas d'objets Python arbitraires)
4. **Aplatit la structure imbriquée** : `position.skills.genai` (chemin imbriqué dans le YAML) devient `skills_genai` (colonne plate dans le DataFrame)
5. Extrait des **métadonnées de chemin** : la source vient du nom du dossier parent, le mois de publication vient du nom du sous-dossier
6. Calcule **deux colonnes dérivées du titre** : `title_canonical` (forme normalisée du titre) et `job_family` (famille canonique parmi les 13 du schéma)
7. Renvoie un `pd.DataFrame` où chaque ligne = une offre, chaque colonne = un attribut

### A.1 bis Canonicalisation : compétences + titres + famille de poste

Trois niveaux de normalisation appliqués au chargement :

**Niveau 1. Compétences (`SKILL_ALIASES`, `canonicaliser_skill`, `canonicaliser_liste`)**

Pour éviter que `LLM`, `LLMs`, `llm`, `Large Language Model` soient comptés
comme 4 compétences différentes. ~190 alias couvrent les variantes les plus
fréquentes des 10 familles. La fonction `canonicaliser_liste` applique
l'alias **et** dédoublonne en case-insensitive dans la même offre.

**Niveau 2. Titres de poste (`TITLE_ALIASES`, `canonicaliser_titre`)**

Trois étapes successives sur chaque titre :

1. `strip_gender_suffix()` retire les suffixes parité/genre : `H/F`, `Hf`, `F/H`, `M/F`, `F/M`, `(m/f/x)`, `(M/W/D)` etc.
2. Recherche dans `TITLE_ALIASES` (dict des ~30 titres les plus fréquents). Exemple : `data scientist` -> `Data Scientist`.
3. Sinon, `smart_title_case()` met en Title Case **en préservant les acronymes connus** (AI, ML, BI, NLP, CV, MLOps, GenAI, LLM, RAG, API, SQL, GCP, AWS).

Effet observé : `Data Scientist` (20 occurrences) + `Data scientist` (4 occurrences) deviennent un seul `Data Scientist` (24).

**Niveau 3. Famille de poste (`detecter_famille_poste`, `JOB_FAMILY_PATTERNS`, `FAMILY_FR`)**

Mapping regex du titre brut vers une des 13 `job_family` du schéma SKILLNAV
(`DATA_ANALYST`, `DATA_SCIENTIST`, `AI_ENGINEER`, `ML_ENGINEER`,
`GENAI_LLM_ENGINEER`, `MLOPS_ENGINEER`, `DATA_ENGINEER`, ...). Les patterns
sont ordonnés du plus spécifique au plus général : `GenAI / LLM Engineer`
match avant `AI Engineer` qui match avant `ML Engineer`.

## A.2 Helpers `comptage_skills` / `jobs_avec_skill` / `all_skills_lower` (cellule §0.4)

- `comptage_skills(df, colonne)` : sur une colonne de listes (ex: `skills_genai`), elle « explose » chaque liste en autant de lignes, puis compte. Résultat : `pd.Series` `{ 'RAG': 1064, 'LangChain': 726, ... }`.
- `all_skills_lower(row)` : concatène toutes les compétences des 10 familles d'une offre en une seule liste minuscule, pratique pour rechercher un mot-clé sans se soucier de la casse.
- `jobs_avec_skill(df, skill)` : compte le nombre d'offres qui mentionnent une compétence (recherche par sous-chaîne).

## A.3 Pattern « 1 fonction d'analyse = 2 appels » (§0.5)

Chaque analyse est encapsulée dans une `section_xxx(df, libelle)`, appelée
deux fois (une fois avec `df_maroc`, une fois avec `df_international`),
ce qui évite la duplication entre Partie I et Partie II.

## A.4 Heuristique « recherche vs applied » (§I.7, §II.7)

`section_recherche_vs_applied` utilise un **scoring par mots-clés** :

- Titre contenant `research engineer` / `research scientist` -> recherche, point.
- Sinon, scoring `research` (publication, paper, SOTA, RL...) vs `applied` (production, deploy, customer...). Seuil `score_r >= 2` pour éviter les faux positifs.

## A.5 Pour aller plus loin

Voir le notebook compagnon [`01_visualisations.ipynb`](../notebooks/01_visualisations.ipynb)
qui transforme les analyses du notebook 00 en **8 figures haute qualité**
exportées en PNG dans `docs/figures/`, prêtes à coller dans le rapport
L5 et le deck PPTX de soutenance.
