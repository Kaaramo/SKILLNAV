"""Évaluation des 3 modèles NER : Précision / Rappel / F1 + tableau §N2.1.

Métriques calculées :

1. **Skills** (la métrique principale, alignée sur l'objectif SKILLNAV) :
   pour chaque fiche, on compare la liste `gold_skills` à l'ensemble des
   tokens texte des entités prédites par le modèle (toutes catégories).
   Une compétence gold est considérée « détectée » si un de ses tokens
   apparaît comme sous-chaîne case-insensitive dans une entité prédite.

2. **Précision** = TP / (TP + FP)
   « Quelle proportion des entités prédites est dans le gold ? »

3. **Rappel** = TP / (TP + FN)
   « Quelle proportion du gold a été trouvée par le modèle ? »

4. **F1** = harmonic mean(P, R) = 2 P R / (P + R)

5. **Temps d'inférence moyen** par fiche (issu de `02_run_inference.py`).

Le tableau final est sauvé au format Markdown dans
`data/ner/tableau_n2_1.md`, prêt à coller dans le rapport L5.

Exécution : python scripts/ner/03_evaluate.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (  # noqa: E402
    EVALUATION_PATH,
    GOLD_SET_PATH,
    MODELES,
    PREDICTIONS_DIR,
    TABLEAU_MD_PATH,
)


def charger_gold_set() -> list[dict]:
    with open(GOLD_SET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def charger_predictions(model_key: str) -> dict:
    chemin = PREDICTIONS_DIR / f"{model_key}.json"
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def texte_normalise(s: str) -> str:
    """Strip + lowercase + suppression de la ponctuation à l'extrémité."""
    return s.strip().lower().strip(".,;:()[]{}\"'`")


def skill_apparait_dans_entites(skill: str, entites: list[dict]) -> bool:
    """Vérifie si une compétence gold est détectée dans les entités prédites.

    Logique souple : on cherche si le texte du skill (ou une de ses parties
    significatives > 2 caractères) apparaît dans le texte d'au moins une
    entité prédite, en ignorant la casse.
    """
    skill_norm = texte_normalise(skill)
    if not skill_norm:
        return False

    for e in entites:
        entite_norm = texte_normalise(e.get("text", ""))
        if not entite_norm:
            continue
        if skill_norm in entite_norm or entite_norm in skill_norm:
            return True
        # Match sur les mots individuels (utile pour compétences multi-mots)
        mots_skill = {m for m in skill_norm.split() if len(m) > 2}
        mots_entite = {m for m in entite_norm.split() if len(m) > 2}
        if mots_skill and mots_entite and (mots_skill & mots_entite):
            return True
    return False


def entite_predite_correspond_a_gold(entite: dict, gold_skills: list[str]) -> bool:
    """Vérifie si une entité prédite correspond à un skill gold."""
    entite_norm = texte_normalise(entite.get("text", ""))
    if not entite_norm:
        return False
    for skill in gold_skills:
        skill_norm = texte_normalise(skill)
        if not skill_norm:
            continue
        if skill_norm in entite_norm or entite_norm in skill_norm:
            return True
        mots_skill = {m for m in skill_norm.split() if len(m) > 2}
        mots_entite = {m for m in entite_norm.split() if len(m) > 2}
        if mots_skill and mots_entite and (mots_skill & mots_entite):
            return True
    return False


def evaluer_modele(model_key: str, gold_set: list[dict], pred_data: dict) -> dict:
    """Calcule P / R / F1 d'un modèle sur le gold set."""
    pred_par_id = {p["job_id"]: p for p in pred_data.get("predictions", [])}

    tp = 0  # entités prédites correctes
    fp = 0  # entités prédites mais hors gold
    fn = 0  # skills gold non détectés
    total_pred = 0
    total_gold = 0
    accord_par_fiche: list[float] = []

    for fiche in gold_set:
        gold_skills = fiche.get("gold_skills", [])
        total_gold += len(gold_skills)
        entites = pred_par_id.get(fiche["job_id"], {}).get("entites", [])
        total_pred += len(entites)

        # Comptage TP/FN (orienté gold)
        n_detectes = 0
        for skill in gold_skills:
            if skill_apparait_dans_entites(skill, entites):
                n_detectes += 1
        fn += len(gold_skills) - n_detectes
        tp_fiche = n_detectes

        # Comptage FP (orienté prédictions)
        fp_fiche = 0
        for entite in entites:
            if not entite_predite_correspond_a_gold(entite, gold_skills):
                fp_fiche += 1
        tp += tp_fiche
        fp += fp_fiche

        accord = (
            tp_fiche / max(len(gold_skills), 1)
            if gold_skills
            else (1.0 if not entites else 0.0)
        )
        accord_par_fiche.append(accord)

    precision = tp / max(tp + fp, 1)
    rappel = tp / max(tp + fn, 1)
    f1 = (2 * precision * rappel / max(precision + rappel, 1e-9)) if (precision + rappel) else 0.0

    return {
        "modele": model_key,
        "modele_nom": MODELES[model_key]["name"],
        "modele_hf_id": MODELES[model_key]["hf_id"],
        "taille_params": MODELES[model_key]["taille_params"],
        "n_fiches": len(gold_set),
        "n_entites_predites": total_pred,
        "n_skills_gold": total_gold,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 4),
        "rappel": round(rappel, 4),
        "f1": round(f1, 4),
        "rappel_moyen_par_fiche": round(sum(accord_par_fiche) / max(len(accord_par_fiche), 1), 4),
        "duree_inference_moyenne_s": pred_data.get("duree_inference_moyenne_s", 0.0),
        "duree_chargement_s": pred_data.get("duree_chargement_s", 0.0),
    }


