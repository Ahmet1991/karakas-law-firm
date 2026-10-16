#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Legacy EN generator: remove the homepage Insights/article section if it remains
# after the broader cleanup migration.
path = ROOT / "tools" / "build-en.py"
text = path.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)
out: list[str] = []
i = 0
while i < len(lines):
    if "Insights</p>" in lines[i]:
        if out and 'section class=\\"section section--deep\\"' in out[-1]:
            out.pop()
        i += 1
        while i < len(lines) and "article-grid" not in lines[i]:
            i += 1
        if i < len(lines):
            i += 1
        continue
    out.append(lines[i])
    i += 1
text = "".join(out)
path.write_text(text, encoding="utf-8", newline="\n")

# README: remove stale route/asset documentation for the retired article section.
path = ROOT / "README.md"
lines = path.read_text(encoding="utf-8").splitlines()
markers = ("makaleler/", "en/articles/", "assets/makale-", "makaleler-hero")
lines = [line for line in lines if not any(marker in line for marker in markers)]
path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

print("Final stale article source markers removed.")
