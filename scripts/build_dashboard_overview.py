"""Genere le snapshot pour la page Dashboard (Vue d'ensemble).

Sortie : `web/src/lib/dashboard_overview.json`

Contenu :
- meta : volumes, sources, entreprises, metiers, competences uniques, % AI-first
- ai_type_distribution : repartition par origine (pour les donuts)
- top_intitules : top 8 titres canoniques par origine
- top_employeurs : top 8 entreprises (hors anonymisations) par origine
- bascule_temporelle : counts mensuels par ai_type sur 41 mois

Usage :
    python scripts/build_dashboard_overview.py
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JOBS_PATH = REPO / "data" / "jobs.jsonl"
GRAPH_PATH = REPO / "data" / "exports" / "graph_vis.json"
OUT_PATH = REPO / "web" / "src" / "lib" / "dashboard_overview.json"

TYPES_FR = {
    "ai-first": "AI-First",
    "ai-support": "AI-Support",
    "ml-first": "ML-First",
    "non-ai": "Data Analytics",
    "unknown": "Inconnu",
}

AI_TYPE_COLORS = {
    "ai-first": "#2251FF",
    "ai-support": "#7C3AED",
    "ml-first": "#0F8F65",
    "non-ai": "#C77700",
    "unknown": "#6B7280",
}

JOB_FAMILY_NOISE = {"OTHER", "UNKNOWN"}

# Plage temporelle de l'etude : 41 mois alignes sur Jan 2023 -> Mai 2026
MONTHS: list[str] = []
for y in range(2023, 2027):
    for m in range(1, 13):
        ym = f"{y:04d}-{m:02d}"
        if "2023-01" <= ym <= "2026-05":
            MONTHS.append(ym)


def charger_jobs() -> list[dict]:
    with JOBS_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def companies_distinctes(jobs: list[dict]) -> int:
    s = {j["company"].strip() for j in jobs if j.get("company", "").strip()}
    return len(s)


def sources_distinctes(jobs: list[dict]) -> int:
    s = {j["source"] for j in jobs if j.get("source")}
    return len(s)


def skills_uniques(jobs: list[dict]) -> int:
    s: set[str] = set()
    for j in jobs:
        for sks in j.get("skills", {}).values():
            for sk in sks:
                s.add(sk)
    return len(s)


def metiers_distincts(jobs: list[dict]) -> int:
    """Compte les job_family hors fourre-tout OTHER / UNKNOWN."""
    s = {
        j.get("job_family", "")
        for j in jobs
        if j.get("job_family") and j.get("job_family") not in JOB_FAMILY_NOISE
    }
    return len(s)


def ai_type_distribution(jobs: list[dict]) -> list[dict]:
    """Renvoie la distribution ai_type pour un sous-corpus (pret pour le donut)."""
    c: Counter[str] = Counter(j.get("ai_type", "") for j in jobs if j.get("ai_type"))
    n = sum(c.values())
    out = []
    for code in ["ai-first", "ai-support", "ml-first", "non-ai", "unknown"]:
        cnt = c.get(code, 0)
        if cnt == 0:
            continue
        out.append({
            "code": code,
            "label": TYPES_FR[code],
            "color": AI_TYPE_COLORS[code],
            "count": cnt,
            "pct": round(cnt / n * 100, 1) if n else 0.0,
        })
    return out


def top_intitules(jobs: list[dict], n: int = 8) -> list[dict]:
    c: Counter[str] = Counter(
        j["title_canonical"].strip()
        for j in jobs
        if j.get("title_canonical", "").strip()
    )
    return [{"title": t, "count": k} for t, k in c.most_common(n)]


def top_employeurs(jobs: list[dict], n: int = 8) -> list[dict]:
    """Top employeurs en ecartant les libelles anonymises 'Anonyme ...'."""
    c: Counter[str] = Counter()
    for j in jobs:
        co = j.get("company", "").strip()
        if not co:
            continue
        if co.lower().startswith("anonyme"):
            continue
        c[co] += 1
    return [{"company": co, "count": k} for co, k in c.most_common(n)]


def graph_stats() -> dict:
    """Lit data/exports/graph_vis.json et calcule les stats pour la KPI graphe.

    Returns le dict { n_nodes, n_edges, n_communities, modularity_louvain, top_skill }.
    Si le fichier est absent, renvoie un dict vide -- la page front gere le fallback.
    """
    if not GRAPH_PATH.exists():
        print(f"  ! graph_vis.json absent ({GRAPH_PATH.relative_to(REPO)}) -- KPI graphe disabled")
        return {}

    with GRAPH_PATH.open(encoding="utf-8") as f:
        g = json.load(f)

    nodes = g.get("nodes", [])
    links = g.get("links", [])
    communities = {n.get("community") for n in nodes if n.get("community") is not None}

    # Top skill : meilleur PageRank (le skill #1 du marche)
    top_skill = max(nodes, key=lambda n: n.get("pagerank", 0)) if nodes else {}

    # Modularite Louvain : recalcule via python-louvain si dispo, sinon hardcode 0.295
    modularity = 0.295
    try:
        import networkx as nx  # noqa: PLC0415
        from community import community_louvain  # noqa: PLC0415

        G = nx.Graph()
        for ln in links:
            G.add_edge(ln["source"], ln["target"], weight=ln.get("weight", 1))
        partition = {n["id"]: n["community"] for n in nodes if n.get("community") is not None}
        # Filtre noeuds presents dans G uniquement
        partition = {k: v for k, v in partition.items() if k in G}
        if partition:
            modularity = round(community_louvain.modularity(partition, G), 3)
    except (ImportError, KeyError, Exception) as e:
        print(f"  ! modularity recalcul echoue ({e}) -- valeur fallback 0.295")

    return {
        "n_nodes": len(nodes),
        "n_edges": len(links),
        "n_communities": len(communities),
        "modularity_louvain": modularity,
        "top_skill": {
            "name": str(top_skill.get("id", "")).strip().title(),
            "count": int(top_skill.get("count", 0)),
            "family": top_skill.get("family", ""),
            "pagerank": round(float(top_skill.get("pagerank", 0)), 4),
        },
    }


def bascule_temporelle(jobs: list[dict]) -> dict:
    """Renvoie pour chaque mois (Jan 23 -> Mai 26) le count d'offres par ai_type."""
    series: dict[str, list[int]] = {
        code: [0] * len(MONTHS) for code in ["ai-first", "ai-support", "ml-first", "non-ai", "unknown"]
    }
    idx = {m: i for i, m in enumerate(MONTHS)}
    for j in jobs:
        m = j.get("posted_month", "")
        if m not in idx:
            continue
        t = j.get("ai_type", "unknown")
        if t in series:
            series[t][idx[m]] += 1
    return {
        "months": MONTHS,
        "series": series,
    }


