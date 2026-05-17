"""Endpoint /search : full-text via OpenSearch."""

from fastapi import APIRouter, Query

from api.db.elastic import search
from api.models.common import SearchHit, SearchResponse


router = APIRouter(tags=["search"])


@router.get("/search", response_model=SearchResponse)
def search_jobs(
    q: str | None = Query(None, description="Requête full-text"),
    origine: str | None = Query(None),
    ai_type: str | None = Query(None),
    job_family: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
) -> SearchResponse:
    res = search(
        query=q, origine=origine, ai_type=ai_type, job_family=job_family,
        limit=limit, skip=skip,
    )
    return SearchResponse(
        total=res["total"],
        items=[SearchHit(**h) for h in res["items"]],
        skip=res["skip"],
        limit=res["limit"],
    )
