"""Calcule le gap analysis marche <-> formation ENSA Tetouan SDBIA.

Source de verite unique : data/jobs.jsonl (3 467 offres, MA + INTL, canonicalisees Pydantic).
Le graphe (graph_vis.json) n'est plus utilise comme proxy -- on lit directement les skills
declarees dans chaque offre. Plus fiable, exhaustif.

Sortie :
    data/exports/gap_analysis_ensat.json   pour notebook 06 + dashboard
    web/src/lib/gap_analysis_ensat.json    copie consommee par /gap

Methodologie :
    1. Charge curriculum ENSAT (parser MD -> Pydantic)
    2. Charge toutes les skills demandees par origine depuis jobs.jsonl
       (champ skills = dict { genai, ml, web, databases, data, cloud, ops, languages, ... })
    3. Normalise des deux cotes (lowercase + clean + alias)
    4. Match : exact lowercase + substring + alias manuels
    5. Calcule par famille (MA et INTL separes) : couverture, gap, mismatch
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from skillnav.pipelines.curriculum_mining import parse_filiere_md

REPO = Path(__file__).resolve().parent.parent
CURR_ROOT = REPO / "sources" / "curricula" / "ensa-tetouan"
JOBS = REPO / "data" / "jobs.jsonl"
OUT_DATA = REPO / "data" / "exports" / "gap_analysis_ensat.json"
OUT_WEB = REPO / "web" / "src" / "lib" / "gap_analysis_ensat.json"

# Mapping cles techniques jobs.jsonl -> libelles humains pour les graphiques
FAMILY_LABELS: dict[str, str] = {
    "genai": "IA Générative",
    "ml": "Machine Learning",
    "web": "Web & APIs",
    "databases": "Bases de données",
    "data": "Data Engineering",
    "cloud": "Cloud",
    "ops": "DevOps / MLOps",
    "languages": "Langages de programmation",
    "domains": "Domaines métier",
    "other": "Soft skills & autres",
}

# Alias manuels : forme libre -> forme canonique marche (lowercase)
# Couvre les cas ou skill_taught et skill_marche differents mais designent la meme chose
ALIASES: dict[str, str] = {
    # ML / DL
    "machine learning": "machine learning",
    "ml": "machine learning",
    "deep learning": "deep learning",
    "dl": "deep learning",
    "réseaux de neurones": "deep learning",
    "neural networks": "deep learning",
    "computer vision": "computer vision",
    "cv": "computer vision",
    "vision par ordinateur": "computer vision",
    # NLP
    "nlp": "nlp",
    "natural language processing": "nlp",
    "traitement automatique des langues naturelles": "nlp",
    "taln": "nlp",
    "ner": "ner",
    "named entity recognition": "ner",
    "transformers": "transformers",
    "bert": "bert",
    "gpt": "gpt",
    "word embeddings": "word embeddings",
    "word2vec": "word2vec",
    "tokenization": "tokenization",
    "spacy": "spacy",
    "nltk": "nltk",
    "huggingface": "huggingface",
    "llm": "llm",
    # IA
    "intelligence artificielle": "artificial intelligence",
    "ai": "artificial intelligence",
    "artificial intelligence": "artificial intelligence",
    "ia": "artificial intelligence",
    "reinforcement learning": "reinforcement learning",
    "q-learning": "reinforcement learning",
    # Data
    "data mining": "data mining",
    "fouille de données": "data mining",
    "data visualization": "data visualization",
    "visualisation de données": "data visualization",
    "data viz": "data visualization",
    "dataviz": "data visualization",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "plotly": "plotly",
    "tableau": "tableau",
    "power bi": "power bi",
    "powerbi": "power bi",
    "dashboards": "dashboards",
    "reporting": "reporting",
    "kpis": "kpis",
    # Big Data / Stockage
    "big data": "big data",
    "hadoop": "hadoop",
    "spark": "spark",
    "pyspark": "spark",
    "mapreduce": "mapreduce",
    "hdfs": "hdfs",
    "hive": "hive",
    "kafka": "kafka",
    "sql": "sql",
    "nosql": "nosql",
    "mongodb": "mongodb",
    "mysql": "mysql",
    "postgresql": "postgresql",
    "postgres": "postgresql",
    "cassandra": "cassandra",
    "redis": "redis",
    "elasticsearch": "elasticsearch",
    # Langages
    "python": "python",
    "java": "java",
    "c++": "c++",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "pandas": "pandas",
    "numpy": "numpy",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "keras": "keras",
    "xgboost": "xgboost",
    "opencv": "opencv",
    "yolo": "yolo",
    # Web / API
    "rest api": "rest api",
    "rest": "rest api",
    "api": "api",
    "http": "http",
    "grpc": "grpc",
    "websocket": "websocket",
    # Web semantique
    "knowledge graph": "knowledge graph",
    "neo4j": "neo4j",
    "rdf": "rdf",
    "sparql": "sparql",
    "ontologies": "ontologies",
    "owl": "owl",
    "blockchain": "blockchain",
    "ethereum": "ethereum",
    "solidity": "solidity",
    "smart contracts": "smart contracts",
    # BI / ETL
    "etl": "etl",
    "business intelligence": "business intelligence",
    "bi": "business intelligence",
    "informatique décisionnelle": "business intelligence",
    "data warehouse": "data warehouse",
    "olap": "olap",
    "talend": "talend",
    # Web Mining
    "web mining": "web mining",
    "web scraping": "web scraping",
    "scraping": "web scraping",
    "beautifulsoup": "beautifulsoup",
    "selenium": "selenium",
    "crawl4ai": "crawl4ai",
    "playwright": "playwright",
    "pydantic": "pydantic",
    # Securite
    "cybersécurité": "cybersecurity",
    "cybersecurity": "cybersecurity",
    "sécurité": "cybersecurity",
    "rgpd": "gdpr",
    "gdpr": "gdpr",
    "cryptographie": "cryptography",
    "owasp": "owasp",
    # DevOps / Systeme
    "docker": "docker",
    "kubernetes": "kubernetes",
    "linux": "linux",
    "bash": "bash",
    "shell": "bash",
    "git": "git",
    "github": "git",
    "ci/cd": "ci/cd",
    "devops": "devops",
    "mlops": "mlops",
    # Stats / Maths
    "statistics": "statistics",
    "statistiques": "statistics",
    "probabilités": "probability",
    "probability": "probability",
    "algèbre linéaire": "linear algebra",
    "linear algebra": "linear algebra",
    "pca": "pca",
    "acp": "pca",
    "svd": "svd",
    "kmeans": "clustering",
    "clustering": "clustering",
    "régression": "regression",
    "regression": "regression",
    "classification": "classification",
    "svm": "svm",
    "random forest": "random forest",
    # Soft skills
    "communication": "communication",
    "management": "management",
    "leadership": "leadership",
    "anglais": "english",
    "english": "english",
    "agile": "agile",
    "scrum": "scrum",
    "uml": "uml",
}


def normalize(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[\(\)\[\]]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


def canonicalize(s: str) -> str:
    """Mappe une forme libre vers sa forme canonique marche."""
    n = normalize(s)
    if n in ALIASES:
        return ALIASES[n]
    return n


def is_match(taught: str, demanded: str) -> bool:
    """Vrai si skill enseignee couvre une skill demandee (canonicalisees, lowercase).

    Match exact OU substring dans un sens ou l'autre.
    """
    t, d = canonicalize(taught), canonicalize(demanded)
    if t == d:
        return True
    if len(t) >= 4 and t in d:
        return True
    if len(d) >= 4 and d in t:
        return True
    return False


def charge_skills_marche_par_origine() -> dict[str, Counter]:
    """Pour MA et INTL separes : compte le nombre d'offres ou apparait chaque skill canonique."""
    counters: dict[str, Counter] = {"Maroc": Counter(), "International": Counter()}
    with JOBS.open(encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            origine = j.get("origine")
            if origine not in counters:
                continue
            skills_dict = j.get("skills", {})
            if not isinstance(skills_dict, dict):
                continue
            seen: set[str] = set()
            for lst in skills_dict.values():
                for s in lst or []:
                    if not isinstance(s, str):
                        continue
                    cs = canonicalize(s)
                    seen.add(cs)
            for cs in seen:
                counters[origine][cs] += 1
    return counters


def charge_skills_par_famille(origines: list[str]) -> dict[str, dict[str, set[str]]]:
    """Pour chaque origine, pour chaque famille marche, renvoie le set des skills canoniques demandees.

    Returns : { origine: { famille: {skill_canon, ...} } }
    """
    out: dict[str, dict[str, set[str]]] = {
        origine: defaultdict(set) for origine in origines
    }
    with JOBS.open(encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            origine = j.get("origine")
            if origine not in out:
                continue
            skills_dict = j.get("skills", {})
            if not isinstance(skills_dict, dict):
                continue
            for famille_key, lst in skills_dict.items():
                if famille_key not in FAMILY_LABELS:
                    continue
                for s in lst or []:
                    if isinstance(s, str) and s.strip():
                        out[origine][famille_key].add(canonicalize(s))
    return out


def main() -> None:
    print("=== Gap analysis marche <-> ENSA Tetouan SDBIA ===\n")

    # 1. Curriculum
    curriculum = parse_filiere_md(CURR_ROOT / "filiere.md", CURR_ROOT / "source.yaml")
    skills_taught = {canonicalize(s) for s in curriculum.all_skills_taught}
    print(f"Curriculum : {curriculum.n_modules} modules, {curriculum.volume_total} h")
    print(f"  Skills enseignees (canon)  : {len(skills_taught)}")

    # 2. Marche par origine -- source unique = jobs.jsonl
    marche_par_origine = charge_skills_marche_par_origine()
    skills_demanded_ma = set(marche_par_origine["Maroc"].keys())
    skills_demanded_intl = set(marche_par_origine["International"].keys())
    skills_demanded_all = skills_demanded_ma | skills_demanded_intl
    print(f"  Skills demandees MA   : {len(skills_demanded_ma)}")
    print(f"  Skills demandees INTL : {len(skills_demanded_intl)}")
    print(f"  Skills demandees ALL  : {len(skills_demanded_all)}\n")

    # 3. Skills par famille via jobs.jsonl (MA et INTL separes, source unique)
    skills_par_famille = charge_skills_par_famille(["Maroc", "International"])

    # 4. Matching : taught vs demanded
    def match_sets(taught: set[str], demanded: set[str]) -> dict:
        couvertes: set[str] = set()
        for d in demanded:
            for t in taught:
                if is_match(t, d):
                    couvertes.add(d)
                    break
        gap = demanded - couvertes
        mismatch = {t for t in taught if not any(is_match(t, d) for d in demanded)}
        return {
            "couvertes": couvertes,
            "gap": gap,
            "mismatch": mismatch,
        }

    res_ma = match_sets(skills_taught, skills_demanded_ma)
    res_intl = match_sets(skills_taught, skills_demanded_intl)
    res_all = match_sets(skills_taught, skills_demanded_all)

    # Aliases d'affichage : rebadge le label final SANS toucher au matching.
    DISPLAY_ALIASES = {
        "next": "Next.js",
        "agents": "Agents IA",
    }

    def display(s: str) -> str:
        return DISPLAY_ALIASES.get(s.lower().strip(), s.title())

    # 5. Top gaps ponderes par volume marche (pour focus impact)
    def top_gaps(gap: set[str], counter: Counter, n: int = 30) -> list[dict]:
        scored = [(s, counter.get(s, 0)) for s in gap]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [
            {"skill": display(s), "demand_count": c}
            for s, c in scored[:n]
            if c > 0
        ]

    # 6. Couverture par famille -- pour MA et INTL separes, base jobs.jsonl
    def couverture_par_famille(origine: str) -> dict[str, dict]:
        familles = skills_par_famille[origine]
        out: dict[str, dict] = {}
        for famille_key, skills_set in familles.items():
            if not skills_set:
                continue
            couvertes = {s for s in skills_set if any(is_match(t, s) for t in skills_taught)}
            out[FAMILY_LABELS[famille_key]] = {
                "demanded": len(skills_set),
                "couvertes": len(couvertes),
                "pct": round(len(couvertes) / len(skills_set) * 100, 1) if skills_set else 0.0,
            }
        return out

    couv_famille_ma = couverture_par_famille("Maroc")
    couv_famille_intl = couverture_par_famille("International")

    # 7. Couverture VRAIE des offres : % d'offres qui contiennent au moins
    # une skill enseignee (definition intuitive, employabilite).
    def pct_offres_avec_au_moins_une_skill_enseignee(origine: str) -> float:
        n_couvert = 0
        n_total = 0
        with JOBS.open(encoding="utf-8") as f:
            for line in f:
                j = json.loads(line)
                if j.get("origine") != origine:
                    continue
                n_total += 1
                skills_dict = j.get("skills", {})
                if not isinstance(skills_dict, dict):
                    continue
                # Au moins une skill de l'offre matche-t-elle une skill enseignee ?
                trouve = False
                for lst in skills_dict.values():
                    for s in lst or []:
                        if not isinstance(s, str):
                            continue
                        cs = canonicalize(s)
                        if any(is_match(t, cs) for t in skills_taught):
                            trouve = True
                            break
                    if trouve:
                        break
                if trouve:
                    n_couvert += 1
        return round(n_couvert / n_total * 100, 1) if n_total else 0.0

    couverture_ponderee_ma = pct_offres_avec_au_moins_une_skill_enseignee("Maroc")
    couverture_ponderee_intl = pct_offres_avec_au_moins_une_skill_enseignee("International")

    # 8. Compose la sortie JSON
    snapshot = {
        "meta": {
            "school": curriculum.school,
            "school_code": curriculum.school_code,
            "filiere": curriculum.filiere,
            "filiere_code": curriculum.filiere_code,
            "n_modules": curriculum.n_modules,
            "volume_total_h": curriculum.volume_total,
            "n_skills_taught": len(skills_taught),
            "n_skills_demanded_ma": len(skills_demanded_ma),
            "n_skills_demanded_intl": len(skills_demanded_intl),
            "generated_at": date.today().isoformat(),
        },
        "couverture": {
            "Maroc": {
                "n_demanded": len(skills_demanded_ma),
                "n_couvertes": len(res_ma["couvertes"]),
                "pct_skills": round(
                    len(res_ma["couvertes"]) / len(skills_demanded_ma) * 100, 1
                )
                if skills_demanded_ma
                else 0.0,
                "pct_offres_couvertes": couverture_ponderee_ma,
            },
            "International": {
                "n_demanded": len(skills_demanded_intl),
                "n_couvertes": len(res_intl["couvertes"]),
                "pct_skills": round(
                    len(res_intl["couvertes"]) / len(skills_demanded_intl) * 100, 1
                )
                if skills_demanded_intl
                else 0.0,
                "pct_offres_couvertes": couverture_ponderee_intl,
            },
        },
        "top_gaps": {
            "Maroc": top_gaps(res_ma["gap"], marche_par_origine["Maroc"], n=25),
            "International": top_gaps(res_intl["gap"], marche_par_origine["International"], n=25),
        },
        "mismatch": sorted(res_all["mismatch"])[:25],
        "couverture_par_famille": {
            "Maroc": couv_famille_ma,
            "International": couv_famille_intl,
        },
        "curriculum": {
            "semesters": [
                {
                    "code": s.code,
                    "annee": s.annee,
                    "n_modules": s.n_modules,
                    "volume_total": s.volume_total,
                    "modules": [
                        {
                            "code": m.code,
                            "title": m.title,
                            "volume_horaire": m.volume_horaire,
                            "skills_taught": m.skills_taught,
                        }
                        for m in s.modules
                    ],
                }
                for s in curriculum.semesters
            ],
        },
    }

    OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    OUT_DATA.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Ecrit : {OUT_DATA.relative_to(REPO)}")
    print(f"        {OUT_WEB.relative_to(REPO)}")
    print()
    print("=== Synthese ===")
    print(f"  Couverture skills MA    : {snapshot['couverture']['Maroc']['pct_skills']} % "
          f"({snapshot['couverture']['Maroc']['n_couvertes']}/{snapshot['couverture']['Maroc']['n_demanded']})")
    print(f"  Couverture skills INTL  : {snapshot['couverture']['International']['pct_skills']} % "
          f"({snapshot['couverture']['International']['n_couvertes']}/{snapshot['couverture']['International']['n_demanded']})")
    print(f"  Couverture offres MA    : {snapshot['couverture']['Maroc']['pct_offres_couvertes']} %")
    print(f"  Couverture offres INTL  : {snapshot['couverture']['International']['pct_offres_couvertes']} %")
    print()
    print(f"  Top 5 gaps marche MA :")
    for g in snapshot["top_gaps"]["Maroc"][:5]:
        print(f"    - {g['skill']:35} {g['demand_count']:>4} offres")


if __name__ == "__main__":
    main()
