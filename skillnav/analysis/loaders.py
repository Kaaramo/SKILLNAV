"""Loaders SKILLNAV — lecture des postings JSON depuis sources/collected/.

Equivalent du common.py upstream (ai-engineering-field-guide).
Remplace temporairement la lecture MongoDB tant que la base n'est pas peuplée.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COLLECTED = PROJECT_ROOT / "sources" / "collected"

SOURCES_MA: list[str] = [
    "anapec",
    "rekrute",
    "indeed-ma",
    "linkedin-ma",
    "pages-carrieres-ma",
    "glassdoor-ma",
]
SOURCES_INTL: list[str] = ["intl-ai-corpus"]
SOURCES_ALL: list[str] = SOURCES_MA + SOURCES_INTL


def load_postings(sources: list[str] | None = None) -> list[dict[str, Any]]:
    """Charge tous les postings JSON SKILLNAV (couche pivot Pydantic-compatible)."""
    resolved = sources if sources is not None else SOURCES_ALL
    records: list[dict[str, Any]] = []
    for src in resolved:
        postings_dir = COLLECTED / src / "postings"
        if not postings_dir.exists():
            continue
        for json_file in sorted(postings_dir.glob("*.json")):
            with json_file.open("r", encoding="utf-8") as f:
                records.append(json.load(f))
    return records


def load_data_raw(sources: list[str] | None = None) -> Iterator[dict[str, Any]]:
    """Iterator sur les YAML data_raw (couche 1 — texte brut)."""
    resolved = sources if sources is not None else SOURCES_ALL
    for src in resolved:
        for yaml_file in (COLLECTED / src / "data_raw").rglob("*.yaml"):
            with yaml_file.open("r", encoding="utf-8") as f:
                data: dict[str, Any] | None = yaml.safe_load(f)
            if data:
                yield {"_source": src, "_file": yaml_file.name, **data}


def load_data_structured(sources: list[str] | None = None) -> Iterator[dict[str, Any]]:
    """Iterator sur les YAML data_structured (couche 2 — enrichissement LLM)."""
    resolved = sources if sources is not None else SOURCES_ALL
    for src in resolved:
        for yaml_file in (COLLECTED / src / "data_structured").rglob("*.yaml"):
            with yaml_file.open("r", encoding="utf-8") as f:
                data: dict[str, Any] | None = yaml.safe_load(f)
            if data:
                yield {"_source": src, "_file": yaml_file.name, **data}
