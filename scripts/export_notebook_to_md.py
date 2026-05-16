"""Exporte le notebook en Markdown lisible (cellules sources, sans outputs)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(r"F:\Web Mining Project")
NB = REPO / "notebooks" / "00_market_analysis.ipynb"
OUT = REPO / "notebooks" / "00_market_analysis.md"

nb = json.loads(NB.read_text(encoding="utf-8"))

lines: list[str] = []
lines.append(f"<!-- Export Markdown du notebook : {NB.name} -->\n")
lines.append(f"<!-- {len(nb['cells'])} cellules · regénérable via scripts/export_notebook_to_md.py -->\n\n")

for i, cell in enumerate(nb["cells"]):
    src = "".join(cell.get("source", []))
    if cell.get("cell_type") == "markdown":
        lines.append(src.rstrip() + "\n\n")
    elif cell.get("cell_type") == "code":
        lines.append(f"```python\n# Cellule [{i}]\n{src.rstrip()}\n```\n\n")

OUT.write_text("".join(lines), encoding="utf-8")
print(f"Markdown écrit : {OUT}")
print(f"Taille : {OUT.stat().st_size // 1024} KB")
