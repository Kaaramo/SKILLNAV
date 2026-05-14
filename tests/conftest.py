"""Configuration partagée pytest — fixtures globales SKILLNAV."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Racine du repository (parent de tests/)."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def gold_set_dir(repo_root: Path) -> Path:
    """Dossier des 30 offres gold annotées manuellement (PRD §16.3).

    Sert de jeu test pour l'étude comparative NER (notebook 02_ner_comparison).
    """
    return repo_root / "data" / "gold_set"


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Fixtures de tests (offres exemples, payloads MongoDB, etc.)."""
    return Path(__file__).resolve().parent / "fixtures"
