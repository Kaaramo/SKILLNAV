#!/usr/bin/env python3
"""SKILLNAV — Phase 3 extraction Glassdoor → JSON + MD.

Override CLAUDE.md §N4 autorisé par Karamo Sylla 2026-05-14 pour cette source.

Usage : python sources/collected/glassdoor-ma/_generate_postings.py
"""
from __future__ import annotations
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent
RAW = ROOT / "raw"
POSTINGS = ROOT / "postings"
ARCHIVE = ROOT / "archive_pre_2023"
TODAY = date(2026, 5, 14)
TODAY_ISO_DT = "2026-05-14T22:00:00Z"

SCRAPER = "skillnav-firecrawl-v1.0"

# ─── 1. SRCH index loader ────────────────────────────────────────────────────

def load_srch_index() -> dict:
    """Parse all SRCH markdowns to build jl_id → metadata map."""
    sources = [
        RAW / "_srch-data-scientist.json",
        RAW / "_srch-data-engineer.json",
        RAW / "_srch-machine-learning.json",
        RAW / "_srch-data-analyst.json",
    ]
    index: dict[str, dict] = {}
    for fp in sources:
        if not fp.exists():
            continue
        with fp.open(encoding="utf-8") as f:
            d = json.load(f)
        md = d.get("markdown", "")
        lines = md.split("\n")
        for i, l in enumerate(lines):
            m_link = re.search(
                r"\[([^\]]+)\]\((https://www\.glassdoor\.com/job-listing/[^\)]+)\)", l
            )
            if not m_link:
                continue
            title = m_link.group(1).strip()
            url = m_link.group(2).strip()
            jl_m = re.search(r"jl=(\d+)", url)
            if not jl_m:
                continue
            jl = jl_m.group(1)
            if jl in index:
                continue  # already have it

            # Backward: find company + rating
            company = None
            for j in range(i - 1, max(0, i - 30), -1):
                lj = lines[j].strip()
                if not lj:
                    continue
                if re.match(r"^[0-5]\.\d$|^N/A$", lj):
                    continue
                if lj.startswith("!["):
                    m_logo = re.match(r"!\[([^\]]+?)\s*Logo\]", lj)
                    if m_logo and not company:
                        company = m_logo.group(1).strip()
                    continue
                if re.match(r"^\d+d\+?$", lj) or lj in (
                    "Easy Apply",
                    "Discover more",
                    "Show more",
                ):
                    continue
                if not company and len(lj) < 80 and not lj.startswith(("-", "[")):
                    company = lj
                    break

            # Forward: find location + date_rel
            location, date_rel = None, None
            for j in range(i + 1, min(len(lines), i + 35)):
                lj = lines[j].strip()
                if not lj or lj.startswith("!["):
                    continue
                if re.match(r"^\d+d\+?$", lj):
                    date_rel = lj
                    break
                if (
                    not location
                    and len(lj) < 50
                    and re.match(r"^[A-Z][\w\-\s,.()/]*$", lj)
                    and lj not in ("Easy Apply", "Discover more", "Show more")
                ):
                    location = lj

            index[jl] = {
                "title": title,
                "company": company,
                "location": location,
                "date_rel": date_rel,
                "url": url,
            }
    return index


# ─── 2. URL slug fallback (KO/KE coordinates) ────────────────────────────────

def slug_fallback(url: str) -> tuple[str | None, str | None]:
    """Glassdoor URL pattern: /job-listing/<slug>-JV_IC<n>_KO<a>,<b>_KE<c>,<d>.htm
    KO = title indices, KE = company indices in slug.
    """
    m = re.search(
        r"/job-listing/(.+?)-JV_IC\d+_KO(\d+),(\d+)_KE(\d+),(\d+)\.htm", url
    )
    if not m:
        return None, None
    slug, ko_s, ko_e, ke_s, ke_e = m.groups()
    from urllib.parse import unquote

    slug_dec = unquote(slug)
    try:
        title_slug = slug_dec[int(ko_s) : int(ko_e)]
        comp_slug = slug_dec[int(ke_s) : int(ke_e)]
    except Exception:
        return None, None

    def deslug(s: str) -> str:
        s = s.replace("-", " ").strip()
        # Title-case but preserve internal CamelCase / abbreviations
        return " ".join(w.capitalize() for w in s.split())

    return deslug(title_slug), deslug(comp_slug)


