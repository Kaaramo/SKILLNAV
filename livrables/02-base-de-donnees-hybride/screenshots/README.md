# Captures à produire — preuve visuelle que les 3 bases tournent

Les 3 captures ci-dessous prouvent que les trois technologies sont
effectivement provisionnées et peuplées. Les générer à la dernière minute
(la veille du rendu) pour avoir des chiffres frais.

| Fichier attendu | Contenu attendu | Où le capturer |
|---|---|---|
| `atlas_dashboard.png` | Vue de la collection `skillnav.jobs` montrant le compteur **3 467 documents** + la liste des indexes (text + multikey) | https://cloud.mongodb.com → cluster SKILLNAV → Database → `skillnav.jobs` → onglet **Indexes** |
| `neo4j_graph_view.png` | Visualisation Neo4j Browser d'un sous-graphe Skill-Skill (~50 nœuds, ~150 arêtes) avec les couleurs de famille | https://workspace-preview.neo4j.io → exécuter la requête ci-dessous puis bouton **Graph** |
| `bonsai_stats.png` | Onglet « Stats » du dashboard Bonsai montrant l'index `skillnav_jobs` avec **3 467 docs** et la taille de l'index | https://app.bonsai.io → cluster → onglet **Indices** |

## Requête à exécuter dans Neo4j Browser avant la capture

```cypher
MATCH (a:Skill)-[r:CO_OCCURS_WITH]-(b:Skill)
WHERE r.weight >= 30
RETURN a, r, b
LIMIT 200
```

Cliquer sur l'icône `Graph` (à gauche du panneau résultat), zoomer pour cadrer
le sous-graphe au centre, puis capture d'écran de toute la fenêtre.

## Conseils de capture

* Cadrer sur la zone qui contient les chiffres importants ; éviter les barres
  de navigation et les URL qui montrent des credentials.
* Format PNG, largeur 1 400-1 800 px (le rendu reste net sans peser trop).
* Si le nom du cluster ou un identifiant sensible apparaît, le flouter ou le
  recadrer.

Une fois les 3 fichiers déposés ici, supprimer ce `README.md` (ou le laisser,
il documente la démarche pour les contributeurs futurs).