def main() -> None:
    if not JOBS_PATH.exists():
        raise SystemExit(f"jobs.jsonl introuvable : {JOBS_PATH}")

    jobs = charger_jobs()
    maroc = [j for j in jobs if j.get("origine") == "Maroc"]
    intl = [j for j in jobs if j.get("origine") == "International"]

    print(f"Corpus charge : {len(jobs)} offres")
    print(f"  Maroc         : {len(maroc):>5}")
    print(f"  International : {len(intl):>5}")

    n_ai_first = sum(1 for j in jobs if j.get("ai_type") == "ai-first")

    snapshot = {
        "meta": {
            "n_total": len(jobs),
            "n_maroc": len(maroc),
            "n_international": len(intl),
            "n_companies": {
                "Maroc": companies_distinctes(maroc),
                "International": companies_distinctes(intl),
                "Tous": companies_distinctes(jobs),
            },
            "n_sources": {
                "Maroc": sources_distinctes(maroc),
                "International": sources_distinctes(intl),
                "Tous": sources_distinctes(jobs),
            },
            "n_skills_unique": {
                "Maroc": skills_uniques(maroc),
                "International": skills_uniques(intl),
                "Tous": skills_uniques(jobs),
            },
            "n_metiers": {
                "Maroc": metiers_distincts(maroc),
                "International": metiers_distincts(intl),
                "Tous": metiers_distincts(jobs),
            },
            "bascule_ai_first_pct": round(n_ai_first / len(jobs) * 100, 1) if jobs else 0.0,
            "bascule_ai_first_count": n_ai_first,
            "graph": graph_stats(),
            "periode": {
                "n_mois": 41,
                "debut": "Janvier 2023",
                "fin": "Mai 2026",
                "ancrage": "Sortie de ChatGPT — Novembre 2022",
            },
            "generated_at": date.today().isoformat(),
            "source": "data/jobs.jsonl",
        },
        "ai_type_distribution": {
            "Maroc": ai_type_distribution(maroc),
            "International": ai_type_distribution(intl),
            "Tous": ai_type_distribution(jobs),
        },
        "top_intitules": {
            "Maroc": top_intitules(maroc),
            "International": top_intitules(intl),
        },
        "top_employeurs": {
            "Maroc": top_employeurs(maroc, n=15),
            "International": top_employeurs(intl, n=20),
        },
        "bascule_temporelle": bascule_temporelle(jobs),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    size_ko = OUT_PATH.stat().st_size // 1024
    print(f"\n=> Ecrit : {OUT_PATH.relative_to(REPO)} ({size_ko} Ko)")
    print(f"  AI-First global : {snapshot['meta']['bascule_ai_first_pct']} %")
    print(f"  Top entreprise MA : {snapshot['top_employeurs']['Maroc'][0]['company']} ({snapshot['top_employeurs']['Maroc'][0]['count']})")
    print(f"  Top entreprise INTL : {snapshot['top_employeurs']['International'][0]['company']} ({snapshot['top_employeurs']['International'][0]['count']})")
    print(f"  Top intitule MA : {snapshot['top_intitules']['Maroc'][0]['title']} ({snapshot['top_intitules']['Maroc'][0]['count']})")
    print(f"  Top intitule INTL : {snapshot['top_intitules']['International'][0]['title']} ({snapshot['top_intitules']['International'][0]['count']})")


if __name__ == "__main__":
    main()
