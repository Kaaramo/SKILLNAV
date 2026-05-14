# Plan de soutenance — SKILLNAV

> Document de répétition autonome — extrait et étendu de la §22 du PRD.

**Date** : 28 mai 2026
**Format** : 15 min présentation (avec démo live intégrée) + 10 min Q&A
**Équipe** : Karamo Sylla + Bachirou Konaté
**Module** : M242 Analyse de Web · ENSA-Tétouan · Pr. Imad Sassi

---

## 1. Objectif de la soutenance

Démontrer en 25 minutes que SKILLNAV répond intégralement aux exigences du sujet imposé :

1. Couverture des **3 axes Web Mining** (Content, Structure, Usage) — équilibre démontrable
2. Architecture **NoSQL polyglotte** justifiée
3. **HuggingFace Transformers** intégrés
4. **Étude comparative chiffrée** (4 comparaisons : NER, communautés, forecasting, émergence)
5. **RGPD documentée**
6. **6 livrables** remis

---

## 2. Structure minute par minute (15 min)

| Minute | Section | Contenu | Lead | Slide |
|:---:|---|---|:---:|:---:|
| M0–M1 | Ouverture | Titre, équipe, contexte M242, objectif soutenance | Karamo | 1–2 |
| M1–M2 | Sujet imposé + 3 axes | Reformulation sujet + tableau couverture 3 axes | Karamo | 3 |
| M2–M4 | Architecture polyglotte | Schéma global + justification MongoDB + Neo4j + ES | Karamo | 4–5 |
| M4–M5 | Stack technique | Tableau condensé + 3 décisions clés (ADR-02, 03, 04) | Karamo | 6 |
| M5–M9 | **Démo live dashboard** | `skillnav.vercel.app` — 5 pages | Karamo | 7 |
| M9–M12 | Résultats étude comparative | 4 tableaux chiffrés (N2.1–N2.4) | Karamo | 8–11 |
| M12–M13 | Data Quality + biais | Page `/quality` + transparence biais | Bachirou Konaté | 12 |
| M13–M14 | RGPD + robots.txt | Base légale + protocole + DPIA | Bachirou Konaté | 13 |
| M14–M15 | Conclusion + roadmap | 6 livrables remis + V1.5 / V2 | Bachirou Konaté | 14–15 |

---

## 3. Démo live — script précis (4 min inclus dans M5–M9)

| Étape | Page | Action | Durée | Verbatim type |
|---|---|---|:---:|---|
| 1 | `/` | Pointer KPIs marché IA, volume X offres, top 5 compétences | 15 s | « Voici l'overview en temps réel. 1 247 offres, top compétences PyTorch / Python / SQL. » |
| 2 | `/graph` | Zoom sur cluster « NLP », communauté Louvain colorée, hover top 5 PageRank | 60 s | « Le graphe Neo4j révèle des communautés. Voici la communauté NLP, isolée par Louvain avec une modularité de 0.X. PageRank identifie BERT comme nœud central. » |
| 3 | `/forecasting` | Sélectionner « Transformers » → ARIMA + Prophet + LSTM superposés, lire MAPE chiffré | 60 s | « Sur la compétence Transformers, Prophet bat ARIMA et LSTM avec un MAPE de X %. Voici l'intervalle de confiance à 95 %. » |
| 4 | `/ner-explorer` | Afficher offre annotée, basculer BERT → CamemBERT → DistilBERT | 60 s | « Sur cette offre française, CamemBERT identifie correctement « PyTorch » comme FRAMEWORK alors que BERT-multi rate cette entité. » |
| 5 | `/comparative-study` | Montrer les 4 tableaux récapitulatifs synthétiques | 45 s | « Voici l'étude comparative complète : NER, communautés, forecasting, émergence — chacun avec protocole, métriques, choix justifié. » |

**Plan B démo HS** : projeter `web/screenshots/{page}.png` (HD préparés) + verbaliser le même script.

---

## 4. Slides — wireframes

### Slide 1 — Couverture
```
SKILLNAV
Skills Navigator — Observatoire Compétences IA & DS par Web Mining
Karamo Sylla & Bachirou Konaté
M242 · ENSA-Tétouan · Pr. Imad Sassi
28 mai 2026
```

### Slide 3 — 3 axes Web Mining
```
┌──────────────┬──────────────┬──────────────┐
│  CONTENT     │  STRUCTURE   │  USAGE       │
│              │              │              │
│  NER × 3     │  Graphe Neo4j│  Forecasting │
│  modèles HF  │  PageRank    │  ARIMA       │
│              │  Louvain     │  Prophet     │
│              │  LP, Leiden  │  LSTM        │
│              │              │              │
│  35 % code   │  30 % code   │  30 % code   │
└──────────────┴──────────────┴──────────────┘
```

