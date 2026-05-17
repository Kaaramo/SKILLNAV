"""Construction du graphe Skill <-> Job depuis les postings SKILLNAV.

Pipeline :
  load_postings()
    -> extraction skills par offre
    -> comptage occurrences + co-occurrences
    -> SkillGraph (Pydantic snapshot) + nx.Graph (pour algos)
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from itertools import combinations
from typing import Any

import networkx as nx

from skillnav.analysis.loaders import load_postings
from skillnav.schemas.graph import (
    BelongsToEdge,
    CoOccursWithEdge,
    CompanyNode,
    GraphMetrics,
    JobNode,
    PostedByEdge,
    RequiresEdge,
    SkillFamily,
    SkillFamilyNode,
    SkillGraph,
    SkillNode,
)

# ── Taxonomie famille de competences ─────────────────────────────────────────
# Correspondance keyword (lowercase) -> SkillFamily.
# Ordre important : la premiere correspondance gagne.

_FAMILY_KEYWORDS: dict[SkillFamily, frozenset[str]] = {
    # Agents AI (le plus specifique, doit passer avant GenAI et NLP)
    SkillFamily.AGENTS_AI: frozenset(
        [
            "agentic",
            "ai agent",
            "agents",
            "multi-agent",
            "agent framework",
            "agent orchestration",
            "crewai",
            "autogen",
            "langgraph",
            "semantic kernel",
            "mcp",
            "model context protocol",
            "function calling",
            "tool calling",
            "conversational ai",
            "rag",
            "google adk",
            "dialogflow",
        ]
    ),
    # GenAI (passe avant NLP pour capter llm, fine-tuning, openai, claude, gemini, ...)
    SkillFamily.GENAI: frozenset(
        [
            "llm",
            "large language model",
            "generative ai",
            "genai",
            "foundation model",
            "prompt engineering",
            "fine-tuning",
            "lora",
            "qlora",
            "peft",
            "rlhf",
            "quantization",
            "model distillation",
            "few-shot",
            "multimodal",
            "structured outputs",
            "context engineering",
            "guardrails",
            "responsible ai",
            "embedding",
            "huggingface",
            "hugging face",
            "langchain",
            "llamaindex",
            "haystack",
            "dspy",
            "langfuse",
            "openai",
            "anthropic",
            "claude",
            "gemini",
            "llama",
            "mistral",
            "gpt",
            "chatgpt",
            "cursor",
            "copilot",
        ]
    ),
    SkillFamily.COMPUTER_VISION: frozenset(
        [
            "opencv",
            "yolo",
            "torchvision",
            "detectron",
            "pillow",
            "object detection",
            "image segmentation",
            "computer vision",
            "image classification",
            "face recognition",
            "ocr",
        ]
    ),
    # NLP recadre sur le NLP classique (les LLM/GenAI sont passes en GenAI)
    SkillFamily.NLP: frozenset(
        [
            "nlp",
            "natural language processing",
            "bert",
            "camembert",
            "distilbert",
            "spacy",
            "nltk",
            "named entity",
            "text mining",
            "text classification",
            "question answering",
            "semantic search",
            "vector search",
            "similarity search",
            "retrieval",
            "faiss",
            "knowledge graphs",
        ]
    ),
    SkillFamily.DEEP_LEARNING: frozenset(
        [
            "pytorch",
            "tensorflow",
            "keras",
            "jax",
            "deep learning",
            "neural network",
            "lstm",
            "gan",
            "autoencoder",
            "diffusion",
            "cnn",
            "cnns",
            "rnn",
            "rnns",
            "transformer",
            "backpropagation",
            "gradient descent",
            "cuda",
        ]
    ),
    SkillFamily.MLOPS: frozenset(
        [
            "mlflow",
            "kubeflow",
            "docker",
            "kubernetes",
            "mlops",
            "dvc",
            "wandb",
            "prefect",
            "dagster",
            "bentoml",
            "seldon",
            "ci/cd",
            "devops",
            "model deployment",
            "model monitoring",
        ]
    ),
    SkillFamily.DATA_ENGINEERING: frozenset(
        [
            "spark",
            "kafka",
            "dbt",
            "etl",
            "hadoop",
            "databricks",
            "flink",
            "dask",
            "pandas",
            "polars",
            "data pipeline",
            "data warehouse",
            "data lake",
            "airflow",
            "nifi",
            "big data",
        ]
    ),
    # Machine Learning (NOUVELLE famille, separe de Statistics)
    SkillFamily.MACHINE_LEARNING: frozenset(
        [
            "machine learning",
            "scikit-learn",
            "sklearn",
            "xgboost",
            "lightgbm",
            "catboost",
            "random forest",
            "decision tree",
            "decision trees",
            "svm",
            "reinforcement learning",
            "supervised learning",
            "unsupervised learning",
            "feature engineering",
            "model evaluation",
            "model training",
            "model optimization",
            "predictive modeling",
            "classification",
            "anomaly detection",
        ]
    ),
    # Statistics recadre sur les vraies stats
    SkillFamily.STATISTICS: frozenset(
        [
            "statistics",
            "statistical analysis",
            "probability",
            "bayesian",
            "regression",
            "hypothesis testing",
            "a/b testing",
            "scipy",
            "statsmodels",
            "linear algebra",
            "arima",
        ]
    ),
    SkillFamily.DATABASES: frozenset(
        [
            "postgresql",
            "mysql",
            "mongodb",
            "neo4j",
            "redis",
            "elasticsearch",
            "cassandra",
            "snowflake",
            "bigquery",
            "sqlite",
            "oracle",
            "sql",
            "nosql",
            "pinecone",
            "weaviate",
            "chroma",
            "qdrant",
        ]
    ),
    SkillFamily.CLOUD: frozenset(
        [
            "aws",
            "gcp",
            "azure",
            "s3",
            "ec2",
            "lambda",
            "vertex ai",
            "sagemaker",
            "terraform",
            "gke",
            "eks",
            "cloud run",
            "cloud functions",
            "cloud",
        ]
    ),
    # BI & Analytics (NOUVELLE famille pour profils Data/Business Analyst)
    SkillFamily.BI_ANALYTICS: frozenset(
        [
            "power bi",
            "tableau",
            "excel",
            "sas",
        ]
    ),
    # Programming en dernier (mots-cles courts moins prioritaires)
    # Note : "go" supprime car matchait "google" en substring (bug Google ADK/Gemini/Dialogflow)
    SkillFamily.PROGRAMMING: frozenset(
        [
            "python",
            "java",
            "scala",
            "javascript",
            "typescript",
            "c++",
            "golang",
            "rust",
            "julia",
            "bash",
            "shell",
            "numpy",
            "git",
        ]
    ),
}


def _infer_family(skill: str) -> SkillFamily:
    """Assigne une SkillFamily a partir des mots-cles (premiere correspondance)."""
    skill_lower = skill.lower()
    for family, keywords in _FAMILY_KEYWORDS.items():
        for kw in keywords:
            if kw == skill_lower or kw in skill_lower:
                return family
    return SkillFamily.OTHER


def _extract_skills(posting: dict[str, Any]) -> list[str]:
    """Extrait les skills d'un posting (required + optional), dedupliques."""
    required: list[Any] = posting.get("skills_required") or []
    optional: list[Any] = posting.get("skills_optional") or []
    seen: set[str] = set()
    result: list[str] = []
    for raw in list(required) + list(optional):
        if isinstance(raw, str):
            name = raw.strip()
            key = name.lower()
            if name and key not in seen:
                seen.add(key)
                result.append(name)
    return result


