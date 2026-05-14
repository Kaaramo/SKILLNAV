"""Connexions DB — NoSQL polyglotte (PRD §7).

- `mongodb/`      : motor — source of truth (raw_jobs, extracted_jobs, ner_annotations, …)
- `neo4j/`        : neo4j-driver — graphe Skill ↔ Job ↔ Family
- `elasticsearch/`: elasticsearch — indices jobs_search, skills_timeseries
"""
