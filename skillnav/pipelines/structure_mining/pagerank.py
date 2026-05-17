"""PageRank sur le graphe de co-occurrences de competences.

Repond a : "quelle competence est la plus centrale dans le marche ?"
Score eleve = competence co-presente avec beaucoup d'autres competences importantes.
"""

from __future__ import annotations

from typing import Any

import networkx as nx

from skillnav.schemas.graph import PageRankEntry, SkillGraph


def compute_pagerank(
    nx_graph: nx.Graph,
    skill_graph: SkillGraph,
    alpha: float = 0.85,
) -> SkillGraph:
    """Calcule le PageRank (alpha=0.85) et met a jour SkillGraph.

    Args:
        nx_graph: graphe NetworkX Skill <-> Skill issu de build_graph().
        skill_graph: snapshot Pydantic a mettre a jour (in-place sur les noeuds).
        alpha: facteur d'amortissement (defaut Google = 0.85).

    Returns:
        Le meme SkillGraph avec nodes_skills[*].pagerank_score et
        metrics.pagerank_top_20 remplis.
    """
    if nx_graph.number_of_nodes() == 0:
        return skill_graph

    raw: dict[Any, Any] = nx.pagerank(nx_graph, alpha=alpha, weight="weight")
    scores: dict[str, float] = {str(k): float(v) for k, v in raw.items()}

    skill_map = {s.name: s for s in skill_graph.nodes_skills}
    for name, score in scores.items():
        if name in skill_map:
            skill_map[name].pagerank_score = score

    skill_graph.nodes_skills = list(skill_map.values())
    skill_graph.metrics.pagerank_top_20 = [
        PageRankEntry(skill_name=name, score=score)
        for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]
    ]

    return skill_graph
