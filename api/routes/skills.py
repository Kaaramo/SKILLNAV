"""Endpoints /skills : top compétences + jobs par compétence."""

from fastapi import APIRouter, Query

from api.db.mongo import jobs_par_skill, top_skills
from api.models.common import JobSummary, SkillCount


router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/top", response_model=list[SkillCount])
def get_top_skills(
    famille: str | None = Query(None, description="genai, ml, web, databases, data, cloud, ops, languages, domains, other"),
    origine: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> list[SkillCount]:
    rows = top_skills(famille=famille, origine=origine, limit=limit)
    return [SkillCount(**r) for r in rows]


@router.get("/{name}/jobs", response_model=list[JobSummary])
def jobs_for_skill(name: str, limit: int = Query(50, ge=1, le=200)) -> list[JobSummary]:
    docs = jobs_par_skill(name, limit=limit)
    return [JobSummary.model_validate(d) for d in docs]