# ─── 3. Description extraction from detail page ──────────────────────────────

DESC_MARKERS_START = [
    "**About The Job**",
    "**À propos du poste**",
    "**Job Description**",
    "**Description du poste**",
    "**About the Role**",
    "**Mission**",
]
DESC_MARKERS_END = [
    "Show more!",
    "Show more",
    "### Related pages",
    "### Working here",
    "More jobs like this one",
    "See company reviews",
    "By applying, you agree",
]


def extract_description(md: str) -> str:
    text = md
    # Try to find a known start marker
    start = -1
    for marker in DESC_MARKERS_START:
        idx = text.find(marker)
        if idx >= 0:
            start = idx
            break
    if start < 0:
        # Fallback: start after "Apply on employer siteApply now" or "Apply now"
        for cue in ("Apply on employer siteApply now", "Apply now"):
            idx = text.find(cue)
            if idx >= 0:
                start = idx + len(cue)
                break
    if start < 0:
        start = 0
    # Find end
    end = len(text)
    for marker in DESC_MARKERS_END:
        idx = text.find(marker, start)
        if idx >= 0 and idx < end:
            end = idx
    desc = text[start:end].strip()
    # Strip skip links and known boilerplate
    desc = re.sub(r"\[Skip to[^\]]+\]\([^\)]+\)", "", desc)
    desc = re.sub(r"!\[[^\]]*\]\([^\)]+\)", "", desc)  # images
    desc = re.sub(r"Is your resume a good match\?.*?Upload your resume", "", desc, flags=re.S)
    desc = re.sub(r"Find your perfect job\s*", "", desc)
    desc = re.sub(r"\n{3,}", "\n\n", desc).strip()
    return desc


# ─── 4. Skills patterns ──────────────────────────────────────────────────────

