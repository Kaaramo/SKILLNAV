"""Génère notebooks/02_graph_starter.ipynb (template Structure Mining).

Notebook de démarrage destiné au développeur en charge du volet Structure
Mining. Couvre :

    - Connexion à Neo4j AuraDB (variables d'environnement, .env)
    - Chargement bulk des CSV générés par scripts/build_dataset.py
    - Création des contraintes d'unicité et des index
    - Validation par comptages
    - Exemple Louvain commenté via Graph Data Science library
    - TODO marqués pour Leiden, Label Propagation et PageRank

Régénération : python scripts/build_graph_starter_notebook.py
"""

from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
NB_PATH = REPO / "notebooks" / "02_graph_starter.ipynb"


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source.splitlines(keepends=True)}


CELLS: list[dict] = []

# ============================================================================
# HEADER
# ============================================================================
CELLS.append(md(
    """# SKILLNAV : Graph Starter (volet Structure Mining)

> **Module** : M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi
> **Destinataire** : développeur en charge du volet Structure Mining
> **Référence** : [`docs/handoff/SKILLNAV_Guide_Modelisation_Structure_Mining.pdf`](../docs/handoff/SKILLNAV_Guide_Modelisation_Structure_Mining.pdf) et [`docs/MODELISATION_GUIDE.md`](../docs/MODELISATION_GUIDE.md)

---

## Objectif du notebook

Ce notebook constitue le **point de démarrage** du volet Structure Mining.
Il enchaîne :

1. Connexion à l'instance Neo4j AuraDB (Free Tier)
2. Chargement bulk des 13 071 nœuds et 62 341 arêtes générés par `scripts/build_dataset.py`
3. Validation par comptages
4. Premier exemple d'algorithme de communautés : **Louvain** (commenté)
5. Trois cellules `TODO` à compléter : **Leiden**, **Label Propagation**, **PageRank**
6. Tableau comparatif §N2.2 du PRD (à reporter dans le rapport L5)

## Prérequis

- Variables d'environnement renseignées dans le fichier `.env` à la racine du dépôt :
  - `NEO4J_URI` (format `neo4j+s://xxxxx.databases.neo4j.io`)
  - `NEO4J_USER` (typiquement `neo4j`)
  - `NEO4J_PASSWORD`
- Fichiers `data/jobs.jsonl`, `data/graph_nodes.csv` et `data/graph_edges.csv` présents
  (générés par `python scripts/build_dataset.py`)
- Packages Python : `neo4j`, `python-dotenv`, `pandas` (déjà dans `pyproject.toml`)
"""
))

# ============================================================================
# §0 Setup
# ============================================================================
CELLS.append(md(
    """## 0. Setup

Import des modules nécessaires, lecture des variables d'environnement et
connexion au cluster Neo4j AuraDB.
"""
))

CELLS.append(code(
    """import os
import sys
import time
from pathlib import Path

import pandas as pd
from neo4j import GraphDatabase

# Charge .env (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print(\"[!] python-dotenv non installé : poetry add python-dotenv\")

# Module utilitaire SKILLNAV (mêmes constantes que pour l'EDA)
sys.path.insert(0, str(Path.cwd().parent / 'scripts'))
from skillnav_eda import FAMILLES_FR, FAMILY_FR, TYPES_FR  # noqa: F401

REPO = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()
DATA = REPO / 'data'

NEO4J_URI = os.environ.get('NEO4J_URI', '')
NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', '')

if not NEO4J_URI or not NEO4J_PASSWORD:
    print(\"[!] NEO4J_URI ou NEO4J_PASSWORD absents du .env, la connexion va échouer.\")
    print(\"    Voir docs/MODELISATION_GUIDE.md §3 pour la procédure de création AuraDB.\")
else:
    print(f\"NEO4J_URI : {NEO4J_URI}\")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
driver.verify_connectivity()
print(\"Connexion AuraDB OK.\")
"""
))

# ============================================================================
# §1 Vérification des fichiers data
# ============================================================================
CELLS.append(md(
    """## 1. Vérification des artefacts de données

Lecture rapide des trois fichiers générés par `scripts/build_dataset.py`
pour confirmer la volumétrie attendue avant d'attaquer le chargement Neo4j.
"""
))

CELLS.append(code(
    """nodes_df = pd.read_csv(DATA / 'graph_nodes.csv')
edges_df = pd.read_csv(DATA / 'graph_edges.csv')

print(\"=== graph_nodes.csv ===\")
print(nodes_df['node_type'].value_counts().to_string())
print(f\"  Total : {len(nodes_df)} nœuds\\n\")

print(\"=== graph_edges.csv ===\")
print(edges_df['relation'].value_counts().to_string())
print(f\"  Total : {len(edges_df)} arêtes\")
"""
))

