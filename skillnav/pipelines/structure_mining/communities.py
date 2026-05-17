"""Detection de communautes de competences — etude comparative PRD §N2.2.

3 algorithmes compares :
  - Louvain  (python-louvain) : reference, maximise la modularite
  - Leiden   (igraph)         : version amelioree de Louvain, plus stable
  - Label Propagation (networkx) : baseline rapide, non-deterministe

Metrique de comparaison : modularite Q ([-1, 1], plus eleve = meilleures communautes).
"""

from __future__ import annotations

from typing import Any

import community as community_louvain  # type: ignore[import-untyped]
import igraph as ig  # type: ignore[import-untyped]
import networkx as nx

from skillnav.schemas.graph import GraphMetrics, SkillGraph


# ── Helpers ───────────────────────────────────────────────────────────────────


def _apply_partition(skill_graph: SkillGraph, partition: dict[str, int]) -> SkillGraph:
    """Met a jour community_id sur chaque SkillNode selon la partition donnee."""
    skill_map = {s.name: s for s in skill_graph.nodes_skills}
    for name, cid in partition.items():
        if name in skill_map:
            skill_map[name].community_id = cid
    skill_graph.nodes_skills = list(skill_map.values())
    return skill_graph


def _nx_to_igraph(nx_graph: nx.Graph) -> tuple[Any, dict[int, str]]:
    """Convertit un nx.Graph en ig.Graph (pour Leiden)."""
    nodes: list[str] = list(nx_graph.nodes())
    node_to_idx: dict[str, int] = {n: i for i, n in enumerate(nodes)}
    idx_to_node: dict[int, str] = dict(enumerate(nodes))
    edges = [(node_to_idx[u], node_to_idx[v]) for u, v in nx_graph.edges()]
    weights = [float(nx_graph[u][v].get("weight", 1)) for u, v in nx_graph.edges()]
    ig_graph = ig.Graph(n=len(nodes), edges=edges, directed=False)
    ig_graph.es["weight"] = weights
    return ig_graph, idx_to_node


# ── Les 3 algorithmes ─────────────────────────────────────────────────────────


def compute_louvain(nx_graph: nx.Graph, skill_graph: SkillGraph) -> tuple[SkillGraph, float]:
    """Louvain (python-louvain) — maximise la modularite de facon gloutonne.

    Returns:
        (SkillGraph mis a jour, modularite Q)
    """
    if nx_graph.number_of_nodes() == 0:
        return skill_graph, 0.0

    partition: dict[str, int] = community_louvain.best_partition(nx_graph, weight="weight")
    modularity: float = float(
        community_louvain.modularity(partition, nx_graph, weight="weight")
    )
    skill_graph = _apply_partition(skill_graph, partition)
    skill_graph.metrics.louvain_modularity = modularity
    return skill_graph, modularity


def compute_leiden(nx_graph: nx.Graph, skill_graph: SkillGraph) -> tuple[SkillGraph, float]:
    """Leiden (igraph) — version amelioree de Louvain, garantit des communautes connectees.

    Returns:
        (SkillGraph mis a jour, modularite Q)
    """
    if nx_graph.number_of_nodes() == 0:
        return skill_graph, 0.0

    ig_graph, idx_to_node = _nx_to_igraph(nx_graph)
    result = ig_graph.community_leiden(
        objective_function="modularity",
        weights="weight",
        n_iterations=10,
    )
    modularity: float = float(result.modularity)
    partition: dict[str, int] = {
        idx_to_node[i]: cid for cid, members in enumerate(result) for i in members
    }
    skill_graph = _apply_partition(skill_graph, partition)
    skill_graph.metrics.leiden_modularity = modularity
    return skill_graph, modularity


def compute_label_propagation(
    nx_graph: nx.Graph, skill_graph: SkillGraph
) -> tuple[SkillGraph, float]:
    """Label Propagation (networkx) — algorithme baseline non-deterministe.

    Returns:
        (SkillGraph mis a jour, modularite Q)
    """
    if nx_graph.number_of_nodes() == 0:
        return skill_graph, 0.0

    communities_gen = nx.community.asyn_lpa_communities(nx_graph, weight="weight", seed=42)
    communities: list[frozenset[str]] = [frozenset(c) for c in communities_gen]
    modularity: float = float(
        nx.community.modularity(nx_graph, communities, weight="weight")
    )
    partition: dict[str, int] = {
        node: cid for cid, community in enumerate(communities) for node in community
    }
    skill_graph = _apply_partition(skill_graph, partition)
    skill_graph.metrics.label_propagation_modularity = modularity
    return skill_graph, modularity


# ── Fonction principale ───────────────────────────────────────────────────────


def compute_all_communities(
    nx_graph: nx.Graph, skill_graph: SkillGraph
) -> tuple[SkillGraph, GraphMetrics]:
    """Execute les 3 algorithmes et determine le meilleur par modularite.

    Ordre d'execution : Leiden -> Label Propagation -> Louvain (en dernier).
    community_id final sur chaque SkillNode = partitionnement Louvain (le plus etabli).

    Returns:
        (SkillGraph complet, GraphMetrics avec les 3 modularites)
    """
    if nx_graph.number_of_nodes() == 0:
        return skill_graph, skill_graph.metrics

    # Leiden et LP en premier (Louvain en dernier pour que community_id = Louvain)
    _, leiden_mod = compute_leiden(nx_graph, skill_graph)
    _, lp_mod = compute_label_propagation(nx_graph, skill_graph)
    skill_graph, louvain_mod = compute_louvain(nx_graph, skill_graph)

    best_method, _ = max(
        [("louvain", louvain_mod), ("leiden", leiden_mod), ("label_propagation", lp_mod)],
        key=lambda x: x[1],
    )
    skill_graph.metrics.best_community_method = best_method
    skill_graph.metrics.community_count = len({s.community_id for s in skill_graph.nodes_skills})

    return skill_graph, skill_graph.metrics
