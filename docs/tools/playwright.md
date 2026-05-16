# Playwright

## Qu'est-ce que c'est ?

Playwright est un **framework d'automatisation de browser** Microsoft (open-source). Il pilote Chromium, Firefox et WebKit en mode headless ou réel, avec une API Python/Node.js complète : `goto()`, `click()`, `fill()`, `wait_for_selector()`, etc.

- **Installation** : `pip install playwright && playwright install chromium`
- **MCP** : intégration native Claude Code via Playwright MCP
- **Avantage clé** : on contrôle **chaque action utilisateur** (login, clic pagination, scroll, formulaire)

## Pourquoi SKILLNAV l'a choisi

### 1. Sites avec interactions complexes

ANAPEC, Rekrute et Indeed MA ne sont pas accessibles via une simple URL `?keyword=...`. Il faut :
- Remplir un champ de recherche
- Cliquer sur "Rechercher"
- Attendre le rendu JS de la liste
- Paginer (cliquer "Suivant" pour charger les pages 2, 3, ...)

Playwright fait tout ça avec quelques lignes :

```python
await page.goto("https://www.anapec.org/sigec/portail/index.do")
await page.fill("#keyword", "data scientist")
await page.click("button[type=submit]")
await page.wait_for_selector(".job-card")
```

### 2. Browser réel = empreinte humaine

Contrairement à `requests` ou même Firecrawl, Playwright lance un **vrai Chromium** avec une fenêtre, des cookies, des headers normaux, un user-agent réaliste. C'est plus discret pour les sites avec détection comportementale.

### 3. Fallback universel

Quand Firecrawl rate sur un site (anti-bot trop fort) et que Apify n'a pas d'actor dédié, Playwright reste l'option de dernier recours qui marche presque toujours — au prix d'un setup plus long.

### 4. Gratuit et auto-hébergé

Pas de quota, pas de coût par requête. On lance autant de pages qu'on veut, limite seulement la machine locale.

## Cas d'usage SKILLNAV

| Source | Pourquoi Playwright | Méthode |
|---|---|---|
| **ANAPEC** | Formulaire de recherche obligatoire | Fill + submit + parse cards |
| **Rekrute** | Pagination JS (boutons Suivant) | Loop click "Suivant" + extract |
| **Indeed MA** | Cookies de session requis pour stabilité | Persistent context + parse listing |
| **CIH Bank** (en attente) | Custom HTML avec anti-bot 403 | Bypass anti-bot via vrai browser |
| **Maroc Telecom** (en attente) | SharePoint + JS rendering | Scénario à scénariser |

## Limitations

- **Lent** : ~3-5 s par page vs ~1 s pour Firecrawl
- **Setup local** : nécessite Chromium installé (~200 MB)
- **Pas d'anti-bot intégré** : si IP bloquée, il faut configurer son propre proxy
- **Captcha** : ne résout pas les hCaptcha / reCAPTCHA — il faut un service tiers (2captcha, etc.)

## Stack alternative envisagée et écartée

| Alternative | Pourquoi écartée |
|---|---|
| Selenium | API plus verbeuse, perf inférieure, communauté en déclin |
| Puppeteer | Limité à Node.js (notre stack est Python) |
| BeautifulSoup pur | Inutilisable pour les SPA — pas de rendu JS |
| Scrapy + Splash | Splash est plus vieux, moins bon support Chrome modern features |

## Pattern SKILLNAV typique

```python
from playwright.async_api import async_playwright

async def scrape_anapec():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(user_agent="SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)")
        page = await ctx.new_page()
        await page.goto("https://www.anapec.org/sigec/portail/")
        await page.fill("#keyword", "data scientist")
        await page.click("button#search")
        await page.wait_for_selector(".job-result")
        urls = await page.eval_on_selector_all(".job-result a", "els => els.map(e => e.href)")
        for url in urls:
            await page.goto(url)
            html = await page.content()
            # parse via BeautifulSoup ou regex
            ...
        await browser.close()
```

Rate-limit : `await asyncio.sleep(5)` entre les fiches pour respecter le User-Agent SKILLNAV qui s'identifie comme bot académique.
