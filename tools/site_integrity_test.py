#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


# Removed sections must stay removed.
for rel in ("makaleler", "en/articles"):
    if (ROOT / rel).exists():
        fail(f"Removed article directory still exists: {rel}")

for rel in (
    "article-detail.css",
    "assets/makale-is-hukuku.webp",
    "assets/makale-kira-sozlesmeleri.webp",
    "assets/makale-ticari-sozlesmeler.webp",
    "assets/makaleler-hero.webp",
    "assets/_source/makalelerhero.png",
):
    if (ROOT / rel).exists():
        fail(f"Removed article asset still exists: {rel}")

href_re = re.compile(r'href=["\'][^"\']*(?:makaleler|articles)/', re.IGNORECASE)
for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    if href_re.search(text):
        fail(f"Article link remains in HTML: {path.relative_to(ROOT)}")

for rel in ("index.html", "en/index.html"):
    path = ROOT / rel
    if path.exists():
        text = path.read_text(encoding="utf-8")
        for marker in ("Makaleler", "All Articles", ">Articles<", ">Insights<"):
            if marker in text:
                fail(f"Article section marker {marker!r} remains in {rel}")

# Build/source files must not be able to re-introduce the removed section.
for path in list((ROOT / "tools").glob("*.py")) + [ROOT / "README.md", ROOT / ".github/workflows/seo-build.yml"]:
    if not path.exists() or path.name == Path(__file__).name:
        continue
    text = path.read_text(encoding="utf-8")
    for marker in ("makaleler/", "articles/"):
        if marker in text:
            fail(f"Article route marker {marker!r} remains in source: {path.relative_to(ROOT)}")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
for marker in ("/makaleler/", "/en/articles/"):
    if marker in sitemap:
        fail(f"Article route remains in sitemap: {marker}")

# Public privacy notices must not contain internal draft/review instructions.
privacy_files = (
    ROOT / "kvkk/index.html",
    ROOT / "en/privacy/index.html",
    ROOT / "tools/legal-tr.html",
    ROOT / "tools/legal-en.html",
)
for path in privacy_files:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    for marker in (
        "Taslak metin",
        "taslak bilgilendirme",
        "Av. Pınar Karakaş tarafından gözden geçirilmeli",
        "Nihai hukuki kontrol gereklidir",
        "yayına alınmadan önce nihai metinde",
        "Draft text",
        "Draft information",
        "Att. Pınar Karakaş should review",
        "Final legal review is required",
        "before launch",
    ):
        if marker.lower() in text.lower():
            fail(f"Draft/review marker {marker!r} remains in {path.relative_to(ROOT)}")

if ERRORS:
    print("Site integrity check failed:")
    for item in ERRORS:
        print(f"- {item}")
    sys.exit(1)

print("Site integrity check passed: articles removed and privacy notices are publication-ready.")
