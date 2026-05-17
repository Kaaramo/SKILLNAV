"""Deploie le graphe SKILLNAV vers Neo4j AuraDB.

Pipeline complet :
  build_graph()  -> nx.Graph + SkillGraph (Pydantic snapshot)
  compute_pagerank()  -> scores PageRank dans SkillNode
  compute_all_communities()  -> community_id (Louvain) dans SkillNode
  push_graph_to_neo4j()  -> ecrit tout dans Neo4j via Cypher UNWIND batch

Verification finale via requete Cypher : compte les noeuds + arcs crees.

Usage :
  poetry run python scripts/push_graph_to_neo4j.py
"""

from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from skillnav.db.neo4j.client import make_neo4j_client
from skillnav.pipelines.structure_mining.communities import compute_all_communities
from skillnav.pipelines.structure_mining.graph_builder import build_graph
from skillnav.pipelines.structure_mining.pagerank import compute_pagerank
from skillnav.schemas.converters.to_neo4j import push_graph_to_neo4j

VERIFY_QUERIES: dict[str, str] = {
    "Skill nodes": "MATCH (s:Skill) RETURN count(s) AS n",
    "Job nodes": "MATCH (j:Job) RETURN count(j) AS n",
    "Company nodes": "MATCH (c:Company) RETURN count(c) AS n",
    "SkillFamily nodes": "MATCH (f:SkillFamily) RETURN count(f) AS n",
    "CO_OCCURS_WITH edges": "MATCH ()-[r:CO_OCCURS_WITH]-() RETURN count(r) / 2 AS n",
    "REQUIRES edges": "MATCH ()-[r:REQUIRES]->() RETURN count(r) AS n",
    "BELONGS_TO edges": "MATCH ()-[r:BELONGS_TO]->() RETURN count(r) AS n",
    "POSTED_BY edges": "MATCH ()-[r:POSTED_BY]->() RETURN count(r) AS n",
}


async def main() -> None:
    print("=" * 70)
    print("SKILLNAV — Deploiement Neo4j AuraDB")
    print("=" * 70)

    # 1. Construction du graphe en memoire
    print("\n[1/4] Construction du graphe depuis les postings JSON...")
    t0 = time.perf_counter()
    skill_graph, nx_graph = build_graph()
    print(
        f"      OK : {skill_graph.metrics.node_count:,} skills, "
        f"{skill_graph.metrics.edge_count:,} aretes co-occurs, "
        f"{skill_graph.job_count:,} offres, "
        f"{skill_graph.company_count:,} entreprises "
        f"({time.perf_counter() - t0:.1f}s)"
    )

    # 2. PageRank
    print("\n[2/4] Calcul PageRank (alpha=0.85)...")
    t0 = time.perf_counter()
    skill_graph = compute_pagerank(nx_graph, skill_graph)
    print(f"      OK ({time.perf_counter() - t0:.2f}s)")

    # 3. Communautes (3 algorithmes)
    print("\n[3/4] Detection de communautes (Louvain + Leiden + Label Propagation)...")
    t0 = time.perf_counter()
    skill_graph, metrics = compute_all_communities(nx_graph, skill_graph)
    print(
        f"      OK : Louvain Q={metrics.louvain_modularity:.4f} | "
        f"Leiden Q={metrics.leiden_modularity:.4f} | "
        f"LP Q={metrics.label_propagation_modularity:.4f} "
        f"({time.perf_counter() - t0:.2f}s)"
    )

    # 4. Push vers Neo4j
    print("\n[4/4] Push vers Neo4j AuraDB...")
    t0 = time.perf_counter()
    async with make_neo4j_client() as client:
        await push_graph_to_neo4j(skill_graph, client)
        print(f"      OK ({time.perf_counter() - t0:.1f}s)")

        # Verification
        print("\n" + "=" * 70)
        print("Verification (requetes Cypher sur Neo4j)")
        print("=" * 70)
        for label, query in VERIFY_QUERIES.items():
            rows = await client.run(query)
            count = rows[0]["n"] if rows else 0
            print(f"  {label:<25} : {count:,}")

    print("\nDeploiement termine. Neo4j AuraDB contient le graphe SKILLNAV.")
    print("Ouvre console.neo4j.io > ton instance > 'Open' pour explorer en Cypher.")


if __name__ == "__main__":
    asyncio.run(main())
