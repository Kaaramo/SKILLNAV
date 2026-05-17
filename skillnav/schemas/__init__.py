"""Pydantic v2 models — source de vérité unique pour MongoDB / Neo4j / Elasticsearch."""

from skillnav.schemas.graph import (
    BelongsToEdge,
    CoOccursWithEdge,
    CompanyNode,
    GraphMetrics,
    JobNode,
    PageRankEntry,
    PostedByEdge,
    RequiresEdge,
    SkillFamily,
    SkillFamilyNode,
    SkillGraph,
    SkillNode,
    SourceNode,
)
from skillnav.schemas.job import (
    ContractType,
    JobExtraction,
    JobStatus,
    RawJob,
    SeniorityLevel,
)
from skillnav.schemas.ner import (
    Entity,
    EntityType,
    NerAnnotation,
    NerComparison,
    NerModel,
)
from skillnav.schemas.timeseries import (
    DataPoint,
    Forecast,
    ForecastComparison,
    ForecastMethod,
    ForecastPoint,
    SkillTimeSeries,
)

__all__ = [
    # graph
    "BelongsToEdge",
    "CoOccursWithEdge",
    "CompanyNode",
    "GraphMetrics",
    "JobNode",
    "PageRankEntry",
    "PostedByEdge",
    "RequiresEdge",
    "SkillFamily",
    "SkillFamilyNode",
    "SkillGraph",
    "SkillNode",
    "SourceNode",
    # job
    "ContractType",
    "JobExtraction",
    "JobStatus",
    "RawJob",
    "SeniorityLevel",
    # ner
    "Entity",
    "EntityType",
    "NerAnnotation",
    "NerComparison",
    "NerModel",
    # timeseries
    "DataPoint",
    "Forecast",
    "ForecastComparison",
    "ForecastMethod",
    "ForecastPoint",
    "SkillTimeSeries",
]