def build_graph(
    sources: list[str] | None = None,
    min_cooccurrence: int = 2,
) -> tuple[SkillGraph, nx.Graph]:
    """Construit le SkillGraph et le graphe NetworkX depuis les postings JSON.

    Args:
        sources: liste de sources a charger (None = toutes).
        min_cooccurrence: seuil minimum de co-occurrences pour creer un arc.

    Returns:
        (SkillGraph, nx.Graph) - snapshot Pydantic + graphe NetworkX pour algos.
    """
    postings = load_postings(sources)

    skill_occurrence: Counter[str] = Counter()
    skill_canonical: dict[str, str] = {}  # lowercase -> nom canonique
    co_occurrence: Counter[tuple[str, str]] = Counter()
    job_nodes: list[JobNode] = []
    requires_edges: list[RequiresEdge] = []

    # Companies : dedoublonnees par nom canonique (lower)
    company_canonical: dict[str, str] = {}  # lower -> nom canonique
    company_country: dict[str, str] = {}  # lower -> pays
    company_jobs: Counter[str] = Counter()  # lower -> nb d'offres publiees
    posted_by_edges: list[PostedByEdge] = []

    for posting in postings:
        skills = _extract_skills(posting)

        # Compte les occurrences et enregistre le nom canonique
        skill_keys: list[str] = []
        for s in skills:
            key = s.lower()
            if key not in skill_canonical:
                skill_canonical[key] = s
            skill_occurrence[key] += 1
            skill_keys.append(key)

        # Co-occurrences : paires triees pour eviter (a,b) et (b,a)
        for key_a, key_b in combinations(sorted(set(skill_keys)), 2):
            co_occurrence[(key_a, key_b)] += 1

        # Noeud Job
        job_id = str(posting.get("job_id", ""))
        if not job_id:
            continue

        published_at: datetime | None = None
        if date_str := posting.get("posted_date"):
            try:
                published_at = datetime.fromisoformat(str(date_str))
            except ValueError:
                pass

        company_name = str(posting.get("company", "")).strip()
        country = str(posting.get("country", ""))

        job_nodes.append(
            JobNode(
                job_id=job_id,
                title=str(posting.get("title", "")),
                company=company_name,
                country=country,
                source=str(posting.get("source", "")),
                published_at=published_at,
            )
        )

        for s in skills:
            requires_edges.append(
                RequiresEdge(
                    job_id=job_id,
                    skill_name=skill_canonical.get(s.lower(), s),
                )
            )

        # Company : dedoublonnage + arc POSTED_BY (uniquement si nom non vide)
        if company_name:
            company_key = company_name.lower()
            if company_key not in company_canonical:
                company_canonical[company_key] = company_name
                company_country[company_key] = country
            company_jobs[company_key] += 1
            posted_by_edges.append(
                PostedByEdge(
                    company_name=company_canonical[company_key],
                    job_id=job_id,
                )
            )

    # Noeuds Skill
    skill_nodes: list[SkillNode] = [
        SkillNode(
            name=canonical,
            family=_infer_family(canonical),
            occurrence_count=skill_occurrence[key],
        )
        for key, canonical in skill_canonical.items()
    ]

    # Aretes CO_OCCURS (filtrees par seuil)
    co_occurs_edges: list[CoOccursWithEdge] = [
        CoOccursWithEdge(
            skill_a=skill_canonical.get(a, a),
            skill_b=skill_canonical.get(b, b),
            weight=count,
        )
        for (a, b), count in co_occurrence.items()
        if count >= min_cooccurrence
    ]

    # Aretes BELONGS_TO
    belongs_to_edges: list[BelongsToEdge] = [
        BelongsToEdge(skill_name=node.name, family_name=node.family.value)
        for node in skill_nodes
    ]

    # Noeuds SkillFamily (un par valeur d'enum)
    family_nodes: list[SkillFamilyNode] = [SkillFamilyNode(name=f.value) for f in SkillFamily]

    # Noeuds Company (dedoublonnes par nom canonique)
    company_nodes: list[CompanyNode] = [
        CompanyNode(
            name=canonical,
            country=company_country[key],
            job_count=company_jobs[key],
        )
        for key, canonical in company_canonical.items()
    ]

    # Graphe NetworkX (Skill <-> Skill avec poids = nombre de co-occurrences)
    nx_graph: nx.Graph = nx.Graph()
    for node in skill_nodes:
        nx_graph.add_node(node.name, family=node.family.value)
    for edge in co_occurs_edges:
        nx_graph.add_edge(edge.skill_a, edge.skill_b, weight=edge.weight)

    metrics = GraphMetrics(
        node_count=len(skill_nodes),
        edge_count=len(co_occurs_edges),
    )

    skill_graph = SkillGraph(
        nodes_skills=skill_nodes,
        nodes_jobs=job_nodes,
        nodes_families=family_nodes,
        nodes_companies=company_nodes,
        edges_co_occurs=co_occurs_edges,
        edges_requires=requires_edges,
        edges_belongs_to=belongs_to_edges,
        edges_posted_by=posted_by_edges,
        metrics=metrics,
        job_count=len(job_nodes),
        company_count=len(company_nodes),
    )

    return skill_graph, nx_graph
