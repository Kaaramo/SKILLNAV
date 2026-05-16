"""Exécute un notebook en place via nbclient (sans dépendance jupyter CLI)."""
from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main(path: Path) -> None:
    print(f"Exécution de : {path}")
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()
    nbformat.write(nb, path)
    print("OK")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
