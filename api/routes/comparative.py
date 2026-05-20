"""Endpoint /comparative/{section} : tableaux §N2 chiffrés.

Sources :
- N2.1 : data/ner/evaluation_n2_1.json (NER comparatif)
- N2.2 : à venir (communautés graphe, Bachirou)
- N2.3 : à venir (forecasting, Bachirou)
- N2.4 : préfiguré dans notebook 01_visualisations §IV.10 (émergence)
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/comparative", tags=["comparative"])

REPO = Path(__file__).resolve().parent.parent.parent


@router.get("/{section}")
def section(section: str) -> dict:
    sections = {
        "n21": {
            "fichier": REPO / "data" / "ner" / "evaluation_n2_1.json",
            "titre": "NER comparatif (BERT-mult / CamemBERT / DistilBERT)",
            "axe": "Content Mining",
        },
    }
    if section.lower() not in sections:
        raise HTTPException(404, f"Section {section} non disponible. Disponibles : {list(sections.keys())}")
    cfg = sections[section.lower()]
    fichier = cfg["fichier"]
    if not Path(fichier).exists():
        raise HTTPException(404, f"Source de données manquante : {fichier.name}")
    with open(fichier, "r", encoding="utf-8") as f:
        return {
            "section": section.upper(),
            "titre": cfg["titre"],
            "axe": cfg["axe"],
            "data": json.load(f),
        }


@router.get("")
def list_sections() -> list[dict]:
    """Liste les sections §N2 disponibles."""
    return [
        {"section": "N2.1", "titre": "NER comparatif", "statut": "disponible"},
        {"section": "N2.2", "titre": "Communautés graphe", "statut": "en attente Bachirou"},
        {"section": "N2.3", "titre": "Forecasting", "statut": "en attente Bachirou"},
        {"section": "N2.4", "titre": "Détection émergence", "statut": "préfiguré dans notebook 01"},
    ]