# ============================================================================
# §2 Contraintes et index
# ============================================================================
CELLS.append(md(
    """## 2. Contraintes d'unicité et index

À exécuter une seule fois sur une base vierge. Les contraintes accélèrent les
`MERGE` et garantissent l'unicité des identifiants. La commande utilise
`IF NOT EXISTS` pour rester idempotente.
"""
))

CELLS.append(code(
    """CYPHER_CONTRAINTES = [
    'CREATE CONSTRAINT job_id_unique IF NOT EXISTS FOR (j:Job) REQUIRE j.node_id IS UNIQUE',
    'CREATE CONSTRAINT skill_id_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.node_id IS UNIQUE',
    'CREATE CONSTRAINT company_id_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.node_id IS UNIQUE',
]

with driver.session() as session:
    for q in CYPHER_CONTRAINTES:
        session.run(q)
        print(\"OK :\", q[:60], \"...\")
"""
))

# ============================================================================
# §3 Chargement bulk des nœuds
# ============================================================================
CELLS.append(md(
    """## 3. Chargement des nœuds (Job, Skill, Company)

Trois passes UNWIND par type. Chaque batch fait l'objet d'une transaction
unique, ce qui est l'idiome recommandé par Neo4j pour AuraDB Free Tier
(meilleure performance que le `LOAD CSV FROM URL` quand les fichiers ne sont
pas hébergés publiquement).
"""
))

CELLS.append(code(
    """BATCH_SIZE = 500


def loader_nodes(session, df, label: str, props: list[str]) -> int:
    \"\"\"Charge un sous-ensemble de nœuds par batch.\"\"\"
    rows = df.to_dict(orient='records')
    total = 0
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        # Construction du SET dynamique sur les propriétés non vides
        set_clause = ', '.join([f'n.{p} = row.{p}' for p in props if p != 'node_id'])
        query = (
            f\"UNWIND $rows AS row \"
            f\"MERGE (n:{label} {{ node_id: row.node_id }}) \"
            f\"SET {set_clause}\"
        )
        session.run(query, rows=batch)
        total += len(batch)
    return total


debut = time.time()
with driver.session() as session:
    # Job
    jobs = nodes_df[nodes_df['node_type'] == 'Job'].fillna('')
    n_jobs = loader_nodes(session, jobs, 'Job',
                          ['node_id', 'title_canonical', 'ai_type', 'job_family',
                           'posted_month', 'origine', 'source'])
    print(f\"Job   : {n_jobs} chargés\")

    # Skill
    skills = nodes_df[nodes_df['node_type'] == 'Skill'].fillna('')
    n_skills = loader_nodes(session, skills, 'Skill',
                            ['node_id', 'name', 'famille'])
    print(f\"Skill : {n_skills} chargés\")

    # Company
    companies = nodes_df[nodes_df['node_type'] == 'Company'].fillna('')
    n_companies = loader_nodes(session, companies, 'Company',
                               ['node_id', 'name', 'stage', 'focus'])
    print(f\"Company : {n_companies} chargés\")

print(f\"\\nTemps total chargement nœuds : {time.time()-debut:.1f} s\")
"""
))

# ============================================================================
# §4 Chargement bulk des arêtes
# ============================================================================
CELLS.append(md(
    """## 4. Chargement des arêtes (REQUIRES, POSTED_BY)

Même approche que pour les nœuds : UNWIND + MERGE par batch. La requête
joint le nœud source et le nœud cible par leur `node_id`.
"""
))

CELLS.append(code(
    """def loader_edges(session, df, relation: str) -> int:
    \"\"\"Charge des arêtes Job->X par batch.\"\"\"
    rows = df[df['relation'] == relation].to_dict(orient='records')
    total = 0
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        query = (
            \"UNWIND $rows AS row \"
            \"MATCH (a { node_id: row.source_id }) \"
            \"MATCH (b { node_id: row.target_id }) \"
            f\"MERGE (a)-[r:{relation}]->(b) \"
            \"SET r.weight = toInteger(row.weight)\"
        )
        session.run(query, rows=batch)
        total += len(batch)
    return total


debut = time.time()
with driver.session() as session:
    n_req = loader_edges(session, edges_df, 'REQUIRES')
    print(f\"REQUIRES   : {n_req} arêtes chargées\")

    n_post = loader_edges(session, edges_df, 'POSTED_BY')
    print(f\"POSTED_BY  : {n_post} arêtes chargées\")

print(f\"\\nTemps total chargement arêtes : {time.time()-debut:.1f} s\")
"""
))

