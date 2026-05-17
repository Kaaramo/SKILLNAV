"""Ingestion du corpus SKILLNAV dans Bonsai (OpenSearch 2.x).

Lit data/jobs.jsonl (produit par scripts/build_dataset.py) et indexe les
3 467 documents dans l'index `skillnav_jobs` du cluster Bonsai défini par
ELASTIC_URL dans `.env`.

Bonsai Sandbox provisionne OpenSearch 2.x (fork open source d'Elasticsearch).
Le client utilisé est `opensearch-py`, compatible avec l'API Elasticsearch
7.x et OpenSearch 1.x/2.x.

Idempotent : chaque document utilise son `_id` issu de jobs.jsonl
(`job_<source>_<job_id>`). Une nouvelle exécution remplace simplement les
documents existants.

Exécution :  python scripts/ingestion/ingest_elasticsearch.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from opensearchpy import OpenSearch, helpers
from opensearchpy.exceptions import ConnectionError as OSConnectionError

REPO = Path(__file__).resolve().parent.parent.parent
DATA_FILE = REPO / "data" / "jobs.jsonl"

BATCH_SIZE = 500


# ----------------------------------------------------------------------------
# Mapping de l'index
# ----------------------------------------------------------------------------
INDEX_MAPPING = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "fr_en_mixed": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding"],
                }
            }
        },
    },
    "mappings": {
        "properties": {
            "origine": {"type": "keyword"},
            "source": {"type": "keyword"},
            "posted_month": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "fr_en_mixed",
                "fields": {"raw": {"type": "keyword"}},
            },
            "title_canonical": {"type": "keyword"},
            "job_family": {"type": "keyword"},
            "ai_type": {"type": "keyword"},
            "company": {
                "type": "keyword",
                "fields": {"text": {"type": "text", "analyzer": "fr_en_mixed"}},
            },
            "stage": {"type": "keyword"},
            "focus": {"type": "text", "analyzer": "fr_en_mixed"},
            "is_customer_facing": {"type": "boolean"},
            "is_management": {"type": "boolean"},
            "responsibilities": {"type": "text", "analyzer": "fr_en_mixed"},
            "use_cases": {"type": "text", "analyzer": "fr_en_mixed"},
            "skills": {
                "properties": {
                    "genai": {"type": "keyword"},
                    "ml": {"type": "keyword"},
                    "web": {"type": "keyword"},
                    "databases": {"type": "keyword"},
                    "data": {"type": "keyword"},
                    "cloud": {"type": "keyword"},
                    "ops": {"type": "keyword"},
                    "languages": {"type": "keyword"},
                    "domains": {"type": "keyword"},
                    "other": {"type": "keyword"},
                }
            },
            # Champ aplati pour faciliter les agrégations cross-famille
            "skills_all": {"type": "keyword"},
        }
    },
}


def get_client() -> tuple[OpenSearch, str]:
    """Charge .env, parse ELASTIC_URL, retourne (client, index_name)."""
    load_dotenv(REPO / ".env")
    url = os.environ.get("ELASTIC_URL")
    index_name = os.environ.get("ELASTIC_INDEX", "skillnav_jobs")
    if not url:
        sys.exit("ERREUR : ELASTIC_URL introuvable dans .env")

    parsed = urlparse(url)
    auth = (parsed.username, parsed.password) if parsed.username else None
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 9200)

    print("Connexion au cluster Bonsai (OpenSearch)...")
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=parsed.scheme == "https",
        verify_certs=True,
        ssl_show_warn=False,
        timeout=30,
    )
    try:
        info = client.info()
    except OSConnectionError as exc:
        sys.exit(f"ERREUR : connexion impossible. Détails : {exc}")
    print(f"  Distribution  : {info['version'].get('distribution', 'elasticsearch')}")
    print(f"  Version       : {info['version']['number']}")
    print(f"  Index cible   : {index_name}\n")
    return client, index_name


def lire_jobs_jsonl(chemin: Path):
    """Itère ligne par ligne sur data/jobs.jsonl en aplatissant skills.* dans skills_all."""
    if not chemin.exists():
        sys.exit(f"ERREUR : fichier introuvable {chemin}")
    with chemin.open("r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            doc = json.loads(ligne)
            # Aplatit toutes les compétences en une seule liste pour les agrégations
            skills_dict = doc.get("skills", {})
            skills_all = []
            for liste in skills_dict.values():
                if isinstance(liste, list):
                    skills_all.extend(liste)
            doc["skills_all"] = skills_all
            yield doc


def construire_index(client: OpenSearch, index_name: str) -> None:
    """Crée ou recrée l'index avec le mapping cible."""
    if client.indices.exists(index=index_name):
        print(f"  Index existant {index_name} : suppression et recréation...")
        client.indices.delete(index=index_name)
    client.indices.create(index=index_name, body=INDEX_MAPPING)
    print(f"  Index {index_name} créé avec mapping multilingue (FR + EN)\n")


