# Projet de fin de module — Analyse de Web (M242)

> **Énoncé officiel transcrit du PDF** : `Projet Final Analyse de Web_Sujet 1.pdf`
> Université Abdelmalek Essaâdi · École Nationale des Sciences Appliquées · Tétouan
> Département IA & Digitalisation · Filière Sciences des Données, Big Data & IA
> Module **Analyse de Web (M242)** · Prof. **Imad Sassi**
> Année 2025-2026

---

## Sujet du Projet (1)

**Observatoire de Data Science et l'IA : Ingénierie de la donnée et Analyse prédictive de l'Évolution des Compétences IA par le Web Mining.**

---

## Présentation Générale

- **Modalités** : Travail collaboratif en groupes
- **Objectif** : Concevoir un **pipeline complet de Web Intelligence**, allant de la collecte de données brutes sur le Web à la modélisation prédictive des tendances du marché de l'emploi technologique

---

## Contexte & Problématique

L'essor du Big Data et de l'Intelligence Artificielle (IA) modifie profondément le paysage des compétences et des métiers. LinkedIn et d'autres plateformes professionnelles offrent une source précieuse de données permettant d'analyser les tendances actuelles et de projeter les évolutions futures.

Ce sujet a pour objectif d'exploiter les techniques d'**Analyse de Web** afin d'extraire, analyser et modéliser l'évolution des compétences en Data Science et IA.

---

## Architecture des Données et Méthodologie

> Il est demandé d'aborder les **trois axes piliers de Web Mining** (Content, Structure, Usage) :

### Axe 1 — Web Content Mining (Intelligence Sémantique & Extraction du contenu)

Conception de pipelines d'ingestion **asynchrones** et déploiement de modèles **Transformers (NER)** pour l'extraction de vecteurs de compétences et la classification automatisée des domaines d'expertise à partir de **données non structurées**.

### Axe 2 — Web Structure Mining (Graph Mining & Analyse des liens et réseaux)

Modélisation des écosystèmes technologiques en **graphes complexes** pour quantifier l'autorité (**PageRank**) et détecter des **communautés (Louvain)**, identifiant ainsi les dépendances critiques et les pôles d'influence du marché.

### Axe 3 — Web Usage Mining (Analyse Prédictive & Usage Forecasting)

Développement de modèles de **prédiction de séries temporelles** et de **moteurs de recommandation** basés sur les signaux faibles (Google Trends, engagement) pour anticiper l'émergence des futures compétences clés.

---

## Spécifications Techniques & Exigences

> Le projet doit **impérativement** respecter un ensemble de standards et certaines spécifications.

### 1. Architecture de Stockage Big Data & Hybride

Mise en œuvre de bases de données **NoSQL** (MongoDB, Neo4J, ElasticSearch ou Cassandra) pour gérer la **vélocité** et la **variété** des données (Content, Structure, Usage).

### 2. Modélisation IA

L'analyse doit obligatoirement reposer sur une **étude comparative de trois approches algorithmiques distinctes** pour garantir la robustesse des prédictions.

### 3. Data Quality Framework

Analyse critique de la qualité des données (**complétude**, **bruit**, **biais algorithmiques**) dans un contexte Big Data.

### 4. Éthique & Conformité

Respect strict du **RGPD** et des politiques **robots.txt** des sites scrapés. Toute collecte doit être **justifiée et anonymisée**.

---

## Note du Prof

> En tant qu'**Ingénieurs Data**, vous êtes censé être capables d'**industrialiser une solution** pour la problématique étudiée. Ainsi, **la qualité de la justification des outils choisis** (pourquoi tel algorithme ? pourquoi telle base NoSQL ?) sera un **critère majeur d'évaluation**.

---

## Livrables Finaux (6)

| # | Livrable | Détail |
|---|---|---|
| 1 | **Scripts de Collecte** | Code documenté pour le scraping et l'appel aux API |
| 2 | **Base de Données Hybride** | Base de données consolidée, structurée et prête à l'emploi |
| 3 | **Pipeline IA** | Modèles prédictifs entraînés, testés et validés par des métriques d'évaluation précises |
| 4 | **Dashboard Interactif** | Dashboard interactif déployé, fonctionnel et conforme aux exigences des utilisateurs |
| 5 | **Rapport** | Document explicatif de la méthodologie pour assurer la **reproductibilité** du projet, incluant une analyse des résultats avec des justifications des choix d'algorithmes et des recommandations pour les professionnels |
| 6 | **Présentation** | Présentation orale synthétique du projet |

---

## Modalités de Rendu

- **Format** : archive zip nommée `Projet Final_Analyse de Web_Noms et Prénoms des étudiants` ou un lien Drive
- **Destinataire** : `i.sassi@uae.ac.ma`
- **Date limite** : **Jeudi 28 Mai**

---

## Soutenance

Le projet sera évalué sur la base de la **pertinence** et de l'**efficacité de la solution proposée** suivi d'une **présentation du projet**.

Chaque groupe disposera de **25 minutes de soutenance** :

- **15 minutes** pour la présentation
- **10 minutes** de questions

---

## ✅ Checklist de conformité au sujet (auto-audit SKILLNAV)

| Exigence | Statut |
|---|:-:|
| Pipeline complet de Web Intelligence | ✅ |
| Couverture **Axe 1 — Content Mining** (NER Transformers) | ✅ §N1 PRD |
| Couverture **Axe 2 — Structure Mining** (PageRank + Louvain) | ✅ §N1 PRD |
| Couverture **Axe 3 — Usage Mining** (séries temporelles) | ✅ §N1 PRD |
| Bases NoSQL (MongoDB / Neo4J / ElasticSearch / Cassandra) | ✅ Trio MongoDB + Neo4J + Elastic |
| Étude comparative de **3 approches algorithmiques** | ✅ §N2 PRD |
| Data Quality Framework (complétude, bruit, biais) | ✅ §N3 PRD |
| RGPD strict + robots.txt | ✅ §N4 PRD + DPIA séparée |
| Justification des outils (critère majeur) | ✅ Documenté dans `docs/tools/*.md` |
| 6 livrables (scripts, BDD, pipeline IA, dashboard, rapport, présentation) | 🔄 En cours |
| Soutenance 25 min (15 + 10) | 🔄 Plan §22 PRD |
