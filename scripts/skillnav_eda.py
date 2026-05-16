"""Module utilitaire pour les notebooks EDA et visualisation SKILLNAV.

Centralise toute la plomberie partagée par les notebooks :

- Constantes : mappings FR (`FAMILLES_FR`, `TYPES_FR`, `FAMILY_FR`),
  alias compétences (`SKILL_ALIASES`), alias titres (`TITLE_ALIASES`),
  patterns famille de poste (`JOB_FAMILY_PATTERNS`)
- Canonicalisation : `canonicaliser_skill`, `canonicaliser_liste`,
  `canonicaliser_titre`, `detecter_famille_poste`
- Chargement : `charger_corpus()` -> `(df_maroc, df_international)`
- Contrôle qualité : `controle_qualite(df_maroc, df_international)`
- Helpers d'analyse : `comptage_skills`, `jobs_avec_skill`,
  `all_skills_lower`, `afficher_top_skills`, `top_skills_global`
- Fonctions de section pour notebook 00 : `section_vue_ensemble`,
  `section_distribution_type`, `section_top_entreprises`,
  `section_top_titres`, `section_competences_par_famille`,
  `section_frameworks_genai`, `section_recherche_vs_applied`
- Style viz : `configurer_style()`, `sauver_figure()`, `titrer()`,
  constantes de couleurs

Usage dans un notebook (3 lignes) :

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path.cwd().parent / 'scripts'))
    from skillnav_eda import *

    df_maroc, df_international = charger_corpus()
    FIGURES_DIR = configurer_style()
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================================
# MAPPINGS FR
# ============================================================================
FAMILLES_FR = {
    'genai':     'IA générative',
    'ml':        'Machine Learning',
    'web':       'Web & APIs',
    'databases': 'Bases de données',
    'data':      'Data Engineering',
    'cloud':     'Cloud',
    'ops':       'Ops & MLOps',
    'languages': 'Langages',
    'domains':   'Domaines',
    'other':     'Autres',
}

TYPES_FR = {
    'ai-first':   'AI-First',
    'ai-support': 'AI-Support',
    'ml-first':   'ML-First',
    'non-ai':     'Data Analytics',
    'unknown':    'Inconnu',
}

FAMILY_FR = {
    'DATA_ANALYST':       'Data Analyst',
    'BUSINESS_ANALYST':   'Business Analyst',
    'DATA_SCIENTIST':     'Data Scientist',
    'DATA_ENGINEER':      'Data Engineer',
    'DATA_ARCHITECT':     'Data Architect',
    'ML_ENGINEER':        'ML Engineer',
    'MLOPS_ENGINEER':     'MLOps Engineer',
    'AI_ENGINEER':        'AI Engineer',
    'NLP_ENGINEER':       'NLP Engineer',
    'CV_ENGINEER':        'CV Engineer (Computer Vision)',
    'RESEARCH_SCIENTIST': 'Research Scientist',
    'GENAI_LLM_ENGINEER': 'GenAI / LLM Engineer',
    'OTHER':              'Autre',
    'UNKNOWN':            'Non détecté',
}

SKILL_FAMILIES = list(FAMILLES_FR.keys())
SKILL_COLS = [f'skills_{f}' for f in SKILL_FAMILIES]

# ============================================================================
# ALIAS COMPETENCES (~190 entrées)
# ============================================================================
SKILL_ALIASES = {
    # IA générative
    'llm': 'LLM', 'llms': 'LLM', 'large language model': 'LLM', 'large language models': 'LLM',
    'genai': 'GenAI', 'gen ai': 'GenAI', 'gen-ai': 'GenAI',
    'generative ai': 'GenAI', 'generative-ai': 'GenAI',
    'rag': 'RAG', 'retrieval augmented generation': 'RAG', 'retrieval-augmented generation': 'RAG',
    'retrieval augmented': 'RAG', 'retrieval-augmented': 'RAG',
    'prompt engineering': 'Prompt Engineering', 'prompt-engineering': 'Prompt Engineering',
    'prompt eng': 'Prompt Engineering',
    'fine-tuning': 'Fine-tuning', 'fine tuning': 'Fine-tuning', 'finetuning': 'Fine-tuning',
    'agent': 'Agents', 'agents': 'Agents', 'ai agent': 'Agents', 'ai agents': 'Agents',
    'agentic': 'Agents', 'agentic ai': 'Agents', 'agentic workflows': 'Agents',
    'embedding': 'Embeddings', 'embeddings': 'Embeddings',
    'vector embedding': 'Embeddings', 'vector embeddings': 'Embeddings',
    'langchain': 'LangChain', 'lang chain': 'LangChain',
    'langgraph': 'LangGraph', 'lang graph': 'LangGraph',
    'llamaindex': 'LlamaIndex', 'llama index': 'LlamaIndex', 'llama-index': 'LlamaIndex',
    'crewai': 'CrewAI', 'crew ai': 'CrewAI',
    'autogen': 'AutoGen', 'auto-gen': 'AutoGen',
    'mcp': 'MCP', 'model context protocol': 'MCP', 'mcp server': 'MCP',
    'openai api': 'OpenAI API', 'openai': 'OpenAI',
    'anthropic api': 'Anthropic API', 'anthropic': 'Anthropic', 'claude': 'Claude',
    'gpt': 'GPT', 'gpt-4': 'GPT-4', 'gpt-4o': 'GPT-4o',

    # ML/DL
    'ml': 'Machine Learning', 'machine learning': 'Machine Learning', 'machine-learning': 'Machine Learning',
    'dl': 'Deep Learning', 'deep learning': 'Deep Learning', 'deep-learning': 'Deep Learning',
    'neural network': 'Neural Networks', 'neural networks': 'Neural Networks',
    'rl': 'Reinforcement Learning', 'reinforcement learning': 'Reinforcement Learning',
    'nlp': 'NLP', 'natural language processing': 'NLP',
    'cv': 'Computer Vision', 'computer vision': 'Computer Vision',
    'tts': 'TTS', 'text-to-speech': 'TTS', 'text to speech': 'TTS',

    # Frameworks ML/DL
    'pytorch': 'PyTorch', 'torch': 'PyTorch',
    'tensorflow': 'TensorFlow', 'tf': 'TensorFlow',
    'sklearn': 'scikit-learn', 'scikit-learn': 'scikit-learn', 'scikit learn': 'scikit-learn',
    'huggingface': 'HuggingFace', 'hugging face': 'HuggingFace',
    'transformers': 'Transformers', 'transformer': 'Transformers',
    'xgboost': 'XGBoost', 'lightgbm': 'LightGBM',
    'keras': 'Keras', 'jax': 'JAX', 'numpy': 'NumPy', 'pandas': 'Pandas',
    'opencv': 'OpenCV', 'spacy': 'spaCy', 'nltk': 'NLTK',

    # Cloud / Ops / DB / Web / Langues / Data / BI
    'aws': 'AWS', 'amazon web services': 'AWS',
    'gcp': 'GCP', 'google cloud': 'GCP', 'google cloud platform': 'GCP',
    'azure': 'Azure', 'microsoft azure': 'Azure',
    'k8s': 'Kubernetes', 'kubernetes': 'Kubernetes', 'docker': 'Docker',
    'ci/cd': 'CI/CD', 'ci-cd': 'CI/CD', 'cicd': 'CI/CD', 'continuous integration': 'CI/CD',
    'mlops': 'MLOps', 'terraform': 'Terraform',
    'postgresql': 'PostgreSQL', 'postgres': 'PostgreSQL',
    'mongodb': 'MongoDB', 'mongo': 'MongoDB',
    'redis': 'Redis', 'mysql': 'MySQL', 'oracle': 'Oracle', 'snowflake': 'Snowflake',
    'pgvector': 'pgvector',
    'react': 'React', 'reactjs': 'React', 'react.js': 'React',
    'nextjs': 'Next.js', 'next.js': 'Next.js', 'next js': 'Next.js',
    'fastapi': 'FastAPI', 'flask': 'Flask', 'django': 'Django',
    'api': 'APIs', 'apis': 'APIs',
    'rest': 'REST APIs', 'rest api': 'REST APIs', 'rest apis': 'REST APIs',
    'restful': 'REST APIs', 'restful api': 'REST APIs', 'restful apis': 'REST APIs',
    'python': 'Python', 'python3': 'Python',
    'typescript': 'TypeScript', 'ts': 'TypeScript',
    'javascript': 'JavaScript', 'js': 'JavaScript',
    'go': 'Go', 'golang': 'Go',
    'sql': 'SQL', 'java': 'Java',
    'c++': 'C++', 'cpp': 'C++', 'c#': 'C#',
    'rust': 'Rust', 'scala': 'Scala', 'r': 'R',
    'etl': 'ETL', 'airflow': 'Airflow', 'apache airflow': 'Airflow',
    'spark': 'Spark', 'apache spark': 'Spark',
    'kafka': 'Kafka', 'apache kafka': 'Kafka',
    'databricks': 'Databricks',
    'power bi': 'Power BI', 'powerbi': 'Power BI',
    'tableau': 'Tableau',
    'excel': 'Excel', 'microsoft excel': 'Excel',
    'looker': 'Looker',

    # Concepts / archi
    'multi-agent systems': 'Multi-Agent Systems', 'multi agent systems': 'Multi-Agent Systems',
    'multi-agent system': 'Multi-Agent Systems',
    'multi-agent orchestration': 'Multi-Agent Orchestration', 'multi agent orchestration': 'Multi-Agent Orchestration',
    'full-stack development': 'Full-Stack Development', 'full stack development': 'Full-Stack Development',
    'fullstack development': 'Full-Stack Development', 'full-stack': 'Full-Stack', 'full stack': 'Full-Stack',
    'cloud-native architectures': 'Cloud-Native Architectures', 'cloud native architectures': 'Cloud-Native Architectures',
    'cloud-native architecture': 'Cloud-Native Architecture', 'cloud native architecture': 'Cloud-Native Architecture',
    'event-driven systems': 'Event-Driven Systems', 'event driven systems': 'Event-Driven Systems',
    'event-driven': 'Event-Driven',
    'data warehouse': 'Data Warehouse', 'data warehousing': 'Data Warehousing',
    'data lake': 'Data Lake', 'data lakes': 'Data Lake', 'data lakehouse': 'Data Lakehouse',
    'data pipelines': 'Data Pipelines', 'data pipeline': 'Data Pipelines',
    'data engineering': 'Data Engineering',
    'function calling': 'Function Calling', 'function-calling': 'Function Calling', 'function calls': 'Function Calling',
    'model deployment': 'Model Deployment', 'model evaluation': 'Model Evaluation', 'model training': 'Model Training',
    'model fine-tuning': 'Fine-tuning', 'model finetuning': 'Fine-tuning',
    'distributed systems': 'Distributed Systems',
    'vector database': 'Vector Databases', 'vector databases': 'Vector Databases', 'vector db': 'Vector Databases',
    'microservices': 'Microservices', 'micro-services': 'Microservices', 'micro services': 'Microservices',
    'observability': 'Observability', 'monitoring': 'Monitoring', 'statistics': 'Statistics',
    'agile': 'Agile', 'agile methodology': 'Agile', 'agile methodologies': 'Agile',
    'scrum': 'Scrum', 'kanban': 'Kanban',
    'production ml': 'Production ML', 'production-ml': 'Production ML',
}

# ============================================================================
# CANONICALISATION
# ============================================================================
def canonicaliser_skill(skill) -> str:
    """Renvoie la forme canonique d'une compétence."""
    if not isinstance(skill, str):
        return ''
    s = skill.strip()
    if not s:
        return ''
    return SKILL_ALIASES.get(s.lower(), s)


