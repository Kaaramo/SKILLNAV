"""Génère le snapshot de distribution des compétences pour le dashboard /skills.

Produit `web/src/lib/skills_distribution.json` à partir de `data/jobs.jsonl`.
Le dashboard /skills consomme ce JSON pour brancher le design d'origine
(filter panel + KPI + table) sur les vraies données du corpus.

Contenu généré pour 3 origines (Maroc, International, Tous) :
- compteurs par famille (filter panel · checkboxes 10 familles)
- compteurs par source (filter panel · checkboxes sources)
- catalogue top 50 cross-famille (table principale) avec sparkline
  mensuelle réelle + score d'émergence dérivé du growth
- top 8 par famille (utilisé en KPI top1 famille)
- trois insights data-driven

Usage :
    python scripts/build_skills_distribution.py
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JOBS_PATH = REPO / "data" / "jobs.jsonl"
OUT_PATH = REPO / "web" / "src" / "lib" / "skills_distribution.json"

FAMILLES_FR = {
    "genai": "IA générative",
    "ml": "Machine Learning",
    "web": "Web & APIs",
    "databases": "Bases de données",
    "data": "Data Engineering",
    "cloud": "Cloud",
    "ops": "Ops & MLOps",
    "languages": "Langages",
    "domains": "Domaines",
    "other": "Autres",
}
SKILL_FAMILIES = list(FAMILLES_FR.keys())

# Plage mensuelle finale du sparkline : aligné sur la période de l'étude
# Jan 2023 -> Mai 2026 (41 mois). Les rares offres antérieures sont ignorées
# côté sparkline mais comptées dans la volumétrie globale.
SPARKLINE_MONTHS = []
for y in range(2023, 2027):
    for m in range(1, 13):
        ym = f"{y:04d}-{m:02d}"
        if "2023-01" <= ym <= "2026-05":
            SPARKLINE_MONTHS.append(ym)


def charger_jobs() -> list[dict]:
    with JOBS_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def comptes_skills(jobs: list[dict]) -> Counter[str]:
    """Compte toutes les compétences cross-famille."""
    c: Counter[str] = Counter()
    for j in jobs:
        for famille in SKILL_FAMILIES:
            for sk in j.get("skills", {}).get(famille, []):
                c[sk] += 1
    return c


def famille_de(jobs: list[dict]) -> dict[str, str]:
    """Pour chaque skill, mémorise la première famille où il apparaît."""
    fam_of: dict[str, str] = {}
    for j in jobs:
        for famille in SKILL_FAMILIES:
            for sk in j.get("skills", {}).get(famille, []):
                if sk not in fam_of:
                    fam_of[sk] = famille
    return fam_of


def comptes_par_famille(jobs: list[dict]) -> dict[str, int]:
    """Pour chaque famille, nombre d'offres distinctes qui citent au moins une
    compétence de cette famille. Utilisé pour les compteurs du filter panel.
    """
    out: dict[str, int] = {}
    for famille in SKILL_FAMILIES:
        n = sum(1 for j in jobs if j.get("skills", {}).get(famille, []))
        out[famille] = n
    return out


def comptes_par_source(jobs: list[dict]) -> dict[str, int]:
    c: Counter[str] = Counter()
    for j in jobs:
        s = j.get("source", "")
        if s:
            c[s] += 1
    return dict(c.most_common())


MOIS_FR = {
    "01": "Janvier", "02": "Février", "03": "Mars", "04": "Avril",
    "05": "Mai", "06": "Juin", "07": "Juillet", "08": "Août",
    "09": "Septembre", "10": "Octobre", "11": "Novembre", "12": "Décembre",
}


TYPES_FR = {
    "ai-first": "AI-First",
    "ai-support": "AI-Support",
    "ml-first": "ML-First",
    "non-ai": "Data Analytics",
    "unknown": "Inconnu",
}

# Taxonomie metier (champ job_family de jobs.jsonl).
# Source : FAMILY_FR dans skillnav_eda.py.
JOB_FAMILY_FR = {
    "DATA_ANALYST": "Data Analyst",
    "BUSINESS_ANALYST": "Business Analyst",
    "DATA_SCIENTIST": "Data Scientist",
    "DATA_ENGINEER": "Data Engineer",
    "DATA_ARCHITECT": "Data Architect",
    "ML_ENGINEER": "ML Engineer",
    "MLOPS_ENGINEER": "MLOps Engineer",
    "AI_ENGINEER": "AI Engineer",
    "NLP_ENGINEER": "NLP Engineer",
    "CV_ENGINEER": "CV Engineer",
    "RESEARCH_SCIENTIST": "Research Scientist",
    "GENAI_LLM_ENGINEER": "GenAI / LLM Engineer",
    "OTHER": "Autre",
    "UNKNOWN": "Non detecte",
}

# Categories ecartees du calcul du metier dominant — ce sont des fourre-tout
# qui masqueraient le vrai signal metier.
JOB_FAMILY_NOISE = {"OTHER", "UNKNOWN"}


def type_poste_dominant(jobs: list[dict]) -> dict[str, str | int | float]:
    """Renvoie le ai_type majoritaire sur le sous-corpus (FR + count + pct)."""
    c: Counter[str] = Counter(j.get("ai_type", "") for j in jobs)
    if not c:
        return {"code": "", "label": "—", "count": 0, "pct": 0.0}
    code, count = c.most_common(1)[0]
    n = len(jobs)
    return {
        "code": code,
        "label": TYPES_FR.get(code, code),
        "count": count,
        "pct": round(count / n * 100, 1) if n else 0.0,
    }


def metier_dominant(jobs: list[dict]) -> dict[str, str | int | float]:
    """Renvoie le job_family dominant sur le sous-corpus, en ecartant les
    categories fourre-tout OTHER et UNKNOWN qui n'apportent pas de signal."""
    c: Counter[str] = Counter()
    for j in jobs:
        jf = j.get("job_family", "")
        if jf and jf not in JOB_FAMILY_NOISE:
            c[jf] += 1
    if not c:
        return {"code": "", "label": "—", "count": 0, "pct": 0.0}
    code, count = c.most_common(1)[0]
    n = len(jobs)
    return {
        "code": code,
        "label": JOB_FAMILY_FR.get(code, code),
        "count": count,
        "pct": round(count / n * 100, 1) if n else 0.0,
    }


