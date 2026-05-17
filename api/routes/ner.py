"""Endpoint /ner/extract : inférence live des 3 modèles NER §N2.1.

Pipeline retenue : Union des 3 modèles BERT (DistilBERT + CamemBERT +
BERT multilingue) avec dédoublonnage case-insensitive. F1 = 0.501 sur
le gold set §N2.1 (cf. notebook 03_ner_improvement.ipynb).
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from api.config import get_settings
from api.ml.ner_pipeline import extract_union, status
from api.models.common import NerExtractRequest, NerExtractResponse


router = APIRouter(prefix="/ner", tags=["ner"])


@router.post("/extract", response_model=NerExtractResponse)
def extract(req: NerExtractRequest) -> NerExtractResponse:
    """Extrait les entités nommées d'un texte avec la pipeline Union 3 BERT.

    Le premier appel charge les 3 modèles en mémoire (~20 s). Les appels
    suivants sont rapides (~0.8 s par texte).
    """
    s = get_settings()
    if s.DISABLE_NER:
        raise HTTPException(503, "Inférence NER désactivée sur cet environnement")
    try:
        result = extract_union(req.text, score_min=req.score_min)
        return NerExtractResponse.model_validate(result)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc


@router.get("/status")
def ner_status() -> dict:
    """Statut de chargement des 3 modèles NER."""
    return status()


@router.get("/comparison")
def ner_comparison() -> dict:
    """Tableau §N2.1 chiffré + métadonnées de l'étude comparative.

    Renvoie le contenu de data/ner/evaluation_n2_1.json.
    """
    chemin = Path(__file__).resolve().parent.parent.parent / "data" / "ner" / "evaluation_n2_1.json"
    if not chemin.exists():
        raise HTTPException(404, "Évaluation §N2.1 absente. Exécuter scripts/ner/03_evaluate.py.")
    with open(chemin, "r", encoding="utf-8") as f:
        return {
            "section": "N2.1",
            "axe": "Content Mining",
            "gold_set_size": 30,
            "resultats": json.load(f),
        }