def canonicaliser_liste(skills) -> list:
    """Canonicalise et dédoublonne (case-insensitive) une liste de compétences."""
    if not isinstance(skills, list):
        return []
    sortie: list = []
    vues: set = set()
    for s in skills:
        c = canonicaliser_skill(s)
        if not c:
            continue
        cl = c.lower()
        if cl in vues:
            continue
        vues.add(cl)
        sortie.append(c)
    return sortie


# ---- Canonicalisation des titres de poste ----
TITLE_ALIASES = {
    'data scientist': 'Data Scientist',
    'data analyst': 'Data Analyst',
    'data engineer': 'Data Engineer',
    'data architect': 'Data Architect',
    'business analyst': 'Business Analyst',
    'business intelligence analyst': 'BI Analyst',
    'bi analyst': 'BI Analyst',
    'ml engineer': 'ML Engineer',
    'machine learning engineer': 'ML Engineer',
    'mlops engineer': 'MLOps Engineer',
    'ai engineer': 'AI Engineer',
    'applied ai engineer': 'Applied AI Engineer',
    'ai software engineer': 'AI Software Engineer',
    'ai platform engineer': 'AI Platform Engineer',
    'ai solutions engineer': 'AI Solutions Engineer',
    'genai engineer': 'GenAI Engineer',
    'llm engineer': 'LLM Engineer',
    'nlp engineer': 'NLP Engineer',
    'computer vision engineer': 'Computer Vision Engineer',
    'cv engineer': 'Computer Vision Engineer',
    'research scientist': 'Research Scientist',
    'research engineer': 'Research Engineer',
    'applied scientist': 'Applied Scientist',
    'prompt engineer': 'Prompt Engineer',
    'devops engineer': 'DevOps Engineer',
    'software engineer': 'Software Engineer',
    'backend engineer': 'Backend Engineer',
    'frontend engineer': 'Frontend Engineer',
    'full stack engineer': 'Full-Stack Engineer',
    'fullstack engineer': 'Full-Stack Engineer',
    'full-stack engineer': 'Full-Stack Engineer',
}

