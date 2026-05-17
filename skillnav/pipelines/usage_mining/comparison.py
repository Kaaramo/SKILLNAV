"""Orchestration de l'etude comparative §N2.3.

Lance les 3 modeles (ARIMA, Prophet, LSTM) sur chaque serie temporelle,
calcule les metriques MAPE / RMSE / MAE / runtime / couverture IC95%, et
selectionne le meilleur modele par skill (et globalement).

Le meilleur est determine par RMSE (robuste aux zeros, contrairement au MAPE).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from skillnav.pipelines.usage_mining.arima_model import (
    fit_arima_and_forecast,
    fit_arima_auto,
)
from skillnav.pipelines.usage_mining.lstm_model import (
    fit_lstm_and_forecast,
    fit_lstm_auto,
)
from skillnav.pipelines.usage_mining.prophet_model import (
    fit_prophet_and_forecast,
    fit_prophet_auto,
)
from skillnav.schemas.timeseries import (
    Forecast,
    ForecastComparison,
    ForecastMethod,
    SkillTimeSeries,
)

# ── Metriques ─────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class ForecastMetrics:
    """Metriques d'erreur sur le test set pour un modele donne."""

    skill_name: str
    method: ForecastMethod
    mape: float | None  # peut etre None si test ne contient que des zeros
    rmse: float
    mae: float
    runtime: float
    coverage_95: float  # % de valeurs reelles dans l'IC95%


def _compute_metrics(
    actual: np.ndarray,
    forecast: Forecast,
    runtime: float,
) -> ForecastMetrics:
    pred = np.array([p.value for p in forecast.predictions], dtype=float)
    lower = np.array([p.lower for p in forecast.predictions], dtype=float)
    upper = np.array([p.upper for p in forecast.predictions], dtype=float)

    # Aligne longueurs
    n = min(len(actual), len(pred))
    actual = actual[:n]
    pred = pred[:n]
    lower = lower[:n]
    upper = upper[:n]

    rmse = float(np.sqrt(np.mean((actual - pred) ** 2)))
    mae = float(np.mean(np.abs(actual - pred)))

    # MAPE robuste : ignore actual=0 et actual<5 (sinon explose)
    mask = actual >= 5
    mape: float | None = None
    if mask.any():
        mape = float(np.mean(np.abs((actual[mask] - pred[mask]) / actual[mask])) * 100)

    coverage_95 = float(np.mean((actual >= lower) & (actual <= upper)) * 100)

    return ForecastMetrics(
        skill_name=forecast.skill_name,
        method=forecast.method,
        mape=mape,
        rmse=rmse,
        mae=mae,
        runtime=runtime,
        coverage_95=coverage_95,
    )


# ── Pipeline complet ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class SkillForecastResult:
    """Resultat complet d'une skill : 3 forecasts (train/test) + 3 metriques +
    3 predictions futures (re-entraine sur tout l'historique).
    """

    skill_name: str
    test_arima: Forecast
    test_prophet: Forecast
    test_lstm: Forecast
    metrics_arima: ForecastMetrics
    metrics_prophet: ForecastMetrics
    metrics_lstm: ForecastMetrics
    future_arima: Forecast
    future_prophet: Forecast
    future_lstm: Forecast
    best_method: ForecastMethod

    @property
    def comparison(self) -> ForecastComparison:
        return ForecastComparison(
            skill_name=self.skill_name,
            arima=self.test_arima,
            prophet=self.test_prophet,
            lstm=self.test_lstm,
            best_method=self.best_method,
        )


def run_forecast_comparison(
    series: SkillTimeSeries,
    train_periods: int = 15,
    test_periods: int = 4,
    horizon: int = 4,
) -> SkillForecastResult:
    """Execute la comparaison complete pour une skill.

    Phase 1 : Train/test split (train_periods semaines train, test_periods test)
              Pour chaque modele : fit + predict sur test + calcul metriques.
    Phase 2 : Re-entraine chaque modele sur TOUTE la serie + predit `horizon`
              semaines dans le futur reel.
    Phase 3 : Selectionne le meilleur par RMSE (robuste).

    Returns:
        SkillForecastResult contenant tout.
    """
    counts = np.array([d.count for d in series.data_points], dtype=float)
    test_actual = counts[train_periods : train_periods + test_periods]

    # Phase 1 : test set
    arima_fc, arima_rt = fit_arima_auto(series, train_periods, test_periods)
    prophet_fc, prophet_rt = fit_prophet_auto(series, train_periods, test_periods)
    lstm_fc, lstm_rt = fit_lstm_auto(series, train_periods, test_periods)

    m_arima = _compute_metrics(test_actual, arima_fc, arima_rt)
    m_prophet = _compute_metrics(test_actual, prophet_fc, prophet_rt)
    m_lstm = _compute_metrics(test_actual, lstm_fc, lstm_rt)

    # Phase 2 : forecast futur reel
    future_arima, _ = fit_arima_and_forecast(series, horizon)
    future_prophet, _ = fit_prophet_and_forecast(series, horizon)
    future_lstm, _ = fit_lstm_and_forecast(series, horizon)

    # Phase 3 : meilleur par RMSE
    best = min(
        [
            (m_arima.rmse, ForecastMethod.ARIMA),
            (m_prophet.rmse, ForecastMethod.PROPHET),
            (m_lstm.rmse, ForecastMethod.LSTM),
        ],
        key=lambda x: x[0],
    )[1]

    return SkillForecastResult(
        skill_name=series.skill_name,
        test_arima=arima_fc,
        test_prophet=prophet_fc,
        test_lstm=lstm_fc,
        metrics_arima=m_arima,
        metrics_prophet=m_prophet,
        metrics_lstm=m_lstm,
        future_arima=future_arima,
        future_prophet=future_prophet,
        future_lstm=future_lstm,
        best_method=best,
    )


def run_all(
    series_list: list[SkillTimeSeries],
    train_periods: int = 15,
    test_periods: int = 4,
    horizon: int = 4,
) -> list[SkillForecastResult]:
    """Execute run_forecast_comparison sur chaque serie. Imprime un log par skill."""
    results: list[SkillForecastResult] = []
    n = len(series_list)
    for i, s in enumerate(series_list, 1):
        print(f"  [{i:2}/{n}] {s.skill_name}")
        results.append(
            run_forecast_comparison(s, train_periods, test_periods, horizon)
        )
    return results


def aggregate_metrics(results: list[SkillForecastResult]) -> dict[str, dict[str, float]]:
    """Aggregate RMSE/MAE/MAPE/runtime par methode sur l'ensemble des skills.

    Returns:
        {method_name: {metric: median_value, ...}, ...}
    """
    methods = {
        "ARIMA": [r.metrics_arima for r in results],
        "Prophet": [r.metrics_prophet for r in results],
        "LSTM": [r.metrics_lstm for r in results],
    }
    summary: dict[str, dict[str, float]] = {}
    for name, ms in methods.items():
        valid_mapes = [m.mape for m in ms if m.mape is not None]
        summary[name] = {
            "rmse_median": float(np.median([m.rmse for m in ms])),
            "mae_median": float(np.median([m.mae for m in ms])),
            "mape_median": float(np.median(valid_mapes)) if valid_mapes else float("nan"),
            "runtime_total": float(sum(m.runtime for m in ms)),
            "coverage_95_mean": float(np.mean([m.coverage_95 for m in ms])),
            "n_wins": sum(1 for r in results if r.best_method.value == name),
        }
    return summary
