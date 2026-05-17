"""Endpoint /overview : KPI globaux pour la page d'accueil du dashboard."""

from fastapi import APIRouter

from api.db.mongo import overview_kpi
from api.models.common import OverviewKPI


router = APIRouter(tags=["overview"])


@router.get("/overview", response_model=OverviewKPI)
def get_overview() -> OverviewKPI:
    """Statistiques globales sur les 3 467 fiches : volumétrie, distribution
    par type de poste, par famille, par origine."""
    data = overview_kpi()
    return OverviewKPI(**data)
