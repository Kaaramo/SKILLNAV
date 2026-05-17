import hashlib
from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class ContractType(StrEnum):
    CDI = "CDI"
    CDD = "CDD"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    PART_TIME = "part_time"
    OTHER = "other"


class SeniorityLevel(StrEnum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    UNKNOWN = "unknown"


class JobStatus(StrEnum):
    EXTRACTED = "extracted"
    QUARANTINED = "quarantined"  # confidence < 0.75


class RawJob(BaseModel):
    """Offre brute telle que reçue du scraper — stockée dans MongoDB raw_jobs."""

    source: str
    source_url: str
    title_raw: str
    company_raw: str
    location_raw: str = ""
    html_raw: str
    text_clean: str
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lang: str = "fr"
    sha256: str = ""

    @model_validator(mode="after")
    def _compute_sha256(self) -> "RawJob":
        if not self.sha256:
            key = f"{self.company_raw}|{self.title_raw}|{self.source_url}"
            self.sha256 = hashlib.sha256(key.encode()).hexdigest()
        return self


class JobExtraction(BaseModel):
    """Offre structurée après extraction Pydantic AI + Claude — stockée dans MongoDB extracted_jobs."""

    raw_job_id: str
    title: str
    company: str
    location: str = ""
    country: str = ""
    contract_type: ContractType = ContractType.OTHER
    seniority: SeniorityLevel = SeniorityLevel.UNKNOWN
    skills: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    programming_languages: list[str] = Field(default_factory=list)
    source: str
    source_url: str
    published_at: datetime | None = None
    scraped_at: datetime
    lang: str = "fr"
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    status: JobStatus = JobStatus.EXTRACTED

    @property
    def all_technical_terms(self) -> list[str]:
        """Tous les termes techniques extraits, dédupliqués."""
        return list(
            set(self.skills + self.tools + self.frameworks + self.programming_languages)
        )
