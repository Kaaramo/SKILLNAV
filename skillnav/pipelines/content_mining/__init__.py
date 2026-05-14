"""Content Mining — NER + extraction Pydantic AI (PRD §6.B, §9).

Étapes :

1. Cleaning (Crawl4AI fournit du markdown déjà propre · selectolax pour
   parsing HTML rapide si besoin · fasttext-langdetect pour la langue ·
   spaCy pour la tokenization)
2. Extraction structurée (Pydantic AI + Claude Sonnet 4.5)
3. NER comparatif 3 modèles HuggingFace (BERT-multi · CamemBERT · DistilBERT)
4. Normalisation taxonomique (sentence-transformers + cosine sim ≥ 0.85)
"""
