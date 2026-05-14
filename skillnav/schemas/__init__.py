"""Pydantic v2 models — source de vérité unique pour MongoDB / Neo4j / Elasticsearch.

Voir PRD §7.5. Tout converter (`schemas/converters/`) doit dériver de ces modèles.
Une mutation de schéma casse au type-check tous les converters — c'est voulu.

Modules à implémenter :

- `job.py`        : RawJob, JobExtraction
- `ner.py`        : NerAnnotation, Entity
- `graph.py`      : SkillNode, JobNode, SkillFamilyNode, Edge
- `timeseries.py` : SkillTimeSeries, Forecast
"""
