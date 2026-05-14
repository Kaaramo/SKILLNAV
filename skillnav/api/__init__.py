"""API FastAPI — endpoints exposant Mongo / Neo4j / ES au front Next.js (PRD §11).

Module à implémenter :

- `main.py`     : `app = FastAPI(...)` + montage des routers
- `routers/`    : un router par ressource (skills, jobs, graph, forecasts, quality)
- `deps.py`     : dépendances (DB clients, settings, auth si V1.5)
"""
