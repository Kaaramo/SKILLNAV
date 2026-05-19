"""Schemas Pydantic v2 du volet curriculum mining (gap analysis ENSA Maroc).

Source de verite des programmes de filieres Data / IA / Big Data des 8 ENSA
publiques marocaines dispensant un cycle ingenieur dedie.

Le semestre S6 = PFE (Projet de Fin d'Etudes) n'est pas modelise ici :
la chaine de valeur n'extrait les competences enseignees que sur les semestres
S1 a S5 (modules academiques avec volume horaire).

Une mutation de ce schema doit casser tous les consommateurs au type-check :
- skillnav/pipelines/curriculum_mining/parser.py
- skillnav/pipelines/curriculum_mining/skill_extractor.py
- skillnav/pipelines/curriculum_mining/normalizer.py
- skillnav/pipelines/curriculum_mining/orchestrator.py
- notebooks/06_gap_analysis_market_vs_curriculum.ipynb
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator

SemesterLabel = Literal["S1", "S2", "S3", "S4", "S5"]
SEMESTER_LABELS: tuple[SemesterLabel, ...] = ("S1", "S2", "S3", "S4", "S5")


class ExtractionStatus(StrEnum):
    """Etat d'avancement de l'extraction d'un curriculum."""

    COMPLETE = "complete"
    PARTIAL = "partial"
    PLACEHOLDER = "placeholder"
    PENDING = "pending"


class Module(BaseModel):
    """Module academique d'un semestre (cours, TD, TP, projet)."""

    name: str
    code: str | None = None
    hours: int | None = Field(default=None, ge=0)
    credits: int | None = Field(default=None, ge=0)
    description: str | None = None
    skills: list[str] = Field(default_factory=list)


class Semester(BaseModel):
    """Semestre d'une filiere ingenieur (S1 a S5)."""

    label: SemesterLabel
    modules: list[Module] = Field(default_factory=list)

    @property
    def total_hours(self) -> int:
        """Somme des heures sur l'ensemble des modules du semestre."""
        return sum(m.hours for m in self.modules if m.hours is not None)


class CurriculumExtraction(BaseModel):
    """Programme complet d'une filiere ENSA - source de verite gap analysis.

    Persiste en JSON dans data/curricula/<school_id>.json apres execution
    du pipeline curriculum_mining.
    """

    school_id: str
    school_name: str
    filiere_name: str
    filiere_acronym: str
    filiere_url: str
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: ExtractionStatus = ExtractionStatus.PENDING
    semesters: list[Semester] = Field(default_factory=list)
    skills_taught: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_semesters(self) -> CurriculumExtraction:
        """Verifie l'unicite des labels de semestre (pas de doublon S1, S1)."""
        labels = [s.label for s in self.semesters]
        if len(labels) != len(set(labels)):
            duplicates = sorted({label for label in labels if labels.count(label) > 1})
            msg = f"Semestres dupliques dans {self.school_id}: {duplicates}"
            raise ValueError(msg)
        return self

    @property
    def total_hours(self) -> int:
        """Volume horaire total agrege sur l'ensemble du cursus S1 a S5."""
        return sum(s.total_hours for s in self.semesters)

    @property
    def all_modules(self) -> list[Module]:
        """Aplatissement de tous les modules de tous les semestres."""
        return [m for s in self.semesters for m in s.modules]
