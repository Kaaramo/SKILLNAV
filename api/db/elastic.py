"""Client OpenSearch (Bonsai) + requêtes full-text et agrégations."""

from __future__ import annotations

from functools import lru_cache
from typing import Any
from urllib.parse import urlparse

from opensearchpy import OpenSearch

from api.config import get_settings


@lru_cache
def get_es_client() -> OpenSearch:
    """Singleton OpenSearch client."""
    s = get_settings()
    parsed = urlparse(s.ELASTIC_URL)
    auth = (parsed.username, parsed.password) if parsed.username else None
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 9200)
    return OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=(parsed.scheme == "https"),
        verify_certs=True,
        ssl_show_warn=False,
        timeout=20,
    )


def ping_elastic() -> bool:
    try:
        return bool(get_es_client().ping())
    except Exception:
        return False


def search(
    query: str | None = None,
    origine: str | None = None,
    ai_type: str | None = None,
    job_family: str | None = None,
    limit: int = 20,
    skip: int = 0,
) -> dict[str, Any]:
    """Recherche full-text avec filtres facettés."""
    s = get_settings()
    must: list[dict] = []
    if query:
        must.append({
            "multi_match": {
                "query": query,
                "fields": ["title^2", "title_canonical^2", "responsibilities", "use_cases", "focus", "company"],
                "fuzziness": "AUTO",
            }
        })
    filter_clauses: list[dict] = []
    if origine:
        filter_clauses.append({"term": {"origine.keyword": origine}})
    if ai_type:
        filter_clauses.append({"term": {"ai_type.keyword": ai_type}})
    if job_family:
        filter_clauses.append({"term": {"job_family.keyword": job_family}})

    body: dict[str, Any] = {
        "from": skip,
        "size": limit,
        "query": {
            "bool": {
                "must": must or [{"match_all": {}}],
                "filter": filter_clauses,
            }
        },
        "highlight": {
            "fields": {
                "title": {},
                "responsibilities": {"fragment_size": 150, "number_of_fragments": 2},
                "use_cases": {"fragment_size": 150, "number_of_fragments": 2},
            },
            "pre_tags": ["<mark>"],
            "post_tags": ["</mark>"],
        },
    }

    res = get_es_client().search(index=s.ELASTIC_INDEX, body=body)
    hits = res.get("hits", {})
    return {
        "total": hits.get("total", {}).get("value", 0),
        "items": [
            {
                "id": h["_id"],
                "score": round(h.get("_score") or 0, 3),
                "source": h.get("_source", {}),
                "highlight": h.get("highlight", {}),
            }
            for h in hits.get("hits", [])
        ],
        "skip": skip,
        "limit": limit,
    }


def agg_top_skills(field: str = "skills_all", origine: str | None = None, limit: int = 20) -> list[dict]:
    s = get_settings()
    body: dict[str, Any] = {
        "size": 0,
        "aggs": {"top": {"terms": {"field": field, "size": limit}}},
    }
    if origine:
        body["query"] = {"bool": {"filter": [{"term": {"origine.keyword": origine}}]}}
    res = get_es_client().search(index=s.ELASTIC_INDEX, body=body)
    return [
        {"skill": b["key"], "n": b["doc_count"]}
        for b in res.get("aggregations", {}).get("top", {}).get("buckets", [])
    ]
