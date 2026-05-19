"""Tests unitaires de skillnav/pipelines/curriculum_mining/parser.py."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from skillnav.pipelines.curriculum_mining.parser import (
    list_available_schools,
    parse_filiere,
)
from skillnav.schemas.curriculum import ExtractionStatus


def _create_minimal_school(tmp_path: Path, slug: str, filiere_md: str, status: str) -> Path:
    """Cree un dossier ENSA minimal pour les tests : source.yaml + filiere.md."""
    school_dir = tmp_path / slug
    school_dir.mkdir(parents=True)
    (school_dir / "source.yaml").write_text(
        dedent(
            f"""\
            slug: {slug}
            school_name: "ENSA Test"
            filiere_name: "Filiere de Test"
            filiere_acronym: "TEST"
            filiere_url: "https://example.com"
            status: {status}
            """
        ),
        encoding="utf-8",
    )
    (school_dir / "filiere.md").write_text(filiere_md, encoding="utf-8")
    return school_dir


def test_parse_filiere_extracts_simple_semester(tmp_path: Path) -> None:
    """Un Markdown minimal avec un module en S1 doit produire un Semester."""
    md = dedent(
        """\
        # ENSA Test

        ## Semestre S1

        ### Module : Machine Learning

        - Code : M101
        - Heures : 60
        """
    )
    _create_minimal_school(tmp_path, "ensa-test", md, "complete")

    curriculum = parse_filiere("ensa-test", base_dir=tmp_path)

    assert len(curriculum.semesters) == 1
    s1 = curriculum.semesters[0]
    assert s1.label == "S1"
    assert len(s1.modules) == 1
    assert s1.modules[0].name == "Machine Learning"
    assert s1.modules[0].code == "M101"
    assert s1.modules[0].hours == 60


def test_parse_filiere_ignores_todo_placeholder_modules(tmp_path: Path) -> None:
    """Les modules nommes 'TODO' (squelette placeholder) doivent etre ignores."""
    md = dedent(
        """\
        # ENSA Placeholder

        ## Semestre S1

        ### Module : TODO

        - Heures : ?

        ## Semestre S2

        ### Module : TODO

        ## Semestre S3

        ### Module : Vraie matiere

        - Heures : 50
        """
    )
    _create_minimal_school(tmp_path, "ensa-placeholder", md, "placeholder")

    curriculum = parse_filiere("ensa-placeholder", base_dir=tmp_path)

    # Seul S3 doit survivre (S1 et S2 sont vides apres filtrage TODO)
    assert len(curriculum.semesters) == 1
    assert curriculum.semesters[0].label == "S3"
    assert curriculum.semesters[0].modules[0].name == "Vraie matiere"


def test_parse_filiere_extracts_multiple_semesters_and_modules(tmp_path: Path) -> None:
    """Plusieurs S et plusieurs modules par S doivent etre extraits."""
    md = dedent(
        """\
        # ENSA Multi

        ## Semestre S1

        ### Module : Algorithmique

        - Heures : 60

        ### Module : Statistiques

        - Heures : 40

        ## Semestre S2

        ### Module : Python pour data science

        - Heures : 80
        """
    )
    _create_minimal_school(tmp_path, "ensa-multi", md, "complete")

    curriculum = parse_filiere("ensa-multi", base_dir=tmp_path)

    assert len(curriculum.semesters) == 2
    assert [s.label for s in curriculum.semesters] == ["S1", "S2"]
    assert len(curriculum.semesters[0].modules) == 2
    assert curriculum.semesters[1].modules[0].name == "Python pour data science"


def test_parse_filiere_handles_hours_with_h_suffix(tmp_path: Path) -> None:
    """Le parser doit accepter '48H' (format ENSA Fes) comme entier 48."""
    md = dedent(
        """\
        # ENSA Fes

        ## Semestre S1

        ### Module : Programmation orientee objet Java

        - Code : M121
        - Heures : 48H
        """
    )
    _create_minimal_school(tmp_path, "ensa-fes-isdia", md, "complete")

    curriculum = parse_filiere("ensa-fes-isdia", base_dir=tmp_path)
    assert curriculum.semesters[0].modules[0].hours == 48


def test_parse_filiere_ignores_semester_S6_if_present(tmp_path: Path) -> None:
    """S6 n'est pas dans le Literal du schema, doit etre ignore proprement."""
    md = dedent(
        """\
        # ENSA Avec PFE

        ## Semestre S5

        ### Module : NLP

        ## Semestre S6

        ### Module : PFE
        """
    )
    _create_minimal_school(tmp_path, "ensa-pfe", md, "complete")

    curriculum = parse_filiere("ensa-pfe", base_dir=tmp_path)
    labels = [s.label for s in curriculum.semesters]
    assert labels == ["S5"]
    assert "S6" not in labels


def test_parse_filiere_status_complete_is_recognized(tmp_path: Path) -> None:
    """Le statut 'complete' dans source.yaml doit etre mappe a ExtractionStatus.COMPLETE."""
    md = "## Semestre S1\n\n### Module : Test\n"
    _create_minimal_school(tmp_path, "ensa-s", md, "complete")
    curriculum = parse_filiere("ensa-s", base_dir=tmp_path)
    assert curriculum.status == ExtractionStatus.COMPLETE


def test_parse_filiere_status_placeholder_is_recognized(tmp_path: Path) -> None:
    """Le statut 'placeholder' dans source.yaml doit etre mappe correctement."""
    md = "## Semestre S1\n\n### Module : TODO\n"
    _create_minimal_school(tmp_path, "ensa-ph", md, "placeholder")
    curriculum = parse_filiere("ensa-ph", base_dir=tmp_path)
    assert curriculum.status == ExtractionStatus.PLACEHOLDER
    assert curriculum.semesters == []


def test_parse_filiere_raises_on_missing_school(tmp_path: Path) -> None:
    """parse_filiere doit lever FileNotFoundError si le dossier ENSA manque."""
    with pytest.raises(FileNotFoundError):
        parse_filiere("ensa-inexistant", base_dir=tmp_path)


def test_list_available_schools_returns_sorted_slugs(tmp_path: Path) -> None:
    """list_available_schools retourne les slugs tries alphabetiquement."""
    for slug in ["ensa-z-test", "ensa-a-test", "ensa-m-test"]:
        _create_minimal_school(tmp_path, slug, "## Semestre S1\n", "complete")

    schools = list_available_schools(base_dir=tmp_path)
    assert schools == ["ensa-a-test", "ensa-m-test", "ensa-z-test"]


def test_list_available_schools_ignores_non_ensa_folders(tmp_path: Path) -> None:
    """Les dossiers non prefixes 'ensa-' doivent etre ignores."""
    _create_minimal_school(tmp_path, "ensa-real", "## Semestre S1\n", "complete")
    (tmp_path / "not-an-ensa").mkdir()

    schools = list_available_schools(base_dir=tmp_path)
    assert schools == ["ensa-real"]