_GENDER_PATTERNS = [
    re.compile(r'\s*\(\s*m\s*/\s*w\s*/\s*d\s*\)\s*$', re.I),
    re.compile(r'\s*\(\s*m\s*/\s*f\s*/\s*x\s*\)\s*$', re.I),
    re.compile(r'\s*\(\s*h\s*/\s*f\s*\)\s*$', re.I),
    re.compile(r'\s*\(\s*f\s*/\s*h\s*\)\s*$', re.I),
    re.compile(r'\s*\(\s*m\s*/\s*f\s*\)\s*$', re.I),
    re.compile(r'\s*\(\s*f\s*/\s*m\s*\)\s*$', re.I),
    re.compile(r'\s+h\s*/\s*f\s*$', re.I),
    re.compile(r'\s+f\s*/\s*h\s*$', re.I),
    re.compile(r'\s+m\s*/\s*f\s*$', re.I),
    re.compile(r'\s+f\s*/\s*m\s*$', re.I),
    re.compile(r'\s+hf\s*$', re.I),
    re.compile(r'\s+fh\s*$', re.I),
]

_ACRONYMS = {'AI', 'ML', 'BI', 'NLP', 'CV', 'LLM', 'RAG', 'API', 'APIs', 'SQL',
             'GCP', 'AWS', 'ETL', 'ELT', 'KPI', 'ERP', 'CRM', 'SaaS', 'PaaS',
             'IaaS', 'GenAI', 'MLOps', 'DevOps', 'iOS', 'TTS'}

