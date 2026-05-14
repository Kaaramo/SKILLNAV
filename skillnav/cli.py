"""SKILLNAV CLI — point d'entrée Typer.

Voir `make cli` ou `poetry run skillnav --help` pour la liste des commandes.

Commandes prévues (PRD §3 — Parcours interne) :

- `skillnav scrape`   : étape 1 — collecte
- `skillnav extract`  : étape 2 — extraction IA + NER
- `skillnav graph`    : étape 3 — construction graphe Neo4j
- `skillnav forecast` : étape 4 — forecasting Usage Mining
- `skillnav index`    : étape 4' — push Elasticsearch
"""

from __future__ import annotations

import typer
from rich.console import Console

from skillnav import __version__

app = typer.Typer(
    name="skillnav",
    help="SKILLNAV — observatoire des compétences IA/DS par Web Mining (M242 ENSA-Tétouan).",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
)
console = Console()


@app.command()
def version() -> None:
    """Affiche la version courante de SKILLNAV."""
    console.print(f"[bold cyan]SKILLNAV[/] version [green]{__version__}[/]")


# Les sous-commandes (scrape, extract, graph, forecast, index) seront branchées
# au fur et à mesure de l'implémentation des pipelines.
# Pattern : app.add_typer(scrape_app, name="scrape") depuis chaque module.


if __name__ == "__main__":
    app()
