"""Pipeline NER Union 3 BERT pour l'inférence live.

Charge les 3 modèles (BERT multilingue, CamemBERT, DistilBERT) en lazy
au premier appel à `extract()`, puis cache en mémoire pour les appels
suivants. Applique la stratégie Union (toutes les entités détectées par
au moins un modèle, dédoublonnées case-insensitive) retenue dans
notebook 03_ner_improvement.ipynb (F1 = 0.501).
"""

from __future__ import annotations

import threading
import time
from typing import Any

_LOCK = threading.Lock()
_MODELS: dict[str, Any] = {}
_LOAD_DURATIONS: dict[str, float] = {}
_LOAD_ERRORS: dict[str, str] = {}


MODELES_HF = {
    "bert_multilingual": "Davlan/bert-base-multilingual-cased-ner-hrl",
    "camembert": "Jean-Baptiste/camembert-ner",
    "distilbert": "dslim/distilbert-NER",
}


def _texte_norm(s: str) -> str:
    return (s or "").strip().lower().strip(".,;:()[]{}\"'`")


def _charger_modele(model_key: str):
    """Charge un modèle HuggingFace dans le cache (avec lock thread-safe).

    Si un modèle échoue (incompatibilité tokenizer, etc.) on enregistre
    l'erreur et on renvoie None. La pipeline Union ignore les modèles
    indisponibles et continue avec les autres.
    """
    with _LOCK:
        if model_key in _MODELS:
            return _MODELS[model_key]
        if model_key in _LOAD_ERRORS:
            return None
        try:
            from transformers import pipeline
        except ImportError as exc:
            _LOAD_ERRORS[model_key] = f"transformers non installé : {exc}"
            return None

        hf_id = MODELES_HF[model_key]
        t0 = time.perf_counter()
        try:
            ner = pipeline("ner", model=hf_id, tokenizer=hf_id, aggregation_strategy="simple")
        except Exception as exc:
            _LOAD_ERRORS[model_key] = f"{type(exc).__name__}: {exc}"
            return None
        _MODELS[model_key] = ner
        _LOAD_DURATIONS[model_key] = round(time.perf_counter() - t0, 2)
        return ner


def load_all_models() -> dict[str, float]:
    """Charge les 3 modèles immédiatement. Renvoie les temps de chargement."""
    for key in MODELES_HF:
        _charger_modele(key)
    return dict(_LOAD_DURATIONS)


def status() -> dict[str, Any]:
    """Statut des modèles (chargés, en erreur, ou non testés)."""
    return {
        "models": {
            key: {
                "hf_id": hf_id,
                "loaded": key in _MODELS,
                "load_duration_s": _LOAD_DURATIONS.get(key),
                "error": _LOAD_ERRORS.get(key),
            }
            for key, hf_id in MODELES_HF.items()
        }
    }


def extract_par_modele(texte: str, score_min: float = 0.5) -> dict[str, list[dict]]:
    """Inférence par chaque modèle, sans agrégation. Tolérant aux échecs."""
    texte = (texte or "")[:5000]
    par_modele: dict[str, list[dict]] = {}
    for key in MODELES_HF:
        ner = _charger_modele(key)
        if ner is None:
            par_modele[key] = []
            continue
        try:
            ents_raw = ner(texte)
        except Exception:
            par_modele[key] = []
            continue
        ents = []
        for e in ents_raw:
            score = float(e.get("score", 0.0))
            if score < score_min:
                continue
            ents.append({
                "text": str(e.get("word", "")).strip(),
                "label": str(e.get("entity_group", e.get("entity", "MISC"))),
                "score": round(score, 4),
                "start": int(e.get("start", 0)),
                "end": int(e.get("end", 0)),
            })
        par_modele[key] = ents
    return par_modele


def extract_union(texte: str, score_min: float = 0.5) -> dict[str, Any]:
    """Pipeline retenue : Union des 3 modèles (déduplication case-insensitive)."""
    t0 = time.perf_counter()
    par_modele = extract_par_modele(texte, score_min=score_min)
    union: list[dict] = []
    vues: set[str] = set()
    for key in MODELES_HF:
        for ent in par_modele.get(key, []):
            cle = _texte_norm(ent.get("text", ""))
            if not cle or cle in vues:
                continue
            vues.add(cle)
            ent["detected_by"] = [key]
            union.append(ent)
        # Croiser avec les entités déjà vues pour noter qui les a détectées aussi
    for ent in union:
        cle = _texte_norm(ent["text"])
        ent["detected_by"] = [
            key for key in MODELES_HF
            if any(_texte_norm(e["text"]) == cle for e in par_modele.get(key, []))
        ]
    return {
        "texte_analyse": texte[:5000],
        "duree_s": round(time.perf_counter() - t0, 3),
        "par_modele": par_modele,
        "union": union,
        "n_union": len(union),
    }
