# Métriques de l'étude 02 — Détection de communautés

Source : notebook [`notebooks/03_graph_analysis.ipynb`](../../../notebooks/03_graph_analysis.ipynb),
cellule *comparaison §N2.2*.

## Modularité Q sur le graphe complet (2 781 skills)

| Algorithme | Modularité Q | Communautés détectées | Temps d'exécution |
|---|:-:|:-:|:-:|
| Label Propagation | 0,148 | 2 784 | 0,504 s |
| **Louvain** | **0,295** | 2 781 | 1,126 s |
| Leiden | 0,298 | 2 785 | 0,581 s |

## Stabilité (Label Propagation, 5 runs avec seeds 0-4)

| Seed | Modularité Q |
|:-:|:-:|
| 0 | 0,151 |
| 1 | 0,128 |
| 2 | 0,173 |
| 3 | 0,142 |
| 4 | 0,166 |

Louvain et Leiden sont **déterministes** (variance nulle entre runs).
Label Propagation oscille entre 0,12 et 0,17 selon le seed.

## Cohérence sémantique des 5 plus grandes communautés Louvain

| ID | Taille | Aperçu des membres | Interprétation |
|:-:|:-:|---|---|
| 0 | 312 | Python, SQL, Pandas, NumPy, scikit-learn | Data science classique |
| 3 | 245 | AWS, Docker, Kubernetes, Terraform, CI/CD | Cloud / MLOps |
| 1 | 198 | LLM, RAG, LangChain, OpenAI API, Vector | GenAI agentique |
| 7 | 174 | Tableau, Power BI, Excel, DAX, SSAS | BI & Reporting |
| 4 | 152 | TensorFlow, PyTorch, Keras, CUDA, GPU | Deep Learning |

Cette interprétabilité qualitative confirme que les communautés détectées
ne sont pas un artefact mathématique mais reflètent bien des regroupements
métier.
