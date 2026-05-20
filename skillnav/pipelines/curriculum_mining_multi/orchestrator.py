"""Orchestrateur du pipeline curriculum_mining.

Chaine de valeur : parser -> skill_extractor -> normalizer -> persistance JSON.

Modes d'extraction :
- llm   : Claude Sonnet 4.5 via pydantic-ai (necessite ANTHROPIC_API_KEY)
- rules : deterministe via heuristiques de titre + taxonomie SKILLNAV
- auto  : LLM si ANTHROPIC_API_KEY present, sinon rules

Sortie : data/curricula/<school_slug>.json (Pydantic model_dump_json).
"""

from __future__ import annotations

import asyncio
import logging
import os
from collections import Counter
from pathlib import Path
from typing import Literal

from skillnav.analysis.loaders import load_postings
from skillnav.pipelines.curriculum_mining_multi.normalizer import normalize_skills
from skillnav.pipelines.curriculum_mining_multi.parser import (
    list_available_schools,
    parse_filiere,
)
from skillnav.pipelines.curriculum_mining_multi.skill_extractor import (
    extract_skills_batch_rules,
    extract_skills_llm_batch,
)
from skillnav.schemas.curriculum_multi_ensa import CurriculumExtraction

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "curricula"

ExtractionMode = Literal["llm", "rules", "auto"]

_canonical_vocab_cache: list[str] | None = None


def _compute_canonical_vocab(top_n: int = 500) -> list[str]:
    """Agrege les top N skills marche depuis sources/collected/<src>/postings/."""
    counter: Counter[str] = Counter()
    for posting in load_postings():
        required = posting.get("skills_required") or []
        optional = posting.get("skills_optional") or []
        for raw in list(required) + list(optional):
            if isinstance(raw, str) and raw.strip():
                counter[raw.strip()] += 1
    return [name for name, _ in counter.most_common(top_n)]


def get_canonical_vocab(top_n: int = 500, force_reload: bool = False) -> list[str]:
    """Top N skills marche (cache memoire, recalcule si force_reload)."""
    global _canonical_vocab_cache
    if _canonical_vocab_cache is None or force_reload:
        _canonical_vocab_cache = _compute_canonical_vocab(top_n)
    return _canonical_vocab_cache


def _resolve_mode(mode: ExtractionMode) -> Literal["llm", "rules"]:
    """Resout 'auto' en 'llm' ou 'rules' selon disponibilite de la cle API."""
    if mode == "auto":
        return "llm" if os.environ.get("ANTHROPIC_API_KEY") else "rules"
    return mode


def _extract_skills_per_module(
    module_names: list[str],
    mode: Literal["llm", "rules"],
) -> list[list[str]]:
    """Dispatch vers la strategie d'extraction selon le mode resolu."""
    if not module_names:
        return []
    if mode == "llm":
        return asyncio.run(extract_skills_llm_batch(module_names))
    return extract_skills_batch_rules(module_names)


def run_curriculum_mining(
    school_slug: str,
    mode: ExtractionMode = "auto",
    output_dir: Path | None = None,
    canonical_vocab: list[str] | None = None,
) -> Path:
    """Pipeline complet pour une ENSA : parse -> extract -> normalize -> JSON.

    Args:
        school_slug: identifiant ENSA (ex: "ensa-tetouan-sdbia").
        mode: strategie d'extraction des skills.
        output_dir: dossier de sortie (defaut: data/curricula/).
        canonical_vocab: vocabulaire canonique pre-calcule pour la normalisation.
            Si None, calcule depuis load_postings() (top 500).

    Returns:
        Chemin du JSON produit.
    """
    out_dir = output_dir or DEFAULT_OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    resolved_mode = _resolve_mode(mode)
    logger.info("Pipeline curriculum_mining pour %s (mode=%s)", school_slug, resolved_mode)

    curriculum = parse_filiere(school_slug)
    module_names = [m.name for s in curriculum.semesters for m in s.modules]

    if not module_names:
        logger.info(
            "Aucun module exploitable pour %s (statut=%s) - JSON vide produit",
            school_slug,
            curriculum.status.value,
        )
        return _persist_curriculum(curriculum, out_dir)

    raw_skill_lists = _extract_skills_per_module(module_names, resolved_mode)
    _assign_skills_to_modules(curriculum, raw_skill_lists)

    vocab = canonical_vocab if canonical_vocab is not None else get_canonical_vocab()
    all_skills = [s for sl in raw_skill_lists for s in sl]
    curriculum.skills_taught = normalize_skills(all_skills, vocab)

    return _persist_curriculum(curriculum, out_dir)


def _assign_skills_to_modules(
    curriculum: CurriculumExtraction,
    skill_lists: list[list[str]],
) -> None:
    """Aplatit les listes de skills sur les modules dans l'ordre du parsing."""
    idx = 0
    for semester in curriculum.semesters:
        for module in semester.modules:
            if idx < len(skill_lists):
                module.skills = skill_lists[idx]
            idx += 1


def _persist_curriculum(curriculum: CurriculumExtraction, output_dir: Path) -> Path:
    """Persiste le CurriculumExtraction en JSON et retourne le path."""
    out_path = output_dir / f"{curriculum.school_id}.json"
    out_path.write_text(curriculum.model_dump_json(indent=2), encoding="utf-8")
    return out_path


def run_all_schools(
    mode: ExtractionMode = "auto",
    output_dir: Path | None = None,
) -> dict[str, Path]:
    """Execute le pipeline sur toutes les ENSA presentes dans sources/curricula/."""
    vocab = get_canonical_vocab()
    paths: dict[str, Path] = {}
    for slug in list_available_schools():
        paths[slug] = run_curriculum_mining(
            slug,
            mode=mode,
            output_dir=output_dir,
            canonical_vocab=vocab,
        )
    return paths
