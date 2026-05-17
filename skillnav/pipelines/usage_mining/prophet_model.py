"""Prophet (Meta, ex-Facebook) — modele bayesien decomposable.

Decompose la serie en composantes : tendance (piecewise linear) + saisonnalite
(Fourier) + holidays. Concu pour series quotidiennes / hebdomadaires avec
intervention humaine minimale.

API : poetry add prophet (>=1.1). Backend Stan installe automatiquement.

Limites sur notre cas (19 semaines = 4 mois) :
  - saisonnalite annuelle indetectable
  - saisonnalite hebdomadaire desactivee (donnees deja hebdomadaires)
  - changepoints reduits (prior_scale faible) pour eviter l'overfit
"""

from __future__ import annotations

import logging
import time
from datetime import date, timedelta
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from skillnav.schemas.timeseries import Forecast, ForecastMethod, ForecastPoint

if TYPE_CHECKING:
    from skillnav.schemas.timeseries import SkillTimeSeries


# Reduction du bruit Prophet/cmdstanpy au demarrage
logging.getLogger("prophet").setLevel(logging.WARNING)
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)


def _series_to_dataframe(series: SkillTimeSeries, n: int | None = None) -> pd.DataFrame:
    """Convertit une SkillTimeSeries en DataFrame Prophet (colonnes ds, y)."""
    dps = series.data_points[:n] if n else series.data_points
    return pd.DataFrame(
        {
            "ds": [pd.Timestamp(d.period) for d in dps],
            "y": [float(d.count) for d in dps],
        }
    )


def _next_periods(last_period: str, horizon: int) -> list[str]:
    last_date = date.fromisoformat(last_period)
    return [(last_date + timedelta(weeks=i + 1)).isoformat() for i in range(horizon)]


def _make_prophet():  # type: ignore[no-untyped-def]
    """Cree un modele Prophet configure pour series hebdomadaires courtes."""
    from prophet import Prophet  # type: ignore[import-untyped]

    return Prophet(
        yearly_seasonality=False,    # serie trop courte pour annual
        weekly_seasonality=False,    # deja agrege par semaine
        daily_seasonality=False,
        changepoint_prior_scale=0.05,  # faible flexibilite (eviter overfit)
        interval_width=0.95,
    )


def fit_prophet_auto(
    series: SkillTimeSeries,
    train_periods: int,
    test_periods: int,
) -> tuple[Forecast, float]:
    """Entraine Prophet sur les `train_periods` premieres semaines, predit
    `test_periods` semaines, calcule le MAPE sur le test.

    Returns:
        (Forecast Pydantic, runtime en secondes)
    """
    df_train = _series_to_dataframe(series, n=train_periods)
    test_counts = np.array(
        [d.count for d in series.data_points[train_periods : train_periods + test_periods]],
        dtype=float,
    )

    t0 = time.perf_counter()
    model = _make_prophet()
    model.fit(df_train)

    # Generer le futur (test_periods semaines)
    future = model.make_future_dataframe(periods=test_periods, freq="W-MON")
    future = future.tail(test_periods)
    forecast_df = model.predict(future)

    runtime = time.perf_counter() - t0

    mean = forecast_df["yhat"].to_numpy()
    lower = forecast_df["yhat_lower"].to_numpy()
    upper = forecast_df["yhat_upper"].to_numpy()

    # MAPE (ignore zeros)
    mask = test_counts > 0
    mape: float | None = None
    if mask.any():
        mape = float(np.mean(np.abs((test_counts[mask] - mean[: len(test_counts)][mask]) / test_counts[mask])) * 100)

    future_periods = _next_periods(series.data_points[train_periods - 1].period, test_periods)
    predictions = [
        ForecastPoint(
            period=future_periods[i],
            value=max(0.0, float(mean[i])),
            lower=max(0.0, float(lower[i])),
            upper=max(0.0, float(upper[i])),
        )
        for i in range(test_periods)
    ]

    return (
        Forecast(
            skill_name=series.skill_name,
            method=ForecastMethod.PROPHET,
            train_periods=train_periods,
            test_periods=test_periods,
            mape=mape,
            predictions=predictions,
        ),
        runtime,
    )


def fit_prophet_and_forecast(
    series: SkillTimeSeries,
    horizon: int = 4,
) -> tuple[Forecast, float]:
    """Re-entraine Prophet sur toute la serie et predit `horizon` semaines."""
    df_full = _series_to_dataframe(series)

    t0 = time.perf_counter()
    model = _make_prophet()
    model.fit(df_full)

    future = model.make_future_dataframe(periods=horizon, freq="W-MON")
    future = future.tail(horizon)
    forecast_df = model.predict(future)
    runtime = time.perf_counter() - t0

    mean = forecast_df["yhat"].to_numpy()
    lower = forecast_df["yhat_lower"].to_numpy()
    upper = forecast_df["yhat_upper"].to_numpy()

    future_periods = _next_periods(series.data_points[-1].period, horizon)
    predictions = [
        ForecastPoint(
            period=future_periods[i],
            value=max(0.0, float(mean[i])),
            lower=max(0.0, float(lower[i])),
            upper=max(0.0, float(upper[i])),
        )
        for i in range(horizon)
    ]

    return (
        Forecast(
            skill_name=series.skill_name,
            method=ForecastMethod.PROPHET,
            train_periods=len(series.data_points),
            test_periods=horizon,
            mape=None,
            predictions=predictions,
        ),
        runtime,
    )
