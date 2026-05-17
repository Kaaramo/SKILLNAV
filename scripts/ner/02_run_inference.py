"""Inférence des 3 modèles NER sur le gold set §N2.1.

Pour chaque modèle (BERT multilingue, CamemBERT-NER, DistilBERT-NER) :
1. Charge le modèle depuis HuggingFace (téléchargement automatique 1er lancement)
2. Lance l'inférence sur les 30 fiches du gold set
3. Mesure le temps d'inférence par fiche
4. Sauve les résultats dans `data/ner/predictions/<modele>.json`

Note : le premier lancement télécharge les modèles (~500 Mo chacun), ce qui
peut prendre plusieurs minutes. Les lancements suivants sont quasi instantanés
(cache HuggingFace local).

Exécution : python scripts/ner/02_run_inference.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import GOLD_SET_PATH, MODELES, PREDICTIONS_DIR  # noqa: E402


def charger_gold_set() -> list[dict]:
    with open(GOLD_SET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def inferer_modele(model_key: str, gold_set: list[dict]) -> dict:
    """Charge un modèle HuggingFace et infère sur le gold set."""
    from transformers import pipeline

    cfg = MODELES[model_key]
    print(f"\nChargement du modèle {cfg['name']} ({cfg['hf_id']})...")
    t0_load = time.perf_counter()

    try:
        ner = pipeline(
            "ner",
            model=cfg["hf_id"],
            tokenizer=cfg["hf_id"],
            aggregation_strategy="simple",
        )
    except Exception as exc:
        print(f"  [!] Impossible de charger {cfg['hf_id']} : {exc}")
        return {"modele": model_key, "erreur": str(exc), "predictions": []}

    t_load = time.perf_counter() - t0_load
    print(f"  Chargé en {t_load:.1f} s")

    print(f"  Inférence sur {len(gold_set)} fiches...")
    predictions: list[dict] = []
    durees: list[float] = []

    for i, fiche in enumerate(gold_set, 1):
        texte = fiche["text"][:5000]  # cap à 5000 chars pour éviter OOM
        t0 = time.perf_counter()
        try:
            entites_brutes = ner(texte)
        except Exception as exc:
            print(f"    [!] Fiche {i} erreur : {exc}")
            entites_brutes = []
        dt = time.perf_counter() - t0
        durees.append(dt)

        # Normalisation des entités (sérialisable JSON)
        entites = []
        for e in entites_brutes:
            entites.append({
                "text": str(e.get("word", "")).strip(),
                "label": str(e.get("entity_group", e.get("entity", "MISC"))),
                "score": float(e.get("score", 0.0)),
                "start": int(e.get("start", 0)),
                "end": int(e.get("end", 0)),
            })

        predictions.append({
            "job_id": fiche["job_id"],
            "entites": entites,
            "duree_inference_s": round(dt, 4),
        })

        if i % 5 == 0:
            print(f"    {i}/{len(gold_set)}  ({sum(durees)/len(durees):.2f} s/fiche)")

    duree_totale = sum(durees)
    duree_moyenne = duree_totale / max(len(durees), 1)
    print(f"  Inférence terminée en {duree_totale:.1f} s "
          f"(moyenne {duree_moyenne:.2f} s/fiche)")

    return {
        "modele": model_key,
        "modele_nom": cfg["name"],
        "modele_hf_id": cfg["hf_id"],
        "duree_chargement_s": round(t_load, 2),
        "duree_inference_totale_s": round(duree_totale, 2),
        "duree_inference_moyenne_s": round(duree_moyenne, 4),
        "n_fiches": len(gold_set),
        "predictions": predictions,
    }


def main() -> None:
    print("=" * 60)
    print("  SKILLNAV §N2.1 : inférence des 3 modèles NER")
    print("=" * 60)

    if not GOLD_SET_PATH.exists():
        print(f"\nERREUR : gold set absent ({GOLD_SET_PATH}).")
        print("Lancer d'abord : python scripts/ner/01_build_gold_set.py")
        sys.exit(1)

    gold_set = charger_gold_set()
    print(f"\n{len(gold_set)} fiches chargées depuis le gold set")

    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

    for model_key in MODELES:
        resultat = inferer_modele(model_key, gold_set)
        chemin = PREDICTIONS_DIR / f"{model_key}.json"
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(resultat, f, ensure_ascii=False, indent=2)
        print(f"  Prédictions sauvegardées : {chemin.relative_to(chemin.parent.parent.parent.parent)}")

    print("\n=== Inférence des 3 modèles terminée ===")


if __name__ == "__main__":
    main()
