"""Consolidation du corpus YAML en trois artefacts de modélisation.

Lit les 3 467 fiches YAML du dossier sources/collected/ via le module
`skillnav_eda` (réutilise canonicalisation + déduplication), puis écrit
trois fichiers dérivés directement consommables par les bases de données
cibles du PRD §7.

Sorties (toutes dans data/) :

    data/jobs.jsonl            une offre par ligne (format JSON Lines)
                               -> consommé par MongoDB Atlas (mongoimport)
                               -> consommé par le backend FastAPI / dashboard

    data/graph_nodes.csv       nœuds Job / Skill / Company
                               -> consommé par Neo4j AuraDB via LOAD CSV
                                  ou via le driver Python neo4j en bulk

    data/graph_edges.csv       arêtes REQUIRES (Job→Skill) et POSTED_BY (Job→Company)
                               -> consommé par Neo4j AuraDB via LOAD CSV

Exécution :  python scripts/build_dataset.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from skillnav_eda import (  # noqa: E402
    SKILL_COLS,
    SKILL_FAMILIES,
    charger_corpus,
)

DATA_DIR = REPO / "data"
JSONL_PATH = DATA_DIR / "jobs.jsonl"
NODES_PATH = DATA_DIR / "graph_nodes.csv"
EDGES_PATH = DATA_DIR / "graph_edges.csv"


# ----------------------------------------------------------------------------
# Helpers d'identification
# ----------------------------------------------------------------------------
_SAFE_RE = re.compile(r"[^a-zA-Z0-9]+")


def safe_id(prefix: str, raw: str) -> str:
    """Construit un identifiant déterministe (alphanumeric + underscores)."""
    nettoye = _SAFE_RE.sub("_", raw.strip()).strip("_")
    return f"{prefix}_{nettoye}" if nettoye else prefix


def job_node_id(row) -> str:
    """job_<source>_<job_id>. Le préfixe source garantit l'unicité inter-sources."""
    return safe_id("job", f"{row['source']}_{row['job_id'] or row['title_canonical']}")


def skill_node_id(name: str) -> str:
    return safe_id("skill", name)


def company_node_id(name: str) -> str:
    return safe_id("company", name)


# ----------------------------------------------------------------------------
# Écriture des trois fichiers
# ----------------------------------------------------------------------------
def ecrire_jsonl(df, chemin: Path) -> int:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with chemin.open("w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            doc = {
                "_id": job_node_id(row),
                "job_id": row["job_id"],
                "origine": row["origine"],
                "source": row["source"],
                "posted_month": row["posted_month"],
                "title": row["title"],
                "title_canonical": row["title_canonical"],
                "job_family": row["job_family"],
                "ai_type": row["ai_type"],
                "company": row["company"],
                "stage": row["stage"],
                "focus": row["focus"],
                "is_customer_facing": bool(row["is_customer_facing"]),
                "is_management": bool(row["is_management"]),
                "responsibilities": list(row["responsibilities"]),
                "use_cases": list(row["use_cases"]),
                "skills": {famille: list(row[f"skills_{famille}"]) for famille in SKILL_FAMILIES},
            }
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
            n += 1
    return n


def ecrire_nodes_csv(df, chemin: Path) -> dict:
    """Écrit graph_nodes.csv (Job + Skill + Company).

    Format unifié : node_id, node_type, name, et un ensemble de colonnes
    spécifiques à chaque type (vides quand non applicables).
    """
    chemin.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "node_id",
        "node_type",
        "name",
        # propriétés Job
        "title_canonical",
        "ai_type",
        "job_family",
        "posted_month",
        "origine",
        "source",
        # propriété Skill
        "famille",
        # propriétés Company
        "stage",
        "focus",
    ]

    # Indexes de déduplication
    skills_index: "OrderedDict[str, str]" = OrderedDict()  # name -> famille
    companies_index: "OrderedDict[str, dict]" = OrderedDict()  # name -> {stage, focus}

    compteurs = {"Job": 0, "Skill": 0, "Company": 0}

    with chemin.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        # 1. nœuds Job
        for _, row in df.iterrows():
            writer.writerow({
                "node_id": job_node_id(row),
                "node_type": "Job",
                "name": "",
                "title_canonical": row["title_canonical"],
                "ai_type": row["ai_type"],
                "job_family": row["job_family"],
                "posted_month": row["posted_month"],
                "origine": row["origine"],
                "source": row["source"],
                "famille": "",
                "stage": "",
                "focus": "",
            })
            compteurs["Job"] += 1

            # indexation des skills (avec leur famille)
            for famille in SKILL_FAMILIES:
                for skill in row[f"skills_{famille}"]:
                    if skill and skill not in skills_index:
                        skills_index[skill] = famille

            # indexation des companies
            cname = (row["company"] or "").strip()
            if cname:
                if cname not in companies_index:
                    companies_index[cname] = {
                        "stage": row["stage"] or "",
                        "focus": row["focus"] or "",
                    }

        # 2. nœuds Skill (dédoublonnés)
        for name, famille in skills_index.items():
            writer.writerow({
                "node_id": skill_node_id(name),
                "node_type": "Skill",
                "name": name,
                "title_canonical": "",
                "ai_type": "",
                "job_family": "",
                "posted_month": "",
                "origine": "",
                "source": "",
                "famille": famille,
                "stage": "",
                "focus": "",
            })
            compteurs["Skill"] += 1

        # 3. nœuds Company (dédoublonnés)
        for name, props in companies_index.items():
            writer.writerow({
                "node_id": company_node_id(name),
                "node_type": "Company",
                "name": name,
                "title_canonical": "",
                "ai_type": "",
                "job_family": "",
                "posted_month": "",
                "origine": "",
                "source": "",
                "famille": "",
                "stage": props["stage"],
                "focus": props["focus"],
            })
            compteurs["Company"] += 1

    return compteurs


