"""Ingestion du corpus SKILLNAV dans MongoDB Atlas.

Lit data/jobs.jsonl (produit par scripts/build_dataset.py) et insère/upsert
les 3 467 documents dans la collection `skillnav.jobs` du cluster Atlas
défini par MONGODB_URI dans `.env`.

Idempotent : chaque document utilise son `_id` issu de jobs.jsonl
(`job_<source>_<job_id>`). Une nouvelle exécution remplace simplement les
documents existants.

Exécution :  python scripts/ingestion/ingest_mongodb.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient, ReplaceOne
from pymongo.errors import BulkWriteError, ConnectionFailure

REPO = Path(__file__).resolve().parent.parent.parent
DATA_FILE = REPO / "data" / "jobs.jsonl"

BATCH_SIZE = 500
COLLECTION_NAME = "jobs"


def get_client() -> tuple[MongoClient, str]:
    """Charge les variables d'environnement et retourne (client, db_name)."""
    load_dotenv(REPO / ".env")
    uri = os.environ.get("MONGODB_URI")
    db_name = os.environ.get("MONGODB_DB", "skillnav")
    if not uri:
        sys.exit("ERREUR : MONGODB_URI introuvable dans .env")

    print("Connexion au cluster MongoDB Atlas...")
    # tlsCAFile=certifi.where() évite le bug SSL Windows qui ne trouve pas le bundle CA système
    client = MongoClient(
        uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=20_000,
        connectTimeoutMS=20_000,
    )
    try:
        client.admin.command("ping")
    except ConnectionFailure as exc:
        sys.exit(f"ERREUR : impossible de se connecter au cluster. Détails : {exc}")
    print(f"  Connexion OK  ->  base cible : {db_name}.{COLLECTION_NAME}\n")
    return client, db_name


def lire_jobs_jsonl(chemin: Path):
    """Itère ligne par ligne sur le fichier JSON Lines."""
    if not chemin.exists():
        sys.exit(f"ERREUR : fichier introuvable {chemin}. Lancer scripts/build_dataset.py d'abord.")
    with chemin.open("r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                yield json.loads(ligne)
            except json.JSONDecodeError as exc:
                print(f"  [!] Ligne ignorée (JSON invalide) : {exc}")


def upsert_par_batch(collection, jobs, batch_size: int = BATCH_SIZE) -> int:
    """Upsert en bulk par batches. Retourne le nombre total de docs traités."""
    buffer: list = []
    total = 0
    for job in jobs:
        # Pymongo ne permet pas le _id custom dans bulk_write si on utilise replace_one ;
        # mais ReplaceOne accepte un filter sur _id, c'est ce qu'on veut.
        buffer.append(ReplaceOne({"_id": job["_id"]}, job, upsert=True))
        if len(buffer) >= batch_size:
            collection.bulk_write(buffer, ordered=False)
            total += len(buffer)
            print(f"  Batch upserté  ({total:>5} documents)")
            buffer.clear()
    if buffer:
        collection.bulk_write(buffer, ordered=False)
        total += len(buffer)
        print(f"  Batch upserté  ({total:>5} documents)")
    return total


def creer_indexes(collection) -> None:
    """Crée les indexes utiles pour les queries du dashboard et de l'API."""
    print("\nCréation des indexes...")
    indexes = [
        ("origine", 1),
        ("source", 1),
        ("posted_month", -1),
        ("ai_type", 1),
        ("job_family", 1),
        ("company", 1),
        ("title_canonical", 1),
    ]
    for field, direction in indexes:
        collection.create_index([(field, direction)], background=True)
        print(f"  Index simple  : {field} ({'asc' if direction == 1 else 'desc'})")

    # Multikey indexes sur les listes de skills (recherche par compétence)
    for famille in ["genai", "ml", "web", "databases", "data", "cloud", "ops", "languages", "domains"]:
        collection.create_index(f"skills.{famille}", background=True)
        print(f"  Index multikey: skills.{famille}")

    # Text index pour la recherche plein texte (page /search dashboard)
    collection.create_index(
        [("title", "text"), ("responsibilities", "text"), ("focus", "text")],
        name="text_search_idx",
        default_language="french",
        background=True,
    )
    print("  Index full-text : title + responsibilities + focus")


def afficher_resume(collection) -> None:
    """Affiche un résumé post-ingestion : comptages et 1 sample."""
    print("\n=== Résumé final ===")
    total = collection.count_documents({})
    print(f"  Total documents          : {total}")

    n_maroc = collection.count_documents({"origine": "Maroc"})
    n_intl = collection.count_documents({"origine": "International"})
    print(f"  Origine Maroc            : {n_maroc}")
    print(f"  Origine International    : {n_intl}")

    print("\n  Distribution ai_type :")
    pipeline = [
        {"$group": {"_id": "$ai_type", "n": {"$sum": 1}}},
        {"$sort": {"n": -1}},
    ]
    for row in collection.aggregate(pipeline):
        print(f"    {row['_id']:<12}  {row['n']:>5}")

    print("\n  Échantillon (1 document) :")
    sample = collection.find_one({"origine": "International", "ai_type": "ai-first"})
    if sample:
        cles = ["_id", "origine", "source", "title_canonical", "company", "ai_type", "job_family", "posted_month"]
        for k in cles:
            print(f"    {k:<18} : {sample.get(k, '')}")


def main() -> None:
    print("=" * 60)
    print("  SKILLNAV : ingestion MongoDB Atlas")
    print("=" * 60 + "\n")

    client, db_name = get_client()
    db = client[db_name]
    collection = db[COLLECTION_NAME]

    print(f"Lecture du fichier {DATA_FILE.relative_to(REPO)} ...")
    debut = time.time()

    try:
        total = upsert_par_batch(collection, lire_jobs_jsonl(DATA_FILE))
    except BulkWriteError as exc:
        print(f"\nERREUR bulk_write : {exc.details}")
        sys.exit(1)

    duree = time.time() - debut
    print(f"\n{total} documents upsertés en {duree:.1f} s ({total/max(duree,0.001):.0f} docs/s)")

    creer_indexes(collection)
    afficher_resume(collection)

    client.close()
    print("\nIngestion terminée. La collection skillnav.jobs est prête.")


if __name__ == "__main__":
    main()