_STOPWORDS = {'and', 'or', 'of', 'for', 'to', 'in', 'the', 'a', 'an', 'on', 'at', 'with'}


def _strip_gender_suffix(title: str) -> str:
    for pat in _GENDER_PATTERNS:
        title = pat.sub('', title)
    return title.strip()


def _smart_title_case(title: str) -> str:
    """Title-case en préservant les acronymes IA/ML/SaaS/etc."""
    if not title:
        return title
    out = []
    for i, mot in enumerate(title.split()):
        if not mot:
            continue
        upper = mot.upper()
        lower = mot.lower()
        if upper in _ACRONYMS:
            out.append(upper)
        elif lower == 'mlops':
            out.append('MLOps')
        elif lower == 'devops':
            out.append('DevOps')
        elif lower == 'genai':
            out.append('GenAI')
        elif lower == 'ios':
            out.append('iOS')
        elif lower in _STOPWORDS and i > 0:
            out.append(lower)
        else:
            out.append(mot[:1].upper() + mot[1:])
    return ' '.join(out)


def canonicaliser_titre(titre) -> str:
    """Strip suffixes genre + lookup alias + Title Case smart."""
    if not isinstance(titre, str):
        return ''
    s = titre.strip()
    if not s:
        return ''
    s = _strip_gender_suffix(s)
    if not s:
        return ''
    cle = s.lower()
    if cle in TITLE_ALIASES:
        return TITLE_ALIASES[cle]
    return _smart_title_case(s)