def ecrire_edges_csv(df, chemin: Path) -> dict:
    """Écrit graph_edges.csv (REQUIRES + POSTED_BY)."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["source_id", "target_id", "relation", "weight"]
    compteurs = {"REQUIRES": 0, "POSTED_BY": 0}

    with chemin.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for _, row in df.iterrows():
            jid = job_node_id(row)

            # REQUIRES (Job -> Skill)
            for famille in SKILL_FAMILIES:
                for skill in row[f"skills_{famille}"]:
                    if skill:
                        writer.writerow({
                            "source_id": jid,
                            "target_id": skill_node_id(skill),
                            "relation": "REQUIRES",
                            "weight": 1,
                        })
                        compteurs["REQUIRES"] += 1

            # POSTED_BY (Job -> Company)
            cname = (row["company"] or "").strip()
            if cname:
                writer.writerow({
                    "source_id": jid,
                    "target_id": company_node_id(cname),
                    "relation": "POSTED_BY",
                    "weight": 1,
                })
                compteurs["POSTED_BY"] += 1

    return compteurs


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main() -> None:
    import pandas as pd  # noqa: F401 — utilisé indirectement par charger_corpus

    print("=== Build Dataset SKILLNAV ===\n")
    print("Chargement du corpus via skillnav_eda.charger_corpus() ...")
    df_maroc, df_international = charger_corpus(verbose=True)
    df_combine = pd.concat([df_maroc, df_international], ignore_index=True)
    print()

    print(f"Écriture {JSONL_PATH.relative_to(REPO)} ...")
    n_jsonl = ecrire_jsonl(df_combine, JSONL_PATH)
    taille_jsonl = JSONL_PATH.stat().st_size // 1024
    print(f"  >>> {n_jsonl} lignes, {taille_jsonl} Ko\n")

    print(f"Écriture {NODES_PATH.relative_to(REPO)} ...")
    cpt_nodes = ecrire_nodes_csv(df_combine, NODES_PATH)
    taille_nodes = NODES_PATH.stat().st_size // 1024
    print(f"  >>> Job : {cpt_nodes['Job']}, Skill : {cpt_nodes['Skill']}, Company : {cpt_nodes['Company']}")
    print(f"  >>> {sum(cpt_nodes.values())} nœuds, {taille_nodes} Ko\n")

    print(f"Écriture {EDGES_PATH.relative_to(REPO)} ...")
    cpt_edges = ecrire_edges_csv(df_combine, EDGES_PATH)
    taille_edges = EDGES_PATH.stat().st_size // 1024
    print(f"  >>> REQUIRES : {cpt_edges['REQUIRES']}, POSTED_BY : {cpt_edges['POSTED_BY']}")
    print(f"  >>> {sum(cpt_edges.values())} arêtes, {taille_edges} Ko\n")

    print("Récapitulatif final :")
    print(f"  - data/jobs.jsonl       {n_jsonl:>5} lignes      {taille_jsonl:>5} Ko")
    print(f"  - data/graph_nodes.csv  {sum(cpt_nodes.values()):>5} nœuds       {taille_nodes:>5} Ko")
    print(f"  - data/graph_edges.csv  {sum(cpt_edges.values()):>5} arêtes      {taille_edges:>5} Ko")
    print("\nLes trois fichiers sont prêts pour la modélisation NoSQL polyglotte.")


if __name__ == "__main__":
    main()
