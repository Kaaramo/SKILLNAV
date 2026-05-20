"""Genere le snapshot top_skills.json pour les figures F.11 + F.14 du dashboard.

Reproduit `top_skills_global` du notebook 01_visualisations.ipynb :
    comptage de toutes les skills (toutes familles confondues),
    trie decroissant, top 20.

Sortie : web/src/lib/top_skills.json
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JOBS = REPO / "data" / "jobs.jsonl"
OUT = REPO / "web" / "src" / "lib" / "top_skills.json"

def humanize(skill: str) -> str:
    """Renvoie la skill telle quelle (pas d'expansion -- preserve la forme courte officielle)."""
    return skill.strip()


def compute_top_skills(jobs: list[dict], top_n: int = 20) -> list[dict]:
    """Compte chaque skill distincte par offre (une mention par offre, pas par champ)."""
    counter: Counter[str] = Counter()
    for j in jobs:
        skills_dict = j.get("skills", {})
        if not isinstance(skills_dict, dict):
            continue
        # Une skill = un seul comptage par offre meme si elle apparait dans plusieurs familles
        seen: set[str] = set()
        for lst in skills_dict.values():
            for s in lst or []:
                if isinstance(s, str) and s.strip():
                    seen.add(s.strip())
        for s in seen:
            counter[s] += 1
    total = len(jobs) or 1
    return [
        {
            "skill": humanize(s),
            "count": c,
            "pct": round(c / total * 100, 1),
        }
        for s, c in counter.most_common(top_n)
    ]


def main() -> None:
    jobs = [json.loads(line) for line in JOBS.open(encoding="utf-8")]
    ma = [j for j in jobs if j.get("origine") == "Maroc"]
    intl = [j for j in jobs if j.get("origine") == "International"]

    snapshot = {
        "meta": {
            "n_maroc": len(ma),
            "n_international": len(intl),
            "top_n": 20,
            "source": "data/jobs.jsonl",
        },
        "Maroc": compute_top_skills(ma, 20),
        "International": compute_top_skills(intl, 20),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    size_ko = OUT.stat().st_size // 1024
    print(f"Ecrit : {OUT.relative_to(REPO)} ({size_ko} Ko)")
    print(f"\nTop 5 MA :")
    for r, s in enumerate(snapshot["Maroc"][:5], 1):
        print(f"  #{r}  {s['skill']:30} {s['count']:>4}  ({s['pct']:>4} %)")
    print(f"\nTop 5 INTL :")
    for r, s in enumerate(snapshot["International"][:5], 1):
        print(f"  #{r}  {s['skill']:30} {s['count']:>4}  ({s['pct']:>4} %)")


if __name__ == "__main__":
    main()
