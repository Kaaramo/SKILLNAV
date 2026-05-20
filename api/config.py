"""Configuration de l'API FastAPI SKILLNAV.

Lit les variables d'environnement depuis `.env` à la racine du projet via
pydantic-settings. Toutes les valeurs sensibles (URI Mongo, URL ES, etc.)
proviennent du `.env` qui est gitignored.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


REPO = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Configuration globale de l'API.

    Charge automatiquement les variables depuis `.env` à la racine du repo.
    """

    model_config = SettingsConfigDict(
        env_file=str(REPO / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ────────────────────────────────────────────────────────────────────
    # Application
    # ────────────────────────────────────────────────────────────────────
    APP_NAME: str = "SKILLNAV API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DEFAULT_LANGUAGE: str = "fr"

    # ────────────────────────────────────────────────────────────────────
    # MongoDB Atlas (source of truth)
    # ────────────────────────────────────────────────────────────────────
    MONGODB_URI: str
    MONGODB_DB: str = "skillnav"
    MONGODB_COLLECTION: str = "jobs"

    # ────────────────────────────────────────────────────────────────────
    # Elasticsearch / OpenSearch (Bonsai)
    # ────────────────────────────────────────────────────────────────────
    ELASTIC_URL: str
    ELASTIC_INDEX: str = "skillnav_jobs"

    # ────────────────────────────────────────────────────────────────────
    # Neo4j (Bachirou, peut être indisponible)
    # ────────────────────────────────────────────────────────────────────
    NEO4J_URI: str = ""
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""

    # ────────────────────────────────────────────────────────────────────
    # NER pipeline
    # ────────────────────────────────────────────────────────────────────
    # Si True, les 3 modèles BERT sont chargés au démarrage (~20 s).
    # Si False (défaut), ils sont chargés à la première requête NER.
    LOAD_NER_AT_STARTUP: bool = False
    # Si True, l'endpoint /ner/extract est désactivé (utile pour le déploiement
    # Vercel qui n'a pas assez de RAM pour les modèles BERT).
    DISABLE_NER: bool = False

    # ────────────────────────────────────────────────────────────────────
    # CORS
    # ────────────────────────────────────────────────────────────────────
    # En dev : ouvert. En prod : restreint à *.vercel.app + localhost.
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://skillnav.vercel.app",
    ]

    # ────────────────────────────────────────────────────────────────────
    # API
    # ────────────────────────────────────────────────────────────────────
    API_PREFIX: str = "/api/v1"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000


@lru_cache
def get_settings() -> Settings:
    """Renvoie le singleton Settings (cache LRU)."""
    return Settings()  # type: ignore[call-arg]
