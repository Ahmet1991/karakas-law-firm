#!/usr/bin/env python3
"""Rewrite legacy one-page navigation in generated practice pages.

The legacy generator still emits links to retired homepage fragments. The
current site uses separate pages, so this pass converts those links after every
generation without touching the generator's content rendering.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def root_prefix(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parent.parts)
    return "../" * depth


def patch(path: Path, lang: str) -> bool:
    doc = path.read_text(encoding="utf-8")
    root = root_prefix(path)

    if lang == "tr":
        old_home = root
        replacements = {
            old_home + "#hakkimizda": root + "hakkimizda/",
            old_home + "#faaliyet-alanlari": root + "uzmanlik-alanlari/",
            old_home + "#pinar-karakas": root + "hakkimizda/#founder-title",
            old_home + "#iletisim": root + "iletisim/",
        }
    else:
        old_home = root + "en/"
        replacements = {
            old_home + "#about": root + "en/about/",
            old_home + "#practice-areas": root + "en/practice-areas/",
            old_home + "#pinar-karakas": root + "en/about/#founder-title",
            old_home + "#contact": root + "en/contact/",
        }

    updated = doc
    for old, new in replacements.items():
        updated = updated.replace(f'href="{old}"', f'href="{new}"')
        updated = updated.replace(f"href='{old}'", f"href='{new}'")

    if updated == doc:
        return False
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    changed = 0

    tr_root = ROOT / "faaliyet-alanlari"
    for path in sorted(tr_root.glob("*/index.html")):
        changed += int(patch(path, "tr"))

    en_root = ROOT / "en" / "practice-areas"
    for path in sorted(en_root.glob("*/index.html")):
        changed += int(patch(path, "en"))

    print(f"Navigation post-process tamamlandı: {changed} detay sayfası güncellendi")


if __name__ == "__main__":
    main()