SKILLS_PATTERNS = {
    "Python": r"\bPython\b",
    "SQL": r"\bSQL\b",
    "R": r"(?<![a-zA-Z])R(?:[\s,]|$)",
    "Java": r"\bJava\b(?!Script)",
    "JavaScript": r"\bJavaScript\b",
    "TypeScript": r"\bTypeScript\b",
    "Scala": r"\bScala\b",
    "PySpark": r"\bPySpark\b",
    "Spark": r"\bSpark\b",
    "Hadoop": r"\bHadoop\b",
    "Machine Learning": r"\bMachine Learning\b|\bapprentissage automatique\b",
    "Deep Learning": r"\bDeep Learning\b|\bapprentissage profond\b",
    "NLP": r"\bNLP\b|\bnatural language\b|\btraitement.{0,10}langage\b",
    "Computer Vision": r"\bcomputer vision\b|\bvision (par )?ordinateur\b",
    "TensorFlow": r"\bTensorFlow\b",
    "PyTorch": r"\bPyTorch\b",
    "Scikit-learn": r"\bScikit[- ]?learn\b",
    "Keras": r"\bKeras\b",
    "MLflow": r"\bMLflow\b",
    "Kubeflow": r"\bKubeflow\b",
    "Databricks": r"\bDatabricks\b",
    "Snowflake": r"\bSnowflake\b",
    "BigQuery": r"\bBigQuery\b",
    "PostgreSQL": r"\bPostgre(SQL)?\b",
    "MySQL": r"\bMySQL\b",
    "MongoDB": r"\bMongoDB\b",
    "NoSQL": r"\bNoSQL\b",
    "Redis": r"\bRedis\b",
    "Elasticsearch": r"\bElastic(search)?\b",
    "Power BI": r"\bPower\s*BI\b",
    "Tableau": r"\bTableau\b(?!\sde)",
    "Looker": r"\bLooker\b",
    "Excel": r"\bExcel\b",
    "Azure": r"\bAzure\b",
    "Azure ML": r"\bAzure\s*ML\b|\bAzure Machine Learning\b",
    "AWS": r"\bAWS\b|Amazon Web Services",
    "GCP": r"\bGCP\b|Google Cloud",
    "Vertex AI": r"\bVertex AI\b",
    "SageMaker": r"\bSageMaker\b",
    "Docker": r"\bDocker\b",
    "Kubernetes": r"\bKubernetes\b|\bK8s\b",
    "Terraform": r"\bTerraform\b",
    "Git": r"\bGit\b(?!Hub)",
    "GitHub": r"\bGitHub\b",
    "GitLab": r"\bGitLab\b",
    "Linux": r"\bLinux\b",
    "Airflow": r"\bAirflow\b",
    "Kafka": r"\bKafka\b",
    "Hive": r"\bHive\b",
    "Talend": r"\bTalend\b",
    "Informatica": r"\bInformatica\b",
    "CI/CD": r"\bCI/CD\b|\bGitHub Actions\b|\bAzure DevOps\b|\bJenkins\b",
    "Big Data": r"\bBig Data\b",
    "Data Warehouse": r"\bdata\s*warehouse\b",
    "Data Lake": r"\bdata\s*lake\b|\bDelta Lake\b",
    "Statistics": r"\bstatistiques?\b|\bstatistics\b|\bstatistical modeling\b",
    "LLM": r"\bLLMs?\b|\blarge language models?\b",
    "GenAI": r"\bGenAI\b|\bGenerative AI\b",
    "RAG": r"\bRAG\b|\bRetrieval[- ]?Augmented\b",
    "Fine-tuning": r"\bfine[- ]?tuning\b",
    "Transformers": r"\bTransformers?\b",
    "Hugging Face": r"\bHugging\s*Face\b",
    "MLOps": r"\bMLOps\b",
    "SAS": r"\bSAS\b",
    "Pandas": r"\bPandas\b",
    "NumPy": r"\bNumPy\b",
    "Power Apps": r"\bPower\s*Apps?\b",
    "Power Automate": r"\bPower\s*Automate\b",
    "FastAPI": r"\bFastAPI\b",
    "Django": r"\bDjango\b",
    "Flask": r"\bFlask\b",
    "REST API": r"\bREST(\s*API)?\b",
    "GraphQL": r"\bGraphQL\b",
    "ETL": r"\bETL\b",
    "ELT": r"\bELT\b",
    "dbt": r"\bdbt\b",
    "A/B Testing": r"\bA/B\s*test(ing)?\b",
    "Time Series": r"\btime[- ]?series\b|\bs[ée]ries?\s*temporelles?\b",
    "Forecasting": r"\bforecast(ing)?\b|\bpr[ée]vision",
    "Reinforcement Learning": r"\breinforcement\s*learning\b",
    "Anglais": r"\bAnglais\b|\b(fluent|professional)\s+English\b",
    "Français": r"\bFran[çc]ais\b|\bFrench\b",
    "Business Intelligence": r"\bbusiness intelligence\b|\binformatique d[ée]cisionnelle\b|\boutils BI\b|\bBI\b(?=\s+(?:tools|outils|dashboard|reporting))",
    "Agile": r"\bagile\b|\bscrum\b|\bkanban\b",
    "ETL/Data Pipeline": r"\bdata pipeline\b|\bpipeline (de )?donn[ée]es\b",
    "Data Visualization": r"\bdashboards?\b|\btableaux? de bord\b|\bdata visualization\b|\bvisualisation\b",
    "KPI / Reporting": r"\bKPIs?\b|\breporting\b|\btableaux? de bord\b",
}


def detect_skills(text: str) -> list[str]:
    found = []
    for skill, pat in SKILLS_PATTERNS.items():
        if re.search(pat, text, re.I):
            found.append(skill)
    # Filter language pairs to avoid duplicates
    return found


# ─── 5. Family + domains heuristic ───────────────────────────────────────────

