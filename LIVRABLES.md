# SKILLNAV — Carte des livrables

Module M242 « Analyse de Web » · ENSA-Tétouan · Pr. Imad Sassi
Karamo Sylla & Bachirou Konaté

Cette page liste les 6 livrables exigés par le sujet et donne l'accès direct à
chaque pièce.

| # | Livrable | Où le trouver |
|:-:|---|---|
| 1 | **Scripts de collecte** | Dépôt séparé [`Kaaramo/SKILLNAV-COLLECT`](https://github.com/Kaaramo/SKILLNAV-COLLECT) — corpus de 3 468 fiches + 5 templates de scraping + protocole versionné |
| 2 | **Base de données hybride** | [`livrables/02-base-de-donnees-hybride/`](livrables/02-base-de-donnees-hybride/) — MongoDB Atlas + Neo4j AuraDB + Elasticsearch (Bonsai), schémas, requêtes types, captures |
| 3 | **Pipeline IA** | `skillnav/pipelines/` et `skillnav/comparative_studies/` · notebooks `02_ner_comparison.ipynb`, `03_graph_analysis.ipynb`, `04_forecasting_comparison.ipynb` |
| 4 | **Dashboard interactif** | Application Next.js dans `web/` · 6 pages (Vue d'ensemble, Compétences, Graphe, Prévisions, Gap Analysis, Méthodologie) |
| 5 | **Rapport** | [`docs/Rapport.md`](docs/Rapport.md) (export PDF généré au moment du rendu) |
| 6 | **Présentation** | `docs/Soutenance.pdf` (à produire) |

---

## Structure générale du dépôt

```
SKILLNAV/
├── LIVRABLES.md                    (cette page)
├── CLAUDE.md                       (consignes internes du binôme)
├── livrables/                      (pièces livrées au prof)
│   └── 02-base-de-donnees-hybride/
├── skillnav/                       (package Python — schémas, pipelines, API, DB)
│   ├── schemas/                    (Pydantic v2 — source de vérité)
│   ├── db/                         (clients MongoDB / Neo4j / Elasticsearch)
│   ├── pipelines/                  (content_mining, structure_mining, usage_mining, curriculum_mining)
│   ├── comparative_studies/        (NER, communautés, forecasting)
│   └── api/                        (FastAPI, 15 endpoints)
├── web/                            (dashboard Next.js)
├── notebooks/                      (6 notebooks numérotés)
├── scripts/                        (ingestion, builders de snapshots)
├── data/                           (jobs.jsonl, exports CSV)
├── tests/                          (pytest)
└── docs/                           (rapport, PRD, schémas, charte graphique)
```

---

## Comment naviguer

Pour le livrable **2** (Base de données hybride), commencer par
[`livrables/02-base-de-donnees-hybride/README.md`](livrables/02-base-de-donnees-hybride/README.md).
Ce document contient le schéma d'architecture, les choix techniques justifiés,
les schémas de chaque base, les exemples de requêtes et les captures de preuve.

Pour les autres livrables, les pointeurs ci-dessus mènent directement aux pièces
correspondantes.