def periode_corpus(jobs: list[dict]) -> dict[str, str]:
    """Renvoie la période réelle (mois min/max) du sous-corpus, en français."""
    mois = sorted({j.get("posted_month", "") for j in jobs if j.get("posted_month")})
    if not mois:
        return {"debut": "—", "fin": "—", "n_mois": "0"}
    debut, fin = mois[0], mois[-1]
    return {
        "debut": f"{MOIS_FR[debut[5:7]]} {debut[:4]}",
        "fin": f"{MOIS_FR[fin[5:7]]} {fin[:4]}",
        "n_mois": str(len(mois)),
    }


def serie_mensuelle(jobs: list[dict], skill: str) -> list[int]:
    """Retourne, pour le skill donné, le nombre d'offres par mois dans
    SPARKLINE_MONTHS. Recherche insensible à la casse, sur toutes les familles.
    """
    skill_lower = skill.lower()
    par_mois: Counter[str] = Counter()
    for j in jobs:
        ym = j.get("posted_month", "")
        if ym not in SPARKLINE_MONTHS:
            continue
        for famille in SKILL_FAMILIES:
            if any(s.lower() == skill_lower for s in j.get("skills", {}).get(famille, [])):
                par_mois[ym] += 1
                break
    return [par_mois.get(m, 0) for m in SPARKLINE_MONTHS]