# ============================================================================
# §5 Validation
# ============================================================================
CELLS.append(md(
    """## 5. Validation par comptages

Vérification que les comptages dans Neo4j correspondent à ceux des CSV.
Si l'écart est nul, le graphe est correctement peuplé.
"""
))

CELLS.append(code(
    """with driver.session() as session:
    print(\"=== Comptages Neo4j ===\")
    result = session.run('MATCH (n) RETURN labels(n)[0] AS label, count(*) AS n ORDER BY n DESC')
    for record in result:
        print(f\"  {record['label']:<10} {record['n']:>6}\")

    print(\"\\n=== Relations Neo4j ===\")
    result = session.run('MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS n ORDER BY n DESC')
    for record in result:
        print(f\"  {record['type']:<12} {record['n']:>6}\")
"""
))

# ============================================================================
# §6 Exemple Louvain
# ============================================================================
CELLS.append(md(
    """## 6. Exemple : algorithme de communautés Louvain

Première exécution sur le sous-graphe **Skill ↔ Skill** induit par les
co-occurrences dans les offres. Étapes :

1. Projection en mémoire d'un graphe `gds.graph.project` pondéré
2. Exécution de Louvain en mode `stream` (sans écrire dans la base)
3. Agrégation : taille des communautés et top 5 compétences par communauté

> Cette cellule sert de **patron** : les trois algorithmes suivants
> (Leiden, Label Propagation, PageRank) suivent exactement la même structure.
"""
))

CELLS.append(code(
    """# Création d'un graphe de projection pondéré Skill-Skill
# Note : Louvain travaille mieux sur un graphe non orienté.
# On part du graphe biparti Job-Skill et on l'agrège côté Skill.

PROJECTION_NAME = 'skillnav_skills'

CYPHER_DROP = f\"CALL gds.graph.drop('{PROJECTION_NAME}', false) YIELD graphName RETURN graphName\"
CYPHER_PROJECT = f\"\"\"
CALL gds.graph.project(
  '{PROJECTION_NAME}',
  ['Skill', 'Job'],
  {{ REQUIRES: {{ orientation: 'UNDIRECTED' }} }}
)
\"\"\"

with driver.session() as session:
    try:
        session.run(CYPHER_DROP)
    except Exception:
        pass
    result = session.run(CYPHER_PROJECT).single()
    print(\"Projection :\", result['graphName'] if result else PROJECTION_NAME)


# --- Louvain (algorithme de référence) ---
CYPHER_LOUVAIN = f\"\"\"
CALL gds.louvain.stream('{PROJECTION_NAME}')
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS node, communityId
WHERE node:Skill
RETURN communityId,
       count(*) AS taille,
       collect(node.name)[..5] AS top_5_competences
ORDER BY taille DESC
LIMIT 15
\"\"\"

debut = time.time()
with driver.session() as session:
    result = session.run(CYPHER_LOUVAIN)
    communautes_louvain = list(result)
runtime_louvain = time.time() - debut

print(f\"\\n=== Louvain : top 15 communautés ===\")
for r in communautes_louvain:
    skills = ', '.join(r['top_5_competences'])
    print(f\"  Communauté #{r['communityId']:>5} ({r['taille']:>4} skills) : {skills}\")

print(f\"\\nNombre de communautés (top 15 affichées) : voir résultat ci-dessus\")
print(f\"Temps d'exécution Louvain : {runtime_louvain:.2f} s\")
"""
))

# ============================================================================
# §7 TODO Bachirou : Leiden, Label Propagation, PageRank
# ============================================================================
CELLS.append(md(
    """## 7. TODO : Leiden, Label Propagation et PageRank

> **À compléter par le destinataire.** Pour chaque algorithme :
>
> 1. Adapter la requête Cypher en s'inspirant de §6 (Louvain).
> 2. Mesurer le temps d'exécution.
> 3. Compter le nombre de communautés détectées.
> 4. Sauvegarder le top 15 des communautés dans une variable Python.
>
> Documentation de référence (Graph Data Science library) :
>
> - Leiden : https://neo4j.com/docs/graph-data-science/current/algorithms/leiden/
> - Label Propagation : https://neo4j.com/docs/graph-data-science/current/algorithms/label-propagation/
> - PageRank : https://neo4j.com/docs/graph-data-science/current/algorithms/page-rank/
"""
))