def construire_tableau_markdown(resultats: list[dict]) -> str:
    """Tableau Markdown prêt pour le rapport L5 §N2.1."""
    lignes = [
        "# Tableau §N2.1 — Étude comparative NER sur 30 fiches gold",
        "",
        "| Modèle | Paramètres | Précision | Rappel | F1 | Temps moyen (s/fiche) | Entités prédites | Skills gold détectés |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in resultats:
        lignes.append(
            f"| **{r['modele_nom']}** | {r['taille_params']} | "
            f"{r['precision']:.3f} | {r['rappel']:.3f} | **{r['f1']:.3f}** | "
            f"{r['duree_inference_moyenne_s']:.2f} | "
            f"{r['n_entites_predites']} | "
            f"{r['tp']} / {r['n_skills_gold']} |"
        )

    lignes.extend([
        "",
        "## Lecture du tableau",
        "",
        "- **Précision** : proportion d'entités prédites qui correspondent à une compétence du gold set.",
        "- **Rappel** : proportion des compétences gold qui ont été détectées par le modèle.",
        "- **F1** : moyenne harmonique de la précision et du rappel (métrique synthétique).",
        "- **Temps moyen** : secondes d'inférence par fiche (CPU, fiches de longueur moyenne ~1500 caractères).",
        "",
        "## Choix retenu pour la V1 SKILLNAV",
        "",
        "Le modèle retenu pour la pipeline de production est celui qui présente le meilleur F1",
        "tout en gardant un temps d'inférence acceptable pour le traitement batch des "
        "3 467 offres collectées.",
    ])
    return "\n".join(lignes) + "\n"


def main() -> None:
    print("=" * 60)
    print("  SKILLNAV §N2.1 : évaluation P/R/F1 des 3 modèles")
    print("=" * 60)

    gold_set = charger_gold_set()
    print(f"\nGold set : {len(gold_set)} fiches")

    resultats: list[dict] = []
    for model_key in MODELES:
        chemin = PREDICTIONS_DIR / f"{model_key}.json"
        if not chemin.exists():
            print(f"\n[!] Prédictions manquantes pour {model_key} ({chemin})")
            continue
        pred = charger_predictions(model_key)
        if pred.get("erreur"):
            print(f"\n[!] Modèle {model_key} en erreur, ignoré : {pred['erreur'][:120]}")
            continue
        r = evaluer_modele(model_key, gold_set, pred)
        resultats.append(r)
        print(f"\n  {r['modele_nom']:<22}  P={r['precision']:.3f}  R={r['rappel']:.3f}  F1={r['f1']:.3f}  "
              f"t={r['duree_inference_moyenne_s']:.2f}s/fiche")

    EVALUATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EVALUATION_PATH, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)
    print(f"\n  Évaluation JSON sauvegardée : {EVALUATION_PATH.relative_to(EVALUATION_PATH.parent.parent.parent)}")

    tableau = construire_tableau_markdown(resultats)
    with open(TABLEAU_MD_PATH, "w", encoding="utf-8") as f:
        f.write(tableau)
    print(f"  Tableau Markdown sauvegardé : {TABLEAU_MD_PATH.relative_to(TABLEAU_MD_PATH.parent.parent.parent)}")

    if resultats:
        best = max(resultats, key=lambda r: r["f1"])
        print(f"\n=== Meilleur F1 : {best['modele_nom']} ({best['f1']:.3f}) ===")
        print(f"=== Choix retenu pour V1 SKILLNAV : {best['modele_nom']} ===")


if __name__ == "__main__":
    main()