def score_emergence(series: list[int]) -> float:
    """Score d'émergence dérivé de la pente : recent 12 mois / first 12 mois.
    Capped à 3, normalisé sur [0, 1]. Permet de remplir la colonne « Score »
    du design d'origine avec une métrique réelle (pas un mock).
    """
    if len(series) < 24:
        return 0.0
    first = sum(series[:12])
    last = sum(series[-12:])
    if first == 0:
        return 1.0 if last > 0 else 0.0
    ratio = last / first
    capped = min(ratio, 3.0)
    return round(capped / 3.0, 2)


def construire_catalogue(jobs: list[dict], top_n: int = 50) -> list[dict]:
    """Top N compétences toutes familles confondues, avec sparkline mensuelle
    et score d'émergence dérivé. Ce sont les lignes du tableau principal."""
    n_jobs = len(jobs)
    c = comptes_skills(jobs)
    fam_of = famille_de(jobs)
    rows: list[dict] = []
    for skill, count in c.most_common(top_n):
        series = serie_mensuelle(jobs, skill)
        rows.append({
            "skill": skill,
            "count": count,
            "family": fam_of.get(skill, "other"),
            "share_pct": round(count / n_jobs * 100, 1) if n_jobs else 0.0,
            "series": series,
            "score": score_emergence(series),
        })
    return rows


def top_n_par_famille(jobs: list[dict], famille: str, n: int = 8) -> list[dict]:
    c: Counter[str] = Counter()
    for j in jobs:
        for sk in j.get("skills", {}).get(famille, []):
            c[sk] += 1
    return [{"skill": s, "count": k} for s, k in c.most_common(n)]


def calculer_insights(maroc: list[dict], intl: list[dict]) -> list[dict]:
    n_ma = len(maroc) or 1
    n_in = len(intl) or 1
    c_ma = comptes_skills(maroc)
    c_in = comptes_skills(intl)

    # 1. Grand écart : skill très présent INTL, ratio INTL/MA élevé
    candidats = []
    for sk, ki in c_in.items():
        if ki < 100:
            continue
        km = c_ma.get(sk, 0)
        ratio = float("inf") if km == 0 else ki / km
        candidats.append((sk, ki, km, ratio))
    candidats.sort(key=lambda x: (-x[1] if x[3] == float("inf") else -x[3], -x[1]))
    grand_ecart = candidats[0] if candidats else None

    # 2. Spécificité MA : skill cité >= 10x MA, %MA - %INTL maximal
    spec_ma = None
    best_diff = -1.0
    for sk, km in c_ma.items():
        if km < 10:
            continue
        ki = c_in.get(sk, 0)
        diff = (km / n_ma) - (ki / n_in)
        if diff > best_diff:
            best_diff = diff
            spec_ma = (sk, km, ki, diff)

    # 3. Convergence : top 1 d'une famille identique des deux côtés
    convergence = None
    for famille in SKILL_FAMILIES:
        top_ma = top_n_par_famille(maroc, famille, n=1)
        top_in = top_n_par_famille(intl, famille, n=1)
        if top_ma and top_in and top_ma[0]["skill"] == top_in[0]["skill"]:
            convergence = (famille, top_ma[0]["skill"], top_ma[0]["count"], top_in[0]["count"])
            break

    insights: list[dict] = []
    if grand_ecart:
        sk, ki, km, ratio = grand_ecart
        ratio_str = "absente du corpus marocain" if km == 0 else f"×{ratio:.0f}"
        insights.append({
            "title": "Le grand écart GenAI",
            "body": (
                f"« {sk} » est cité {ki:,} fois à l'international "
                f"contre {km} fois au Maroc ({ratio_str}). L'écart trahit un "
                f"décalage temporel d'au moins 18 mois sur l'adoption des stacks LLM."
            ).replace(",", " "),
        })
    if spec_ma:
        sk, km, ki, diff = spec_ma
        insights.append({
            "title": "Spécificité marocaine",
            "body": (
                f"« {sk} » apparaît dans {km / n_ma * 100:.1f} % des offres "
                f"marocaines contre {ki / n_in * 100:.1f} % à l'international. "
                f"Le marché local maintient une demande forte sur ce socle."
            ),
        })
    if convergence:
        famille, sk, km, ki = convergence
        insights.append({
            "title": "Point de convergence",
            "body": (
                f"Sur la famille « {FAMILLES_FR[famille]} », {sk} domine "
                f"des deux côtés (Maroc {km} · International {ki:,}). "
                f"Socle technique partagé."
            ).replace(",", " "),
        })
    return insights


