# Firecrawl

## Qu'est-ce que c'est ?

Firecrawl est un service d'extraction Web spécialisé pour les **pages JS-rendered** (Single Page Applications, sites React/Vue/Next.js) et les sites avec **anti-bot léger à modéré**. Il combine un browser headless managé, des proxies résidentiels rotatifs et un parser markdown propre.

- **API REST** : `POST https://api.firecrawl.dev/v1/scrape`
- **CLI** : `firecrawl scrape <url> -o output.md`
- **MCP** : intégration native Claude Code via `firecrawl:firecrawl-scrape`
- **Pricing** : 500 crédits gratuits/mois · ~$20 / 2 500 crédits supplémentaires

## Pourquoi SKILLNAV l'a choisi

### 1. JSON-LD propre dès la 1ère requête

builtin.com, Glassdoor et la plupart des job boards modernes embarquent du **schema.org** dans leurs pages. Firecrawl rend la page complètement, ce qui rend ces blocs accessibles dans le markdown de sortie. Pas besoin d'un second outil pour le rendu JS.

### 2. Markdown lisible et exploitable

Contrairement à un parser HTML brut qui force ensuite à appliquer BeautifulSoup, Firecrawl renvoie directement du **markdown nettoyé** — descriptions, titres, sections H2/H3 préservés. C'est exactement ce dont on a besoin pour la couche `data_raw/` du pipeline 3-couches SKILLNAV.

### 3. Anti-bot intégré sans effort

Pas besoin de configurer Oxylabs, Bright Data ou un autre proxy. Firecrawl gère lui-même la rotation IP et les headers. Pour Glassdoor (anti-bot moyen), c'est ce qui fait la différence avec un `requests.get()` qui retournerait un challenge JS.

### 4. Coût raisonnable pour le volume SKILLNAV

500 crédits/mois gratuits = ~500 fiches Indeed FR (1 listing + détails à coût marginal). Pour 3 087 fiches Built In INTL, on a tenu sur les crédits free + 1 top-up modéré (~$20).

## Cas d'usage SKILLNAV

| Source | Volume | Crédits utilisés (~) |
|---|:-:|:-:|
| **Glassdoor MA** | 72 fiches détails + 4 search pages | ~80 |
| **Built In INTL** | 3 090 fiches + ~50 listings | ~3 200 |

## Limitations rencontrées

- **Indeed FR** : anti-bot trop fort même pour Firecrawl, ~50% des URLs viewjob retournent du contenu vide. Solution choisie : pivoter vers Apify (actor `misceres/indeed-scraper`).
- **LinkedIn** : bloqué dès la 1ère requête, login requis. Solution : Apify `cheap-advance-linkedin-jobs-scraper`.

## Stack alternative envisagée et écartée

| Alternative | Pourquoi écartée |
|---|---|
| Scrapy + Splash | Configuration lourde, pas de proxies managés inclus |
| Selenium pur | Plus lent, pas de markdown propre, anti-bot à gérer soi-même |
| ScrapingBee | Concurrent direct mais moins bon parser markdown |
| Bright Data Web Unlocker | Plus cher, overkill pour notre volume |
