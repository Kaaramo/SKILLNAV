"""Génère le schéma d'architecture de la base de données hybride SKILLNAV.

Sortie : livrables/02-base-de-donnees-hybride/architecture.png

Usage : python scripts/build_hybrid_db_architecture.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mp
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUTPUT = Path(__file__).resolve().parents[1] / "livrables" / "02-base-de-donnees-hybride" / "architecture.png"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


# Palette
COL_PIVOT = "#1F2937"
COL_MONGO = "#10B981"
COL_NEO = "#3B82F6"
COL_ES = "#F59E0B"
COL_API = "#7C3AED"
COL_WEB = "#EF4444"

TEXT_FG = "#FFFFFF"
BG = "#FAFAF7"
ARROW = "#94A3B8"
DARK = "#0F172A"
MUTED = "#64748B"

LABEL_BG = dict(
    boxstyle="round,pad=0.25",
    facecolor=BG,
    edgecolor="#E2E8F0",
    linewidth=0.8,
)


def box(ax, x, y, w, h, color, title, subtitle, lines):
    """Dessine un rectangle arrondi avec titre, sous-titre coloré et 2-3 lignes."""
    rect = mp.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.10",
        linewidth=0,
        facecolor=color,
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2, y + h - 0.35,
        title,
        ha="center", va="top",
        color=TEXT_FG, fontsize=12, fontweight="bold",
        family="DejaVu Sans",
    )
    if subtitle:
        ax.text(
            x + w / 2, y + h - 0.62,
            subtitle,
            ha="center", va="top",
            color=TEXT_FG, fontsize=8.5,
            style="italic",
            family="DejaVu Sans",
            alpha=0.88,
        )
    start_y = y + h - 0.95 if subtitle else y + h - 0.65
    for i, line in enumerate(lines):
        ax.text(
            x + w / 2, start_y - i * 0.24,
            line,
            ha="center", va="top",
            color=TEXT_FG, fontsize=9,
            family="DejaVu Sans",
        )


def arrow(ax, x1, y1, x2, y2):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="->", mutation_scale=18,
        color=ARROW, linewidth=1.5,
    )
    ax.add_patch(arr)


def label(ax, x, y, text):
    """Étiquette posée par-dessus une flèche, lisible grâce à son fond."""
    ax.text(
        x, y, text,
        ha="center", va="center",
        fontsize=8, color=MUTED,
        style="italic",
        family="DejaVu Sans",
        bbox=LABEL_BG,
    )


def main() -> None:
    fig, ax = plt.subplots(figsize=(14, 8), dpi=170)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG)

    # ─── Titre ────────────────────────────────────────────────────────────
    ax.text(
        7.0, 8.10,
        "SKILLNAV — Architecture de la base de données hybride",
        ha="center", va="top",
        fontsize=15, fontweight="bold", color=DARK,
        family="DejaVu Sans",
    )
    ax.text(
        7.0, 7.70,
        "polyglot persistence  ·  document store + graph DB + search index",
        ha="center", va="top",
        fontsize=10, color=MUTED, style="italic",
        family="DejaVu Sans",
    )

    # ─── Pivot ────────────────────────────────────────────────────────────
    box(
        ax, x=0.2, y=3.3, w=2.4, h=2.0,
        color=COL_PIVOT,
        title="data/jobs.jsonl",
        subtitle="source de vérité",
        lines=["3 467 documents", "schéma Pydantic"],
    )

    # ─── 3 bases ──────────────────────────────────────────────────────────
    box(
        ax, x=4.6, y=5.6, w=3.4, h=1.9,
        color=COL_MONGO,
        title="MongoDB Atlas",
        subtitle="Content Mining",
        lines=["collection skillnav.jobs", "17 index + full-text"],
    )
    box(
        ax, x=4.6, y=3.3, w=3.4, h=1.9,
        color=COL_NEO,
        title="Neo4j AuraDB",
        subtitle="Structure Mining",
        lines=["5 labels · 4 relations", "Louvain · PageRank"],
    )
    box(
        ax, x=4.6, y=1.0, w=3.4, h=1.9,
        color=COL_ES,
        title="Elasticsearch · Bonsai",
        subtitle="Usage Mining",
        lines=["index skillnav_jobs", "agrégations + search"],
    )

    # ─── FastAPI ──────────────────────────────────────────────────────────
    box(
        ax, x=9.4, y=3.3, w=2.4, h=1.9,
        color=COL_API,
        title="FastAPI",
        subtitle="couche de service",
        lines=["15 endpoints", "OpenAPI · asyncio"],
    )

    # ─── Dashboard ────────────────────────────────────────────────────────
    box(
        ax, x=12.2, y=3.3, w=1.7, h=1.9,
        color=COL_WEB,
        title="Dashboard",
        subtitle="restitution",
        lines=["Next.js", "6 pages"],
    )

    # ─── Flèches pivot → 3 DBs (avec labels au-dessus de chaque flèche) ──
    arrow(ax, 2.7, 4.6, 4.6, 6.4)
    label(ax, 3.65, 5.75, "ingest_mongodb.py")

    arrow(ax, 2.7, 4.3, 4.6, 4.25)
    label(ax, 3.65, 4.55, "push_graph_to_neo4j.py")

    arrow(ax, 2.7, 4.0, 4.6, 2.1)
    label(ax, 3.65, 2.85, "ingest_elasticsearch.py")

    # ─── Flèches 3 DBs → FastAPI ─────────────────────────────────────────
    arrow(ax, 8.0, 6.4, 9.4, 4.7)
    arrow(ax, 8.0, 4.25, 9.4, 4.25)
    arrow(ax, 8.0, 2.1, 9.4, 3.8)

    # ─── Flèche FastAPI → Dashboard ──────────────────────────────────────
    arrow(ax, 11.8, 4.25, 12.2, 4.25)

    # ─── Légende basse (3 axes Web Mining) — 3 positions équilibrées ─────
    legend_y = 0.30
    ax.text(3.5,  legend_y, "● Content Mining",   ha="center", color=COL_MONGO, fontsize=10, fontweight="bold")
    ax.text(7.0,  legend_y, "● Structure Mining", ha="center", color=COL_NEO,   fontsize=10, fontweight="bold")
    ax.text(10.5, legend_y, "● Usage Mining",     ha="center", color=COL_ES,    fontsize=10, fontweight="bold")

    plt.savefig(OUTPUT, dpi=190, bbox_inches="tight", facecolor=BG, pad_inches=0.30)
    print(f"[ok] {OUTPUT.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
