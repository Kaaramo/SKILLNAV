"""Schémas Pydantic communs : pagination, erreurs, réponses standard."""

from __future__ import annotations

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class HealthResponse(BaseModel):
    status: str
    app_name: str
    app_version: str
    mongo: str
    elastic: str
    ner_loaded: bool


class ErrorResponse(BaseModel):
    detail: str


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: list[T]
    skip: int = 0
    limit: int = 20


class KeyValueCount(BaseModel):
    """Couple clé/compte utilisé par les agrégations (top skills, etc.)."""
    key: str
    n: int


class SkillCount(BaseModel):
    skill: str
    n: int


class CompanyCount(BaseModel):
    company: str
    n: int


class TitleCount(BaseModel):
    title: str
    n: int


class OverviewKPI(BaseModel):
    total_jobs: int
    par_origine: list[dict[str, Any]] = Field(default_factory=list)
    par_ai_type: list[dict[str, Any]] = Field(default_factory=list)
    par_job_family: list[dict[str, Any]] = Field(default_factory=list)


class JobSummary(BaseModel):
    id: str = Field(alias="_id")
    job_id: str = ""
    title: str = ""
    title_canonical: str = ""
    company: str = ""
    origine: str = ""
    source: str = ""
    ai_type: str = ""
    job_family: str = ""
    posted_month: str = ""

    model_config = {"populate_by_name": True}


class JobDetail(BaseModel):
    id: str = Field(alias="_id")
    job_id: str = ""
    title: str = ""
    title_canonical: str = ""
    company: str = ""
    stage: str = ""
    focus: str = ""
    origine: str = ""
    source: str = ""
    ai_type: str = ""
    job_family: str = ""
    posted_month: str = ""
    is_customer_facing: bool = False
    is_management: bool = False
    responsibilities: list[str] = Field(default_factory=list)
    use_cases: list[str] = Field(default_factory=list)
    skills: dict[str, list[str]] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}


class SearchHit(BaseModel):
    id: str
    score: float
    source: dict[str, Any]
    highlight: dict[str, list[str]] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    total: int
    items: list[SearchHit]
    skip: int = 0
    limit: int = 20


class NerEntity(BaseModel):
    text: str
    label: str
    score: float
    start: int = 0
    end: int = 0
    detected_by: list[str] = Field(default_factory=list)


class NerExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    score_min: float = Field(default=0.5, ge=0.0, le=1.0)


class NerExtractResponse(BaseModel):
    texte_analyse: str
    duree_s: float
    par_modele: dict[str, list[NerEntity]]
    union: list[NerEntity]
    n_union: int