def get_family(title: str) -> str:
    t = title.lower()
    if "tech lead" in t and "data" in t:
        return "DATA_ARCHITECT"
    if "lead data" in t or "architect" in t or "architecte" in t:
        return "DATA_ARCHITECT"
    if "mlops" in t or "ml ops" in t or "dataops" in t:
        return "MLOPS_ENGINEER"
    if "research" in t:
        return "RESEARCH_SCIENTIST"
    if "nlp" in t:
        return "NLP_ENGINEER"
    if "computer vision" in t or " cv " in t or "vision engineer" in t:
        return "CV_ENGINEER"
    if "genai" in t or "generative ai" in t or "llm" in t:
        return "GENAI_LLM_ENGINEER"
    if (
        "ml engineer" in t
        or "machine learning engineer" in t
        or "ml/ai" in t
        or "ai/ml" in t
        or "ml-engineer" in t
        or "data scientist / ml" in t
        or "ml engineer" in t
        or " ai engineer" in t
        or t.startswith("ai engineer")
        or "ai specialist" in t
        or "ai architect" in t
        or "ai-software" in t
        or "applied ai" in t
        or "machine learning" in t
        or "ai python" in t  # AI Python Developer
    ):
        return "ML_ENGINEER" if "architect" not in t else "DATA_ARCHITECT"
    if "data scientist" in t or "science engineer" in t:
        return "DATA_SCIENTIST"
    if (
        "data engineer" in t
        or "data ingénieur" in t
        or "data ingenieur" in t
        or "data platform engineer" in t
    ):
        return "DATA_ENGINEER"
    if "business intelligence" in t or "bi analyst" in t or "bi -" in t or "data po" in t:
        return "BUSINESS_ANALYST"
    if "business analyst" in t or "business data" in t:
        return "BUSINESS_ANALYST"
    if "reporting analyst" in t:
        return "DATA_ANALYST"
    if "crm analyst" in t:
        return "BUSINESS_ANALYST"
    if (
        "data analyst" in t
        or "analyste data" in t
        or ("quantitative" in t and "analyst" in t)
        or "data analytics" in t
        or "analytics" in t  # Analytics Graduate Program, etc.
        or "analyst" in t and "data" in t  # Associate Analyst - Data Solutions
    ):
        return "DATA_ANALYST"
    return "OTHER"


def get_domains(skills: list[str], title: str, desc: str) -> list[str]:
    domains = set()
    t = (title + " " + desc).lower()
    if any(s in skills for s in ("Machine Learning", "Scikit-learn", "TensorFlow", "PyTorch", "Keras")):
        domains.add("ML_CLASSIC")
    if any(s in skills for s in ("Deep Learning", "TensorFlow", "PyTorch", "Transformers")):
        domains.add("DEEP_LEARNING")
    if "NLP" in skills or "RAG" in skills or "Hugging Face" in skills or "Transformers" in skills:
        domains.add("NLP")
    if "Computer Vision" in skills or "computer vision" in t or "vision par ordinateur" in t:
        domains.add("COMPUTER_VISION")
    if "LLM" in skills or "GenAI" in skills or "Fine-tuning" in skills or "RAG" in skills:
        domains.add("GENERATIVE_AI")
    if "Reinforcement Learning" in skills:
        domains.add("REINFORCEMENT_LEARNING")
    if "Time Series" in skills or "Forecasting" in skills:
        domains.add("TIME_SERIES")
    if any(s in skills for s in ("Airflow", "Kafka", "Spark", "Hadoop", "Databricks", "ETL", "ELT", "dbt", "Talend")):
        domains.add("DATA_ENGINEERING")
    if "MLOps" in skills or "Docker" in skills and ("Kubernetes" in skills or "MLflow" in skills):
        domains.add("MLOPS")
    if any(s in skills for s in ("Power BI", "Tableau", "Looker")) or "business intelligence" in t:
        domains.add("BUSINESS_INTELLIGENCE")
    if any(s in skills for s in ("Big Data", "Hadoop", "Spark", "Databricks", "Data Lake", "Data Warehouse")):
        domains.add("BIG_DATA")
    if any(s in skills for s in ("Azure", "AWS", "GCP", "Vertex AI", "SageMaker")):
        domains.add("CLOUD_DATA")
    if "research" in t and ("ai" in t or "ml" in t or "deep learning" in t):
        domains.add("RESEARCH")
    return sorted(domains)


# ─── 6. Posted date computation ──────────────────────────────────────────────

def compute_posted_date(date_rel: str | None) -> date | None:
    if not date_rel:
        return None
    m = re.match(r"^(\d+)d(\+)?$", date_rel)
    if not m:
        return None
    days, plus = int(m.group(1)), m.group(2)
    if plus:
        # "30d+" = posted more than 30 days ago — approximate at 45 days
        days = days + 15
    return TODAY - timedelta(days=days)


# ─── 7. Out of scope filter ──────────────────────────────────────────────────

