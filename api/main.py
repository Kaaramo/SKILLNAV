"""Application FastAPI SKILLNAV.

Démarrage : uvicorn api.main:app --reload --port 8000
Documentation interactive : http://localhost:8000/docs
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.config import get_settings
from api.routes import comparative, companies, health, jobs, ner, overview, search, skills


@asynccontextmanager
async def lifespan(app: FastAPI):
    s = get_settings()
    print(f"\n=== {s.APP_NAME} v{s.APP_VERSION} ===")
    print(f"  Environnement : {s.APP_ENV}")
    print(f"  MongoDB DB    : {s.MONGODB_DB}")
    print(f"  ES index      : {s.ELASTIC_INDEX}")
    print(f"  Préfixe API   : {s.API_PREFIX}")
    print(f"  CORS origins  : {s.CORS_ORIGINS}")

    if s.LOAD_NER_AT_STARTUP and not s.DISABLE_NER:
        from api.ml.ner_pipeline import load_all_models
        print(f"\n  Chargement des modèles NER...")
        durations = load_all_models()
        for k, d in durations.items():
            print(f"    {k:<22} {d:.1f} s")

    print("=" * 50, flush=True)
    yield


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(
        title=s.APP_NAME,
        version=s.APP_VERSION,
        description=(
            "API SKILLNAV : observatoire des compétences IA et Data Science "
            "(Maroc + International). Source de données : 3 467 offres collectées "
            "puis indexées sur MongoDB Atlas + Bonsai OpenSearch + Neo4j AuraDB."
        ),
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=s.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix=s.API_PREFIX)
    app.include_router(overview.router, prefix=s.API_PREFIX)
    app.include_router(jobs.router, prefix=s.API_PREFIX)
    app.include_router(skills.router, prefix=s.API_PREFIX)
    app.include_router(companies.router, prefix=s.API_PREFIX)
    app.include_router(search.router, prefix=s.API_PREFIX)
    app.include_router(ner.router, prefix=s.API_PREFIX)
    app.include_router(comparative.router, prefix=s.API_PREFIX)

    @app.get("/")
    def racine() -> JSONResponse:
        return JSONResponse({
            "app": s.APP_NAME,
            "version": s.APP_VERSION,
            "docs": "/docs",
            "openapi": "/openapi.json",
            "api_prefix": s.API_PREFIX,
        })

    return app


app = create_app()
