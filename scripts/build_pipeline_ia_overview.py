"""Génère le schéma des 4 études comparatives IA de SKILLNAV.

Sortie : livrables/03-pipeline-ia/pipeline_overview.png

Usage : python scripts/build_pipeline_ia_overview.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mp
import matplotlib.pyplot as plt

OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "livrables"
    / "03-pipeline-ia"
    / "pipeline_overview.png"
)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


# Palette : 3 axes Web Mining + 1 étude pending
COL_NER = "#7C3AED"       # violet — Content Mining
COL_GRAPH = "#3B82F6"     # bleu   — Structure Mining
COL_FORECAST = "#10B981"  # vert   — Usage Mining
COL_EMERGE = "#94A3B8"    # gris   — pending

TEXT_FG = "#FFFFFF"
BG = "#FAFAF7"
DARK = "#0F172A"
MUTED = "#64748B"


def study_card(ax, x, y, w, h, color, num, title, axis_label, models, metric, winner, dataset, pending=False):
    """Carte verticale pour une étude comparative."""
    rect = mp.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.10",
        linewidth=0,
        facecolor=color,
        alpha=0.95 if not pending else 0.55,
    )
    ax.add_patch(rect)

    # Numéro étude (top-left, petit badge mono)
    ax.text(
        x + 0.28, y + h - 0.25,
        f"étude {num}",
        ha="left", va="top",
        color=TEXT_FG, fontsize=8,
        family="DejaVu Sans Mono",
        alpha=0.6,
    )
    # Titre (centré, ligne dédiée)
    ax.text(
        x + w / 2, y + h - 0.65,
        title,
        ha="center", va="top",
        color=TEXT_FG, fontsize=11, fontweight="bold",
        family="DejaVu Sans",
    )
    # Axe Web Mining
    ax.text(
        x + w / 2, y + h - 0.95,
        axis_label,
        ha="center", va="top",
        color=TEXT_FG, fontsize=8.5, style="italic",
        family="DejaVu Sans",
        alpha=0.88,
    )

    # Séparateur
    ax.plot(
        [x + 0.2, x + w - 0.2],
        [y + h - 1.20, y + h - 1.20],
        color=TEXT_FG, linewidth=0.8, alpha=0.35,
    )

    # 3 modèles avec leur métrique
    line_y = y + h - 1.50
    for model_name, model_score, is_winner in models:
        prefix = "✓ " if is_winner else "  "
        weight = "bold" if is_winner else "normal"
        text = f"{prefix}{model_name}"
        ax.text(
            x + 0.30, line_y,
            text,
            ha="left", va="top",
            color=TEXT_FG, fontsize=9, fontweight=weight,
            family="DejaVu Sans",
        )
        ax.text(
            x + w - 0.30, line_y,
            model_score,
            ha="right", va="top",
            color=TEXT_FG, fontsize=9, fontweight=weight,
            family="DejaVu Sans Mono",
        )
        line_y -= 0.30

    # Footer : metric name + dataset
    ax.plot(
        [x + 0.2, x + w - 0.2],
        [y + 0.65, y + 0.65],
        color=TEXT_FG, linewidth=0.8, alpha=0.35,
    )
    ax.text(
        x + w / 2, y + 0.50,
        f"métrique : {metric}",
        ha="center", va="top",
        color=TEXT_FG, fontsize=8,
        family="DejaVu Sans",
        alpha=0.85,
    )
    ax.text(
        x + w / 2, y + 0.25,
        f"jeu de test : {dataset}",
        ha="center", va="top",
        color=TEXT_FG, fontsize=8,
        family="DejaVu Sans",
        alpha=0.85,
    )

    if pending:
        ax.text(
            x + w / 2, y + h / 2,
            "à venir",
            ha="center", va="center",
            color=TEXT_FG, fontsize=20, fontweight="bold",
            family="DejaVu Sans",
            alpha=0.4,
            rotation=15,
        )


def main() -> None:
    fig, ax = plt.subplots(figsize=(14, 7.6), dpi=170)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.2)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG)

    # ─── Titre ────────────────────────────────────────────────────────────
    ax.text(
        7.0, 7.85,
        "SKILLNAV — Pipeline IA",
        ha="center", va="top",
        fontsize=15, fontweight="bold", color=DARK,
        family="DejaVu Sans",
    )
    ax.text(
        7.0, 7.45,
        "4 études comparatives  ·  9 algorithmes testés  ·  une décision chiffrée par axe",
        ha="center", va="top",
        fontsize=10, color=MUTED, style="italic",
        family="DejaVu Sans",
    )

    # ─── 4 cartes ─────────────────────────────────────────────────────────
    cards = [
        {
            "x": 0.3, "color": COL_NER, "num": "01",
            "title": "Entités nommées (NER)",
            "axis": "Content Mining",
            "models": [
                ("BERT multilingual", "F1 0,054", False),
                ("CamemBERT-NER",    "F1 0,348", False),
                ("DistilBERT-NER",   "F1 0,463", True),
            ],
            "metric": "F1 score (TP / TP+½(FP+FN))",
            "winner": "DistilBERT",
            "dataset": "30 fiches gold (543 skills)",
        },
        {
            "x": 3.7, "color": COL_GRAPH, "num": "02",
            "title": "Communautés du graphe",
            "axis": "Structure Mining",
            "models": [
                ("Label Propagation", "Q 0,148", False),
                ("Louvain",           "Q 0,295", True),
                ("Leiden",            "Q 0,298", False),
            ],
            "metric": "Modularité Q ∈ [-1, 1]",
            "winner": "Louvain",
            "dataset": "graphe 2 781 skills",
        },
        {
            "x": 7.1, "color": COL_FORECAST, "num": "03",
            "title": "Prévision temporelle",
            "axis": "Usage Mining",
            "models": [
                ("LSTM",     "RMSE 20,3", False),
                ("Prophet",  "RMSE 17,5", False),
                ("ARIMA",    "RMSE 16,2", True),
            ],
            "metric": "RMSE moyen sur 10 séries",
            "winner": "ARIMA",
            "dataset": "Top 10 skills PageRank",
        },
        {
            "x": 10.5, "color": COL_EMERGE, "num": "04",
            "title": "Skills émergents",
            "axis": "Sprint 2",
            "models": [
                ("Heuristique trends", "—", False),
                ("XGBoost classif.",   "—", False),
                ("KMeans clustering",  "—", False),
            ],
            "metric": "à définir",
            "winner": "—",
            "dataset": "à constituer",
            "pending": True,
        },
    ]

    card_w = 3.2
    card_h = 5.4
    card_y = 1.40

    for c in cards:
        study_card(
            ax, c["x"], card_y, card_w, card_h, c["color"],
            c["num"], c["title"], c["axis"],
            c["models"], c["metric"], c["winner"], c["dataset"],
            pending=c.get("pending", False),
        )

    # ─── Légende basse ────────────────────────────────────────────────────
    ax.text(
        7.0, 0.85,
        "« ✓ »  = modèle retenu pour la V1 SKILLNAV  ·  métriques calculées sur jeux de test séparés",
        ha="center", va="top",
        fontsize=9, color=MUTED, style="italic",
        family="DejaVu Sans",
    )
    ax.text(
        7.0, 0.45,
        "01 + 02 + 03 = livrables.  04 = documenté comme prochain sprint, sans dissimulation.",
        ha="center", va="top",
        fontsize=8.5, color=MUTED,
        family="DejaVu Sans",
    )

    plt.savefig(OUTPUT, dpi=190, bbox_inches="tight", facecolor=BG, pad_inches=0.30)
    print(f"[ok] {OUTPUT.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
