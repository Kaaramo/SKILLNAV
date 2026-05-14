# SKILLNAV — commandes courantes
# Usage : `make help`

.PHONY: help install install-web setup lint format typecheck test test-fast quality audit audit-web audit-all clean api web-dev cli

# ─── Installation ───────────────────────────────────────────────────────────
install: ## Installe les dépendances Python via Poetry
	poetry install

install-web: ## Installe les dépendances front Next.js
	cd web && pnpm install

setup: install install-web ## Setup complet (Python + web + pre-commit hooks)
	poetry run pre-commit install
	@echo "✅ Setup complet — prêt à coder."

# ─── Qualité ────────────────────────────────────────────────────────────────
lint: ## Lint Python (ruff)
	poetry run ruff check .

format: ## Formate Python (black + ruff format)
	poetry run black .
	poetry run ruff format .

typecheck: ## Type-check Python strict (mypy)
	poetry run mypy skillnav

test: ## Lance les tests avec couverture
	poetry run pytest

test-fast: ## Tests rapides (skip integration + slow)
	poetry run pytest -m "not slow and not integration"

quality: lint typecheck test ## Pipeline qualité complet (lint + typecheck + test)
	@echo "✅ Quality gate passé."

# ─── Sécurité (audit supply-chain) ─────────────────────────────────────────
audit: ## Audit Python (vulnérabilités via pip-audit)
	poetry run pip-audit

audit-web: ## Audit web (pnpm audit niveau moderate+)
	cd web && pnpm audit --prod --audit-level=moderate

audit-all: audit audit-web ## Audit Python + web — à lancer avant chaque push
	@echo "✅ Audit supply-chain passé."

# ─── Maintenance ────────────────────────────────────────────────────────────
clean: ## Nettoie caches + builds
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov coverage.xml
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} + 2>/dev/null || true

# ─── Dev runtime ────────────────────────────────────────────────────────────
api: ## Lance l'API FastAPI en dev
	poetry run uvicorn skillnav.api.main:app --reload --host 0.0.0.0 --port 8000

web-dev: ## Lance le front Next.js en dev
	cd web && pnpm dev

cli: ## Affiche l'aide CLI skillnav
	poetry run skillnav --help

# ─── Aide ───────────────────────────────────────────────────────────────────
help: ## Affiche cette aide
	@echo "SKILLNAV — Skills Navigator"
	@echo "M242 ENSA-Tétouan · Karamo Sylla & Bachirou Konaté"
	@echo ""
	@echo "Commandes disponibles :"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
