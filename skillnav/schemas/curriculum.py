"""Schemas Pydantic v2 -- Curriculum SKILLNAV.

Source de verite pour le volet "gap analysis marche <-> formation" (CLAUDE.md).
Consomme par notebooks/06_gap_analysis_market_vs_curriculum.ipynb et la page /gap.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Module(BaseModel):
    """Un module d'enseignement (= UE = matiere)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    code: str = Field(..., description="Code module (ex: M243)")
    title: str = Field(..., description="Intitule officiel du module")
    volume_horaire: int = Field(..., ge=0, description="Volume horaire annuel en heures")
    skills_taught: list[str] = Field(
        default_factory=list,
        description="Skills enseignees, canonicalisees contre dico marche",
    )
    ects: float | None = Field(
        default=None, ge=0, description="Credits ECTS si documente"
    )


class Semester(BaseModel):
    """Un semestre du cycle ingenieur."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(..., description="Code semestre (S1 .. S6)")
    annee: int = Field(..., ge=1, le=3, description="Annee du cycle ingenieur")
    modules: list[Module] = Field(default_factory=list)
    pfe: bool = Field(default=False, description="Vrai si ce semestre est dedie au PFE")

    @property
    def n_modules(self) -> int:
        return len(self.modules)

    @property
    def volume_total(self) -> int:
        return sum(m.volume_horaire for m in self.modules)


class CurriculumExtraction(BaseModel):
    """Curriculum complet d'une filiere donnee dans une ecole."""

    model_config = ConfigDict(extra="forbid")

    school: str = Field(..., description="Nom court de l'ecole (ex: 'ENSA Tetouan')")
    school_code: str = Field(..., description="Slug machine (ex: 'ensa-tetouan')")
    university: str | None = Field(default=None, description="Universite de rattachement")
    filiere: str = Field(..., description="Nom complet de la filiere")
    filiere_code: str = Field(..., description="Code court (ex: 'SDBIA')")
    diplome: str = Field(..., description="Type de diplome delivre")
    objectif: str | None = Field(default=None, description="Resume de l'objectif filiere")
    semesters: list[Semester] = Field(default_factory=list)
    source_file: str = Field(..., description="Chemin du PDF/HTML source")
    extraction_date: str = Field(..., description="ISO date de l'extraction (YYYY-MM-DD)")

    @property
    def all_skills_taught(self) -> set[str]:
        """Union de toutes les skills enseignees sur tout le cursus."""
        skills: set[str] = set()
        for sem in self.semesters:
            for module in sem.modules:
                skills.update(module.skills_taught)
        return skills

    @property
    def n_modules(self) -> int:
        return sum(s.n_modules for s in self.semesters)

    @property
    def volume_total(self) -> int:
        return sum(s.volume_total for s in self.semesters)


class GapAnalysis(BaseModel):
    """Resultat d'une comparaison curriculum <-> marche."""

    model_config = ConfigDict(extra="forbid")

    curriculum_school: str = Field(..., description="Ecole de reference")
    market_origin: str = Field(..., description="'Maroc' | 'International' | 'Tous'")

    skills_taught: set[str] = Field(default_factory=set)
    skills_demanded: set[str] = Field(default_factory=set)

    skills_in_common: set[str] = Field(default_factory=set, description="Intersection")
    skills_gap: set[str] = Field(
        default_factory=set,
        description="Demandees marche mais non enseignees -- a combler",
    )
    skills_mismatch: set[str] = Field(
        default_factory=set,
        description="Enseignees mais peu demandees -- a questionner",
    )

    @property
    def coverage_pct(self) -> float:
        """% de skills demandees qui sont couvertes par l'enseignement."""
        if not self.skills_demanded:
            return 0.0
        return round(len(self.skills_in_common) / len(self.skills_demanded) * 100, 1)
