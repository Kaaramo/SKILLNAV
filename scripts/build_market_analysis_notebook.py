"""Génère notebooks/00_market_analysis.ipynb (notebook 00 : EDA descriptive).

Notebook minimaliste qui utilise le module `skillnav_eda` pour tout le code
plumbing (chargement, canonicalisation, helpers, fonctions de section).

Régénération : python scripts/build_market_analysis_notebook.py
"""

from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
NB_PATH = REPO / "notebooks" / "00_market_analysis.ipynb"


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source.splitlines(keepends=True)}


CELLS: list[dict] = []

# ============================================================================
# HEADER
# ============================================================================
CELLS.append(md(
    """# SKILLNAV : Analyse exploratoire du marché Data & IA (Maroc + International)

> **Module** : M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi
> **Auteurs** : Karamo Sylla & Bachirou Konaté · **Soutenance** : 28 mai 2026

---

## Objectif

Première lecture chiffrée du corpus SKILLNAV collecté en mai 2026, **niveau
EDA descriptive** : qui recrute, quels métiers, quelles compétences, sur
quelles plateformes. Les **visualisations** correspondantes (16 figures
exportées en PNG) sont dans le notebook compagnon
[`01_visualisations.ipynb`](./01_visualisations.ipynb).

| Bloc                     | Fiches | Période              | Sources                                                                     |
|--------------------------|-------:|----------------------|-----------------------------------------------------------------------------|
| **Partie I : Maroc**     |    381 | août 2022 / mai 2026 | ANAPEC · Rekrute · Indeed MA · LinkedIn MA · Pages carrières · Glassdoor MA |
| **Partie II : INTL**     |  3 086 | août 2025 / mai 2026 | Corpus Tech INTL (builtin.com, 6 pays)                                      |
| **Partie III : Synthèse**|      . | .                    | Comparaison side-by-side et écarts marquants                                |

Toute la plomberie (chargement, canonicalisation 3 niveaux, helpers
d'analyse, fonctions de section) est dans le module `scripts/skillnav_eda.py`.
Voir [`docs/NOTEBOOK_00_ANNEXE_CODE.md`](../docs/NOTEBOOK_00_ANNEXE_CODE.md)
pour les explications pédagogiques.
"""
))

# ============================================================================
# SETUP MINIMAL (3 cellules)
# ============================================================================
CELLS.append(md("## 0. Setup\n"))

CELLS.append(code(
    """# Import du module utilitaire SKILLNAV (chargement, canonicalisation, helpers)
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd().parent / 'scripts'))
from skillnav_eda import *  # noqa: F401,F403

# Chargement des deux corpus + contrôle qualité automatique
df_maroc, df_international = charger_corpus()
controle_qualite(df_maroc, df_international)
"""
))

CELLS.append(md(
    """### Glossaire : AI-First / AI-Support / ML-First / Data Analytics

Quatre catégories de postes utilisées tout au long du notebook, classifiées
automatiquement au moment de la collecte par Claude Sonnet 4.5 à partir du
titre, des responsabilités et des compétences requises.

| Catégorie           | Définition courte                                                     | Exemples typiques                                       |
|---------------------|-----------------------------------------------------------------------|---------------------------------------------------------|
| **AI-First**        | L'IA générative (LLM, RAG, agents) **est** le produit                 | AI Engineer, Applied AI Engineer, GenAI / LLM Engineer  |
| **AI-Support**      | Le poste appuie une équipe IA sans construire les modèles             | AI Platform Engineer, AI Solutions Engineer, MLOps Eng  |
| **ML-First**        | ML traditionnel (CV, NLP pré-LLM, RecSys, recherche)                  | ML Engineer, Research Scientist, Computer Vision Eng    |
| **Data Analytics**  | SQL, BI, ETL, Excel ; pas de modélisation prédictive forte            | Data Analyst, BI Engineer, Business Analyst             |
"""
))

# ============================================================================
# PARTIE I : MAROC
# ============================================================================
CELLS.append(md("---\n\n# Partie I : Marché Data & IA au Maroc (381 fiches)\n"))

CELLS.append(md(
    """## I.1 Vue d'ensemble du corpus marocain

> **Comment lire les deux derniers compteurs ?**
>
> - **Postes managériaux** : offres pour lesquelles le poste implique d'encadrer une équipe (intitulés contenant *lead, head, director, manager, VP, chief, principal*).
> - **Postes à interface client** : offres pour lesquelles le titulaire est en contact direct avec des clients externes (intitulés ou descriptions contenant *sales engineer, customer success, solutions engineer, presales*).
"""
))
CELLS.append(code("section_vue_ensemble(df_maroc, 'Maroc')\n"))