CELLS.append(code(
    """# === TODO 1 : Leiden ===
# Astuce : la requête est identique à Louvain, remplacer gds.louvain.stream
# par gds.leiden.stream.

CYPHER_LEIDEN = f\"\"\"
CALL gds.leiden.stream('{PROJECTION_NAME}')
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS node, communityId
WHERE node:Skill
RETURN communityId, count(*) AS taille, collect(node.name)[..5] AS top_5_competences
ORDER BY taille DESC
LIMIT 15
\"\"\"

# debut = time.time()
# with driver.session() as session:
#     communautes_leiden = list(session.run(CYPHER_LEIDEN))
# runtime_leiden = time.time() - debut
# for r in communautes_leiden:
#     print(f\"  Communauté #{r['communityId']} ({r['taille']} skills) : {', '.join(r['top_5_competences'])}\")
# print(f\"Temps Leiden : {runtime_leiden:.2f} s\")

print(\"TODO : décommenter et exécuter le bloc Leiden ci-dessus.\")
"""
))

CELLS.append(code(
    """# === TODO 2 : Label Propagation ===
# Astuce : gds.labelPropagation.stream, algorithme rapide mais non-déterministe.
# Penser à fixer le seed si on veut un résultat reproductible.

CYPHER_LABELPROP = f\"\"\"
CALL gds.labelPropagation.stream('{PROJECTION_NAME}', {{ maxIterations: 10 }})
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS node, communityId
WHERE node:Skill
RETURN communityId, count(*) AS taille, collect(node.name)[..5] AS top_5_competences
ORDER BY taille DESC
LIMIT 15
\"\"\"

print(\"TODO : exécuter Label Propagation avec la requête ci-dessus.\")
"""
))

CELLS.append(code(
    """# === TODO 3 : PageRank ===
# PageRank n'est pas un algorithme de communautés mais un calcul de centralité.
# Il sert à identifier les compétences les plus 'centrales' dans le graphe.

CYPHER_PAGERANK = f\"\"\"
CALL gds.pageRank.stream('{PROJECTION_NAME}')
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS node, score
WHERE node:Skill
RETURN node.name AS competence, score
ORDER BY score DESC
LIMIT 20
\"\"\"

print(\"TODO : exécuter PageRank avec la requête ci-dessus.\")
"""
))

# ============================================================================
# §8 Tableau comparatif §N2.2
# ============================================================================
CELLS.append(md(
    """## 8. Tableau comparatif §N2.2 (à remplir et reporter dans le rapport L5)

Après exécution des trois algorithmes ci-dessus, compléter le tableau
suivant. Les colonnes attendues sont alignées avec la section §N2.2 du PRD
et la grille d'évaluation §16 du rapport L5.

| Algorithme         | Nombre de communautés | Modularité | Temps (s) | Notes interprétatives                          |
|--------------------|-----------------------|------------|-----------|------------------------------------------------|
| Louvain            | _à compléter_         | _à compléter_ | _à compléter_ | Méthode itérative classique             |
| Leiden             | _à compléter_         | _à compléter_ | _à compléter_ | Amélioration de Louvain (garantie de connexité) |
| Label Propagation  | _à compléter_         | _à compléter_ | _à compléter_ | Très rapide, mais non-déterministe       |
| PageRank           | n/a                   | n/a        | _à compléter_ | Centralité plutôt que partition          |

**Critères d'acceptation** :

- Toutes les cellules « à compléter » sont renseignées avec des valeurs numériques.
- Un paragraphe d'interprétation est ajouté en dessous du tableau dans le rapport L5.
- Le choix d'algorithme retenu pour la version 1.0 de SKILLNAV est justifié en deux à trois phrases.
"""
))

# ============================================================================
# §9 Fermeture
# ============================================================================
CELLS.append(md("## 9. Fermeture de la connexion\n"))

CELLS.append(code(
    """driver.close()
print(\"Driver Neo4j fermé. Notebook terminé.\")
"""
))

# ============================================================================
# Sérialisation
# ============================================================================
NOTEBOOK = {
    "cells": CELLS,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


def main() -> None:
    NB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(NB_PATH, "w", encoding="utf-8") as f:
        json.dump(NOTEBOOK, f, ensure_ascii=False, indent=1)
    with open(NB_PATH, "r", encoding="utf-8") as f:
        contenu = f.read()
    n_emdash = contenu.count("—")
    print(f"Notebook écrit : {NB_PATH}")
    print(f"Cellules : {len(CELLS)}")
    print(f"Em-dashes restants : {n_emdash}")
    if n_emdash:
        raise SystemExit("ERREUR : des em-dashes subsistent.")


if __name__ == "__main__":
    main()
