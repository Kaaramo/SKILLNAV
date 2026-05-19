"""Tests unitaires du schema Pydantic curriculum.py."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from skillnav.schemas.curriculum import (
    SEMESTER_LABELS,
    CurriculumExtraction,
    ExtractionStatus,
    Module,
    Semester,
)


def test_semester_labels_constant_is_immutable_tuple() -> None:
    """SEMESTER_LABELS doit etre un tuple immutable de 5 valeurs S1 a S5."""
    assert SEMESTER_LABELS == ("S1", "S2", "S3", "S4", "S5")
    assert isinstance(SEMESTER_LABELS, tuple)


def test_module_minimal_construction() -> None:
    """Un Module n'a besoin que d'un nom pour etre valide."""
    module = Module(name="Apprentissage profond")
    assert module.name == "Apprentissage profond"
    assert module.code is None
    assert module.hours is None
    assert module.credits is None
    assert module.skills == []


def test_module_full_construction() -> None:
    """Un Module complet rassemble code, heures, credits, description, skills."""
    module = Module(
        name="Traitement automatique des langues naturelles",
        code="M353",
        hours=94,
        credits=6,
        description="Pipeline NLP : tokenisation, embeddings, transformers.",
        skills=["NLP", "transformers", "tokenisation"],
    )
    assert module.hours == 94
    assert module.credits == 6
    assert "transformers" in module.skills


def test_module_rejects_negative_hours() -> None:
    """Le volume horaire ne peut pas etre negatif."""
    with pytest.raises(ValidationError):
        Module(name="Test", hours=-10)


def test_module_rejects_negative_credits() -> None:
    """Les credits ECTS ne peuvent pas etre negatifs."""
    with pytest.raises(ValidationError):
        Module(name="Test", credits=-1)


def test_semester_total_hours_sum() -> None:
    """total_hours additionne les heures des modules en ignorant les None."""
    sem = Semester(
        label="S1",
        modules=[
            Module(name="Genie logiciel", hours=114),
            Module(name="Bases de donnees", hours=109),
            Module(name="Module sans heures"),  # hours = None doit etre ignore
        ],
    )
    assert sem.total_hours == 223


def test_semester_accepts_only_valid_labels() -> None:
    """Le label doit appartenir au Literal S1 a S5."""
    for valid_label in SEMESTER_LABELS:
        sem = Semester(label=valid_label)
        assert sem.label == valid_label

    with pytest.raises(ValidationError):
        Semester(label="S6")  # type: ignore[arg-type]

    with pytest.raises(ValidationError):
        Semester(label="S0")  # type: ignore[arg-type]


def test_curriculum_extraction_minimal() -> None:
    """Un CurriculumExtraction minimal ne necessite que les identifiants."""
    curriculum = CurriculumExtraction(
        school_id="ensa-test",
        school_name="ENSA Test",
        filiere_name="Filiere Test",
        filiere_acronym="TEST",
        filiere_url="https://example.com",
    )
    assert curriculum.status == ExtractionStatus.PENDING
    assert curriculum.semesters == []
    assert curriculum.skills_taught == []
    assert isinstance(curriculum.extracted_at, datetime)


def test_curriculum_rejects_duplicate_semester_labels() -> None:
    """Deux semestres avec le meme label doivent etre rejetes."""
    with pytest.raises(ValidationError) as exc:
        CurriculumExtraction(
            school_id="ensa-test",
            school_name="ENSA Test",
            filiere_name="Filiere Test",
            filiere_acronym="TEST",
            filiere_url="https://example.com",
            semesters=[
                Semester(label="S1", modules=[Module(name="A")]),
                Semester(label="S1", modules=[Module(name="B")]),
            ],
        )
    assert "Semestres dupliques" in str(exc.value)


def test_curriculum_total_hours_aggregates_all_semesters() -> None:
    """total_hours additionne sur l'ensemble du cursus."""
    curriculum = CurriculumExtraction(
        school_id="ensa-test",
        school_name="ENSA Test",
        filiere_name="Filiere Test",
        filiere_acronym="TEST",
        filiere_url="https://example.com",
        semesters=[
            Semester(label="S1", modules=[Module(name="A", hours=100)]),
            Semester(label="S2", modules=[Module(name="B", hours=120)]),
            Semester(label="S3", modules=[Module(name="C", hours=80)]),
        ],
    )
    assert curriculum.total_hours == 300
    assert len(curriculum.all_modules) == 3


def test_curriculum_json_roundtrip() -> None:
    """Serialisation JSON puis rechargement preserve le contenu."""
    original = CurriculumExtraction(
        school_id="ensa-tetouan-sdbia",
        school_name="ENSA Tetouan",
        filiere_name="Sciences des Donnees, Big Data et IA",
        filiere_acronym="SDBIA",
        filiere_url="http://ensa.ac.ma/",
        extracted_at=datetime(2026, 5, 19, tzinfo=timezone.utc),
        status=ExtractionStatus.COMPLETE,
        semesters=[
            Semester(
                label="S5",
                modules=[
                    Module(
                        name="Traitement automatique des langues naturelles",
                        code="M353",
                        hours=94,
                        skills=["NLP", "transformers"],
                    ),
                ],
            ),
        ],
        skills_taught=["NLP", "transformers"],
    )
    payload = original.model_dump_json()
    restored = CurriculumExtraction.model_validate_json(payload)
    assert restored == original


def test_curriculum_status_enum_values() -> None:
    """Les 4 statuts d'extraction sont disponibles."""
    assert ExtractionStatus.COMPLETE.value == "complete"
    assert ExtractionStatus.PARTIAL.value == "partial"
    assert ExtractionStatus.PLACEHOLDER.value == "placeholder"
    assert ExtractionStatus.PENDING.value == "pending"


def test_curriculum_accepts_all_5_semesters() -> None:
    """Cas reel : un curriculum a typiquement les 5 semestres S1 a S5."""
    curriculum = CurriculumExtraction(
        school_id="ensa-test",
        school_name="ENSA Test",
        filiere_name="Filiere Test",
        filiere_acronym="TEST",
        filiere_url="https://example.com",
        semesters=[Semester(label=label) for label in SEMESTER_LABELS],
    )
    assert len(curriculum.semesters) == 5
    assert [s.label for s in curriculum.semesters] == list(SEMESTER_LABELS)


def test_curriculum_model_dump_excludes_no_field() -> None:
    """model_dump doit serialiser tous les champs definis."""
    curriculum = CurriculumExtraction(
        school_id="ensa-test",
        school_name="ENSA Test",
        filiere_name="Filiere Test",
        filiere_acronym="TEST",
        filiere_url="https://example.com",
    )
    dumped = curriculum.model_dump(mode="json")
    expected_keys = {
        "school_id",
        "school_name",
        "filiere_name",
        "filiere_acronym",
        "filiere_url",
        "extracted_at",
        "status",
        "semesters",
        "skills_taught",
    }
    assert set(dumped.keys()) == expected_keys
    # extracted_at doit etre serialisable en ISO format JSON
    assert isinstance(json.dumps(dumped), str)
