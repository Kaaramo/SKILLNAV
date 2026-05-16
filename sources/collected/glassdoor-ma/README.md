# Glassdoor Maroc : fiches Data/IA

> **Statut** : Phase 1 + 2 complètes. 72 fiches, 100 % exploitables.
> **Période publication** : Novembre 2024 à Mai 2026.
> **Outil principal** : Firecrawl. Recovery : Apify (`memo23/glassdoor-scraper-ppr`).

## 1. Pourquoi cette source ?

Glassdoor agrège les offres tech du marché marocain avec une couverture distincte de LinkedIn et Indeed (souvent des employeurs intermédiaires comme cabinets de recrutement, sociétés de conseil internationales basées à Casablanca, etc.). Source secondaire utile pour le maillage Data/IA local.

## 2. Volume et qualité

| Indicateur | Valeur |
|---|:-:|
| Total fiches | **72** |
| Description >= 200 caractères | **100 %** |
| Période publication | 4 mois (nov 2024, fév-mai 2026) |
| Famille majoritaire | DATA_ANALYST (32 %) |

### Distribution par famille métier

| Famille | Fiches |
|---|:-:|
| DATA_ANALYST | 23 |
| DATA_SCIENTIST | 17 |
| DATA_ENGINEER | 13 |
| OTHER | 12 |
| ML_ENGINEER | 3 |
| AI_ENGINEER | 2 |
| MLOPS_ENGINEER | 1 |
| DATA_ARCHITECT | 1 |

### Classification IA

| Type | Fiches |
|---|:-:|
| ai-first | 9 |
| ml-first | 29 |
| non-ai | 34 |

## 3. Méthode de collecte (2 phases)

### Phase 1 : scraping initial (2026-05-14)

Outil : **Firecrawl CLI**. 4 keywords : `data-scientist`, `data-engineer`, `machine-learning`, `data-analyst`. Output : 72 fichiers markdown bruts dans `raw/<jobkey>.md`.

Script de parsing : `_parse_glassdoor_to_postings.py` (markdown brut vers postings JSON+MD).

### Phase 2 : recovery descriptions (2026-05-16)

Diagnostic : 55/72 fiches avaient des descriptions vides ou < 200 caractères après le parse initial. Causes :
- Variantes de structure markdown selon employeur (FR vs EN, `Description du poste` vs `Description emploi` vs `Job description`)
- Pages JS-rendered partiellement parsées au premier passage

Méthodes testées :
| Méthode | Coût | Résultat |
|---|:-:|:-:|
| Apify `memo23/glassdoor-scraper-ppr` (smoke 5 URLs) | $0.0005 | OK mais limit free tier sur 5 items |
| **Firecrawl re-scrape direct (55 URLs)** | ~55 credits free tier | **55/55 récupérés** |

Bilan final : **72/72 fiches à 100 % exploitables**.

## 4. Scripts de collecte

| Script | Rôle |
|---|---|
| `_parse_glassdoor_to_postings.py` | Parse markdown raw/ vers postings JSON+MD SKILLNAV |
| `_list_incomplete_urls.py` | Identifie les postings avec description < 200 caractères |
| `_firecrawl_recover.py` | Re-scrape les URLs incomplètes via Firecrawl CLI (gratuit) |
| `_apify_recover.py` | Recovery alternative via actor Apify `memo23/glassdoor-scraper-ppr` |

## 5. Structure 3 couches

```
glassdoor-ma/
├── data_raw/{YYYY-MM}/<id>_<co>_<title>.yaml         (72 fichiers)
├── data_structured/{YYYY-MM}/<id>_<co>_<title>.yaml  (72 fichiers)
└── postings/NNN.{json,md}                            (72 fichiers JSON + 72 MD)
```

## 6. Conformité RGPD

| Règle | Application |
|---|---|
| Personal data | Aucune donnée candidat (entité morale + descriptions publiques uniquement) |
| User-Agent | `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)` |
| Rate limit | 5 secondes minimum entre requêtes |
| robots.txt | Vérifié pour Glassdoor |
