"""Parser des fichiers filiere.md vers le schema Pydantic CurriculumExtraction.

Le format filiere.md attendu :

    # ENSA <Ville> - Filiere <Acronyme>

    **Nom complet** : <nom>
    **Cycle** : Ingenieur d'Etat, 3 ans (S1 a S5 + PFE)
    **URL officielle** : <url>
    **Source primaire** : <source>
    **Date d'extraction** : 2026-05-19
    **Statut** : complete | partial | placeholder

    ## Semestre S1

    ### Module : <intitule>

    - Code : <code optionnel>
    - Heures : <volume optionnel>
    - Credits : <ects optionnel>
    - Description : <texte optionnel>

    ## Semestre S2
    ...

Les modules dont l'intitule est "TODO" sont ignores (squelette placeholder).
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from skillnav.schemas.curriculum import (
    SEMESTER_LABELS,
    CurriculumExtraction,
    ExtractionStatus,
    Module,
    Semester,
    SemesterLabel,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CURRICULA_DIR = PROJECT_ROOT / "sources" / "curricula"

_SEMESTER_HEADING_RE = re.compile(r"^## Semestre (S\d)\s*$", re.MULTILINE)
_MODULE_HEADING_RE = re.compile(r"^### Module : (.+)$", re.MULTILINE)
_FIELD_LINE_RE = re.compile(r"^- (Code|Heures|Credits|Description)\s*:\s*(.+)$", re.MULTILINE)


def _coerce_int(value: str) -> int | None:
    """Convertit une valeur texte en int, retourne None si non parsable."""
    cleaned = value.strip().rstrip("H").strip()
    try:
        return int(cleaned)
    except ValueError:
        return None


def _parse_module_block(block: str, name: str) -> Module:
    """Parse un bloc Markdown d'un module en Module Pydantic."""
    code: str | None = None
    hours: int | None = None
    credits: int | None = None
    description: str | None = None

    for match in _FIELD_LINE_RE.finditer(block):
        field, value = match.group(1), match.group(2).strip()
        if field == "Code":
            code = value if value and value != "?" else None
        elif field == "Heures":
            hours = _coerce_int(value)
        elif field == "Credits":
            credits = _coerce_int(value)
        elif field == "Description":
            description = value if value else None

    return Module(
        name=name.strip(),
        code=code,
        hours=hours,
        credits=credits,
        description=description,
    )


def _parse_semesters(md_text: str) -> list[Semester]:
    """Decoupe le markdown par section Semestre puis extrait les modules."""
    headings = list(_SEMESTER_HEADING_RE.finditer(md_text))
    semesters: list[Semester] = []

    for i, heading in enumerate(headings):
        label_raw = heading.group(1)
        if label_raw not in SEMESTER_LABELS:
            continue
        label: SemesterLabel = label_raw  # type: ignore[assignment]

        section_start = heading.end()
        section_end = headings[i + 1].start() if i + 1 < len(headings) else len(md_text)
        section_text = md_text[section_start:section_end]

        module_headings = list(_MODULE_HEADING_RE.finditer(section_text))
        modules: list[Module] = []

        for j, mod_heading in enumerate(module_headings):
            name = mod_heading.group(1).strip()
            if name.upper() == "TODO":
                continue
            block_start = mod_heading.end()
            block_end = (
                module_headings[j + 1].start()
                if j + 1 < len(module_headings)
                else len(section_text)
            )
            block = section_text[block_start:block_end]
            modules.append(_parse_module_block(block, name))

        if modules:
            semesters.append(Semester(label=label, modules=modules))

    return semesters


def _load_source_metadata(school_dir: Path) -> dict[str, Any]:
    """Charge le source.yaml d'une ENSA."""
    source_yaml = school_dir / "source.yaml"
    if not source_yaml.exists():
        msg = f"source.yaml introuvable pour {school_dir.name}"
        raise FileNotFoundError(msg)
    with source_yaml.open("r", encoding="utf-8") as fh:
        data: dict[str, Any] = yaml.safe_load(fh) or {}
    return data


def _coerce_status(raw: Any) -> ExtractionStatus:
    """Convertit le statut texte en enum, fallback PENDING si invalide."""
    if not isinstance(raw, str):
        return ExtractionStatus.PENDING
    try:
        return ExtractionStatus(raw.lower().strip())
    except ValueError:
        return ExtractionStatus.PENDING


def parse_filiere(school_slug: str, base_dir: Path | None = None) -> CurriculumExtraction:
    """Parse `sources/curricula/<slug>/filiere.md` + `source.yaml` -> CurriculumExtraction.

    Args:
        school_slug: identifiant de l'ENSA (ex: "ensa-tetouan-sdbia").
        base_dir: racine alternative (defaut: sources/curricula/).

    Returns:
        Le CurriculumExtraction sans skills (extraction LLM faite en aval).
    """
    root = base_dir or CURRICULA_DIR
    school_dir = root / school_slug

    if not school_dir.exists():
        msg = f"Dossier ENSA introuvable : {school_dir}"
        raise FileNotFoundError(msg)

    meta = _load_source_metadata(school_dir)
    filiere_md = school_dir / "filiere.md"

    if not filiere_md.exists():
        msg = f"filiere.md introuvable pour {school_slug}"
        raise FileNotFoundError(msg)

    md_text = filiere_md.read_text(encoding="utf-8")
    semesters = _parse_semesters(md_text)

    return CurriculumExtraction(
        school_id=meta.get("slug", school_slug),
        school_name=meta.get("school_name", school_slug),
        filiere_name=meta.get("filiere_name", ""),
        filiere_acronym=meta.get("filiere_acronym", ""),
        filiere_url=meta.get("filiere_url", ""),
        extracted_at=datetime.now(timezone.utc),
        status=_coerce_status(meta.get("status")),
        semesters=semesters,
        skills_taught=[],
    )


def list_available_schools(base_dir: Path | None = None) -> list[str]:
    """Liste les slugs des ENSA disponibles dans sources/curricula/."""
    root = base_dir or CURRICULA_DIR
    if not root.exists():
        return []
    return sorted(
        p.name
        for p in root.iterdir()
        if p.is_dir() and p.name.startswith("ensa-") and (p / "source.yaml").exists()
    )
