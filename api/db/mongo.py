"""Client MongoDB Atlas + requêtes métier SKILLNAV."""

from __future__ import annotations

import certifi
from functools import lru_cache
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from api.config import get_settings


@lru_cache
def get_mongo_client() -> MongoClient:
    """Singleton MongoDB client (réutilise la connexion entre requêtes)."""
    s = get_settings()
    return MongoClient(
        s.MONGODB_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
        appname="skillnav-api",
    )


def get_db() -> Database:
    return get_mongo_client()[get_settings().MONGODB_DB]


def get_jobs_collection() -> Collection:
    return get_db()[get_settings().MONGODB_COLLECTION]


# ============================================================================
# REQUÊTES MÉTIER
# ============================================================================

def ping_mongo() -> bool:
    """Test de connectivité MongoDB."""
    try:
        get_mongo_client().admin.command("ping")
        return True
    except Exception:
        return False


def count_documents(filtre: dict | None = None) -> int:
    return get_jobs_collection().count_documents(filtre or {})


def overview_kpi() -> dict[str, Any]:
    """KPI globaux pour la page d'accueil."""
    coll = get_jobs_collection()
    pipeline_ai_type = [
        {"$group": {"_id": "$ai_type", "n": {"$sum": 1}}},
        {"$sort": {"n": -1}},
    ]
    pipeline_origine = [
        {"$group": {"_id": "$origine", "n": {"$sum": 1}}},
        {"$sort": {"n": -1}},
    ]
    pipeline_job_family = [
        {"$group": {"_id": "$job_family", "n": {"$sum": 1}}},
        {"$sort": {"n": -1}},
        {"$limit": 10},
    ]
    return {
        "total_jobs": coll.count_documents({}),
        "par_origine": [{"origine": d["_id"], "n": d["n"]} for d in coll.aggregate(pipeline_origine)],
        "par_ai_type": [{"ai_type": d["_id"], "n": d["n"]} for d in coll.aggregate(pipeline_ai_type)],
        "par_job_family": [{"job_family": d["_id"], "n": d["n"]} for d in coll.aggregate(pipeline_job_family)],
    }


FAMILLES_SKILLS = ["genai", "ml", "web", "databases", "data", "cloud", "ops", "languages", "domains", "other"]


def top_skills(famille: str | None = None, origine: str | None = None, limit: int = 20) -> list[dict]:
    """Top compétences (toutes familles, ou famille spécifique)."""
    coll = get_jobs_collection()
    filtre: dict = {}
    if origine:
        filtre["origine"] = origine

    if famille and famille in FAMILLES_SKILLS:
        path = f"$skills.{famille}"
        pipeline = [
            {"$match": filtre},
            {"$unwind": path[1:] if path.startswith("$") else path},
            {"$group": {"_id": path, "n": {"$sum": 1}}},
            {"$sort": {"n": -1}},
            {"$limit": limit},
        ]
        # Correction : unwind path doit être le nom sans $
        pipeline[1] = {"$unwind": f"skills.{famille}"}
        pipeline[1] = {"$unwind": "$skills." + famille}
        pipeline[2] = {"$group": {"_id": f"$skills.{famille}", "n": {"$sum": 1}}}
    else:
        # Agrégation sur toutes les familles : on aplatit avec $project + $reduce
        pipeline = [
            {"$match": filtre},
            {"$project": {
                "all_skills": {
                    "$reduce": {
                        "input": [f"$skills.{f}" for f in FAMILLES_SKILLS],
                        "initialValue": [],
                        "in": {"$concatArrays": ["$$value", {"$ifNull": ["$$this", []]}]},
                    }
                }
            }},
            {"$unwind": "$all_skills"},
            {"$group": {"_id": "$all_skills", "n": {"$sum": 1}}},
            {"$sort": {"n": -1}},
            {"$limit": limit},
        ]

    return [{"skill": d["_id"], "n": d["n"]} for d in coll.aggregate(pipeline) if d["_id"]]


def top_companies(origine: str | None = None, limit: int = 20) -> list[dict]:
    coll = get_jobs_collection()
    filtre: dict = {"company": {"$ne": ""}}
    if origine:
        filtre["origine"] = origine
    pipeline = [
        {"$match": filtre},
        {"$group": {"_id": "$company", "n": {"$sum": 1}}},
        {"$sort": {"n": -1}},
        {"$limit": limit},
    ]
    return [{"company": d["_id"], "n": d["n"]} for d in coll.aggregate(pipeline)]


def top_titres(origine: str | None = None, limit: int = 20) -> list[dict]:
    coll = get_jobs_collection()
    filtre: dict = {"title_canonical": {"$ne": ""}}
    if origine:
        filtre["origine"] = origine
    pipeline = [
        {"$match": filtre},
        {"$group": {"_id": "$title_canonical", "n": {"$sum": 1}}},
        {"$sort": {"n": -1}},
        {"$limit": limit},
    ]
    return [{"title": d["_id"], "n": d["n"]} for d in coll.aggregate(pipeline)]


def list_jobs(
    origine: str | None = None,
    ai_type: str | None = None,
    job_family: str | None = None,
    company: str | None = None,
    limit: int = 20,
    skip: int = 0,
) -> dict[str, Any]:
    coll = get_jobs_collection()
    filtre: dict = {}
    if origine:
        filtre["origine"] = origine
    if ai_type:
        filtre["ai_type"] = ai_type
    if job_family:
        filtre["job_family"] = job_family
    if company:
        filtre["company"] = company

    total = coll.count_documents(filtre)
    projection = {
        "_id": 1, "job_id": 1, "title": 1, "title_canonical": 1, "company": 1,
        "origine": 1, "source": 1, "ai_type": 1, "job_family": 1, "posted_month": 1,
    }
    items = list(coll.find(filtre, projection).skip(skip).limit(limit))
    return {"total": total, "items": items, "skip": skip, "limit": limit}


def get_job(job_id: str) -> dict | None:
    """Récupère un job complet par son _id ou son job_id."""
    coll = get_jobs_collection()
    doc = coll.find_one({"_id": job_id})
    if doc:
        return doc
    return coll.find_one({"job_id": job_id})


def jobs_par_skill(skill: str, limit: int = 50) -> list[dict]:
    """Offres qui mentionnent une compétence (toutes familles confondues)."""
    coll = get_jobs_collection()
    skill_lower = skill.lower()
    or_conditions = [
        {f"skills.{f}": {"$regex": f"^{skill}$", "$options": "i"}}
        for f in FAMILLES_SKILLS
    ]
    projection = {
        "_id": 1, "title_canonical": 1, "company": 1,
        "origine": 1, "ai_type": 1, "posted_month": 1,
    }
    return list(coll.find({"$or": or_conditions}, projection).limit(limit))
