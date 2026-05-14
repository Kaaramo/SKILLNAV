"""Scrapers — un sous-package par source (PRD §8).

Maroc          : rekrute, emploitic, apify (LinkedIn MA)
International  : indeed, builtin, apify (LinkedIn International)
                 + welcometothejungle (Playwright dans builtin/)
Signaux faibles: weak_signals (Google Trends, GitHub, HuggingFace)

Tous les scrapers respectent robots.txt + rate-limit (PRD §N4) et écrivent dans
MongoDB raw_jobs au format JSONL normalisé (PRD §8.6).
"""
