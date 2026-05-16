# Pipeline de scraping `intl-ai-corpus` (5 étapes)

> Scrapers SKILLNAV-internes pour collecter les fiches Data/IA depuis **builtin.com**
> sur 6 villes (Los Angeles, New York, London, Amsterdam, Berlin, Inde).
>
> Architecture inspirée des bonnes pratiques de scraping `requests` + JSON-LD,
> sans dépendance à un service tiers payant (au-delà du proxy optionnel).

## Vue d'ensemble du pipeline

```
       Built In listings (par ville)
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ 1. scrape_listings.py               │
   │    Fetch des pages listing          │
   │    Output : listings/{ville}_{date}.json
   └─────────────────────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ 2. clean_dedup.py                   │
   │    Dedup (title, company) + spam    │
   │    Output : dedup/{date}/jobs.csv   │
   └─────────────────────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ 3. download_html.py                 │
   │    8 threads, 3 retries par URL     │
   │    Output : html/{date}/<id>.html   │
   └─────────────────────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ 4. extract_yaml_from_html.py        │
   │    JSON-LD primary + BS4 fallback   │
   │    Output : data_raw/{YYYY-MM}/     │
   └─────────────────────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ 5. enrich_structured.py             │
   │    Classification IA + skills 10D   │
   │    Output : data_structured/{YYYY-MM}/
   └─────────────────────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ ../_import_upstream.py              │
   │    Merge raw + structured           │
   │    Output : postings/NNN.{json,md}  │
   └─────────────────────────────────────┘
```

## Étapes et scripts

| # | Script | Rôle | Output |
|:-:|---|---|---|
| 1 | `1_scrape_listings.py` | Fetch listings par ville et date | `listings/{ville}_{YYYY-MM-DD}.json` |
| 2 | `2_clean_dedup.py` | Déduplication (title, company) + spam filter | `dedup/{YYYY-MM-DD}/jobs.csv` |
| 3 | `3_download_html.py` | Téléchargement HTML complet, 8 threads | `html/{YYYY-MM-DD}/<job_id>.html` |
| 4 | `4_extract_yaml_from_html.py` | Parsing JSON-LD + BeautifulSoup fallback | `../data_raw/{YYYY-MM}/<id>_<co>_<title>.yaml` |
| 5 | `5_enrich_structured.py` | Classification IA + skills en 10 dimensions | `../data_structured/{YYYY-MM}/<id>_<co>_<title>.yaml` |

## Reproductibilité

### Prérequis

```bash
pip install requests beautifulsoup4 lxml PyYAML
```

### Lancement complet de la pipeline

```bash
cd sources/collected/intl-ai-corpus/scrapers

# Etape 1 : listings (1 par ville)
python 1_scrape_listings.py --cities los-angeles,new-york,london,amsterdam,berlin,india

# Etape 2 : dedup
python 2_clean_dedup.py --date 2026-05-16

# Etape 3 : download HTML (parallele, peut prendre ~30 min pour 500 URLs)
python 3_download_html.py --csv dedup/2026-05-16/jobs.csv

# Etape 4 : extract YAML raw
python 4_extract_yaml_from_html.py --date 2026-05-16

# Etape 5 : enrich structured
python 5_enrich_structured.py --date 2026-05-16

# Etape 6 : import vers postings SKILLNAV
cd .. && python _import_upstream.py
```

## Conformité

* User-Agent identifié : `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)`
* Rate limit : 5 secondes entre requêtes par défaut
* `robots.txt` builtin.com vérifié avant chaque collecte
* Aucune donnée personnelle de candidat collectée (entités morales uniquement)

## Note

Les data actuelles de `intl-ai-corpus/` (3 087 fiches dans `data_raw/`, `data_structured/`, `postings/`) ont été produites par une exécution antérieure de cette pipeline. Pour reproduire from scratch, exécuter les 6 étapes dans l'ordre. Pour reproduire uniquement la couche pivot, exécuter directement `../_import_upstream.py` qui consomme les data_raw + data_structured existants.
