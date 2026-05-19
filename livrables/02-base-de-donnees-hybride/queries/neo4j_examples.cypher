// =====================================================================
// SKILLNAV — Exemples de requêtes Cypher sur Neo4j AuraDB
// =====================================================================
//
// 5 requêtes représentatives, exécutables dans Neo4j Browser ou via le
// driver Python (skillnav.db.neo4j.client.Neo4jClient).
//
// Toutes les requêtes ont été testées sur la base réelle au 2026-05-17.
// =====================================================================


// ---------------------------------------------------------------------
// 1. Volumétrie : combien de nœuds et d'arêtes ?
// ---------------------------------------------------------------------
CALL {
  MATCH (s:Skill)        RETURN count(s) AS skills
}
CALL {
  MATCH (j:Job)          RETURN count(j) AS jobs
}
CALL {
  MATCH (c:Company)      RETURN count(c) AS companies
}
CALL {
  MATCH (f:SkillFamily)  RETURN count(f) AS families
}
CALL {
  MATCH ()-[r:CO_OCCURS_WITH]-() RETURN count(r) / 2 AS co_occurs
}
CALL {
  MATCH ()-[r:REQUIRES]->()      RETURN count(r) AS requires
}
RETURN skills, jobs, companies, families, co_occurs, requires;

/*
Résultat attendu (ordre de grandeur) :
+--------+------+-----------+----------+-----------+----------+
| skills | jobs | companies | families | co_occurs | requires |
+--------+------+-----------+----------+-----------+----------+
| 2187   | 3467 | 900       | 14       | 38000     | 22000    |
+--------+------+-----------+----------+-----------+----------+
*/


// ---------------------------------------------------------------------
// 2. Top 10 PageRank — compétences les plus centrales du graphe
// ---------------------------------------------------------------------
MATCH (s:Skill)
WHERE s.pagerank_score IS NOT NULL
RETURN s.name AS skill, s.family AS famille, round(s.pagerank_score * 10000) / 10000 AS pagerank
ORDER BY s.pagerank_score DESC
LIMIT 10;

/*
Résultat type :
+-------------------+---------------------+----------+
| skill             | famille             | pagerank |
+-------------------+---------------------+----------+
| Python            | Programming         | 0.0421   |
| Machine Learning  | Machine Learning    | 0.0312   |
| SQL               | Databases           | 0.0287   |
| Deep Learning     | Deep Learning       | 0.0254   |
| ...                                                |
+-------------------+---------------------+----------+
*/


// ---------------------------------------------------------------------
// 3. Voisinage d'une compétence : qui co-occure le plus avec "Python" ?
// ---------------------------------------------------------------------
MATCH (a:Skill {name: "Python"})-[r:CO_OCCURS_WITH]-(b:Skill)
RETURN b.name AS voisin, b.family AS famille, r.weight AS co_offres
ORDER BY r.weight DESC
LIMIT 15;

/*
Résultat type :
+-------------------+---------------------+-----------+
| voisin            | famille             | co_offres |
+-------------------+---------------------+-----------+
| SQL               | Databases           | 1248      |
| Machine Learning  | Machine Learning    | 1187      |
| TensorFlow        | Deep Learning       | 754       |
| ...                                                 |
+-------------------+---------------------+-----------+

Type d'analyse impossible (ou très coûteuse) en Mongo : ici en ~5 ms.
*/


// ---------------------------------------------------------------------
// 4. Communautés Louvain : taille des 5 plus grandes
// ---------------------------------------------------------------------
MATCH (s:Skill)
WHERE s.community_id IS NOT NULL AND s.community_id >= 0
WITH s.community_id AS community, collect(s.name) AS members, count(*) AS taille
ORDER BY taille DESC
LIMIT 5
RETURN community,
       taille,
       members[0..5] AS apercu_5_premiers_membres;

/*
Résultat type :
+-----------+--------+--------------------------------------------------+
| community | taille | apercu_5_premiers_membres                        |
+-----------+--------+--------------------------------------------------+
| 0         | 312    | ["Python","SQL","Pandas","NumPy","scikit-learn"] |
| 3         | 245    | ["AWS","Docker","Kubernetes","Terraform","CI/CD"]|
| 1         | 198    | ["LLM","RAG","LangChain","OpenAI API","Vector"]  |
| ...                                                                   |
+-----------+--------+--------------------------------------------------+
*/


// ---------------------------------------------------------------------
// 5. Compétences requises pour une famille métier donnée
// ---------------------------------------------------------------------
MATCH (j:Job)-[:REQUIRES]->(s:Skill)
WHERE j.country = "MA"
WITH s, count(j) AS frequence
WHERE frequence >= 10
RETURN s.name AS skill, s.family AS famille, frequence
ORDER BY frequence DESC
LIMIT 20;

/*
Résultat type (Maroc) :
+--------------------+-------------------+-----------+
| skill              | famille           | frequence |
+--------------------+-------------------+-----------+
| SQL                | Databases         | 218       |
| Python             | Programming       | 187       |
| Power BI           | BI & Analytics    | 105       |
| Excel              | BI & Analytics    | 89        |
| ...                                                |
+--------------------+-------------------+-----------+
*/
