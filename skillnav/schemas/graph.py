from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field


class SkillFamily(StrEnum):
    AGENTS_AI = "Agents AI"
    GENAI = "GenAI"
    NLP = "NLP"
    COMPUTER_VISION = "Computer Vision"
    DEEP_LEARNING = "Deep Learning"
    MLOPS = "MLOps"
    DATA_ENGINEERING = "Data Engineering"
    MACHINE_LEARNING = "Machine Learning"
    STATISTICS = "Statistics"
    DATABASES = "Databases"
    CLOUD = "Cloud"
    BI_ANALYTICS = "BI & Analytics"
    PROGRAMMING = "Programming"
    OTHER = "Other"


# ── Nœuds ────────────────────────────────────────────────────────────────────


class SkillNode(BaseModel):
    """(:Skill) — compétence canonique dans le graphe Neo4j."""

    name: str
    aliases: list[str] = Field(default_factory=list)
    family: SkillFamily = SkillFamily.OTHER
    pagerank_score: float = 0.0
    community_id: int = -1
    occurrence_count: int = 0


class JobNode(BaseModel):
    """(:Job) — offre d'emploi dans le graphe Neo4j."""

    job_id: str
    title: str
    company: str
    country: str = ""
    source: str
    published_at: datetime | None = None


class SkillFamilyNode(BaseModel):
    """(:SkillFamily) — famille de compétences (NLP, MLOps, etc.)."""

    name: str
    description: str = ""


class SourceNode(BaseModel):
    """(:Source) — plateforme d'origine de l'offre."""

    name: str
    base_url: str


class CompanyNode(BaseModel):
    """(:Company) — entreprise qui publie des offres (PRD §N2.2, recommandation Karamo)."""

    name: str
    country: str = ""
    job_count: int = 0


# ── Arêtes ────────────────────────────────────────────────────────────────────


class CoOccursWithEdge(BaseModel):
    """(:Skill)-[:CO_OCCURS_WITH {weight}]->(:Skill)"""

    skill_a: str
    skill_b: str
    weight: int = Field(ge=1, default=1)
    period: str = ""  # ex. "2026-04"


class RequiresEdge(BaseModel):
    """(:Job)-[:REQUIRES {confidence}]->(:Skill)"""

    job_id: str
    skill_name: str
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)


class BelongsToEdge(BaseModel):
    """(:Skill)-[:BELONGS_TO]->(:SkillFamily)"""

    skill_name: str
    family_name: str


class PostedByEdge(BaseModel):
    """(:Company)-[:POSTED_BY]->(:Job)

    Indique que `company_name` est l'entreprise qui a publie l'offre `job_id`.
    Le sens de la fleche suit la convention de MODELISATION_GUIDE.md.
    """

    company_name: str
    job_id: str


# ── Métriques & snapshot ──────────────────────────────────────────────────────


class PageRankEntry(BaseModel):
    skill_name: str
    score: float


class GraphMetrics(BaseModel):
    """Métriques post-exécution des algos — stockées dans MongoDB graph_metrics."""

    louvain_modularity: float = 0.0
    leiden_modularity: float = 0.0
    label_propagation_modularity: float = 0.0
    best_community_method: str = "louvain"
    pagerank_top_20: list[PageRankEntry] = Field(default_factory=list)
    community_count: int = 0
    node_count: int = 0
    edge_count: int = 0
    computed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SkillGraph(BaseModel):
    """Snapshot complet du graphe en mémoire — sérialisable pour notebooks et export."""

    nodes_skills: list[SkillNode] = Field(default_factory=list)
    nodes_jobs: list[JobNode] = Field(default_factory=list)
    nodes_families: list[SkillFamilyNode] = Field(default_factory=list)
    nodes_companies: list[CompanyNode] = Field(default_factory=list)
    edges_co_occurs: list[CoOccursWithEdge] = Field(default_factory=list)
    edges_requires: list[RequiresEdge] = Field(default_factory=list)
    edges_belongs_to: list[BelongsToEdge] = Field(default_factory=list)
    edges_posted_by: list[PostedByEdge] = Field(default_factory=list)
    metrics: GraphMetrics = Field(default_factory=GraphMetrics)
    built_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    job_count: int = 0
    company_count: int = 0