CELLS.append(md("## I.2 Distribution par type de poste\n"))
CELLS.append(code("section_distribution_type(df_maroc, 'Maroc')\n"))

CELLS.append(md("## I.3 Top employeurs au Maroc\n"))
CELLS.append(code("section_top_entreprises(df_maroc, 'Maroc', top=15)\n"))

CELLS.append(md(
    """## I.4 Top intitulés de poste (canonicalisés)

Les intitulés bruts sont normalisés au chargement : `H/F`, `Hf`, `M/F`
suffixes retirés ; casse uniformisée ; alias appliqués pour les titres
fréquents (`Data Scientist` ne collisionne plus avec `Data scientist`).
"""
))
CELLS.append(code("section_top_titres(df_maroc, 'Maroc', top=10)\n"))

CELLS.append(md("## I.5 Compétences par famille (10 catégories)\n"))
CELLS.append(code("section_competences_par_famille(df_maroc, 'Maroc', top=8)\n"))

CELLS.append(md("## I.6 Écosystème frameworks d'IA générative au Maroc\n"))
CELLS.append(code("section_frameworks_genai(df_maroc, 'Maroc')\n"))

CELLS.append(md("## I.7 Recherche vs Application/Production\n"))
CELLS.append(code("section_recherche_vs_applied(df_maroc, 'Maroc')\n"))

# ============================================================================
# PARTIE II : INTERNATIONAL
# ============================================================================
CELLS.append(md("---\n\n# Partie II : Marché Data & IA International (3 086 fiches)\n"))

CELLS.append(md("## II.1 Vue d'ensemble du corpus international\n"))
CELLS.append(code("section_vue_ensemble(df_international, 'International')\n"))

CELLS.append(md("## II.2 Distribution par type de poste\n"))
CELLS.append(code("section_distribution_type(df_international, 'International')\n"))

CELLS.append(md("## II.3 Top employeurs à l'international\n"))
CELLS.append(code("section_top_entreprises(df_international, 'International', top=20)\n"))

CELLS.append(md("## II.4 Top intitulés de poste à l'international\n"))
CELLS.append(code("section_top_titres(df_international, 'International', top=10)\n"))

CELLS.append(md("## II.5 Compétences par famille (10 catégories)\n"))
CELLS.append(code("section_competences_par_famille(df_international, 'International', top=10)\n"))

CELLS.append(md("## II.6 Écosystème frameworks d'IA générative à l'international\n"))
CELLS.append(code("section_frameworks_genai(df_international, 'International')\n"))

CELLS.append(md("## II.7 Recherche vs Application/Production\n"))
CELLS.append(code("section_recherche_vs_applied(df_international, 'International')\n"))

# ============================================================================
# PARTIE III : COMPARAISON
# ============================================================================
CELLS.append(md(
    """---

# Partie III : Comparaison Maroc vs International

Synthèse transverse. On cherche les **écarts marquants** entre les deux
marchés pour préparer la soutenance et nourrir le rapport méthodologique L5.
"""
))

CELLS.append(md("## III.1 Tableau comparatif des types de postes\n"))
CELLS.append(code(
    """cnt_ma = df_maroc['ai_type'].value_counts(normalize=True) * 100
cnt_intl = df_international['ai_type'].value_counts(normalize=True) * 100
tableau = pd.DataFrame({
    '% Maroc': cnt_ma.round(1),
    '% International': cnt_intl.round(1),
}).fillna(0.0)
tableau.index = [TYPES_FR.get(t, t) for t in tableau.index]
tableau.index.name = 'Type de poste'
tableau['Écart (INTL - MA)'] = (tableau['% International'] - tableau['% Maroc']).round(1)
tableau.sort_values('% International', ascending=False)
"""
))

CELLS.append(md("## III.2 Top 20 compétences (Maroc vs International)\n\nAgrégation sur les 10 familles. Tri par fréquence dans le corpus international (plus grand, donc plus stable statistiquement).\n"))
CELLS.append(code(
    """def comparaison_skills(df_a, df_b, top=30):
    skills_intl = top_skills_global(df_b, top=top).index.tolist()
    rows = []
    for skill in skills_intl:
        n_a = jobs_avec_skill(df_a, skill)
        n_b = jobs_avec_skill(df_b, skill)
        rows.append({
            'Compétence': skill,
            'Offres Maroc': n_a,
            '% Maroc': round(n_a / max(len(df_a), 1) * 100, 1),
            'Offres INTL': n_b,
            '% INTL': round(n_b / max(len(df_b), 1) * 100, 1),
        })
    t = pd.DataFrame(rows).set_index('Compétence')
    t['Écart (% INTL - % Maroc)'] = (t['% INTL'] - t['% Maroc']).round(1)
    return t


comparaison_skills(df_maroc, df_international, top=20)
"""
))

