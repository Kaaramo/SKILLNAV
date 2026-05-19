"""Genere les 6 figures gap analysis depuis data/exports/gap_analysis_ensat.json.

Usage : python scripts/build_gap_figures.py

Sorties : 6 PNG dans data/exports/ (memes noms que le notebook 06)
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

REPO = Path(__file__).resolve().parent.parent
EXPORTS = REPO / "data" / "exports"
DATA_PATH = EXPORTS / "gap_analysis_ensat.json"

# Palette officielle SKILLNAV
COL_ENSAT = "#0F8F65"   # vert -- enseignement
COL_MA = "#2251FF"      # bleu royal -- marche marocain
COL_INTL = "#C77700"    # ambre -- marche international

# Style matplotlib coherent rapport L5
plt.rcParams["figure.dpi"] = 110
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


def fig1_couverture_globale(data: dict) -> None:
    couv = data["couverture"]
    origines = ["Maroc", "International"]
    x = np.arange(len(origines))
    w = 0.36
    skills_pct = [couv[o]["pct_skills"] for o in origines]
    offres_pct = [couv[o]["pct_offres_couvertes"] for o in origines]

    fig, ax = plt.subplots(figsize=(11, 5))
    b1 = ax.bar(x - w / 2, skills_pct, w, label="Couverture skills (compte distinct)",
                color=COL_MA, alpha=0.92)
    b2 = ax.bar(x + w / 2, offres_pct, w, label="Couverture offres (pondéré volume)",
                color=COL_INTL, alpha=0.92)

    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.2,
                    f"{b.get_height():.1f} %", ha="center", fontsize=10.5, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(origines, fontsize=11.5)
    ax.set_ylabel("Couverture du programme ENSAT-SDBIA (%)", fontsize=10.5)
    ax.set_ylim(0, max(max(skills_pct), max(offres_pct)) * 1.30)
    ax.set_title(
        "Figure 1 — À quelle hauteur le programme ENSAT-SDBIA répond-il aux\n"
        "compétences attendues par les recruteurs Maroc et International ?",
        fontsize=12.5, fontweight="bold", pad=14,
    )
    ax.legend(loc="upper right", frameon=False, fontsize=10.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f} %"))
    ax.grid(axis="y", alpha=0.25)
    ax.text(
        0.5, -0.18,
        f"Source : data/jobs.jsonl ({data['meta']['n_skills_demanded_ma']} skills MA · "
        f"{data['meta']['n_skills_demanded_intl']} skills INTL) vs. curriculum ENSAT "
        f"({data['meta']['n_skills_taught']} skills enseignées)",
        ha="center", va="center", transform=ax.transAxes,
        fontsize=8.5, style="italic", color="gray",
    )
    plt.tight_layout()
    plt.savefig(EXPORTS / "gap_couverture_globale.png", bbox_inches="tight")
    plt.close(fig)
    print("  OK gap_couverture_globale.png")


def fig2_top_gaps_maroc(data: dict) -> None:
    gaps = pd.DataFrame(data["top_gaps"]["Maroc"])
    gaps["skill"] = gaps["skill"].str.title()
    top_n = 20
    g = gaps.head(top_n).iloc[::-1]

    fig, ax = plt.subplots(figsize=(11.5, 7.5))
    bars = ax.barh(g["skill"], g["demand_count"], color=COL_MA, alpha=0.88)
    for b in bars:
        w_ = b.get_width()
        ax.text(w_ + 1.5, b.get_y() + b.get_height() / 2, f"{int(w_)} offres",
                va="center", fontsize=9.5, color="#1a3aa6", fontweight="bold")

    ax.set_xlabel("Nombre d'offres marocaines mentionnant cette compétence (sur 381)",
                  fontsize=10.5)
    ax.set_title(
        f"Figure 2 — Les {top_n} compétences les plus demandées au Maroc qui ne sont\n"
        "PAS enseignées dans le programme ENSAT-SDBIA",
        fontsize=12.5, fontweight="bold", pad=14,
    )
    ax.grid(axis="x", alpha=0.25)
    ax.text(
        0.5, -0.10,
        "Source : 381 offres MA / 6 plateformes / janv. 2023 → mai 2026 · "
        "comparé à 126 skills canonicalisées du curriculum ENSAT",
        ha="center", va="center", transform=ax.transAxes,
        fontsize=8.5, style="italic", color="gray",
    )
    plt.tight_layout()
    plt.savefig(EXPORTS / "gap_top20_maroc.png", bbox_inches="tight")
    plt.close(fig)
    print("  OK gap_top20_maroc.png")


def fig3_top_gaps_intl(data: dict) -> None:
    gaps = pd.DataFrame(data["top_gaps"]["International"])
    gaps["skill"] = gaps["skill"].str.title()
    top_n = 20
    g = gaps.head(top_n).iloc[::-1]

    fig, ax = plt.subplots(figsize=(11.5, 7.5))
    bars = ax.barh(g["skill"], g["demand_count"], color=COL_INTL, alpha=0.88)
    for b in bars:
        w_ = b.get_width()
        ax.text(w_ + 8, b.get_y() + b.get_height() / 2, f"{int(w_)} offres",
                va="center", fontsize=9.5, color="#8b5400", fontweight="bold")

    ax.set_xlabel("Nombre d'offres internationales mentionnant cette compétence (sur 3 086)",
                  fontsize=10.5)
    ax.set_title(
        f"Figure 3 — Les {top_n} compétences les plus demandées à l'International\n"
        "qui ne sont PAS enseignées dans le programme ENSAT-SDBIA",
        fontsize=12.5, fontweight="bold", pad=14,
    )
    ax.grid(axis="x", alpha=0.25)
    ax.text(
        0.5, -0.10,
        "Source : 3 086 offres INTL / corpus intl-ai-corpus / janv. 2023 → mai 2026 · "
        "comparé à 126 skills canonicalisées du curriculum ENSAT",
        ha="center", va="center", transform=ax.transAxes,
        fontsize=8.5, style="italic", color="gray",
    )
    plt.tight_layout()
    plt.savefig(EXPORTS / "gap_top20_international.png", bbox_inches="tight")
    plt.close(fig)
    print("  OK gap_top20_international.png")


def fig4_couverture_par_famille(data: dict) -> None:
    """MA vs INTL cote-a-cote, par famille."""
    fam_ma = data["couverture_par_famille"]["Maroc"]
    fam_intl = data["couverture_par_famille"]["International"]
    all_families = sorted(set(fam_ma.keys()) | set(fam_intl.keys()))

    df = pd.DataFrame([
        {
            "Famille": fam,
            "Couverture MA (%)": fam_ma.get(fam, {}).get("pct", 0.0),
            "Skills demandées MA": fam_ma.get(fam, {}).get("demanded", 0),
            "Couverture INTL (%)": fam_intl.get(fam, {}).get("pct", 0.0),
            "Skills demandées INTL": fam_intl.get(fam, {}).get("demanded", 0),
        }
        for fam in all_families
    ])
    df = df.sort_values("Couverture MA (%)", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 7.5))
    y = np.arange(len(df))
    h = 0.4
    b_ma = ax.barh(y - h / 2, df["Couverture MA (%)"], h,
                   label="Marché Marocain", color=COL_MA, alpha=0.92)
    b_intl = ax.barh(y + h / 2, df["Couverture INTL (%)"], h,
                     label="Marché International", color=COL_INTL, alpha=0.92)

    for bar, demand in zip(b_ma, df["Skills demandées MA"]):
        w_ = bar.get_width()
        ax.text(w_ + 1.0, bar.get_y() + bar.get_height() / 2,
                f"{w_:.0f}% · {int(demand)} skills", va="center",
                fontsize=8.8, color="#1a3aa6")
    for bar, demand in zip(b_intl, df["Skills demandées INTL"]):
        w_ = bar.get_width()
        ax.text(w_ + 1.0, bar.get_y() + bar.get_height() / 2,
                f"{w_:.0f}% · {int(demand)} skills", va="center",
                fontsize=8.8, color="#8b5400")

    ax.set_yticks(y)
    ax.set_yticklabels(df["Famille"], fontsize=10)
    ax.set_xlabel("Couverture du curriculum ENSAT-SDBIA (%)", fontsize=11)
    ax.set_xlim(0, 80)
    ax.axvline(50, color="gray", linewidth=0.6, linestyle="--", alpha=0.4)
    ax.text(50, len(df) - 0.3, "  50 %", fontsize=8.5, color="gray", va="top")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f} %"))
    ax.grid(axis="x", alpha=0.25)
    ax.legend(loc="lower right", frameon=False, fontsize=11)
    ax.set_title(
        "Figure 4 — Où l'ENSAT-SDBIA brille, où elle décroche : couverture par famille\n"
        "de compétences sur les marchés Marocain (bleu) et International (ambre)",
        fontsize=12.5, fontweight="bold", pad=14,
    )
    ax.text(
        0.5, -0.10,
        "Lecture : 67 % de couverture en Machine Learning au Maroc = sur les skills ML "
        "demandées par les recruteurs MA, 2 sur 3 sont enseignées.",
        ha="center", va="center", transform=ax.transAxes,
        fontsize=8.5, style="italic", color="gray",
    )
    plt.tight_layout()
    plt.savefig(EXPORTS / "gap_par_famille.png", bbox_inches="tight")
    plt.close(fig)
    print("  OK gap_par_famille.png")


# --- Vue interne ENSAT (figures 5 et 6) ---

FAMILY_KEYWORDS = {
    "AI/ML": ["intelligence", "apprentissage", "machine learning", "profond"],
    "Data Engineering": ["big data", "bases de données", "fouille", "décisionnelle"],
    "Programmation": ["algorithmique", "génie logiciel", "programmation", "systèmes", "réseaux"],
    "Data Viz": ["visualisation"],
    "NLP": ["langues naturelles", "taln"],
    "Computer Vision": ["vision"],
    "Maths/Stats": ["statistique", "modélisation", "algèbre", "information", "mathématique"],
    "Sécurité": ["sécurité", "éthique", "droit"],
    "Web/Knowledge": ["web", "sémantique", "blockchain"],
    "Soft skills": ["management", "langues", "communication", "veille", "entrepreneuriat", "microéconomie"],
}


def tag_family(title: str) -> str:
    t = title.lower()
    for fam, kws in FAMILY_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return fam
    return "Autres"


def build_modules_df(data: dict) -> pd.DataFrame:
    rows = []
    for sem in data["curriculum"]["semesters"]:
        for m in sem["modules"]:
            rows.append({
                "Semestre": sem["code"],
                "Famille": tag_family(m["title"]),
                "Module": m["code"],
                "Heures": m["volume_horaire"],
            })
    return pd.DataFrame(rows)


def fig5_heatmap(data: dict) -> None:
    df = build_modules_df(data)
    pivot = df.pivot_table(values="Heures", index="Famille", columns="Semestre",
                           aggfunc="sum", fill_value=0).reindex(
        index=df.groupby("Famille")["Heures"].sum().sort_values(ascending=False).index
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt="g", cmap="Blues",
                cbar_kws={"label": "Heures enseignées"},
                linewidths=0.6, linecolor="white", ax=ax,
                annot_kws={"fontsize": 10, "fontweight": "bold"})
    ax.set_title(
        "Figure 5 — Répartition des 3 185 h du curriculum ENSAT-SDBIA\n"
        "famille de compétences × semestre (S1 à S5)",
        fontsize=12.5, fontweight="bold", pad=14,
    )
    ax.set_xlabel("Semestre", fontsize=10.5)
    ax.set_ylabel("Famille de compétences (interne ENSAT)", fontsize=10.5)
    plt.tight_layout()
    plt.savefig(EXPORTS / "gap_heatmap_semestre_famille.png", bbox_inches="tight")
    plt.close(fig)
    print("  OK gap_heatmap_semestre_famille.png")


def fig6_pie(data: dict) -> None:
    df = build_modules_df(data)
    by_family = df.groupby("Famille")["Heures"].sum().sort_values(ascending=False)
    total = by_family.sum()

    fig, ax = plt.subplots(figsize=(10, 7.5))
    colors = ["#2251FF", "#C77700", "#0F8F65", "#7C3AED", "#E11D48", "#0891B2",
              "#A16207", "#6D28D9", "#15803D", "#BE185D"]
    wedges, _texts, autotexts = ax.pie(
        by_family.values,
        labels=by_family.index,
        colors=colors[:len(by_family)],
        autopct=lambda p: f"{p:.0f} %\n({int(p * total / 100)} h)",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 10},
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
        at.set_fontsize(9)
    ax.set_title(
        f"Figure 6 — Répartition horaire enseignée à l'ENSAT-SDBIA\n"
        f"{int(total)} h sur les 5 semestres de cours",
        fontsize=12.5, fontweight="bold", pad=18,
    )
    plt.tight_layout()
    plt.savefig(EXPORTS / "gap_repartition_horaire.png", bbox_inches="tight")
    plt.close(fig)
    print("  OK gap_repartition_horaire.png")


def main() -> None:
    if not DATA_PATH.exists():
        raise SystemExit(
            f"{DATA_PATH.relative_to(REPO)} introuvable -- lance d'abord "
            "scripts/build_gap_analysis.py"
        )

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    print(f"=== Generation 6 figures gap analysis (source : {DATA_PATH.name}) ===\n")

    fig1_couverture_globale(data)
    fig2_top_gaps_maroc(data)
    fig3_top_gaps_intl(data)
    fig4_couverture_par_famille(data)
    fig5_heatmap(data)
    fig6_pie(data)

    print(f"\n=> 6 PNG ecrits dans {EXPORTS.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
