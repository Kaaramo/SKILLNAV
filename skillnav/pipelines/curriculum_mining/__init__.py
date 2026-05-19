"""Pipeline curriculum_mining : extraction des competences enseignees par les ENSA.

Volet parallele SKILLNAV (gap analysis marche IA Maroc vs formation ENSA).
Reference rapport L5 chapitre 5.1.

Chaine de valeur :

    sources/curricula/<slug>/filiere.md
        -> parser.parse_filiere()        -> CurriculumExtraction (sans skills)
        -> skill_extractor.extract_*()   -> skills par module
        -> normalizer.normalize_skills() -> skills canoniques alignes sur le marche
        -> orchestrator.run_curriculum_mining()
        -> data/curricula/<slug>.json
"""

from __future__ import annotations

from skillnav.pipelines.curriculum_mining.orchestrator import run_curriculum_mining
from skillnav.pipelines.curriculum_mining.parser import parse_filiere

__all__ = ["parse_filiere", "run_curriculum_mining"]
