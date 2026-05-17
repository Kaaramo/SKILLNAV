"""LSTM (neuralforecast, Nixtla) — reseau de neurones recurrent.

Reseau LSTM (Long Short-Term Memory, Hochreiter & Schmidhuber 1997) entraine
via PyTorch Lightning, encapsule par neuralforecast pour une API similaire a
Prophet / ARIMA.

Configuration conservatrice pour series courtes (19 semaines) :
  - hidden_size : 16 (petit, eviter l'overfit)
  - n_layers    : 1 (un seul niveau recurrent)
  - max_steps   : 200 iterations (compromis temps / convergence)
  - input_size  : 6 semaines (1.5 mois de lookback)

Sortie : prediction ponctuelle + IC95% estime par bootstrap residus.
"""

from __future__ import annotations

import logging
import os
import time
import warnings
from datetime import date, timedelta
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd

from skillnav.schemas.timeseries import Forecast, ForecastMethod, ForecastPoint

if TYPE_CHECKING:
    from skillnav.schemas.timeseries import SkillTimeSeries


# Silencer pytorch_lightning + neuralforecast (logs tres verbeux par defaut)
logging.getLogger("pytorch_lightning").setLevel(logging.ERROR)
logging.getLogger("lightning_fabric").setLevel(logging.ERROR)
logging.getLogger("neuralforecast").setLevel(logging.ERROR)
os.environ.setdefault("NEURALFORECAST_DISABLE_FALLBACK_WARNING", "1")

# Hyperparametres (calibres pour series courtes)
_HIDDEN_SIZE = 16
_INPUT_SIZE = 6  # 1.5 mois de lookback
_MAX_STEPS = 200
_N_LAYERS = 1


def _series_to_nf_dataframe(series: SkillTimeSeries, n: int | None = None) -> pd.DataFrame:
    """Convertit en format neuralforecast (colonnes unique_id, ds, y)."""
    dps = series.data_points[:n] if n else series.data_points
    return pd.DataFrame(
        {
            "unique_id": [series.skill_name] * len(dps),
            "ds": [pd.Timestamp(d.period) for d in dps],
            "y": [float(d.count) for d in dps],
        }
    )


def _next_periods(last_period: str, horizon: int) -> list[str]:
    last_date = date.fromisoformat(last_period)
    return [(last_date + timedelta(weeks=i + 1)).isoformat() for i in range(horizon)]


def _make_lstm_model(horizon: int):  # type: ignore[no-untyped-def]
    """Construit un LSTM neuralforecast configure pour series courtes."""
    from neuralforecast.losses.pytorch import MAE  # type: ignore[import-untyped]
    from neuralforecast.models import LSTM  # type: ignore[import-untyped]

    return LSTM(
        h=horizon,
        input_size=_INPUT_SIZE,
        encoder_hidden_size=_HIDDEN_SIZE,
        encoder_n_layers=_N_LAYERS,
        max_steps=_MAX_STEPS,
        learning_rate=1e-3,
        random_seed=42,
        loss=MAE(),
        scaler_type="standard",
        enable_progress_bar=False,
    )


def _ic_from_residuals(predictions: np.ndarray, residuals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Estime IC95% par residuals bootstrap simple :
    yhat +/- 1.96 * std(residuals_train)
    """
    if len(residuals) < 2:
        return predictions, predictions
    sigma = float(np.std(residuals))
    margin = 1.96 * sigma
    return predictions - margin, predictions + margin


def fit_lstm_auto(
    series: SkillTimeSeries,
    train_periods: int,
    test_periods: int,
) -> tuple[Forecast, float]:
    """Entraine LSTM sur les `train_periods` premieres semaines, predit
    `test_periods` semaines, calcule le MAPE sur le test.
    """
    from neuralforecast import NeuralForecast  # type: ignore[import-untyped]

    df_train = _series_to_nf_dataframe(series, n=train_periods)
    test_counts = np.array(
        [d.count for d in series.data_points[train_periods : train_periods + test_periods]],
        dtype=float,
    )

    t0 = time.perf_counter()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        nf = NeuralForecast(models=[_make_lstm_model(test_periods)], freq="W-MON")
        nf.fit(df_train)
        pred_df = nf.predict()

    mean = pred_df["LSTM"].to_numpy()

    # IC95% par residus sur le train set
    train_pred = nf.predict_insample()
    train_resid = (train_pred["y"] - train_pred["LSTM"]).to_numpy()
    lower_vals, upper_vals = _ic_from_residuals(mean, train_resid)

    runtime = time.perf_counter() - t0

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
            lower=max(0.0, float(lower_vals[i])),
            upper=max(0.0, float(upper_vals[i])),
        )
        for i in range(test_periods)
    ]

    return (
        Forecast(
            skill_name=series.skill_name,
            method=ForecastMethod.LSTM,
            train_periods=train_periods,
            test_periods=test_periods,
            mape=mape,
            predictions=predictions,
        ),
        runtime,
    )


def fit_lstm_and_forecast(
    series: SkillTimeSeries,
    horizon: int = 4,
) -> tuple[Forecast, float]:
    """Re-entraine LSTM sur toute la serie et predit `horizon` semaines."""
    from neuralforecast import NeuralForecast

    df_full = _series_to_nf_dataframe(series)

    t0 = time.perf_counter()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        nf = NeuralForecast(models=[_make_lstm_model(horizon)], freq="W-MON")
        nf.fit(df_full)
        pred_df = nf.predict()
        train_pred = nf.predict_insample()
    runtime = time.perf_counter() - t0

    mean = pred_df["LSTM"].to_numpy()
    train_resid = (train_pred["y"] - train_pred["LSTM"]).to_numpy()
    lower_vals, upper_vals = _ic_from_residuals(mean, train_resid)

    future_periods = _next_periods(series.data_points[-1].period, horizon)
    predictions = [
        ForecastPoint(
            period=future_periods[i],
            value=max(0.0, float(mean[i])),
            lower=max(0.0, float(lower_vals[i])),
            upper=max(0.0, float(upper_vals[i])),
        )
        for i in range(horizon)
    ]

    return (
        Forecast(
            skill_name=series.skill_name,
            method=ForecastMethod.LSTM,
            train_periods=len(series.data_points),
            test_periods=horizon,
            mape=None,
            predictions=predictions,
        ),
        runtime,
    )


# Aliases pour mypy si besoin d'un type-check fort sur _ic_from_residuals
__all__: list[str] = ["fit_lstm_auto", "fit_lstm_and_forecast"]
_ = Any  # type: ignore[unused-ignore]