OUT_OF_SCOPE_TITLE_PATTERNS = [
    r"\bfull[- ]?stack\b",
    r"\bsoftware engineer(ing)?\b",
    r"\bnode\.?js\b",
    r"\bsenior python developer\b",
    r"\bdevops\b(?! engineer)|\bdevops engineer\b",  # Note: pure DevOps, not data DevOps
    r"\bquality engineer\b|\bingénieur qualité\b",
    r"\bqa engineer\b",
    r"\bcodification\s+plm\b",
    r"\bassembly\b",
    r"\bdesign release engineer\b",
    r"\bcnc technician\b",
    r"\bprocess engineer\b",
    r"\bmaintenance coordinator\b",
    r"\breliability\b",
    r"\bsustainable infrastructure\b",
    r"\bintercompany\b",
    r"\binternship.*software\b",
    r"\bsoftware engineering internship\b",
    r"\btesting research\b",
    r"\bgeomatic\b",
    r"\bperception.*radar\b",  # Stellantis radar = hardware, not ML proper
    r"\bsenior ai software engineer\b",  # Syensqo Senior AI Software Engineer is software dev
]


def is_out_of_scope(title: str) -> bool:
    t = title.lower()
    for pat in OUT_OF_SCOPE_TITLE_PATTERNS:
        if re.search(pat, t, re.I):
            return True
    return False


# ─── 8. Company type & seniority ─────────────────────────────────────────────

PUBLIC_KEYWORDS = ["bank al-maghrib", "anapec", "cnss", "om pi", "office national", "université", "umpe"]
RH_KEYWORDS = ["michael page", "manpower", "alten", "capgemini engineering", "sopra steria", "altius"]


def company_type(company: str) -> str:
    if not company:
        return "inconnu"
    c = company.lower()
    if any(k in c for k in PUBLIC_KEYWORDS):
        return "entité morale publique"
    return "entité morale privée"


def detect_experience_years(text: str) -> tuple[int | None, int | None]:
    """Detect experience range: '2-5 ans', '5+ years', etc."""
    # Range "2-5 ans" or "2 à 5 ans"
    m = re.search(r"(\d+)\s*(?:-|à|to)\s*(\d+)\s*(?:ans|years|year)", text, re.I)
    if m:
        return int(m.group(1)), int(m.group(2))
    # "5+ years" / "2+ ans"
    m = re.search(r"(\d+)\+\s*(?:ans|years|year)", text, re.I)
    if m:
        return int(m.group(1)), None
    # "minimum 5 ans"
    m = re.search(r"(?:minimum|au moins|at least)\s+(\d+)\s*(?:ans|years|year)", text, re.I)
    if m:
        return int(m.group(1)), None
    # "X années d'expérience"
    m = re.search(r"(\d+)\s*(?:ann[ée]es?|years?)\s*(?:d'?\s*)?exp[ée]rience", text, re.I)
    if m:
        return int(m.group(1)), None
    return None, None


def detect_contract(text: str) -> str | None:
    t = text.lower()
    if re.search(r"\bcdi\b|\bpermanent\b|\bregular full[- ]?time\b", t):
        return "CDI"
    if re.search(r"\bcdd\b|\bfixed[- ]?term\b", t):
        return "CDD"
    if re.search(r"\bstage\b|\binternship\b|\bintern\b", t):
        return "Stage"
    if re.search(r"\balternance\b|\bapprentice\b", t):
        return "Alternance"
    if re.search(r"\bfreelance\b|\bcontractor\b", t):
        return "Freelance"
    return None


def detect_remote(text: str) -> str:
    t = text.lower()
    if re.search(r"\b100\s*%?\s*remote\b|\bfully remote\b|\btélétravail intégral\b", t):
        return "remote"
    if re.search(r"\bhybrid\b|\bhybride\b|\b\d+\s*j(ours)?\s*par\s*semaine\b|\b\d+\s*days?\s*per\s*week\b", t):
        return "hybrid"
    if re.search(r"\bon[- ]site\b|\bsur site\b|\bprésentiel\b", t):
        return "on-site"
    if re.search(r"\bremote\b|\btélétravail\b", t):
        return "remote"
    return "unknown"


# ─── 9. Posting dataclass ────────────────────────────────────────────────────

