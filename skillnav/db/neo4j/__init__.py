"""Neo4j AuraDB — graphe Skill ↔ Job ↔ Family (PRD §7.3).

Modèle :

- (:Skill)-[:CO_OCCURS_WITH {weight}]->(:Skill)
- (:Job)-[:REQUIRES {confidence}]->(:Skill)
- (:Skill)-[:BELONGS_TO]->(:SkillFamily)
- (:Job)-[:FROM_SOURCE]->(:Source)
"""
