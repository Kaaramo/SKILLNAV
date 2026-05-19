# Étude 04 — Détection de compétences émergentes

> Axe Web Mining : transversal (touche Content + Usage)
> Statut : **planifiée pour le sprint 2**, non livrée dans la V1

Cette page documente honnêtement ce qui reste à faire. Le sujet n'impose pas
les 4 études — 3 suffisent à valider le livrable 3 — mais l'ajout de cette
quatrième étude est dans la feuille de route du projet.

---

## 1. Problème

Au-delà des compétences déjà connues et présentes en volume dans le corpus,
on veut détecter les compétences **en train d'émerger** : peu fréquentes
aujourd'hui mais avec une dynamique de croissance forte sur les 6-12 derniers
mois.

Question :

> *Comment identifier de manière automatique les compétences qui passeront
> dominantes dans les 6 à 12 mois ?*

C'est typiquement le genre d'information que SKILLNAV vise à fournir à la
direction des études d'une ENSA pour anticiper la mise à jour des
programmes.

---

## 2. Approches envisagées

Trois angles concurrents, chacun avec sa logique propre :

### A. Heuristique de tendance

Calcul simple d'un score d'émergence par compétence :

```
emergence_score = (count_last_3_months / total_count) × growth_rate
```

Avantages : interprétable, sans entraînement, sans biais d'overfit.
Inconvénient : ne capture pas les compétences qui apparaissent ex nihilo.

### B. Classification supervisée — XGBoost

Construire un jeu d'entraînement de compétences passées :

* Positifs : compétences qui ont émergé entre 2023 et 2025 (~30 cas)
* Négatifs : compétences stables ou en déclin (~100 cas)

Features : courbe de fréquence, ratio début/fin de période, présence dans
les communautés émergentes du graphe, co-occurrences avec des compétences
GenAI.

Sortie : pour chaque compétence du corpus, probabilité d'émergence en 2026.

### C. Clustering non supervisé — KMeans sur trajectoires

Représenter chaque compétence comme un vecteur (sa courbe de fréquence
normalisée sur 24 mois), puis clusteriser ces vecteurs en K=5 trajectoires
types. Le cluster « croissance exponentielle récente » contient les
compétences émergentes.

Avantage : pas besoin d'annoter le jeu d'entraînement.
Inconvénient : choix de K subjectif.

---

## 3. Plan d'évaluation

| Métrique | Comment |
|---|---|
| **Précision @ Top 20** | sur les 20 compétences les plus émergentes selon chaque méthode, combien sont réellement émergentes (vérification manuelle par le binôme) |
| **Rappel humain** | sur une liste de 15 compétences que le binôme considère a priori émergentes, combien chaque méthode capture |
| **Faux positifs notables** | quelles compétences sont signalées émergentes alors qu'elles ne le sont pas (analyse qualitative) |

L'évaluation finale est manuelle car il n'existe pas de ground truth
publique sur l'émergence de compétences IA.

---

## 4. Jeu de test à construire

20 compétences candidates, sélectionnées par le binôme et croisées avec un
panel d'experts (à minima Pr. Sassi pour la validation académique).

Format attendu :

```json
{
  "skill": "AI Agents",
  "is_emerging_truth": true,
  "rationale": "explosion en 2025 (LangChain, AutoGPT, CrewAI), encore peu vu dans les fiches MA"
}
```

---

## 5. Livrables attendus pour cette étude

Quand l'étude 04 sera complète, on ajoutera ici :

* Le tableau des 3 méthodes avec leurs précisions @ Top 20
* L'analyse du gagnant et le paradoxe éventuel
* Le verdict V1.5
* La liste finale des compétences émergentes 2026, intégrée au dashboard

---

## 6. Pourquoi ne pas l'avoir fait pour la V1

Choix conscient : les 3 études déjà livrées (NER, communautés, forecasting)
couvrent les 3 axes Web Mining explicitement nommés dans le sujet. L'étude 04
est un **bonus** qui transformerait le livrable 3 d'« acceptable » en
« exhaustif ».

Étant donné la contrainte de temps avant la soutenance, le binôme a préféré
livrer 3 études complètes et discutées plutôt que 4 études bâclées. Cette
priorisation est elle-même une décision méthodologique qui pourra être
discutée à l'oral.

Si le sprint 2 (entre la V1 et la version finale) permet de compléter cette
étude, elle sera intégrée. Sinon, elle restera documentée comme **dette
technique assumée**.
