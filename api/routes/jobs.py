"""Endpoints /jobs : liste paginée + détail."""

from fastapi import APIRouter, HTTPException, Query

from api.db.mongo import get_job, list_jobs
from api.models.common import JobDetail, JobSummary, PaginatedResponse


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=PaginatedResponse[JobSummary])
def jobs(
    origine: str | None = Query(None, description="Maroc ou International"),
    ai_type: str | None = Query(None, description="ai-first, ai-support, ml-first, non-ai"),
    job_family: str | None = Query(None),
    company: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
) -> PaginatedResponse[JobSummary]:
    res = list_jobs(
        origine=origine, ai_type=ai_type, job_family=job_family,
        company=company, limit=limit, skip=skip,
    )
    return PaginatedResponse[JobSummary](
        total=res["total"],
        items=[JobSummary.model_validate(d) for d in res["items"]],
        skip=res["skip"],
        limit=res["limit"],
    )


@router.get("/{job_id}", response_model=JobDetail)
def job_detail(job_id: str) -> JobDetail:
    doc = get_job(job_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"Job {job_id} non trouvé")
    return JobDetail.model_validate(doc)
