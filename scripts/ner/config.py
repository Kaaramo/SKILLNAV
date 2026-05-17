"""Configuration centrale de l'étude NER §N2.1.

Définit les trois modèles HuggingFace comparés, les chemins, et les paramètres
de la sélection du gold set.
"""

from __future__ import annotations
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# ----------------------------------------------------------------------------
# Modèles HuggingFace comparés
# ----------------------------------------------------------------------------
MODELES = {
    "bert_multilingual": {
        "name": "BERT multilingue",
        "hf_id": "Davlan/bert-base-multilingual-cased-ner-hrl",
        "description": "BERT 110M paramètres, fine-tuné sur 10 langues (dont FR/EN/AR) "
                       "pour NER (corpus HRL/CoNLL).",
        "couverture_langues": ["fr", "en", "ar", "es", "de", "..."],
        "taille_params": "110M",
    },
    "camembert": {
        "name": "CamemBERT-NER",
        "hf_id": "Jean-Baptiste/camembert-ner",
        "description": "CamemBERT 110M paramètres, fine-tuné sur corpus français "
                       "(Wikiner-fr). Spécialisé FR.",
        "couverture_langues": ["fr"],
        "taille_params": "110M",
    },
    "distilbert": {
        "name": "DistilBERT-NER",
        "hf_id": "dslim/distilbert-NER",
        "description": "DistilBERT 66M paramètres, version compressée de BERT "
                       "fine-tunée sur CoNLL-03 (anglais).",
        "couverture_langues": ["en"],
        "taille_params": "66M",
    },
}

# ----------------------------------------------------------------------------
# Sélection du gold set
# ----------------------------------------------------------------------------
N_FICHES_GOLD = 30           # taille du gold set
SEED = 42                    # reproductibilité
QUOTA_MAROC = 10             # ~33 %
QUOTA_INTL = 20              # ~67 % (cohérent avec la composition du corpus)

# Diversité ai_type recherchée (proportionnel au corpus)
QUOTAS_AI_TYPE = {
    "ai-first":   12,
    "ai-support":  6,
    "ml-first":    6,
    "non-ai":      6,
}

# ----------------------------------------------------------------------------
# Chemins
# ----------------------------------------------------------------------------
DATA_JOBS_JSONL = REPO / "data" / "jobs.jsonl"
DATA_NER_DIR = REPO / "data" / "ner"
GOLD_SET_PATH = DATA_NER_DIR / "ner_gold_set.json"
PREDICTIONS_DIR = DATA_NER_DIR / "predictions"
EVALUATION_PATH = DATA_NER_DIR / "evaluation_n2_1.json"
TABLEAU_MD_PATH = DATA_NER_DIR / "tableau_n2_1.md"

# ----------------------------------------------------------------------------
# Étiquettes d'entités cibles
# ----------------------------------------------------------------------------
# Les modèles HuggingFace renvoient des labels comme PER, ORG, LOC, MISC.
# Pour SKILLNAV on s'intéresse principalement à :
ENTITES_PERTINENTES = {
    "ORG": "company",     # entreprise qui recrute
    "LOC": "location",    # ville / pays
    "PER": "person",      # nom de recruteur ou contact (devrait être rare/absent)
    "MISC": "misc",       # divers (peut contenir des skills)
}
