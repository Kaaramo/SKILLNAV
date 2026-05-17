"""Endpoint de santé de l'API."""

from fastapi import APIRouter

from api.config import get_settings
from api.db.mongo import ping_mongo
from api.db.elastic import ping_elastic
from api.ml.ner_pipeline import status as ner_status
from api.models.common import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Statut global de l'API et de ses dépendances."""
    s = get_settings()
    mongo_ok = ping_mongo()
    elastic_ok = ping_elastic()
    n_status = ner_status()
    return HealthResponse(
        status="ok" if mongo_ok and elastic_ok else "degraded",
        app_name=s.APP_NAME,
        app_version=s.APP_VERSION,
        mongo="ok" if mongo_ok else "down",
        elastic="ok" if elastic_ok else "down",
        ner_loaded=any(m["loaded"] for m in n_status["models"].values()),
    )
