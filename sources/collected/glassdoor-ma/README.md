# Glassdoor Maroc — Job board international (filtre Morocco)

> **Statut** : ✅ Vérifiée · 🥇 **Tier T1** (Indispensable) · ⚠️ **Override CLAUDE.md §N4 autorisé**
> **URL principale** : https://www.glassdoor.com/Job/morocco-data-scientist-jobs-SRCH_IL.0,7_IN162_KO8,22.htm
> **Date d'audit** : 2026-05-14
> **MCP utilisé** : Firecrawl (production) · Apify possible en fallback

---

## ⚠️ Note de conformité — Override CLAUDE.md §N4

**Le `robots.txt` de Glassdoor bloque explicitement** :
- `User-agent: Claude-Web` (Anthropic crawler banni)
- `/job-listing/*_IE*.htm` — pages détail des offres (Disallow)
- `/jobview/` — vues détail (Disallow)
- `/search/` — recherche (Disallow)
- `/Jobs/*_P*.htm*` — pages paginées (Disallow)

**Override explicite autorisé par Karamo Sylla** le **2026-05-14** via `AskUserQuestion` après signalement formel du conflit avec CLAUDE.md §N4 ("Tous les scrapers respectent robots.txt"). Justification : évaluation académique M242 ENSA-Tétouan, soutenance 28 mai 2026. Risque assumé : violation ToS Glassdoor.

**Mitigations appliquées** :
- User-Agent identifié `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)` via proxy Firecrawl
- Rate limit naturel Firecrawl (2-3 s entre requêtes, concurrency=2 max)
- Aucune pagination massive (1 page SRCH par mot-clé × 4 mots-clés)
- RGPD strict respecté : entité morale uniquement, aucune donnée personnelle de candidat
- Override **LOCAL à `glassdoor-ma`** — ne s'étend pas aux autres sources du projet

---

## 🇲🇦 Qu'est-ce que Glassdoor Maroc ?

**Glassdoor** est une plateforme américaine d'évaluation employeurs + job board. Le filtre Morocco (`IN162`) expose les offres publiées par des entreprises actives au Maroc — souvent des **filiales internationales** (Capgemini, Stellantis, AXA, Mistral AI, McKinsey, BCG) qui ne publient pas sur les job boards locaux.

---

## 🎯 Pourquoi Glassdoor dans le scope SKILLNAV ?

### Atouts (justification du Tier T1)

| Critère | Pertinence |
|---|---|
| **Volume Data/IA Morocco** | 97 Data Scientist · 284 Data Engineer · 164 Data Analyst · 40 Machine Learning · 53 AI Engineer (mai 2026) |
| **Marques internationales exclusives** | Mistral AI, McKinsey QuantumBlack, Boston Consulting Group, Stellantis, Safran, Société Générale — peu/pas visibles sur Rekrute |
| **Ratings entreprises** | Score 0-5 (Glassdoor proprio) — signal qualitatif sur les employeurs |
| **Salaires agrégés** | Plages salariales MAD par poste (mais pas dans `/job-listing/`, dans `/Salaries/`) |
| **Descriptions détaillées** | Souvent en anglais, format LinkedIn-like — bonne extraction skills |
| **Couverture Casablanca dominante** | ~85% Casablanca, le reste Rabat/Tanger/Marrakech |

### Limites assumées

| Limite | Conséquence | Mitigation |
|---|---|---|
| **robots.txt bloque pages détail** | Conflit conformité CLAUDE.md §N4 | Override explicite Karamo (cf. supra) |
| **Pas d'historique URL** | Glassdoor purge les offres expirées → impossible de remonter à 2023-2025 via URL | Wayback (échoué — 1 snapshot 2022) ; cross-ref Indeed/Rekrute pour les mêmes employeurs |
| **Date publication relative** | "7d", "30d+" — pas de date absolue dans la page détail | Calcul `posted_date = today - days_ago` ; "30d+" → today - 45j (approximation) |
| **Auth wall sur infos complémentaires** | Reviews/Salaires nécessitent login | On reste sur la fiche publique de l'offre |
| **Cloudflare actif** | curl direct bloqué (403) | Firecrawl gère le bypass automatique (testé OK) |

---

## 🔧 Méthode de collecte

### Stack utilisée

