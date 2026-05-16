# Apify

## Qu'est-ce que c'est ?

Apify est une plateforme cloud d'**actors** (scrapers managés) pour les sites avec **anti-bot très fort** : LinkedIn, Indeed, Amazon, Booking, etc. Chaque actor est maintenu par une équipe (Apify ou tiers) et expose une API REST simple.

- **API REST** : `POST https://api.apify.com/v2/acts/<actor>/runs`
- **MCP** : intégration native Claude Code via Apify MCP
- **Pricing** : pay-per-result (~$0.50 à $2 / 1 000 résultats selon l'actor)
- **Avantage clé** : on **paie uniquement les résultats**, pas le temps machine — l'anti-bot et les retries sont du problème de l'actor

## Pourquoi SKILLNAV l'a choisi

### 1. Seul moyen viable pour LinkedIn

LinkedIn bloque tout scraper non authentifié dès la 1ère requête. Les solutions DIY (Playwright + login + headers + résidentiels) sont :
- Lentes (5-10 s par fiche)
- Fragiles (déconnexion fréquente, captcha)
- Risque légal pour le compte LinkedIn utilisé

Apify managed actors comme `cheap-advance-linkedin-jobs-scraper` :
- Tournent sur l'infrastructure Apify avec leurs proxies
- Gèrent le login via comptes anonymes managés
- Retournent un JSON structuré directement

### 2. Pay-per-result = coût prévisible

Pour LinkedIn MA, 207 fiches retenues sur 8 runs successifs = **$3.83** dépensés. Vs Playwright DIY qui aurait nécessité 2-3 jours de dev + risque blocage.

### 3. Output structuré JSON

Pas de parsing HTML/markdown nécessaire. L'actor retourne directement :

```json
{
  "title": "Data Analyst",
  "company": "Newrest",
  "location": "Casablanca",
  "description": "...",
  "skills": ["Power BI"],
  "postedDate": "2026-05-08",
  "applyUrl": "https://...",
  ...
}
```

C'est exactement ce qu'on injecte dans la couche `postings/` SKILLNAV.

## Actors utilisés par SKILLNAV

| Actor | Source | Coût |
|---|---|:-:|
| `number_one_scraper/cheap-advance-linkedin-jobs-scraper` | LinkedIn MA (8 runs) | ~$3.83 |
| `misceres/indeed-scraper` | (envisagé pour Indeed MA refresh) | ~$0.50 / 1k |

## Méthode SKILLNAV par run

1. POST `/v2/acts/{actor}/runs` avec input JSON (keyword + filters)
2. Polling sur `/v2/actor-runs/{run_id}` jusqu'à `status == "SUCCEEDED"`
3. GET `/v2/key-value-stores/{store_id}/records/INPUT` (pour le récap)
4. GET `/v2/datasets/{dataset_id}/items` → JSON array de tous les résultats
5. Strip RGPD : retirer `posterFullName`, `posterProfileUrl`, etc.
6. Conversion → format SKILLNAV `postings/NNN.json`

## Limitations

- **Coût qui grimpe vite** sur de gros volumes (10k+ fiches)
- **Dépendance externe** : si l'actor casse (changement LinkedIn), faut attendre la mise à jour
- **Boîte noire** : on ne contrôle pas comment exactement le scraping est fait

## Stack alternative envisagée et écartée

| Alternative | Pourquoi écartée |
|---|---|
| Playwright + LinkedIn DIY | Trop fragile, risque ban compte |
| BrightData LinkedIn dataset | Plus cher (~$1/profil) |
| LinkedIn API officielle | Restreinte aux partenaires LinkedIn, refusée pour usage académique |