JOB_FAMILY_PATTERNS = [
    ('GENAI_LLM_ENGINEER', re.compile(r'\b(genai|gen ai|generative ai engineer|llm engineer|prompt engineer)\b', re.I)),
    ('MLOPS_ENGINEER',     re.compile(r'\b(mlops|ml ops|ml platform|ml infrastructure|ai platform|ai infrastructure)\b', re.I)),
    ('CV_ENGINEER',        re.compile(r'\b(computer vision|cv engineer|vision engineer)\b', re.I)),
    ('NLP_ENGINEER',       re.compile(r'\b(nlp engineer|natural language|nlp/llm)\b', re.I)),
    ('RESEARCH_SCIENTIST', re.compile(r'\b(research scientist|research engineer|applied scientist|chercheur)\b', re.I)),
    ('AI_ENGINEER',        re.compile(r'\b(ai engineer|applied ai|ai software|ai/ml engineer|ai product engineer|ai full[- ]stack|ai full[- ]?stack)\b', re.I)),
    ('ML_ENGINEER',        re.compile(r'\b(machine learning engineer|ml engineer|deep learning engineer|machine learning|ingenieur ml)\b', re.I)),
    ('DATA_SCIENTIST',     re.compile(r'\b(data scientist|datascientist|scientifique des donn)\b', re.I)),
    ('DATA_ENGINEER',      re.compile(r'\b(data engineer|etl engineer|data platform engineer|big data engineer|ingenieur data)\b', re.I)),
    ('DATA_ARCHITECT',     re.compile(r'\b(data architect|architecte data|architecte big data|architecte donn)\b', re.I)),
    ('BUSINESS_ANALYST',   re.compile(r'\b(business analyst|analyste fonctionnel)\b', re.I)),
    ('DATA_ANALYST',       re.compile(r'\b(data analyst|analyste de donn|bi analyst|business intelligence analyst|reporting analyst|analytics engineer|web data)\b', re.I)),
]


def detecter_famille_poste(titre) -> str:
    if not isinstance(titre, str) or not titre.strip():
        return 'UNKNOWN'
    for famille, pat in JOB_FAMILY_PATTERNS:
        if pat.search(titre):
            return famille
    return 'OTHER'


# ============================================================================
# CHARGEMENT DU CORPUS
# ============================================================================
def _detect_repo() -> Path:
    """Détecte la racine du repo en remontant jusqu'au premier pyproject.toml.

    Fonctionne depuis n'importe quel sous-dossier : notebooks/, scripts/,
    racine, etc.
    """
    candidat = Path.cwd().resolve()
    for parent in [candidat, *candidat.parents]:
        if (parent / "pyproject.toml").exists() or (parent / "sources").is_dir():
            return parent
    return candidat


def load_corpus(racines: list, origine: str) -> pd.DataFrame:
    """Charge tous les YAML data_structured/ et applique les 3 canonicalisations."""
    records: list = []
    erreurs = 0
    for racine in racines:
        if not racine.exists():
            print(f'  [!] Racine absente : {racine}')
            continue
        for fichier in racine.rglob('*.yaml'):
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    job = yaml.safe_load(f) or {}
                pos = job.get('position') or {}
                comp = job.get('company') or {}
                meta = job.get('meta') or {}
                skills = pos.get('skills') or {}
                ai_type_info = pos.get('ai_type') or {}
                rel = fichier.relative_to(racine.parent.parent)
                source = rel.parts[0]
                posted_month = fichier.parent.name
                titre_brut = pos.get('title') or ''
                rec = {
                    'origine': origine,
                    'source': source,
                    'posted_month': posted_month,
                    'job_id': meta.get('job_id', ''),
                    'company': comp.get('name') or '',
                    'stage': comp.get('stage') or '',
                    'focus': comp.get('focus') or '',
                    'title': titre_brut,
                    'title_canonical': canonicaliser_titre(titre_brut),
                    'job_family': detecter_famille_poste(titre_brut),
                    'ai_type': ai_type_info.get('type', 'unknown'),
                    'is_customer_facing': bool(pos.get('is_customer_facing', False)),
                    'is_management': bool(pos.get('is_management', False)),
                    'responsibilities': pos.get('responsibilities') or [],
                    'use_cases': comp.get('use_cases') or pos.get('use_cases') or [],
                }
                for famille in SKILL_FAMILIES:
                    rec[f'skills_{famille}'] = canonicaliser_liste(skills.get(famille) or [])
                records.append(rec)
            except Exception as exc:
                erreurs += 1
                if erreurs <= 3:
                    print(f'  [!] Erreur lecture {fichier} : {exc}')
    df = pd.DataFrame(records)
    cols_listes = [c for c in df.columns if c.startswith('skills_')] + ['responsibilities', 'use_cases']
    for col in cols_listes:
        df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])
    if erreurs:
        print(f'  >>> {erreurs} fichier(s) en erreur ignoré(s)')
    return df