def actions_pour_bulk(index_name: str, docs):
    """Génère les actions bulk au format opensearch-py helpers.bulk.

    Important : on retire `_id` du _source car OpenSearch refuse les champs
    metadata (`_id`, `_type`...) à l'intérieur du document. Il faut le
    passer séparément via la clé `_id` de l'action.
    """
    for doc in docs:
        doc_id = doc.pop("_id", None)
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_id": doc_id,
            "_source": doc,
        }


def afficher_resume(client: OpenSearch, index_name: str) -> None:
    """Comptages + agrégations échantillon + 1 sample."""
    # Force la cohérence pour le comptage
    client.indices.refresh(index=index_name)

    total = client.count(index=index_name)["count"]
    print(f"\n=== Résumé final ===")
    print(f"  Total documents indexés : {total}")

    # Distribution origine
    agg_origine = client.search(
        index=index_name,
        body={
            "size": 0,
            "aggs": {"par_origine": {"terms": {"field": "origine"}}},
        },
    )
    print("\n  Distribution origine :")
    for bucket in agg_origine["aggregations"]["par_origine"]["buckets"]:
        print(f"    {bucket['key']:<15} {bucket['doc_count']:>5}")

    # Top 10 compétences toutes familles
    agg_skills = client.search(
        index=index_name,
        body={
            "size": 0,
            "aggs": {"top_skills": {"terms": {"field": "skills_all", "size": 10}}},
        },
    )
    print("\n  Top 10 compétences globales :")
    for bucket in agg_skills["aggregations"]["top_skills"]["buckets"]:
        print(f"    {bucket['key']:<25} {bucket['doc_count']:>5}")

    # Test recherche full-text
    print("\n  Test full-text : 'data scientist' au Maroc")
    res = client.search(
        index=index_name,
        body={
            "size": 3,
            "query": {
                "bool": {
                    "must": [{"match": {"responsibilities": "data scientist"}}],
                    "filter": [{"term": {"origine": "Maroc"}}],
                }
            },
        },
    )
    print(f"    {res['hits']['total']['value']} matches trouvés (top 3 affichés) :")
    for hit in res["hits"]["hits"]:
        s = hit["_source"]
        print(f"      score={hit['_score']:.2f}  {s.get('title_canonical', ''):<30}  {s.get('company', '')}")


def main() -> None:
    print("=" * 60)
    print("  SKILLNAV : ingestion Bonsai OpenSearch")
    print("=" * 60 + "\n")

    client, index_name = get_client()

    print(f"Préparation de l'index {index_name}...")
    construire_index(client, index_name)

    print(f"Lecture et bulk indexation depuis {DATA_FILE.relative_to(REPO)}...")
    debut = time.time()
    succes, erreurs = helpers.bulk(
        client,
        actions_pour_bulk(index_name, lire_jobs_jsonl(DATA_FILE)),
        chunk_size=BATCH_SIZE,
        request_timeout=60,
        raise_on_error=False,
        max_retries=3,
    )
    duree = time.time() - debut
    print(f"\n{succes} documents indexés en {duree:.1f} s ({succes/max(duree,0.001):.0f} docs/s)")
    if erreurs:
        print(f"  ATTENTION : {len(erreurs)} erreurs (3 premières) :")
        for err in erreurs[:3]:
            print(f"    {err}")

    afficher_resume(client, index_name)

    print("\nIngestion terminée. L'index skillnav_jobs est prêt.")


if __name__ == "__main__":
    main()
