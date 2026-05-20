"""Consolide les donnees NER en un seul snapshot pour le dashboard.

Sortie : web/src/lib/ner_snapshot.json
Source : data/ner/{ner_gold_set.json, evaluation_n2_1.json, predictions/*.json}
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NER = ROOT / "data" / "ner"
OUT = ROOT / "web" / "src" / "lib" / "ner_snapshot.json"


def main() -> None:
    gold = json.loads((NER / "ner_gold_set.json").read_text(encoding="utf-8"))
    evaluation = json.loads((NER / "evaluation_n2_1.json").read_text(encoding="utf-8"))

    # Index gold par job_id
    gold_by_id = {g["job_id"]: g for g in gold}

    # Charge les predictions par modele
    models = ["bert_multilingual", "camembert", "distilbert", "gliner"]
    predictions = {}
    for m in models:
        try:
            data = json.loads((NER / "predictions" / f"{m}.json").read_text(encoding="utf-8"))
        except FileNotFoundError:
            continue
        # Index par job_id → liste entités
        preds_by_id: dict[str, list[dict]] = {}
        for p in data.get("predictions", []):
            preds_by_id[p["job_id"]] = p.get("entites", [])
        predictions[m] = {
            "nom": data.get("modele_nom", m),
            "hf_id": data.get("modele_hf_id", ""),
            "duree_chargement_s": data.get("duree_chargement_s"),
            "duree_inference_moyenne_s": data.get("duree_inference_moyenne_s"),
            "predictions_by_job_id": preds_by_id,
        }

    # Identifie le modele retenu (meilleur F1)
    best = max(evaluation, key=lambda e: e["f1"])

    snapshot = {
        "meta": {
            "n_fiches": len(gold),
            "n_skills_gold_total": sum(len(g.get("gold_skills", [])) for g in gold),
            "models_evaluated": [e["modele"] for e in evaluation],
            "models_with_predictions": list(predictions.keys()),
            "best_model_id": best["modele"],
            "best_model_nom": best["modele_nom"],
            "best_f1": best["f1"],
        },
        "evaluation": evaluation,
        "gold": [
            {
                "job_id": g["job_id"],
                "origine": g.get("origine"),
                "source": g.get("source"),
                "ai_type": g.get("ai_type"),
                "title": g.get("title"),
                "title_canonical": g.get("title_canonical"),
                "company": g.get("company"),
                "text": g.get("text", ""),
                "gold_skills": g.get("gold_skills", []),
                "gold_company": g.get("gold_company"),
            }
            for g in gold
        ],
        "predictions": predictions,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    size_ko = OUT.stat().st_size // 1024
    print(f"Ecrit : {OUT.relative_to(ROOT)} ({size_ko} Ko)")
    print()
    print("=== Resume ===")
    print(f"  fiches gold        : {snapshot['meta']['n_fiches']}")
    print(f"  skills gold total  : {snapshot['meta']['n_skills_gold_total']}")
    print(f"  modeles evalues    : {snapshot['meta']['models_evaluated']}")
    print(f"  meilleur modele    : {snapshot['meta']['best_model_nom']} (F1={snapshot['meta']['best_f1']:.3f})")


if __name__ == "__main__":
    main()
