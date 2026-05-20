"""Genere un schema synthetique de la chaine data /forecasting.

Sortie : docs/figures/forecast_pipeline_schema.png (300 DPI)

Usage : python scripts/build_forecast_pipeline_schema.py

Pour rapport L5 §N2.3 + deck de soutenance.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

REPO = Path(__file__).resolve().parent.parent
FORECAST_JSON = REPO / "data" / "exports" / "forecast_top10.json"
OUT = REPO / "docs" / "figures" / "forecast_pipeline_schema.png"

# Palette SKILLNAV
COL_BG = "#0E1320"
COL_BG_BOX = "#1A2238"
COL_FG = "#F1F3F8"
COL_FG_MUTED = "#A7B0C0"
COL_ARIMA = "#2251FF"
COL_PROPHET = "#7C3AED"
COL_LSTM = "#0F8F65"
COL_GREY = "#475569"
COL_GOLD = "#C77700"


def add_box(ax, x, y, w, h, title, subtitle=None, color=COL_BG_BOX, edge=None, title_color=None, title_size=11.5):
    """Ajoute une box arrondie avec titre et sous-titre."""
    edge = edge or color
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.18",
        linewidth=1.8, edgecolor=edge, facecolor=color, zorder=2,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2, y + h / 2 + (0.18 if subtitle else 0),
        title, ha="center", va="center",
        fontsize=title_size, fontweight="bold", color=title_color or COL_FG, zorder=3,
    )
    if subtitle:
        ax.text(
            x + w / 2, y + h / 2 - 0.20,
            subtitle, ha="center", va="center",
            fontsize=8.5, color=COL_FG_MUTED, zorder=3,
        )


def add_arrow(ax, x1, y1, x2, y2, color=COL_FG_MUTED, width=1.4):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=14,
        linewidth=width, color=color, zorder=1,
    )
    ax.add_patch(arrow)


def main() -> None:
    # Charge forecast pour le mini sparkline embedded
    data = json.loads(FORECAST_JSON.read_text(encoding="utf-8"))
    prompt_eng = next(s for s in data if s["skill_name"] == "Prompt engineering")
    hist = [p["count"] for p in prompt_eng["history"]]
    fcst = [p["value"] for p in prompt_eng["forecast"]]
    fcst_lo = [p["lower"] for p in prompt_eng["forecast"]]
    fcst_hi = [p["upper"] for p in prompt_eng["forecast"]]

    # Figure setup
    fig = plt.figure(figsize=(16, 10), facecolor=COL_BG)
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])
    ax.set_facecolor(COL_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")

    # ──────────────── Titre ────────────────
    fig.text(0.5, 0.95, "SKILLNAV · Pipeline Forecasting §N2.3",
             ha="center", fontsize=20, fontweight="bold", color=COL_FG)
    fig.text(0.5, 0.91,
             "Comparaison ARIMA · Prophet · LSTM sur 10 compétences IA du top PageRank",
             ha="center", fontsize=12, color=COL_FG_MUTED, style="italic")

    # ──────────────── Box 1 : Offres datées ────────────────
    add_box(ax, 0.3, 7.5, 2.6, 1.3,
            "3 467 offres datées",
            "data/jobs.jsonl  ·  janv. → avril 2026",
            color="#1F2937", edge=COL_GOLD)

    # ──────────────── Box 2 : series_builder ────────────────
    add_box(ax, 4.0, 7.5, 3.0, 1.3,
            "series_builder.py",
            "10 séries × 16 semaines hebdo\ntop PageRank · truncate 3 sem.",
            color="#1F2937", edge=COL_FG_MUTED)

    add_arrow(ax, 2.9, 8.15, 4.0, 8.15)

    # ──────────────── Branche 3 modèles ────────────────
    add_box(ax, 8.5, 8.4, 3.0, 1.0,
            "arima_model.py",
            "statsmodels · auto-fit AIC",
            color=COL_ARIMA, edge=COL_ARIMA, title_color="#fff", title_size=12)
    add_box(ax, 8.5, 7.2, 3.0, 1.0,
            "prophet_model.py",
            "Meta · trend + saisonnalité",
            color=COL_PROPHET, edge=COL_PROPHET, title_color="#fff", title_size=12)
    add_box(ax, 8.5, 6.0, 3.0, 1.0,
            "lstm_model.py",
            "neuralforecast · LSTM 16 unités",
            color=COL_LSTM, edge=COL_LSTM, title_color="#fff", title_size=12)

    add_arrow(ax, 7.0, 8.15, 8.5, 8.9, color=COL_ARIMA, width=1.8)
    add_arrow(ax, 7.0, 8.15, 8.5, 7.7, color=COL_PROPHET, width=1.8)
    add_arrow(ax, 7.0, 8.15, 8.5, 6.5, color=COL_LSTM, width=1.8)

    # ──────────────── Box comparison ────────────────
    add_box(ax, 12.7, 7.2, 3.0, 1.3,
            "comparison.py",
            "RMSE · MAE · MAPE\nargmin → best_method",
            color="#1F2937", edge=COL_GOLD)

    add_arrow(ax, 11.5, 8.9, 12.7, 8.2, color=COL_ARIMA)
    add_arrow(ax, 11.5, 7.7, 12.7, 7.85, color=COL_PROPHET)
    add_arrow(ax, 11.5, 6.5, 12.7, 7.5, color=COL_LSTM)

    # ──────────────── Verdict (annotation a droite des modeles, hors flux) ────────────────
    verdict_text = (
        "RÉSULTAT  10 skills\n"
        "──────────────────────\n"
        "  LSTM     5/10 victoires\n"
        "  ARIMA    4/10 victoires\n"
        "  Prophet  1/10 victoires\n"
        "──────────────────────\n"
        "RMSE médian global\n"
        "  ARIMA    17,21  ←\n"
        "  Prophet  17,95\n"
        "  LSTM     18,45\n"
        "──────────────────────\n"
        "V1.0 retenu : ARIMA"
    )
    ax.text(
        0.55, 5.4, verdict_text,
        ha="left", va="top", fontsize=8.5, color=COL_FG,
        family="monospace",
        bbox=dict(boxstyle="round,pad=0.55", facecolor="#1F2937", edgecolor=COL_GOLD, linewidth=1.4),
    )

    # ──────────────── Box JSON output ────────────────
    add_box(ax, 5.5, 3.7, 4.0, 1.3,
            "forecast_top10.json",
            "10 skills · history + forecast + RMSE\n19 Ko",
            color="#1F2937", edge=COL_GOLD)

    add_arrow(ax, 14.2, 7.2, 9.5, 5.0, color=COL_GOLD)

    # ──────────────── Mini sparkline (Prompt engineering exemple) ────────────────
    spark_x0, spark_y0 = 5.5, 1.0
    spark_w, spark_h = 4.0, 1.9
    # Box wrapper
    wrap = FancyBboxPatch(
        (spark_x0 - 0.1, spark_y0 - 0.15), spark_w + 0.2, spark_h + 0.35,
        boxstyle="round,pad=0.06,rounding_size=0.15",
        linewidth=1.5, edgecolor=COL_FG_MUTED, facecolor="#1F2937", zorder=2,
    )
    ax.add_patch(wrap)
    ax.text(spark_x0 + spark_w / 2, spark_y0 + spark_h + 0.05,
            'Exemple — "Prompt engineering"',
            ha="center", va="bottom", fontsize=9.5, color=COL_FG, fontweight="bold")

    # Sparkline inline
    n_hist = len(hist)
    n_fcst = len(fcst)
    total = n_hist + n_fcst
    max_v = max(max(hist), max(fcst_hi)) * 1.1
    px = [spark_x0 + i * (spark_w / (total - 1)) for i in range(total)]
    py_h = [spark_y0 + (v / max_v) * spark_h for v in hist]
    py_f = [spark_y0 + (v / max_v) * spark_h for v in fcst]
    py_lo = [spark_y0 + (v / max_v) * spark_h for v in fcst_lo]
    py_hi = [spark_y0 + (v / max_v) * spark_h for v in fcst_hi]

    # Ligne historique
    ax.plot(px[:n_hist], py_h, color=COL_FG_MUTED, linewidth=2, zorder=4)
    ax.scatter(px[:n_hist], py_h, color=COL_FG_MUTED, s=10, zorder=5)

    # Bande IC95 % forecast (polygone upper aller / lower retour)
    xs_band = px[n_hist - 1:n_hist - 1 + 1] + px[n_hist:total] + list(reversed(px[n_hist:total])) + px[n_hist - 1:n_hist - 1 + 1]
    ys_band = [py_h[-1]] + py_hi + list(reversed(py_lo)) + [py_h[-1]]
    ax.fill(xs_band, ys_band, color=COL_ARIMA, alpha=0.15, zorder=3)

    # Ligne forecast pointillee (start = dernier point hist)
    fcst_x = [px[n_hist - 1]] + px[n_hist:total]
    fcst_y = [py_h[-1]] + py_f
    ax.plot(fcst_x, fcst_y, color=COL_ARIMA, linewidth=2.3, linestyle="--", zorder=4)
    ax.scatter(px[n_hist:total], py_f, color=COL_ARIMA, edgecolor="white",
               s=28, zorder=5, linewidth=1.2)

    # Separateur vertical
    sep_x = px[n_hist - 1]
    ax.plot([sep_x, sep_x], [spark_y0, spark_y0 + spark_h],
            color=COL_FG_MUTED, linewidth=0.8, linestyle=":", zorder=3)
    ax.text(sep_x, spark_y0 + spark_h + 0.05 - 1.85, "début prévision",
            ha="center", va="top", fontsize=7.5, color=COL_FG_MUTED, style="italic")

    # Legend mini
    ax.text(spark_x0 + 0.1, spark_y0 - 0.05,
            "● 16 sem. observées  ─ 4 sem. ARIMA (RMSE 17,24)  zone = IC 95 %",
            fontsize=7.5, color=COL_FG_MUTED, va="top")

    add_arrow(ax, 7.5, 3.7, 7.5, 3.0, color=COL_GOLD)

    # ──────────────── Box Page web ────────────────
    add_box(ax, 10.5, 1.3, 5.2, 2.4,
            "Page  /forecasting",
            "4 actes :  KPI strip  ·  sélecteur + chart\n·  comparaison RMSE  ·  synthèse globale",
            color="#1F2937", edge=COL_ARIMA, title_size=13)

    add_arrow(ax, 9.5, 1.95, 10.5, 2.3, color=COL_GOLD)

    # ──────────────── Annotations sections ────────────────
    ax.text(8.0, 9.7, "BACHIROU — Pipeline Python (959 lignes)",
            ha="center", fontsize=10, color=COL_FG_MUTED, style="italic",
            fontweight="bold")
    ax.text(7.8, 5.3, "KARAMO — Visualisation Next.js",
            ha="center", fontsize=10, color=COL_FG_MUTED, style="italic",
            fontweight="bold")

    # Ligne separation horizontale entre Bachirou et Karamo
    ax.plot([0, 16], [5.5, 5.5], color=COL_FG_MUTED, linewidth=0.6,
            linestyle=":", alpha=0.5, zorder=0)

    # Footer
    fig.text(0.5, 0.03,
             "SKILLNAV · M242 Analyse de Web · ENSA Tétouan · Karamo Sylla & Bachirou Konaté · soutenance 28 mai 2026",
             ha="center", fontsize=8.5, color=COL_FG_MUTED, style="italic")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, dpi=300, bbox_inches="tight", facecolor=COL_BG)
    plt.close(fig)

    size_ko = OUT.stat().st_size // 1024
    print(f"=> Ecrit : {OUT.relative_to(REPO)} ({size_ko} Ko, 300 DPI)")


if __name__ == "__main__":
    main()
