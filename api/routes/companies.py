"""Endpoint /companies/top : top employeurs."""

from fastapi import APIRouter, Query

from api.db.mongo import top_companies, top_titres
from api.models.common import CompanyCount, TitleCount


router = APIRouter(tags=["companies"])


@router.get("/companies/top", response_model=list[CompanyCount])
def get_top_companies(
    origine: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> list[CompanyCount]:
    rows = top_companies(origine=origine, limit=limit)
    return [CompanyCount(**r) for r in rows]


@router.get("/titles/top", response_model=list[TitleCount])
def get_top_titles(
    origine: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> list[TitleCount]:
    rows = top_titres(origine=origine, limit=limit)
    return [TitleCount(**r) for r in rows]
