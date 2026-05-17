from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field


class EntityType(StrEnum):
    SKILL = "SKILL"
    TOOL = "TOOL"
    FRAMEWORK = "FRAMEWORK"
    LANGUAGE = "LANGUAGE"
    ROLE = "ROLE"
    MODEL = "MODEL"
    OTHER = "OTHER"


class NerModel(StrEnum):
    BERT_MULTI = "bert-base-multilingual-cased"
    CAMEMBERT = "Jean-Baptiste/camembert-ner"
    DISTILBERT = "elastic/distilbert-base-uncased-finetuned-conll03-english"
    BASELINE_RULES = "baseline-rules"


class Entity(BaseModel):
    """Entité extraite par un modèle NER dans le texte d'une offre."""

    text: str
    entity_type: EntityType
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    normalized: str = ""  # nom canonique après normalisation taxonomique


class NerAnnotation(BaseModel):
    """Résultat NER complet d'un modèle sur une offre — stocké dans MongoDB ner_annotations."""

    job_id: str
    model_name: NerModel
    entities: list[Entity] = Field(default_factory=list)
    lang: str = "fr"
    processed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def technical_entities(self) -> list[Entity]:
        """Entités techniques uniquement (hors ROLE et OTHER)."""
        technical = {
            EntityType.SKILL,
            EntityType.TOOL,
            EntityType.FRAMEWORK,
            EntityType.LANGUAGE,
            EntityType.MODEL,
        }
        return [e for e in self.entities if e.entity_type in technical]


class NerComparison(BaseModel):
    """Comparaison des 3 modèles NER sur une offre — pour l'étude comparative §N2.1."""

    job_id: str
    bert_multi: NerAnnotation | None = None
    camembert: NerAnnotation | None = None
    distilbert: NerAnnotation | None = None
    baseline: NerAnnotation | None = None
