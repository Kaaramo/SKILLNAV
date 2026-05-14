"""Scrapers — un sous-package par source (PRD §8).

Stack scraping moderne (2026) — pas de Scrapy ni BeautifulSoup :

- **Crawl4AI**  : scraper IA-natif, sortie markdown propre, anti-bot intégré
- **Playwright**: navigateur headless pour pages JavaScript / SPA
- **Firecrawl** : service managé (fallback robuste pour pages dynamiques rebelles)
- **Apify**    : actors spécialisés (LinkedIn jobs scraper, conformité TOS)

Maroc          : rekrute, emploitic, apify (LinkedIn MA)
International  : indeed, builtin, apify (LinkedIn International)
                 + welcometothejungle (Playwright dans builtin/)
Signaux faibles: weak_signals (Google Trends, GitHub, HuggingFace, Papers W. C.)

Tous les scrapers respectent robots.txt + rate-limit (PRD §N4) et écrivent dans
MongoDB raw_jobs au format JSONL normalisé (PRD §8.6).
"""
