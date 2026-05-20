"""Parse sources/curricula/<ecole>/filiere.md -> CurriculumExtraction Pydantic.

Format attendu (cf. sources/curricula/ensa-tetouan/filiere.md) :
    # <School> -- <Filiere>
    ...
    ### Semestre N (Sn) -- Annee X
    | Code | Module | Vol. (h) | Skills enseignees |
    |---|---|---:|---|
    | Mxxx | Titre | <h> | skill1, skill2, skill3 |
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from skillnav.schemas.curriculum import CurriculumExtraction, Module, Semester

# Regex pour extraire le header de semestre : "### Semestre 1 (S1) -- Annee 1"
SEMESTER_HEADER_RE = re.compile(
    r"^###\s+Semestre\s+\d+\s*\((S\d+)\)\s*[—\-–]+\s*(?:Année|Annee)\s+(\d+)",
    re.IGNORECASE,
)

# Regex pour les lignes de tableau modules : "| M111 | Titre | 74 | s1, s2 |"
MODULE_ROW_RE = re.compile(
    r"^\|\s*\**(M\s*\d{2,3}\s*\d?)\**\s*\|\s*\**(.+?)\**\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$"
)


def _clean_skill(s: str) -> str:
    """Nettoie une skill : enleve les markdown formats, espaces, parentheses notes."""
    s = re.sub(r"\*+", "", s).strip()
    s = re.sub(r"\s*\(.+?$", "", s).strip()  # coupe les notes parentheses "(← module du PFE)"
    return s


def parse_filiere_md(md_path: Path, source_yaml_path: Path) -> CurriculumExtraction:
    """Parse filiere.md + source.yaml -> CurriculumExtraction.

    Args:
        md_path: chemin vers filiere.md
        source_yaml_path: chemin vers source.yaml (metadonnees)

    Returns:
        CurriculumExtraction Pydantic strict.
    """
    md_text = md_path.read_text(encoding="utf-8")
    meta = yaml.safe_load(source_yaml_path.read_text(encoding="utf-8"))

    semesters: list[Semester] = []
    current_sem: Semester | None = None

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()

        # Header semestre
        sem_match = SEMESTER_HEADER_RE.match(line)
        if sem_match:
            if current_sem is not None:
                semesters.append(current_sem)
            current_sem = Semester(
                code=sem_match.group(1).upper(),
                annee=int(sem_match.group(2)),
                modules=[],
                pfe=False,
            )
            continue

        # PFE explicite (S6) -- detecte sur les sections speciales
        if "PFE" in line and "###" in line and current_sem is None:
            current_sem = Semester(code="S6", annee=3, modules=[], pfe=True)
            continue

        # Ligne de module (uniquement dans un semestre)
        if current_sem is None:
            continue
        mod_match = MODULE_ROW_RE.match(line)
        if not mod_match:
            continue

        code_raw = mod_match.group(1).replace(" ", "")
        title = _clean_skill(mod_match.group(2))
        volume = int(mod_match.group(3))
        skills_raw = mod_match.group(4)
        skills = [_clean_skill(s) for s in skills_raw.split(",") if s.strip()]

        current_sem.modules.append(
            Module(
                code=code_raw,
                title=title,
                volume_horaire=volume,
                skills_taught=skills,
            )
        )

    if current_sem is not None:
        semesters.append(current_sem)

    return CurriculumExtraction(
        school=meta["school"],
        school_code=meta["school_code"],
        university=meta.get("university"),
        filiere=meta["filiere"],
        filiere_code=meta["filiere_code"],
        diplome=meta["diplome"],
        objectif=None,
        semesters=semesters,
        source_file=meta["extraction"]["source_file"],
        extraction_date=meta["extraction"]["extraction_date"],
    )
