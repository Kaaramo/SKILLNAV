"""Content Mining — NER + extraction Pydantic AI (PRD §6.B, §9).

Étapes : cleaning (BeautifulSoup + langid + spaCy) → extraction structurée
(Pydantic AI + Claude Sonnet 4.5) → NER comparatif 3 modèles HuggingFace
(BERT-multi · CamemBERT · DistilBERT) → normalisation taxonomique
(sentence-transformers + cosine sim).
"""