### Slide 4 — Architecture polyglotte
```
   Scrapers → MongoDB (raw + extracted + ner)
                     ↓
              ↗ Neo4j (graphe)
              ↘ Elasticsearch (search + agrégations)
                     ↓
              FastAPI ↔ Next.js
```

### Slides 8–11 — 4 tableaux chiffrés étude comparative

Reprendre tels quels les tableaux de §N2.1–N2.4 du PRD, avec les chiffres mesurés à J16 dans les notebooks.

---

## 5. Q&A — 15 questions probables (cf. PRD §22.4)

Voir le tableau complet dans `docs/PRD.md` §22.4. Synthèse à imprimer pour la soutenance :

| # | Question | Élément clé |
|---|---|---|
| 1 | Pourquoi 3 DBs ? | Chaque store justifié, plans B documentés |
| 2 | Reproductibilité ? | MongoDB = source of truth, Neo4j et ES rederivables |
| 3 | Pourquoi 3 NER ? | Étude comparative + routage par langue |
| 4 | Volume suffisant ? | 500–2 000 MVP, V1.5 = 10 000 |
| 5 | Biais reconnus ? | Affichés sur `/quality` |
| 6 | Claude vs Transformers ? | Complémentaires (extraction structurée vs NER fine) |
| 7 | Pourquoi Louvain plutôt que Leiden ? | Comparés, choix basé sur métriques |
| 8 | RGPD ? | Aucune donnée candidat, base légale art. 6.1.f, DPIA |
| 9 | Si Apify casse ? | Plan B Firecrawl + sources statiques |
| 10 | Validation forecast ? | Train/test 9-3 mois, MAPE médian, IC 95 % |
| 11 | Vs LinkedIn Talent Insights ? | Méthodologie ouverte, étude comparative reproductible |
| 12 | Article 22 RGPD ? | Pas de décision automatisée individuelle |
| 13 | Durée pipeline ? | ~ 60 min pour 500 offres |
| 14 | À refaire différemment ? | Plus de gold set, fine-tuner CamemBERT, élargir géo |
| 15 | Pourquoi 18 jours ? | Calendrier imposé, plans B documentés |

---

## 6. Répartition orale binôme

| Karamo | Bachirou Konaté |
|---|---|
| M0–M4 (contexte, sujet, archi, justification polyglotte) | M12–M13 (Data Quality + biais reconnus) |
| M4–M9 (stack + démo live dashboard) | M13–M14 (RGPD + robots.txt + DPIA) |
| M9–M12 (étude comparative chiffrée) | M14–M15 (conclusion + roadmap) |
| Q&A : architecture / IA / pipelines / dashboard | Q&A : méthodologie / Data Quality / RGPD / Structure Mining |

---

## 7. Répétitions

- **J17 matin (J-1)** : répétition complète chronométrée à voix haute, mesure des dépassements
- **J17 soir** : répétition 2, plan B démo testé, screenshots vérifiés
- **J18 (J-0) matin** : dry-run technique — projection, son, batterie, internet, dashboard live, fallback screenshots ; chrono final à 15:00 max

**Cible** : tenir 14:30–14:50 en présentation pour avoir une marge de 10–30 secondes.

---

## 8. Matériel à apporter

- 2 laptops chargés (Karamo + Bachirou Konaté)
- 2 dongles HDMI / USB-C
- 1 clé USB avec backup (PDF rapport + screenshots HD + zip repo)
- 1 exemplaire imprimé de ce document
- 1 exemplaire imprimé du PRD (sections N1, N2, N4 surlignées)
- Eau, papier, stylos
- Téléphone en mode « Ne pas déranger »

---

## 9. Critères de succès soutenance

| Critère | Mesure |
|---|---|
| Tenue du temps (15:00 ± 0:30) | Chronomètre Bachirou Konaté |
| Démo live fonctionnelle | Test `curl -I skillnav.vercel.app` à J18 + 3h |
| 4 tableaux étude comparative présentés chiffrés | Slides 8–11 finalisées |
| 6 livrables remis (rapport + repo + dashboard + 3 DBs + deck) | Checklist J17 |
| Q&A : ≥ 12 / 15 questions traitées avec confiance | Auto-éval post-soutenance |

---

**Mai 2026 · Karamo Sylla & Bachirou Konaté**
