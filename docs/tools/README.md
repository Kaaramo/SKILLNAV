# Outils de collecte SKILLNAV

> Documentation des outils de scraping et d'extraction de données utilisés dans le projet SKILLNAV.
> Critère majeur d'évaluation du prof Sassi : « **la qualité de la justification des outils choisis** sera un critère majeur d'évaluation ».

## Outils utilisés

| Outil | Cas d'usage SKILLNAV | Fichier dédié |
|---|---|---|
| **Firecrawl** | Scraping pages dynamiques (JS-rendered) avec gestion anti-bot intégrée | [`firecrawl.md`](firecrawl.md) |
| **Apify** | Actors managés pour LinkedIn / Indeed (anti-bot fort) | [`apify.md`](apify.md) |
| **Playwright** | Browser réel pour les sites avec interactions complexes | [`playwright.md`](playwright.md) |

## Logique de choix

Pour chaque source, la décision suit cet arbre :

```
Site cible
├── Anti-bot léger / contenu statique → curl + BeautifulSoup (gratuit, rapide)
├── JS rendering nécessaire / contenu dynamique → Firecrawl
├── Anti-bot fort (LinkedIn, Indeed) → Apify (actor managé)
└── Interactions complexes (login, formulaire) → Playwright
```

## Distribution réelle des outils dans SKILLNAV

| Source | Outil principal | Pourquoi |
|---|---|---|
| ANAPEC | Playwright MCP | Site public léger, formulaire de recherche à manipuler |
| Rekrute | Playwright MCP | Site dynamique avec pagination JS |
| Indeed MA | Playwright MCP | Anti-bot modéré, JSON-LD partiel |
| LinkedIn MA | Apify | Anti-bot fort, actor `cheap-advance-linkedin-jobs-scraper` éprouvé |
| Glassdoor MA | Firecrawl | Pages JS-rendered, anti-bot léger |
| Pages carrières MA | curl + BeautifulSoup | Sites statiques ATS (TalentSoft, TeamTailor) |
| Built In INTL | Firecrawl + parsing JSON-LD | Pages JS modernes, structure schema.org propre |
