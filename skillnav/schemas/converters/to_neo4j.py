"""Converter Pydantic v2 -> parametres Cypher pour Neo4j AuraDB.

Toute mutation dans skillnav/schemas/graph.py doit casser ce fichier au type-check.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from skillnav.schemas.graph import (
    BelongsToEdge,
    CoOccursWithEdge,
    CompanyNode,
    JobNode,
    PostedByEdge,
    RequiresEdge,
    SkillGraph,
    SkillNode,
)

if TYPE_CHECKING:
    from skillnav.db.neo4j.client import Neo4jClient

# ── Requetes Cypher (UNWIND batch) ────────────────────────────────────────────

_MERGE_SKILL = """
UNWIND $rows AS row
MERGE (s:Skill {name: row.name})
SET s.family           = row.family,
    s.pagerank_score   = row.pagerank_score,
    s.community_id     = row.community_id,
    s.occurrence_count = row.occurrence_count
"""

_MERGE_JOB = """
UNWIND $rows AS row
MERGE (j:Job {job_id: row.job_id})
SET j.title        = row.title,
    j.company      = row.company,
    j.country      = row.country,
    j.source       = row.source,
    j.published_at = row.published_at
"""

_MERGE_CO_OCCURS = """
UNWIND $rows AS row
MATCH (a:Skill {name: row.skill_a}), (b:Skill {name: row.skill_b})
MERGE (a)-[r:CO_OCCURS_WITH]-(b)
SET r.weight = row.weight, r.period = row.period
"""

_MERGE_REQUIRES = """
UNWIND $rows AS row
MATCH (j:Job {job_id: row.job_id}), (s:Skill {name: row.skill_name})
MERGE (j)-[r:REQUIRES]->(s)
SET r.confidence = row.confidence
"""

_MERGE_BELONGS_TO = """
UNWIND $rows AS row
MATCH (s:Skill {name: row.skill_name})
MERGE (f:SkillFamily {name: row.family_name})
MERGE (s)-[:BELONGS_TO]->(f)
"""

_MERGE_COMPANY = """
UNWIND $rows AS row
MERGE (c:Company {name: row.name})
SET c.country   = row.country,
    c.job_count = row.job_count
"""

_MERGE_POSTED_BY = """
UNWIND $rows AS row
MATCH (c:Company {name: row.company_name}), (j:Job {job_id: row.job_id})
MERGE (c)-[:POSTED_BY]->(j)
"""

# ── Fonctions de conversion ────────────────────────────────────────────────────


def skill_node_to_params(node: SkillNode) -> dict[str, Any]:
    return {
        "name": node.name,
        "family": node.family.value,
        "pagerank_score": node.pagerank_score,
        "community_id": node.community_id,
        "occurrence_count": node.occurrence_count,
    }


def job_node_to_params(node: JobNode) -> dict[str, Any]:
    return {
        "job_id": node.job_id,
        "title": node.title,
        "company": node.company,
        "country": node.country,
        "source": node.source,
        "published_at": node.published_at.isoformat() if node.published_at else None,
    }


def co_occurs_to_params(edge: CoOccursWithEdge) -> dict[str, Any]:
    return {
        "skill_a": edge.skill_a,
        "skill_b": edge.skill_b,
        "weight": edge.weight,
        "period": edge.period,
    }


def requires_to_params(edge: RequiresEdge) -> dict[str, Any]:
    return {
        "job_id": edge.job_id,
        "skill_name": edge.skill_name,
        "confidence": edge.confidence,
    }


def belongs_to_params(edge: BelongsToEdge) -> dict[str, Any]:
    return {
        "skill_name": edge.skill_name,
        "family_name": edge.family_name,
    }


def company_node_to_params(node: CompanyNode) -> dict[str, Any]:
    return {
        "name": node.name,
        "country": node.country,
        "job_count": node.job_count,
    }


def posted_by_to_params(edge: PostedByEdge) -> dict[str, Any]:
    return {
        "company_name": edge.company_name,
        "job_id": edge.job_id,
    }


# ── Push complet vers Neo4j ────────────────────────────────────────────────────


async def push_graph_to_neo4j(graph: SkillGraph, client: Neo4jClient) -> None:
    """Envoie le SkillGraph complet vers Neo4j AuraDB via requetes UNWIND batch."""
    await client.run_write(_MERGE_SKILL, rows=[skill_node_to_params(n) for n in graph.nodes_skills])
    await client.run_write(_MERGE_JOB, rows=[job_node_to_params(n) for n in graph.nodes_jobs])
    await client.run_write(
        _MERGE_COMPANY, rows=[company_node_to_params(n) for n in graph.nodes_companies]
    )
    await client.run_write(
        _MERGE_CO_OCCURS, rows=[co_occurs_to_params(e) for e in graph.edges_co_occurs]
    )
    await client.run_write(
        _MERGE_REQUIRES, rows=[requires_to_params(e) for e in graph.edges_requires]
    )
    await client.run_write(
        _MERGE_BELONGS_TO, rows=[belongs_to_params(e) for e in graph.edges_belongs_to]
    )
    await client.run_write(
        _MERGE_POSTED_BY, rows=[posted_by_to_params(e) for e in graph.edges_posted_by]
    )
