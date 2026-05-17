from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field


class ForecastMethod(StrEnum):
    ARIMA = "ARIMA"
    PROPHET = "Prophet"
    LSTM = "LSTM"


class DataPoint(BaseModel):
    """Volume mensuel d'une compétence sur une période donnée."""

    period: str  # format "YYYY-MM"
    count: int = Field(ge=0)


class ForecastPoint(BaseModel):
    """Valeur prédite pour une période future avec intervalle de confiance à 95 %."""

    period: str  # format "YYYY-MM"
    value: float
    lower: float
    upper: float


class SkillTimeSeries(BaseModel):
    """Série temporelle mensuelle du volume d'une compétence — stockée dans MongoDB skills_timeseries."""

    skill_name: str
    family: str = ""
    data_points: list[DataPoint] = Field(default_factory=list)
    source_filter: str = "all"  # all | morocco | international
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Forecast(BaseModel):
    """Résultat de prévision pour une compétence avec une méthode donnée — stocké dans MongoDB forecasts."""

    skill_name: str
    method: ForecastMethod
    train_periods: int = Field(ge=1)
    test_periods: int = Field(ge=1)
    mape: float | None = None  # Mean Absolute Percentage Error (%)
    predictions: list[ForecastPoint] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ForecastComparison(BaseModel):
    """Comparaison des 3 méthodes de prévision pour une compétence — pour l'étude comparative §N2.3."""

    skill_name: str
    arima: Forecast | None = None
    prophet: Forecast | None = None
    lstm: Forecast | None = None
    best_method: ForecastMethod | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