| Outil | Rôle |
|---|---|
| **Firecrawl MCP** ⭐ | Phase 1 reconnaissance (SRCH pages) + Phase 2 scraping détail (bypass Cloudflare auto) |
| **WebSearch** | Phase 2 prospection historique (rendu inutile — Google n'indexe pas les `/job-listing/`) |
| **Python regex** | Phase 3 extraction → JSON+MD |

### URLs canoniques

```
SRCH (autorisé robots.txt)   : https://www.glassdoor.com/Job/morocco-<keyword>-jobs-SRCH_IL.0,7_IN162_KO8,<len>.htm
Détail (Disallow robots.txt) : https://www.glassdoor.com/job-listing/<slug>-JV_IC<location>_KO<a>,<b>_KE<c>,<d>.htm?jl=<jl_id>
```

L'astuce des coordonnées `KO<a>,<b>_KE<c>,<d>` dans l'URL : indices du titre (KO) et de l'entreprise (KE) dans le slug. Permet d'extraire `(title, company)` sans parser le HTML quand le SRCH parser échoue.

### Termes de recherche utilisés

| Mot-clé | Total Morocco | URLs récupérées (page 1) |
|---|:-:|:-:|
| `data scientist` | 97 | 30 |
| `data engineer` | 284 | 30 |
| `machine learning` | 40 | 30 |
| `data analyst` | 164 | 30 |
| **Total unique** | **— ** | **99** |

Après filtre scope strict Data/IA (élimination Full Stack, DevOps pur, Quality Engineer, PLM, etc.) : **72 URLs in-scope** scrapées en Phase 2.

---

## 🛡️ Conformité RGPD (CLAUDE.md §N4 — partie données)

| Règle | Application Glassdoor-MA |
|---|---|
| Aucune donnée personnelle candidat | ✅ Glassdoor expose uniquement l'employeur + description publique — pas de contact recruteur dans /job-listing/ |
| Entité morale uniquement | ✅ `company` = nom d'entreprise (jamais de personne physique) |
| User-Agent identifié | `SkillnavBot/1.0` annoncé via proxy Firecrawl |
| Rate limit | 2-3 s naturel via Firecrawl (concurrency 2) |
| **robots.txt** | ⚠️ Override autorisé (cf. note de conformité supra) |

---

## 📦 Échantillon collecté (Phase 1 — 2026-05-14)

> Les chiffres précis sont dans `source.yaml` après extraction Phase 3.

### Méthode hybride utilisée (adaptée pour Glassdoor)

```
PHASE 1 : Firecrawl scrape sur 4 URLs SRCH autorisées
  ├── morocco-data-scientist  (97 jobs · 30 URLs page 1)
  ├── morocco-data-engineer   (284 jobs · 30 URLs page 1)
  ├── morocco-machine-learning (40 jobs · 30 URLs page 1)
  └── morocco-data-analyst    (164 jobs · 30 URLs page 1)
                ↓ 99 URLs uniques → filtre Data/IA strict → 72 URLs in-scope

PHASE 2 : Firecrawl scrape sur chaque /job-listing/ (override CLAUDE.md §N4)
                ↓ 72 markdowns dans raw/<jl_id>.md

PHASE 3 : Python regex extraction
  ├── Cross-réf SRCH index (title/company/location/date_rel)
  ├── Fallback slug KO/KE pour entreprises sans logo
  ├── Description extraite entre "About The Job" et "Related pages"
  ├── Skills via regex (Python, SQL, ML, GenAI, Databricks, etc.)
  ├── Job family via heuristique titre
  └── posted_date = today - days_ago (relative → absolue)
                ↓ postings/NNN.json + NNN.md
```

### Comparaison vs Rekrute (référence T1)

| Aspect | Glassdoor MA | Rekrute |
|---|---|---|
| Volume Data/IA visible | ~99 (DS+DE+DA+ML) | ~50 (data scientist seul) |
| Marques internationales | **Mistral AI · QuantumBlack · BCG · Stellantis** | Cnexia · AXA · Coface · Sofrecom |
| Historique URLs | ❌ Pas conservé | ✅ Conservé 2-3 ans |
| Description riche | ✅ EN/FR long format | ✅ FR format candidat |
| Salaires affichés | ⚠️ Dans /Salaries/ séparé | ❌ Rarement |
| Ratings entreprises | ✅ Score 0-5 | ❌ Non |
| Robots.txt restrictif | ⚠️ Override requis | ✅ Permissif |

---

## 📅 Roadmap Glassdoor-MA

| Sprint | Action |
|---|---|
| **S1 J5** (2026-05-14) | ✅ Sample 99 URLs · 72 in-scope · extraction Phase 3 · structure validée |
| **S1 J6** | Pagination SRCH _IP2 à _IP5 pour atteindre ~300 URLs supplémentaires si quota Firecrawl OK |
| **S2 J7-J12** | Production pipeline `skillnav.scrapers.glassdoor_ma` + persistence MongoDB raw_jobs |
| **S2 J10** | Évaluation Apify actor `glassdoor-jobs-scraper` pour fiches enrichies (date exacte, salary) |
| **S3** | Monitoring continu hebdomadaire (nouvelles annonces uniquement) |

---

## 🔗 Liens

- [Glassdoor Morocco Jobs](https://www.glassdoor.com/Job/morocco-jobs-SRCH_IL.0,7_IN162.htm)
- [Robots.txt](https://www.glassdoor.com/robots.txt)
- [Schéma JSON SKILLNAV](../_schema/job_posting.schema.json)
- [Protocole de collecte v1.0](../COLLECTION_PROTOCOL.md)

---

**Mai 2026 · SKILLNAV · M242 ENSA-Tétouan · Pr. Imad Sassi · Karamo Sylla & Bachirou Konaté**

> _Cette collecte a été effectuée avec un override explicite de CLAUDE.md §N4 sur la conformité robots.txt. La décision est tracée dans `source.yaml` (champ `override_authorized_by`) et dans les messages de commit Git. Aucune donnée personnelle de candidat n'a été collectée. Pour les sources où le robots.txt est respecté, voir Rekrute, ANAPEC, ou Indeed MA._
