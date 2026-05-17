"""ARIMA (statsmodels) — modele statistique Box-Jenkins.

Auto-fit par grid search sur (p, d, q) avec selection AIC minimum.
Compatibilite : statsmodels >= 0.14.

Le modele ARIMA(p, d, q) :
  - p : ordre auto-regressif (AR)
  - d : differenciation (rend la serie stationnaire)
  - q : ordre moyenne mobile (MA)

AIC = 2k - 2 ln(L) : penalise la complexite et la mauvaise vraisemblance.
"""

from __future__ import annotations

import time
import warnings
from datetime import date, timedelta
from itertools import product
from typing import TYPE_CHECKING

import numpy as np

from skillnav.schemas.timeseries import Forecast, ForecastMethod, ForecastPoint

if TYPE_CHECKING:
    from skillnav.schemas.timeseries import SkillTimeSeries


# Grille auto-fit (p, d, q) — gardee petite pour tenir avec des series courtes.
_AR_RANGE = range(0, 3)   # p in {0, 1, 2}
_DIFF_RANGE = range(0, 2)  # d in {0, 1}
_MA_RANGE = range(0, 3)   # q in {0, 1, 2}


def _next_periods(last_period: str, horizon: int) -> list[str]:
    """Genere `horizon` semaines successives au format ISO date (lundi)."""
    last_date = date.fromisoformat(last_period)
    return [(last_date + timedelta(weeks=i + 1)).isoformat() for i in range(horizon)]


def fit_arima_auto(
    series: SkillTimeSeries,
    train_periods: int,
    test_periods: int,
) -> tuple[Forecast, float]:
    """Auto-fit ARIMA sur les `train_periods` premieres semaines, predit
    `test_periods` semaines futures, calcule le MAPE sur le test.

    Returns:
        (Forecast Pydantic, runtime en secondes)
    """
    from statsmodels.tsa.arima.model import ARIMA  # import local pour acceleration

    counts = np.array([d.count for d in series.data_points], dtype=float)
    train = counts[:train_periods]
    test = counts[train_periods : train_periods + test_periods]

    t0 = time.perf_counter()

    # Grid search (p, d, q) — minimise AIC sur le train
    best_aic = float("inf")
    best_order = (1, 1, 1)
    best_model = None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for p, d, q in product(_AR_RANGE, _DIFF_RANGE, _MA_RANGE):
            if p == 0 and q == 0:
                continue  # ARIMA(0, d, 0) = white noise, sans interet
            try:
                model = ARIMA(train, order=(p, d, q)).fit()
                if model.aic < best_aic:
                    best_aic = model.aic
                    best_order = (p, d, q)
                    best_model = model
            except (ValueError, np.linalg.LinAlgError):  # type: ignore[attr-defined]
                continue

    if best_model is None:
        # Fallback : ARIMA(1, 1, 0)
        best_model = ARIMA(train, order=(1, 1, 0)).fit()
        best_order = (1, 1, 0)

    # Prediction (test + horizon futur = 4 semaines par defaut)
    forecast_obj = best_model.get_forecast(steps=test_periods)
    mean = np.asarray(forecast_obj.predicted_mean, dtype=float)
    conf = np.asarray(forecast_obj.conf_int(alpha=0.05), dtype=float)

    runtime = time.perf_counter() - t0

    # MAPE sur le test set (ignore les zeros pour eviter la division par 0)
    mask = test > 0
    mape: float | None = None
    if mask.any():
        mape = float(np.mean(np.abs((test[mask] - mean[: len(test)][mask]) / test[mask])) * 100)

    # Construit les ForecastPoints
    future_periods = _next_periods(series.data_points[train_periods - 1].period, test_periods)
    predictions = [
        ForecastPoint(
            period=future_periods[i],
            value=max(0.0, float(mean[i])),
            lower=max(0.0, float(conf[i, 0])),
            upper=max(0.0, float(conf[i, 1])),
        )
        for i in range(test_periods)
    ]

    return (
        Forecast(
            skill_name=series.skill_name,
            method=ForecastMethod.ARIMA,
            train_periods=train_periods,
            test_periods=test_periods,
            mape=mape,
            predictions=predictions,
        ),
        runtime,
    )


def fit_arima_and_forecast(
    series: SkillTimeSeries,
    horizon: int = 4,
) -> tuple[Forecast, float]:
    """Re-entraine ARIMA sur TOUTE la serie et predit `horizon` semaines futures.

    Utilise apres la comparaison train/test : on prend le modele gagnant,
    on l'entraine sur tout l'historique et on extrapole le futur reel.

    Returns:
        (Forecast Pydantic avec mape=None, runtime en secondes)
    """
    from statsmodels.tsa.arima.model import ARIMA

    counts = np.array([d.count for d in series.data_points], dtype=float)
    t0 = time.perf_counter()

    best_aic = float("inf")
    best_model = None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for p, d, q in product(_AR_RANGE, _DIFF_RANGE, _MA_RANGE):
            if p == 0 and q == 0:
                continue
            try:
                m = ARIMA(counts, order=(p, d, q)).fit()
                if m.aic < best_aic:
                    best_aic = m.aic
                    best_model = m
            except (ValueError, np.linalg.LinAlgError):  # type: ignore[attr-defined]
                continue

    if best_model is None:
        best_model = ARIMA(counts, order=(1, 1, 0)).fit()

    fc = best_model.get_forecast(steps=horizon)
    mean = np.asarray(fc.predicted_mean, dtype=float)
    conf = np.asarray(fc.conf_int(alpha=0.05), dtype=float)

    runtime = time.perf_counter() - t0
    future_periods = _next_periods(series.data_points[-1].period, horizon)
    predictions = [
        ForecastPoint(
            period=future_periods[i],
            value=max(0.0, float(mean[i])),
            lower=max(0.0, float(conf[i, 0])),
            upper=max(0.0, float(conf[i, 1])),
        )
        for i in range(horizon)
    ]

    return (
        Forecast(
            skill_name=series.skill_name,
            method=ForecastMethod.ARIMA,
            train_periods=len(counts),
            test_periods=horizon,
            mape=None,
            predictions=predictions,
        ),
        runtime,
    )