CELLS.append(md("## III.3 Écarts les plus marquants\n\nQuelles compétences sont **massivement plus demandées** à l'international qu'au Maroc, et **lesquelles** sont surreprésentées au Maroc ?\n"))
CELLS.append(code(
    """tab = comparaison_skills(df_maroc, df_international, top=50)

print(\"=== Top 10 compétences SUR-représentées à l'international vs Maroc ===\")
print(tab.sort_values('Écart (% INTL - % Maroc)', ascending=False).head(10).to_string())
print()
print('=== Top 10 compétences SUR-représentées au Maroc vs international ===')
print(tab.sort_values('Écart (% INTL - % Maroc)', ascending=True).head(10).to_string())
"""
))

# ============================================================================
# SYNTHESE EXECUTIVE
# ============================================================================
CELLS.append(md(
    """---

## Synthèse exécutive (slide M9 à M12 de la soutenance)

Reprise des chiffres clés issus des Parties I à III, formatés en bullet
points pour la slide de conclusion.
"""
))

CELLS.append(code(
    """print('=' * 70)
print(\"   SKILLNAV : Synthèse exécutive du corpus (mai 2026)\")
print('=' * 70)

print(f'\\n>> Volumétrie')
print(f'   - Corpus Maroc        : {len(df_maroc):>5} offres   /  6 sources')
print(f'   - Corpus International: {len(df_international):>5} offres   /  builtin.com (6 pays)')
print(f'   - Total               : {len(df_maroc)+len(df_international):>5} offres')

print(f'\\n>> Profil dominant')
ma_top = df_maroc['ai_type'].value_counts().idxmax()
intl_top = df_international['ai_type'].value_counts().idxmax()
ma_pct = df_maroc['ai_type'].value_counts(normalize=True).max() * 100
intl_pct = df_international['ai_type'].value_counts(normalize=True).max() * 100
print(f'   - Maroc        : {TYPES_FR[ma_top]:<15} ({ma_pct:.0f} %)  -> marché encore très Data Analyst')
print(f'   - International: {TYPES_FR[intl_top]:<15} ({intl_pct:.0f} %)  -> marché pleinement basculé GenAI')

print(f'\\n>> Top 3 compétences les plus sur-représentées à l\\'international')
ecarts = tab.sort_values('Écart (% INTL - % Maroc)', ascending=False).head(3)
for skill, row in ecarts.iterrows():
    print(f'   - {skill:<22}: {row[\"% Maroc\"]:>5.1f}% MA   vs  {row[\"% INTL\"]:>5.1f}% INTL   (+{row[\"Écart (% INTL - % Maroc)\"]} pts)')

print(f'\\n>> Lecture pour la soutenance')
print(\"   1. Le marché marocain reste majoritairement Data Analyst (SQL, Excel, Power BI).\")
print(\"   2. La GenAI (RAG, LangChain, prompt engineering) n'a pas encore percé au Maroc.\")
print(\"   3. Les écarts de stack (Docker, K8s, MLOps) signalent un retard MLOps marocain.\")
print(\"   4. L'axe gap analysis curriculum ENSA vs marché est donc PERTINENT.\")
print(\"   5. Visualisations soutenance : voir 01_visualisations.ipynb (16 figures PNG).\")
print('=' * 70)
"""
))

# ============================================================================
# Sérialisation
# ============================================================================
NOTEBOOK = {
    "cells": CELLS,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


def main() -> None:
    NB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(NB_PATH, "w", encoding="utf-8") as f:
        json.dump(NOTEBOOK, f, ensure_ascii=False, indent=1)
    with open(NB_PATH, "r", encoding="utf-8") as f:
        contenu = f.read()
    n_emdash = contenu.count("—")
    print(f"Notebook écrit : {NB_PATH}")
    print(f"Cellules : {len(CELLS)}")
    print(f"Em-dashes restants : {n_emdash}")
    if n_emdash:
        raise SystemExit("ERREUR : des em-dashes subsistent.")


if __name__ == "__main__":
    main()