MA_SOURCES = ['anapec', 'glassdoor-ma', 'indeed-ma', 'linkedin-ma', 'pages-carrieres-ma', 'rekrute']


def charger_corpus(verbose: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Charge les corpus Maroc et International. Affiche un résumé.

    Returns
    -------
    (df_maroc, df_international) : DataFrames pandas avec colonnes canonicalisées.
    """
    REPO = _detect_repo()
    ma_racines = [REPO / 'sources' / 'collected' / s / 'data_structured' for s in MA_SOURCES]
    intl_racines = [REPO / 'sources' / 'collected' / 'intl-ai-corpus' / 'data_structured']

    df_maroc = load_corpus(ma_racines, origine='Maroc')
    df_international = load_corpus(intl_racines, origine='International')

    if verbose:
        print(f'Corpus chargé : {len(df_maroc)} fiches Maroc + {len(df_international)} fiches International '
              f'= {len(df_maroc) + len(df_international)} total.')
    return df_maroc, df_international


# ============================================================================
# CONTROLE QUALITE
# ============================================================================
def _toutes_skills_du_corpus(df: pd.DataFrame) -> Counter:
    c = Counter()
    for col in SKILL_COLS:
        for liste in df[col]:
            for s in liste:
                if isinstance(s, str):
                    c[s] += 1
    return c


def controle_qualite(df_maroc: pd.DataFrame, df_international: pd.DataFrame, verbose: bool = False) -> None:
    """Vérifie qu'aucune compétence du top 100 n'a plusieurs casses.

    Lève AssertionError si un doublon résiduel est détecté. Le notebook 00
    peut appeler cette fonction silencieusement (verbose=False) ou avec
    affichage du top 30 (verbose=True).
    """
    combine = pd.concat([df_maroc, df_international], ignore_index=True)
    skills_globales = _toutes_skills_du_corpus(combine)

    if verbose:
        print('Top 30 compétences globales (MA + INTL) :\n')
        for s, n in skills_globales.most_common(30):
            print(f'  {s:<32} {n}')

    top100 = [s for s, _ in skills_globales.most_common(100)]
    groupes: dict = {}
    for s in top100:
        groupes.setdefault(s.lower(), []).append(s)
    doublons = {low: v for low, v in groupes.items() if len(v) > 1}
    if doublons:
        raise AssertionError(f'{len(doublons)} doublon(s) skill résiduel(s) : {doublons}')

    titres_ma = df_maroc['title_canonical'].value_counts().head(30).index.tolist()
    titres_intl = df_international['title_canonical'].value_counts().head(30).index.tolist()
    all_titres = list(set(titres_ma + titres_intl))
    groupes_t: dict = {}
    for t in all_titres:
        groupes_t.setdefault(t.lower(), []).append(t)
    doublons_t = {low: v for low, v in groupes_t.items() if len(v) > 1}
    if doublons_t:
        raise AssertionError(f'{len(doublons_t)} doublon(s) titre résiduel(s) : {doublons_t}')

    print('Contrôle qualité OK : aucun doublon dans le top 100 compétences ni top 30 titres.')


# ============================================================================
# HELPERS D'ANALYSE
# ============================================================================
def comptage_skills(df_sub: pd.DataFrame, colonne: str) -> pd.Series:
    return df_sub[colonne].explode().dropna().value_counts()


def all_skills_lower(row: pd.Series) -> list:
    out = []
    for col in SKILL_COLS:
        if isinstance(row[col], list):
            out.extend(s.lower() for s in row[col] if isinstance(s, str))
    return out


def jobs_avec_skill(df_sub: pd.DataFrame, skill: str) -> int:
    skill_lower = skill.lower()
    mask = df_sub.apply(
        lambda row: any(skill_lower in s for s in all_skills_lower(row)),
        axis=1,
    )
    return int(mask.sum())


def afficher_top_skills(df_sub: pd.DataFrame, famille: str, top: int = 10, libelle: str = '') -> pd.DataFrame:
    serie = comptage_skills(df_sub, f'skills_{famille}').head(top)
    n = len(df_sub)
    if serie.empty:
        print(f'  (aucune compétence référencée pour la famille « {FAMILLES_FR[famille]} »)')
        return pd.DataFrame(columns=['Offres', '% du corpus'])
    tableau = pd.DataFrame({
        'Offres': serie.astype(int),
        '% du corpus': (serie / n * 100).round(1),
    })
    tableau.index.name = f'{FAMILLES_FR[famille]}' + (f' ({libelle})' if libelle else '')
    return tableau


def top_skills_global(df: pd.DataFrame, top: int = 30) -> pd.Series:
    total = Counter()
    for col in SKILL_COLS:
        for liste in df[col]:
            for s in liste:
                if isinstance(s, str):
                    total[s] += 1
    return pd.Series(total).sort_values(ascending=False).head(top)


# ============================================================================
# FONCTIONS DE SECTION (pour notebook 00)
# ============================================================================
def section_vue_ensemble(df: pd.DataFrame, libelle: str) -> None:
    print(f"=== Vue d'ensemble ({libelle}) ===")
    print(f'Fiches totales : {len(df)}')
    print(f'Sources distinctes : {df["source"].nunique()} ({", ".join(sorted(df["source"].unique()))})')
    if (df['posted_month'] != '').any():
        mois = sorted(m for m in df['posted_month'].unique() if m and m != 'data_structured')
        if mois:
            print(f'Période couverte : {mois[0]} -> {mois[-1]} ({len(mois)} mois distincts)')
    print(f'Entreprises distinctes : {df["company"].nunique()}')
    print(f'Postes managériaux (lead, head, director, manager) : {df["is_management"].sum()} ({df["is_management"].mean()*100:.1f} %)')
    print(f"Postes à interface client (sales, customer success, solutions eng.) : {df['is_customer_facing'].sum()} ({df['is_customer_facing'].mean()*100:.1f} %)")


def section_distribution_type(df: pd.DataFrame, libelle: str) -> pd.DataFrame:
    counts = df['ai_type'].value_counts()
    tableau = pd.DataFrame({
        'Offres': counts,
        '% du corpus': (counts / len(df) * 100).round(1),
    })
    tableau.index = [TYPES_FR.get(t, t) for t in tableau.index]
    tableau.index.name = f'Type de poste ({libelle})'
    return tableau


def section_top_entreprises(df: pd.DataFrame, libelle: str, top: int = 15) -> pd.DataFrame:
    counts = df[df['company'] != '']['company'].value_counts().head(top)
    tableau = pd.DataFrame({'Offres': counts})
    tableau.index.name = f'Top {top} employeurs ({libelle})'
    return tableau


def section_top_titres(df: pd.DataFrame, libelle: str, top: int = 10) -> pd.DataFrame:
    counts = df[df['title_canonical'] != '']['title_canonical'].value_counts().head(top)
    tableau = pd.DataFrame({'Offres': counts})
    tableau.index.name = f'Top {top} intitulés de poste ({libelle})'
    return tableau


def section_competences_par_famille(df: pd.DataFrame, libelle: str, top: int = 8) -> None:
    print(f'=== Top {top} compétences par famille ({libelle}) ===\n')
    for famille in SKILL_FAMILIES:
        tab = afficher_top_skills(df, famille, top=top, libelle=libelle)
        if not tab.empty:
            print(f'>> {FAMILLES_FR[famille]} <<')
            print(tab.to_string())
            print()


def section_frameworks_genai(df: pd.DataFrame, libelle: str) -> pd.DataFrame:
    frameworks = ['LangChain', 'LangGraph', 'LlamaIndex', 'CrewAI', 'AutoGen', 'Haystack', 'Semantic Kernel']
    genai_all = comptage_skills(df, 'skills_genai')
    fw = genai_all[genai_all.index.isin(frameworks)].reindex(frameworks).fillna(0).astype(int)
    fw = fw[fw > 0]
    if fw.empty:
        print(f'  (aucun framework GenAI majeur référencé sur le corpus {libelle})')
        return pd.DataFrame()
    return pd.DataFrame({
        'Offres': fw,
        '% du corpus': (fw / len(df) * 100).round(1),
    }).rename_axis(f'Framework GenAI ({libelle})')


def section_recherche_vs_applied(df: pd.DataFrame, libelle: str) -> pd.DataFrame:
    indicateurs_recherche = ['research', 'scientist', 'publication', 'paper', 'novel', 'algorithm',
                             'state of the art', 'sota', 'reinforcement learning', 'world model']
    indicateurs_applied = ['production', 'deploy', 'shipping', 'product', 'customer', 'enterprise',
                           'api integration', 'apply', 'implement']

    def est_recherche(row: pd.Series) -> bool:
        titre = (row['title'] or '').lower()
        resp = ' '.join(row['responsibilities']).lower()
        use_cases = ' '.join(row['use_cases']).lower()
        if any(kw in titre for kw in ['research engineer', 'research scientist', 'scientist']):
            return True
        texte = f'{resp} {use_cases}'
        score_r = sum(1 for kw in indicateurs_recherche if kw in texte)
        score_a = sum(1 for kw in indicateurs_applied if kw in texte)
        return score_r > score_a and score_r >= 2

    n_recherche = int(df.apply(est_recherche, axis=1).sum())
    n_applied = len(df) - n_recherche
    return pd.DataFrame({
        'Offres': [n_recherche, n_applied],
        '% du corpus': [
            round(n_recherche / len(df) * 100, 1),
            round(n_applied / len(df) * 100, 1),
        ],
    }, index=pd.Index(['Recherche', 'Application/Production'], name=f'Orientation ({libelle})'))


# ============================================================================
# STYLE VIZ
# ============================================================================
COULEUR_MAROC      = '#1565C0'
COULEUR_INTL       = '#EF6C00'
COULEUR_NEUTRE     = '#616161'
COULEUR_ACCENT     = '#2E7D32'
COULEUR_ALERT      = '#C62828'
COULEUR_FOND_GRID  = '#E0E0E0'


def configurer_style() -> Path:
    """Configure matplotlib pour les figures SKILLNAV et crée docs/figures/.

    Returns
    -------
    Path : dossier docs/figures/ où les PNG seront exportés.
    """
    plt.rcParams.update({
        'font.family':      'sans-serif',
        'font.size':         11,
        'axes.titlesize':    14,
        'axes.titleweight':  'bold',
        'axes.labelsize':    11,
        'axes.spines.top':   False,
        'axes.spines.right': False,
        'axes.grid':         True,
        'grid.color':        COULEUR_FOND_GRID,
        'grid.alpha':        0.6,
        'grid.linestyle':    '--',
        'figure.dpi':        100,
        'savefig.dpi':       150,
        'savefig.bbox':      'tight',
        'savefig.facecolor': 'white',
    })
    REPO = _detect_repo()
    figures_dir = REPO / 'docs' / 'figures'
    figures_dir.mkdir(parents=True, exist_ok=True)
    print(f'Style matplotlib configuré. Export PNG vers : {figures_dir.relative_to(REPO)}')
    return figures_dir


def sauver_figure(fig, nom_fichier: str, dossier: Path | None = None) -> None:
    """Sauve une figure en PNG dans docs/figures/ avec DPI 150 et fond blanc."""
    if dossier is None:
        dossier = _detect_repo() / 'docs' / 'figures'
    chemin = dossier / nom_fichier
    fig.savefig(chemin, dpi=150, bbox_inches='tight', facecolor='white')
    repo = _detect_repo()
    try:
        rel = chemin.relative_to(repo)
        print(f'  PNG sauvé : {rel}')
    except ValueError:
        print(f'  PNG sauvé : {chemin}')


def titrer(ax, titre: str, sous_titre: str = '') -> None:
    """Pose un titre + sous-titre interprétatif sur un axe matplotlib."""
    if sous_titre:
        ax.set_title(f'{titre}\n{sous_titre}', fontsize=14, fontweight='bold', loc='left', pad=12)
    else:
        ax.set_title(titre, fontsize=14, fontweight='bold', loc='left', pad=12)