@dataclass
class Posting:
    job_id: str
    source: str = "glassdoor-ma"
    source_url: str = ""
    source_ref: str = ""
    title: str = ""
    title_normalized: str = ""
    company: str = ""
    company_type: str = "inconnu"
    location: str = ""
    country: str = "MA"
    remote_policy: str = "unknown"
    posted_date: str | None = None
    deadline_date: str | None = None
    contract_type: str | None = None
    experience_min_years: int | None = None
    experience_max_years: int | None = None
    salary_range: str | None = None
    description: str = ""
    skills_required: list[str] = field(default_factory=list)
    skills_optional: list[str] = field(default_factory=list)
    responsibilities: list[str] = field(default_factory=list)
    tools_mentioned: list[str] = field(default_factory=list)
    frameworks_mentioned: list[str] = field(default_factory=list)
    languages_programming: list[str] = field(default_factory=list)
    domains_iaml: list[str] = field(default_factory=list)
    job_family: str = "OTHER"
    languages_spoken: list[str] = field(default_factory=list)
    scraped_at: str = TODAY_ISO_DT
    scraper: str = SCRAPER
    rgpd_compliant: bool = True
    personal_data_stripped: bool = True
    extraction_confidence: float = 0.75


PROG_LANGS = {"Python", "SQL", "R", "Java", "JavaScript", "TypeScript", "Scala", "SAS"}
FRAMEWORKS = {
    "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "FastAPI", "Django", "Flask",
    "Spring Boot", "Pandas", "NumPy", "Transformers", "Hugging Face",
}
TOOLS = {
    "Docker", "Kubernetes", "Terraform", "Git", "GitHub", "GitLab", "Airflow", "Kafka",
    "Hive", "MLflow", "Kubeflow", "Databricks", "Snowflake", "BigQuery", "PostgreSQL",
    "MySQL", "MongoDB", "Redis", "Elasticsearch", "Power BI", "Tableau", "Looker",
    "Excel", "Azure", "AWS", "GCP", "Vertex AI", "SageMaker", "Talend", "Informatica",
    "dbt", "Linux", "Power Apps", "Power Automate",
}
LANG_SPOKEN = {"Anglais", "Français"}


def categorize_skills(skills: list[str]):
    langs = [s for s in skills if s in PROG_LANGS]
    fws = [s for s in skills if s in FRAMEWORKS]
    tls = [s for s in skills if s in TOOLS]
    spoken = [s for s in skills if s in LANG_SPOKEN]
    required = [s for s in skills if s not in LANG_SPOKEN]
    return required, langs, fws, tls, spoken


# ─── 10. Markdown template ───────────────────────────────────────────────────

def render_md(p: Posting) -> str:
    skills_str = " · ".join(f"`{s}`" for s in p.skills_required) if p.skills_required else "_(none detected)_"
    domains_str = " · ".join(p.domains_iaml) if p.domains_iaml else "_(none)_"
    lines = [
        f"# {p.title} — {p.company}",
        "",
        f"> **Source** : Glassdoor Maroc · [Voir l'annonce]({p.source_url})",
        f"> **Job ID** : `{p.job_id}` · Réf. `{p.source_ref}`",
        f"> **Date publication** : **{p.posted_date or 'non datée'}**" + (f" · Deadline {p.deadline_date}" if p.deadline_date else ""),
        "",
        "## Identification",
        "",
        "| Champ | Valeur |",
        "|---|---|",
        f"| Entreprise | **{p.company}** ({p.company_type}) |",
        f"| Lieu | {p.location} ({p.country}) |",
        f"| Remote | {p.remote_policy} |",
        f"| Contrat | **{p.contract_type or 'non précisé'}** |",
        f"| Expérience | {p.experience_min_years or '?'}{'+' if p.experience_max_years is None and p.experience_min_years else f' - {p.experience_max_years}'} ans |"
        if p.experience_min_years
        else "| Expérience | non précisée |",
        "",
        "## Famille",
        "",
        f"- Job family : `{p.job_family}`",
        f"- Domaines : {domains_str}",
        "",
        f"## Skills détectés ({len(p.skills_required)})",
        "",
        skills_str,
        "",
        "## Description",
        "",
        p.description[:3000] + ("..." if len(p.description) > 3000 else ""),
        "",
    ]
    return "\n".join(lines)


# ─── 11. Main pipeline ───────────────────────────────────────────────────────

