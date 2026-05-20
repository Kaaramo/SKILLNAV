"""Extraction des competences enseignees a partir des titres de modules.

Deux strategies cohabitent :

1. Strategie LLM (Claude Sonnet 4.5 via pydantic-ai) - decision PRD :
   - Prompt few-shot oriente vocabulaire SKILLNAV
   - Rate-limite par asyncio.Semaphore(3)
   - Necessite ANTHROPIC_API_KEY dans l'environnement

2. Strategie rules (deterministe, sans appel reseau) :
   - Mots-cles tires de skillnav/pipelines/structure_mining/graph_builder.py
   - Heuristiques sur intitules academiques (NLP, ML, Big Data, etc.)
   - Filtre les modules non techniques (langues, management, ethique...)

L'orchestrator choisit "auto" : LLM si la cle API est presente, sinon rules.
"""

from __future__ import annotations

import asyncio
import logging
import os
from collections.abc import Sequence

from pydantic import BaseModel, Field

from skillnav.pipelines.structure_mining.graph_builder import _FAMILY_KEYWORDS

logger = logging.getLogger(__name__)

# ── Strategie LLM ─────────────────────────────────────────────────────────────

_CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
_MAX_CONCURRENT_LLM = 3
_LLM_SYSTEM_PROMPT = (
    "Tu es un expert en programmes d'ingenierie en sciences des donnees et IA.\n"
    "A partir du titre d'un module academique, identifie les COMPETENCES "
    "TECHNIQUES enseignees, en termes courts et canoniques du domaine "
    "professionnel (ex: 'Python', 'Machine Learning', 'SQL', 'NLP', 'PyTorch')."
)
_LLM_USER_TEMPLATE = (
    "Module academique : {module_name}\n\n"
    "Regles strictes :\n"
    "- Maximum 8 competences par module.\n"
    "- Termes courts (1 a 3 mots maximum).\n"
    "- Vocabulaire anglais pour la technique (Python, Apache Spark, AWS).\n"
    "- Si le module est non technique (langues, management, ethique, "
    "communication, culture), retourne une liste vide.\n"
    "- Privilegier les outils et frameworks concrets quand ils sont evidents.\n"
)


class ExtractedSkills(BaseModel):
    """Sortie structuree attendue du LLM."""

    skills: list[str] = Field(default_factory=list)


async def _extract_skills_llm_single(module_name: str) -> list[str]:
    """Appel LLM unique pour un module donne (pydantic-ai + Claude Sonnet 4.5)."""
    from pydantic_ai import Agent
    from pydantic_ai.models.anthropic import AnthropicModel

    if not os.environ.get("ANTHROPIC_API_KEY"):
        msg = "ANTHROPIC_API_KEY absent de l'environnement"
        raise RuntimeError(msg)

    model = AnthropicModel(_CLAUDE_MODEL)
    agent: Agent[None, ExtractedSkills] = Agent(
        model=model,
        result_type=ExtractedSkills,
        system_prompt=_LLM_SYSTEM_PROMPT,
    )
    result = await agent.run(_LLM_USER_TEMPLATE.format(module_name=module_name))
    return list(result.data.skills)


