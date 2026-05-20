"""Normalisation taxonomique des competences enseignees.

Pipeline aval de skill_extractor : reduit la variabilite lexicale en alignant
les skills extraites sur le vocabulaire canonique issu du marche (top N skills
par occurrence dans les postings SKILLNAV).

Methode :
- Embeddings sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`)
- Cosine similarity >= 0.85 -> remplace par le canonique du marche
- Sinon -> conserve le skill original (apres cleanup minimal)

Le modele est charge a la demande (singleton). En l'absence de
sentence-transformers (env non installe), un fallback fuzzy substring/lowercase
est utilise pour ne pas casser le pipeline.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Any

from skillnav.pipelines.structure_mining.graph_builder import _infer_family
from skillnav.schemas.graph import SkillFamily

logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
_COSINE_THRESHOLD = 0.85

# Cache global du modele (chargement lourd : ~470 MB).
_model_cache: Any | None = None


def _try_load_model() -> Any | None:
    """Charge le sentence-transformer si dispo, sinon retourne None (fallback)."""
    global _model_cache
    if _model_cache is not None:
        return _model_cache
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        logger.info("sentence-transformers indisponible, fallback fuzzy substring")
        return None
    try:
        _model_cache = SentenceTransformer(_DEFAULT_MODEL)
    except Exception as exc:
        logger.warning("Chargement sentence-transformer echec : %s", exc)
        return None
    return _model_cache


def _dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    """Deduplique une iterable en preservant l'ordre, comparaison case-insensitive."""
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(item.strip())
    return out


def _fallback_normalize(skills: list[str], canonical_vocab: list[str]) -> list[str]:
    """Fallback sans sentence-transformers : matching substring case-insensitive."""
    vocab_lower = {v.lower(): v for v in canonical_vocab}
    normalized: list[str] = []
    for skill in skills:
        skill_key = skill.strip().lower()
        if skill_key in vocab_lower:
            normalized.append(vocab_lower[skill_key])
            continue
        # Substring match : on cherche le canonique le plus court qui contient ou est contenu.
        candidates = [
            canonical
            for canonical_lower, canonical in vocab_lower.items()
            if skill_key == canonical_lower
            or skill_key in canonical_lower
            or canonical_lower in skill_key
        ]
        if candidates:
            normalized.append(min(candidates, key=len))
        else:
            normalized.append(skill.strip())
    return _dedupe_preserve_order(normalized)


def normalize_skills(
    skills: list[str],
    canonical_vocab: list[str],
    threshold: float = _COSINE_THRESHOLD,
) -> list[str]:
    """Normalise une liste de skills vers le vocabulaire canonique du marche.

    Args:
        skills: skills bruts (issus du LLM ou des regles).
        canonical_vocab: top N skills marche (depuis load_postings + agregat).
        threshold: similarite cosine minimale pour remplacer par le canonique.

    Returns:
        Liste deduplique de skills normalises (canonique marche si similaire,
        sinon le skill original nettoye).
    """
    if not skills:
        return []
    if not canonical_vocab:
        return _dedupe_preserve_order(skills)

    model = _try_load_model()
    if model is None:
        return _fallback_normalize(skills, canonical_vocab)

    from sentence_transformers import util

    skill_emb = model.encode(skills, convert_to_tensor=True, normalize_embeddings=True)
    vocab_emb = model.encode(canonical_vocab, convert_to_tensor=True, normalize_embeddings=True)
    sims = util.cos_sim(skill_emb, vocab_emb)

    normalized: list[str] = []
    for i, raw in enumerate(skills):
        best_idx = int(sims[i].argmax())
        best_score = float(sims[i][best_idx])
        if best_score >= threshold:
            normalized.append(canonical_vocab[best_idx])
        else:
            normalized.append(raw.strip())

    return _dedupe_preserve_order(normalized)


def assign_families(skills: list[str]) -> dict[str, SkillFamily]:
    """Mappe chaque skill normalise a sa SkillFamily SKILLNAV."""
    return {skill: _infer_family(skill) for skill in skills}