def main():
    POSTINGS.mkdir(exist_ok=True)
    ARCHIVE.mkdir(exist_ok=True)

    print(f"[*] Loading SRCH index from {RAW}")
    srch_idx = load_srch_index()
    print(f"[*] {len(srch_idx)} jobs indexed")

    # Find all detail .md files (named <jl_id>.md)
    detail_files = sorted([p for p in RAW.glob("*.md") if p.stem.isdigit()])
    print(f"[*] {len(detail_files)} detail markdown files found")

    postings: list[Posting] = []
    skipped_oos: list[str] = []
    skipped_pre2023: list[str] = []

    for fp in detail_files:
        jl = fp.stem
        with fp.open(encoding="utf-8") as f:
            md = f.read()
        # Title/company/location from index
        idx = srch_idx.get(jl, {})
        title = idx.get("title") or ""
        company = idx.get("company") or ""
        location = idx.get("location") or "Maroc"
        url = idx.get("url") or ""
        date_rel = idx.get("date_rel")

        # Bad company fallback (was eaten by parser): try slug
        if not company or re.match(r"^\d+d\+?$", company) or company == "Most relevant":
            t_slug, c_slug = slug_fallback(url)
            if c_slug:
                company = c_slug
            if not title and t_slug:
                title = t_slug

        # Out of scope?
        if is_out_of_scope(title):
            skipped_oos.append(f"{jl} | {title}")
            continue

        desc = extract_description(md)
        skills = detect_skills(desc + " " + title)
        family = get_family(title)
        domains = get_domains(skills, title, desc)
        posted = compute_posted_date(date_rel)
        contract = detect_contract(desc)
        remote = detect_remote(desc)
        exp_min, exp_max = detect_experience_years(desc)

        if posted and posted < date(2023, 1, 1):
            skipped_pre2023.append(f"{jl} | {posted}")
            continue

        required, langs, fws, tls, spoken = categorize_skills(skills)

        year = (posted.year if posted else TODAY.year)
        p = Posting(
            job_id=f"glassdoor-ma-{year}-PENDING",
            source_url=url,
            source_ref=jl,
            title=title,
            title_normalized=family,
            company=company or "Anonyme",
            company_type=company_type(company),
            location=location,
            country="MA",
            remote_policy=remote,
            posted_date=posted.isoformat() if posted else None,
            contract_type=contract,
            experience_min_years=exp_min,
            experience_max_years=exp_max,
            description=desc,
            skills_required=required,
            languages_programming=langs,
            frameworks_mentioned=fws,
            tools_mentioned=tls,
            languages_spoken=spoken,
            domains_iaml=domains,
            job_family=family,
            extraction_confidence=0.85 if posted else 0.65,
        )
        postings.append(p)

    # Sort by posted_date desc (most recent first), no-date last
    postings.sort(key=lambda p: (p.posted_date or "0000-00-00"), reverse=True)
    # Assign numerical IDs
    for n, p in enumerate(postings, 1):
        year = (p.posted_date or f"{TODAY.year}-01-01")[:4]
        p.job_id = f"glassdoor-ma-{year}-{n:03d}"
        # Write JSON
        json_fp = POSTINGS / f"{n:03d}.json"
        with json_fp.open("w", encoding="utf-8") as f:
            json.dump(asdict(p), f, ensure_ascii=False, indent=2)
        # Write MD
        md_fp = POSTINGS / f"{n:03d}.md"
        with md_fp.open("w", encoding="utf-8") as f:
            f.write(render_md(p))

    # Quality gates
    no_skills = [p.job_id for p in postings if not p.skills_required]
    no_family = [p.job_id for p in postings if p.job_family == "OTHER"]
    print(f"\n=== EXTRACTED: {len(postings)} postings ===")
    print(f"   skipped out-of-scope: {len(skipped_oos)}")
    print(f"   skipped pre-2023: {len(skipped_pre2023)}")
    print(f"\nQuality gates:")
    print(f"   without skills detected: {len(no_skills)} → {no_skills[:5]}")
    print(f"   with family=OTHER: {len(no_family)} → {no_family[:5]}")

    # Distribution by year
    by_year: dict[str, int] = {}
    by_family: dict[str, int] = {}
    by_location: dict[str, int] = {}
    for p in postings:
        y = (p.posted_date or "undated")[:4]
        by_year[y] = by_year.get(y, 0) + 1
        by_family[p.job_family] = by_family.get(p.job_family, 0) + 1
        by_location[p.location] = by_location.get(p.location, 0) + 1
    print(f"\nDistribution year: {dict(sorted(by_year.items(), reverse=True))}")
    print(f"Distribution family: {dict(sorted(by_family.items(), key=lambda x: -x[1]))}")
    print(f"Distribution location: {dict(sorted(by_location.items(), key=lambda x: -x[1])[:10])}")
    print(f"\nOOS skipped: {skipped_oos}")


if __name__ == "__main__":
    main()