async def extract_skills_llm_batch(
    module_names: Sequence[str],
    max_concurrent: int = _MAX_CONCURRENT_LLM,
) -> list[list[str]]:
    """Extraction LLM en batch async, rate-limitee par semaphore."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def _bounded(name: str) -> list[str]:
        async with semaphore:
            try:
                return await _extract_skills_llm_single(name)
            except Exception as exc:
                logger.warning("LLM extraction echec pour %r: %s", name, exc)
                return []

    return await asyncio.gather(*(_bounded(n) for n in module_names))


# ── Strategie rules (deterministe) ────────────────────────────────────────────

# Modules non techniques : on retourne une liste vide pour eviter le bruit.
_NON_TECHNICAL_NEEDLES: frozenset[str] = frozenset(
    [
        "langue", "langues", "communication", "anglais", "francais", "francaise", "anglaise",
        "management", "marketing", "entrepreneuriat", "entreprenariat",
        "ethique", "droit", "gestion des ressources humaines", "grh",
        "culture", "art", "competences personnelles", "competences artistiques",
        "competences numeriques", "competences numérique", "digital skills",
        "transition ecologique", "transition écologique",
        "veille", "parrainage", "projet tutoriel", "projets tutores", "projets tutorés",
        "microeconomie", "macroeconomie", "ingenierie financiere", "developpement durable",
        "culture et art",
    ]
)

# Heuristiques explicites : titre academique -> liste de skills canoniques.
# Ordre important : les regles plus specifiques d'abord.
_TITLE_HEURISTICS: tuple[tuple[str, tuple[str, ...]], ...] = (
    # NLP / TALN
    ("traitement automatique des langues", ("NLP", "transformers", "spaCy")),
    ("natural language processing", ("NLP", "transformers")),
    ("nlp", ("NLP", "transformers")),
    ("taln", ("NLP", "transformers")),
    # Vision
    ("vision par ordinateur", ("computer vision", "OpenCV", "PyTorch")),
    ("computer vision", ("computer vision", "OpenCV", "PyTorch")),
    ("traitement d'image", ("computer vision", "OpenCV", "image processing")),
    ("traitement d image", ("computer vision", "OpenCV", "image processing")),
    ("realite virtuelle", ("computer vision", "3D")),
    ("réalité virtuelle", ("computer vision", "3D")),
    # Deep Learning / Reinforcement Learning
    ("apprentissage profond", ("Deep Learning", "PyTorch", "TensorFlow")),
    ("deep learning", ("Deep Learning", "PyTorch", "TensorFlow")),
    ("apprentissage par renforcement", ("reinforcement learning",)),
    ("reinforcement learning", ("reinforcement learning",)),
    # ML
    ("machine learning en python", ("Machine Learning", "Python", "scikit-learn")),
    ("machine learning sur r", ("Machine Learning", "R", "tidyverse")),
    ("machine learning", ("Machine Learning", "scikit-learn", "Python")),
    ("apprentissage automatique", ("Machine Learning", "scikit-learn", "Python")),
    ("sparsity en machine learning", ("Machine Learning", "regularization")),
    ("algorithme ia et prediction", ("Machine Learning", "predictive modeling")),
    # MLOps / DevOps / Cloud
    ("mlops", ("MLOps", "MLflow", "Docker")),
    ("devops et mlops", ("MLOps", "DevOps", "Docker", "Kubernetes")),
    ("cloud computing", ("Cloud", "AWS", "GCP", "Azure")),
    ("cloud et virtualisation", ("Cloud", "Docker", "virtualization")),
    ("conception des applications pour le cloud", ("Cloud", "AWS", "microservices")),
    # Big Data / Data Engineering
    ("calcul et architecture distribuee en big data", ("Apache Spark", "Hadoop", "big data")),
    ("calcul et architecture distribuée en big data", ("Apache Spark", "Hadoop", "big data")),
    ("ingenierie des donnees massives", ("Apache Spark", "Hadoop", "big data")),
    ("ingénierie des données massives", ("Apache Spark", "Hadoop", "big data")),
    ("fondamentaux du big data", ("Apache Spark", "Hadoop", "big data")),
    ("introduction au big data", ("Apache Spark", "Hadoop", "big data")),
    ("big data i", ("Apache Spark", "Hadoop", "big data", "NoSQL")),
    ("big data ii", ("Apache Spark", "Hadoop", "big data")),
    ("big data", ("Apache Spark", "Hadoop", "big data")),
    ("data analysis", ("data analysis", "Python", "pandas")),
    ("analyse de donnees", ("data analysis", "pandas")),
    ("analyse de données", ("data analysis", "pandas")),
    ("analyse et fouille de donnees", ("data mining", "pandas")),
    ("analyse et fouille de données", ("data mining", "pandas")),
    ("fouille de donnees", ("data mining",)),
    ("fouille de données", ("data mining",)),
    ("data mining", ("data mining",)),
    ("traitement et visualisation des donnees", ("data visualization", "matplotlib", "Plotly")),
    ("traitement et visualisation des données", ("data visualization", "matplotlib", "Plotly")),
    ("visualisation de donnees", ("data visualization", "Tableau", "Power BI")),
    ("visualisation de données", ("data visualization", "Tableau", "Power BI")),
    # Bases de donnees
    ("bases de donnees nosql et intro big data", ("NoSQL", "MongoDB", "big data")),
    ("bases de données nosql et intro big data", ("NoSQL", "MongoDB", "big data")),
    ("bases de donnees relationnelles", ("SQL", "PostgreSQL")),
    ("bases de données relationnelles", ("SQL", "PostgreSQL")),
    ("fondamentaux des bases de donnees", ("SQL", "PostgreSQL")),
    ("fondamentaux des bases de données", ("SQL", "PostgreSQL")),
    ("bases de donnees avancees", ("SQL", "PostgreSQL", "NoSQL")),
    ("bases de données avancées", ("SQL", "PostgreSQL", "NoSQL")),
    ("ingenierie des bases de donnees", ("SQL", "PostgreSQL")),
    ("ingénierie des bases de données", ("SQL", "PostgreSQL")),
    ("bases de donnees", ("SQL",)),
    ("bases de données", ("SQL",)),
    # BI / Decision
    ("business intelligence et datawarehouse", ("BI", "Power BI", "data warehouse")),
    ("business intelligence", ("BI", "Power BI")),
    ("informatique decisionnelle", ("BI", "Power BI")),
    ("informatique décisionnelle", ("BI", "Power BI")),
    # Stats / Maths
    ("statistique inferentielle", ("statistics", "hypothesis testing")),
    ("statistique inférentielle", ("statistics", "hypothesis testing")),
    ("statistique en grande dimension", ("statistics", "high-dimensional statistics")),
    ("series temporelles", ("time series", "ARIMA")),
    ("séries temporelles", ("time series", "ARIMA")),
    ("modelisation statistique", ("statistics", "regression")),
    ("modélisation statistique", ("statistics", "regression")),
    ("modelisations statistiques et mathematiques", ("statistics", "linear algebra")),
    ("modélisations statistiques et mathématiques", ("statistics", "linear algebra")),
    ("analyse stochastique", ("stochastic processes", "Bayesian")),
    ("optimisation stochastique", ("optimization", "stochastic processes")),
    ("modelisation stochastique", ("stochastic processes",)),
    ("modélisation stochastique", ("stochastic processes",)),
    ("probabilite avancee", ("probability", "statistics")),
    ("probabilité avancée", ("probability", "statistics")),
    ("algebre lineaire", ("linear algebra",)),
    ("algèbre linéaire", ("linear algebra",)),
    ("algebre pour ingenieur", ("linear algebra",)),
    ("algèbre pour ingénieur", ("linear algebra",)),
    ("analyse et algebre", ("linear algebra", "mathematical analysis")),
    ("analyse et algèbre", ("linear algebra", "mathematical analysis")),
    ("theorie de l'information", ("information theory",)),
    ("théorie de l'information", ("information theory",)),
    ("theorie des jeux", ("game theory",)),
    ("théorie des jeux", ("game theory",)),
    # Optimisation
    ("optimisation pour sciences des donnees", ("optimization",)),
    ("optimisation pour science des données", ("optimization",)),
    ("optimisation mathematique", ("optimization",)),
    ("optimisation mathématique", ("optimization",)),
    ("techniques d'optimisation avancees", ("optimization",)),
    ("techniques d'optimisation avancées", ("optimization",)),
    ("recherche operationnelle", ("operations research",)),
    ("recherche opérationnelle", ("operations research",)),
    ("methodes heuristiques", ("optimization", "heuristics")),
    ("méthodes heuristiques", ("optimization", "heuristics")),
    # Programmation
    ("python pour data science", ("Python", "pandas", "NumPy")),
    ("python pour la data science", ("Python", "pandas", "NumPy")),
    ("programmation poo python", ("Python", "OOP")),
    ("structures de donnees et python avance", ("Python", "data structures")),
    ("structures de données et python avancé", ("Python", "data structures")),
    ("structures de donnees et python", ("Python", "data structures")),
    ("structures de données et python", ("Python", "data structures")),
    ("structures de donnees et complexite algorithmique", ("data structures", "algorithms")),
    ("structures de données et complexité algorithmique", ("data structures", "algorithms")),
    ("programmation orientee objet c++", ("C++", "OOP")),
    ("programmation orientée objet c++", ("C++", "OOP")),
    ("programmation orientee objet java", ("Java", "OOP")),
    ("programmation orientée objet java", ("Java", "OOP")),
    ("programmation java avancee", ("Java", "OOP")),
    ("programmation java avancée", ("Java", "OOP")),
    ("java ee", ("Java", "Java EE")),
    ("langage de programmation java", ("Java", "OOP")),
    ("modelisation orientee objet", ("OOP", "UML")),
    ("modélisation orientée objet", ("OOP", "UML")),
    ("modelisation uml", ("UML",)),
    ("modélisation uml", ("UML",)),
    ("modelisation uml et genie logiciel", ("UML", "software engineering")),
    ("modélisation uml et génie logiciel", ("UML", "software engineering")),
    ("genie logiciel", ("software engineering",)),
    ("génie logiciel", ("software engineering",)),
    ("algorithmique avancee", ("algorithms",)),
    ("algorithmique avancée", ("algorithms",)),
    ("algorithmique et programmation", ("algorithms", "Python")),
    # Web et mobile
    ("developpement backend en js", ("JavaScript", "Node.js")),
    ("développement backend en js", ("JavaScript", "Node.js")),
    ("technologies js", ("JavaScript", "React", "Node.js")),
    ("developpement web dynamique", ("JavaScript", "React", "Node.js")),
    ("développement web dynamique", ("JavaScript", "React", "Node.js")),
    ("programmation web avancee", ("JavaScript", "Node.js", "React")),
    ("programmation web avancée", ("JavaScript", "Node.js", "React")),
    ("developpement web", ("HTML", "CSS", "JavaScript")),
    ("développement web", ("HTML", "CSS", "JavaScript")),
    ("programmation mobile et web", ("Flutter", "JavaScript")),
    ("programmation mobile", ("Flutter", "Android")),
    # IoT / Embedded / Hardware
    ("internet of things", ("IoT", "MQTT")),
    ("internet des objets", ("IoT", "MQTT")),
    ("systemes embarques", ("embedded systems", "C++")),
    ("systèmes embarqués", ("embedded systems", "C++")),
    # Securite
    ("securite des systemes d'information et technologie blockchain", ("cybersecurity", "blockchain")),
    ("sécurité des systèmes d'information et technologie blockchain", ("cybersecurity", "blockchain")),
    ("securite des systemes d'information", ("cybersecurity",)),
    ("sécurité des systèmes d'information", ("cybersecurity",)),
    ("introduction a la securite des reseaux", ("cybersecurity", "networking")),
    ("introduction à la sécurité des réseaux", ("cybersecurity", "networking")),
    ("cybersecurite", ("cybersecurity",)),
    ("cybersécurité", ("cybersecurity",)),
    ("securite", ("cybersecurity",)),
    ("sécurité", ("cybersecurity",)),
    # Reseau / Systemes
    ("principes fondamentaux des reseaux", ("networking", "TCP/IP")),
    ("principes fondamentaux des réseaux", ("networking", "TCP/IP")),
    ("reseaux et protocoles de communication", ("networking", "TCP/IP")),
    ("réseaux et protocoles de communication", ("networking", "TCP/IP")),
    ("reseaux informatiques", ("networking",)),
    ("réseaux informatiques", ("networking",)),
    ("administration systeme et reseau", ("Linux", "networking")),
    ("administration système et réseau", ("Linux", "networking")),
    ("systemes d'exploitation avances", ("Linux", "operating systems")),
    ("systèmes d'exploitation avancés", ("Linux", "operating systems")),
    ("systemes d'exploitation", ("Linux", "operating systems")),
    ("systèmes d'exploitation", ("Linux", "operating systems")),
    ("theorie et programmation systeme", ("C", "operating systems")),
    ("théorie et programmation système", ("C", "operating systems")),
    ("architecture des systemes", ("computer architecture",)),
    ("architecture des systèmes", ("computer architecture",)),
    ("systemes distribues", ("distributed systems",)),
    ("systèmes distribués", ("distributed systems",)),
    ("systemes temps reel", ("real-time systems",)),
    ("systèmes temps réel", ("real-time systems",)),
    # IA generale
    ("fondamentaux de l'intelligence artificielle", ("AI",)),
    ("applications de l'intelligence artificielle", ("AI",)),
    ("intelligence artificielle skills", ("AI",)),
    ("intelligence artificielle", ("AI",)),
    ("modelisation ia", ("AI", "Machine Learning")),
    ("modélisation ia", ("AI", "Machine Learning")),
    ("ia computer vision", ("AI", "computer vision")),
    ("ia en biomedical", ("AI", "healthcare AI")),
    ("ia en biomédical", ("AI", "healthcare AI")),
    ("ia en agriculture", ("AI", "agritech")),
    ("ia en milieu industriel", ("AI", "industrial AI")),
    ("ingenierie des connaissances et web semantique", ("knowledge graphs", "semantic web")),
    ("ingénierie des connaissances et web sémantique", ("knowledge graphs", "semantic web")),
    ("ingenierie des connaissances", ("knowledge graphs",)),
    ("ingénierie des connaissances", ("knowledge graphs",)),
    ("web semantique", ("semantic web", "RDF")),
    ("web sémantique", ("semantic web", "RDF")),
    # Agents / Recommander / Game theory
    ("systemes multiagents et blockchain", ("AI agents", "blockchain")),
    ("systèmes multiagents et blockchain", ("AI agents", "blockchain")),
    ("systemes multi-agents", ("AI agents",)),
    ("systèmes multi-agents", ("AI agents",)),
    ("systemes de recommandation", ("recommender systems",)),
    ("systèmes de recommandation", ("recommender systems",)),
    ("systemes intelligents flous", ("fuzzy logic",)),
    ("systèmes intelligents flous", ("fuzzy logic",)),
    # Blockchain
    ("fondamentaux de la blockchain", ("blockchain",)),
    ("blockchain", ("blockchain",)),
    # Web (analyse, scraping)
    ("analyse du web", ("web mining", "scraping")),
    # GIS / autres
    ("ingenierie digitale et donnees", ("data engineering",)),
    ("ingénierie digitale et données", ("data engineering",)),
    ("modelisation des donnees", ("data modeling",)),
    ("modélisation des données", ("data modeling",)),
    ("systemes d'informations et bases de donnees", ("information systems", "SQL")),
    ("systèmes d'informations et bases de données", ("information systems", "SQL")),
    ("systemes de gestion de contenu", ("CMS",)),
    ("systèmes de gestion de contenu", ("CMS",)),
    ("systemes d'information", ("information systems",)),
    ("systèmes d'information", ("information systems",)),
    ("architecture des systemes d'information", ("information systems", "SQL")),
    ("architecture des systèmes d'information", ("information systems", "SQL")),
    # Outils statistiques / R
    ("outils informatiques pour la statistique", ("R", "statistics")),
)


def _is_non_technical(module_name: str) -> bool:
    """Detecte les modules non techniques (langues, management, ethique, etc.)."""
    name_lower = module_name.lower()
    return any(needle in name_lower for needle in _NON_TECHNICAL_NEEDLES)


def _match_title_heuristics(module_name: str) -> set[str]:
    """Match le titre du module contre les heuristiques pre-definies."""
    name_lower = module_name.lower()
    matched: set[str] = set()
    for needle, skills in _TITLE_HEURISTICS:
        if needle in name_lower:
            matched.update(skills)
    return matched


def _match_family_keywords(module_name: str) -> set[str]:
    """Match le titre du module contre les mots-cles de la taxonomie SKILLNAV."""
    name_lower = module_name.lower()
    matched: set[str] = set()
    for keywords in _FAMILY_KEYWORDS.values():
        for kw in keywords:
            if kw in name_lower:
                matched.add(kw)
    return matched


def extract_skills_rules(module_name: str) -> list[str]:
    """Extraction deterministe d'un titre de module en skills canoniques.

    Pipeline :
    1. Applique d'abord les heuristiques de titre (NLP, ML, Deep Learning, ...).
       Si au moins une heuristique technique matche, on retourne ces skills
       (priorite forte : permet d'attraper "langues naturelles" -> NLP avant
       que le filtre 'langues' ne disqualifie le module).
    2. Sinon, si le titre est non technique (langues, management, ethique...) -> [].
    3. Sinon, applique les mots-cles de la taxonomie SKILLNAV en filet de secours.
    """
    title_skills = _match_title_heuristics(module_name)
    if title_skills:
        return sorted(title_skills)

    if _is_non_technical(module_name):
        return []

    return sorted(_match_family_keywords(module_name))


def extract_skills_batch_rules(module_names: Sequence[str]) -> list[list[str]]:
    """Version batch de extract_skills_rules (deterministe, sans I/O)."""
    return [extract_skills_rules(name) for name in module_names]