def main() -> None:
    if not JOBS_PATH.exists():
        raise SystemExit(f"jobs.jsonl introuvable : {JOBS_PATH}")

    jobs = charger_jobs()
    maroc = [j for j in jobs if j.get("origine") == "Maroc"]
    intl = [j for j in jobs if j.get("origine") == "International"]

    print(f"Corpus charge : {len(jobs)} offres")
    print(f"  Maroc         : {len(maroc):>5}")
    print(f"  International : {len(intl):>5}")
    print(f"  Sparkline     : {len(SPARKLINE_MONTHS)} mois ({SPARKLINE_MONTHS[0]} -> {SPARKLINE_MONTHS[-1]})")

    snapshot: dict = {
        "meta": {
            "n_total": len(jobs),
            "n_maroc": len(maroc),
            "n_international": len(intl),
            "generated_at": date.today().isoformat(),
            "source": "data/jobs.jsonl",
            "method": "comptage_skills() · 190 alias canonicalises · top 50 cross-famille",
            "sparkline_months": SPARKLINE_MONTHS,
            "periode": {
                "Maroc": periode_corpus(maroc),
                "International": periode_corpus(intl),
                "Tous": periode_corpus(jobs),
            },
            "type_poste_dominant": {
                "Maroc": type_poste_dominant(maroc),
                "International": type_poste_dominant(intl),
                "Tous": type_poste_dominant(jobs),
            },
            "metier_dominant": {
                "Maroc": metier_dominant(maroc),
                "International": metier_dominant(intl),
                "Tous": metier_dominant(jobs),
            },
        },
        "familles": FAMILLES_FR,
        # Compteurs pour le filter panel (checkboxes 10 familles)
        "family_counts": {
            "Maroc": comptes_par_famille(maroc),
            "International": comptes_par_famille(intl),
            "Tous": comptes_par_famille(jobs),
        },
        # Compteurs pour le filter panel (checkboxes sources)
        "source_counts": {
            "Maroc": comptes_par_source(maroc),
            "International": comptes_par_source(intl),
            "Tous": comptes_par_source(jobs),
        },
        # Top 8 par famille (utilisé pour les KPI dérivés)
        "top_par_famille": {
            "Maroc": {f: top_n_par_famille(maroc, f, n=8) for f in SKILL_FAMILIES},
            "International": {f: top_n_par_famille(intl, f, n=8) for f in SKILL_FAMILIES},
            "Tous": {f: top_n_par_famille(jobs, f, n=8) for f in SKILL_FAMILIES},
        },
        # Table principale : top 50 cross-famille avec sparkline et score
        "catalogue": {
            "Maroc": construire_catalogue(maroc, top_n=50),
            "International": construire_catalogue(intl, top_n=50),
            "Tous": construire_catalogue(jobs, top_n=50),
        },
        "insights": calculer_insights(maroc, intl),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    size_ko = OUT_PATH.stat().st_size // 1024
    print(f"\n=> Ecrit : {OUT_PATH.relative_to(REPO)} ({size_ko} Ko)")
    print(f"  catalogue : MA {len(snapshot['catalogue']['Maroc'])} / INTL {len(snapshot['catalogue']['International'])} / TOUS {len(snapshot['catalogue']['Tous'])}")
    print(f"  insights  : {len(snapshot['insights'])}")
    print(f"  sources MA : {list(snapshot['source_counts']['Maroc'].keys())}")
    print(f"  sources INTL : {list(snapshot['source_counts']['International'].keys())}")


if __name__ == "__main__":
    main()
