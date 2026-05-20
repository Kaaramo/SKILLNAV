# Étude 02 — Détection de communautés dans le graphe

> Axe Web Mining : **Structure Mining**
> Pipeline correspondant : `skillnav/pipelines/structure_mining/communities.py`
> Notebook : [`notebooks/03_graph_analysis.ipynb`](../../../notebooks/03_graph_analysis.ipynb)

---

## 1. Problème

Une fois les compétences extraites de chaque fiche (étude 01), on construit
un **graphe Skill ↔ Skill** où une arête `(a, b)` existe si les deux
compétences `a` et `b` apparaissent dans au moins une offre commune, avec un
poids égal au nombre de co-occurrences.

Sur ce graphe se pose une question :

> *Existe-t-il des **groupes naturels** de compétences qui « vont ensemble » ?*

Réponse souhaitée : un partitionnement des nœuds en communautés
sémantiquement cohérentes (par exemple « stack data engineering » d'un côté,
« stack MLOps » de l'autre, etc.).

Cette tâche s'appelle *community detection* en analyse de graphes.

---

## 2. Algorithmes testés

Trois algorithmes, choisis pour couvrir l'histoire du domaine :

| Algorithme | Implémentation | Année | Catégorie |
|---|---|:-:|---|
| Label Propagation | `networkx.algorithms.community.label_propagation_communities` | 2007 | baseline rapide, stochastique |
| Louvain | `python-louvain` (Blondel et al.) | 2008 | référence académique |
| Leiden | `igraph.Graph.community_leiden` (Traag et al.) | 2019 | amélioration de Louvain |

Tous les trois maximisent la **modularité** comme objectif.

---

## 3. Jeu de test

Pas de hold-out ici : la modularité est une métrique **interne au graphe**,
pas un score sur données séparées. Le graphe complet est l'objet d'étude.

* **2 781 nœuds Skill** (compétences extraites du corpus)
* **~38 000 arêtes** `CO_OCCURS_WITH` pondérées par fréquence
* Code de construction : `skillnav/pipelines/structure_mining/graph_builder.py`
* Snapshot Pydantic complet : `data/exports/graph_vis.json`

---

## 4. Méthodologie d'évaluation

### Métrique principale : Modularité Q

```
Q = (1 / 2m) × Σ_{ij} [A_ij - (k_i · k_j / 2m)] · δ(c_i, c_j)
```

Q ∈ [-1, 1] mesure si les nœuds d'une même communauté sont plus densément
connectés entre eux que ce qu'un graphe aléatoire produirait. Plus Q est
élevé, meilleures sont les communautés.

### Métriques secondaires

* **Nombre de communautés détectées** (information descriptive)
* **Temps d'exécution** (impact opérationnel)
* **Stabilité** : on relance Label Propagation 5 fois avec des seeds
  différentes pour mesurer la variance (les deux autres sont déterministes)

---

## 5. Résultats détaillés

| Algorithme | Modularité Q | Communautés | Temps | Déterministe |
|---|:-:|:-:|:-:|:-:|
| Label Propagation | **0,148** | 2 784 | 0,50 s | ❌ non |
| Louvain | **0,295** | 2 781 | 1,13 s | ✅ oui |
| Leiden | **0,298** | 2 785 | 0,58 s | ✅ oui |

Source : sortie cellule du notebook `03_graph_analysis.ipynb` (cellule
*comparaison §N2.2*).

Stabilité Label Propagation sur 5 runs (seeds 0-4) : Q varie de 0,12 à 0,17.

---

## 6. Analyse

### Le modèle retenu : Louvain (Q = 0,295)

Pourquoi pas Leiden, qui a une modularité légèrement supérieure ?

**Trois raisons** :

1. **Différence non significative** : 0,003 d'écart sur la modularité Q n'a
   pas de signification pratique. Sur ce graphe, les deux algorithmes
   produisent essentiellement le même partitionnement (2 781 vs 2 785
   communautés détectées).
2. **Louvain est plus simple** : un seul paramètre (résolution), bibliothèque
   `python-louvain` minimaliste, sortie native NetworkX. Leiden passe par
   `igraph` qui nécessite une conversion intermédiaire `networkx → igraph`.
3. **Louvain est plus répandu** : la communauté académique le connaît, les
   utilisateurs (jury, futurs contributeurs) le comprennent immédiatement.

Le compromis « simplicité × clarté » l'emporte sur le gain marginal de précision.

### Pourquoi Label Propagation est éliminé

Modularité de 0,148 — deux fois moins bonne que Louvain. Et surtout :
**instable**. Une seconde exécution donne des communautés différentes. Pour
un livrable pédagogique reproductible, c'est rédhibitoire.

L'algorithme reste utile comme **baseline temporelle** : 0,50 s contre 1,13 s
pour Louvain. Si on devait gérer un graphe avec 1 million de nœuds en
streaming, Label Propagation serait un candidat. Pour 2 781 nœuds, le gain de
0,6 s ne compense pas la perte de modularité de 50 %.

---

## 7. Cohérence sémantique des communautés Louvain

Au-delà de la modularité (chiffrée), on a vérifié manuellement la
**cohérence sémantique** des plus grandes communautés. Extrait :

| Communauté | Taille (≥) | Premiers membres | Thème |
|---|:-:|---|---|
| C0 | 312 | Python, SQL, Pandas, NumPy, scikit-learn | Data science classique |
| C3 | 245 | AWS, Docker, Kubernetes, Terraform, CI/CD | MLOps / Cloud |
| C1 | 198 | LLM, RAG, LangChain, OpenAI API, Vector DB | GenAI agentique |

Cette cohérence est *qualitative* — elle confirme que le partitionnement
n'est pas un artefact mathématique, mais bien des regroupements
interprétables par un humain du domaine.

---

## 8. Limites assumées

* **Q = 0,295 est modeste.** Q > 0,30 est considéré « bon », Q > 0,50
  « excellent ». Notre score reflète la nature dense du graphe (beaucoup
  de compétences communes à plusieurs métiers).
* **Pas de pondération temporelle.** On agrège toutes les offres
  2023-2026 dans le même graphe. En V2, refaire la détection par fenêtre
  glissante de 6 mois pour observer **l'évolution** des communautés.
* **Pas de comparaison avec une ground truth.** Faute de taxonomie
  officielle des compétences IA, on ne peut pas mesurer un *accuracy*. Q est
  la meilleure approximation disponible.

---

## 9. Verdict V1

**Louvain retenu pour la production SKILLNAV V1.** Les `community_id`
calculés sont écrits dans Neo4j sur chaque nœud `(:Skill)` et permettent
le coloriage des communautés sur la page Graphe du dashboard.
