#!/usr/bin/env python3
"""Audit local HTML links, assets and fragment targets.

Designed for the static Karakaş Law Firm site. External services are ignored;
same-domain absolute URLs are resolved back to the repository so production
links can be checked before launch.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE_HOSTS = {"karakaslawfirm.com", "www.karakaslawfirm.com"}
SKIP_DIRS = {".git", "tools"}
ERRORS: list[str] = []
CHECKED = 0

ATTR_RE = re.compile(r"\b(?:href|src)\s*=\s*([\"'])(.*?)\1", re.I | re.S)
ID_RE = re.compile(r"\b(?:id|name)\s*=\s*([\"'])(.*?)\1", re.I | re.S)


def fail(message: str) -> None:
    ERRORS.append(message)


def html_pages() -> list[Path]:
    pages: list[Path] = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        pages.append(path)
    return sorted(pages)


def local_target(page: Path, raw_url: str) -> tuple[Path | None, str | None]:
    raw_url = html.unescape(raw_url.strip())
    if not raw_url or raw_url.startswith(("mailto:", "tel:", "javascript:", "data:", "blob:")):
        return None, None

    parsed = urlsplit(raw_url)
    if parsed.scheme in {"http", "https"}:
        if (parsed.hostname or "").lower() not in SITE_HOSTS:
            return None, None
        path_text = parsed.path or "/"
    elif parsed.scheme or parsed.netloc:
        return None, None
    else:
        path_text = parsed.path

    fragment = unquote(parsed.fragment) if parsed.fragment else None

    if not path_text:
        target = page
    elif path_text.startswith("/"):
        # Production-domain absolute path. Also tolerate the GitHub Pages
        # project prefix if a staging-oriented link ever appears in markup.
        cleaned = unquote(path_text).lstrip("/")
        if cleaned == "karakas-law-firm":
            cleaned = ""
        elif cleaned.startswith("karakas-law-firm/"):
            cleaned = cleaned[len("karakas-law-firm/"):]
        target = ROOT / cleaned
    else:
        target = page.parent / unquote(path_text)

    target = Path(str(target).split("?", 1)[0])
    if str(target).endswith("/") or target.is_dir():
        target = target / "index.html"
    elif target.suffix == "":
        # Extensionless site routes are directories on GitHub Pages.
        target = target / "index.html"

    return target.resolve(), fragment


def anchors(path: Path) -> set[str]:
    try:
        doc = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()
    return {html.unescape(value) for _, value in ID_RE.findall(doc)}


pages = html_pages()
for page in pages:
    doc = page.read_text(encoding="utf-8")
    rel_page = page.relative_to(ROOT).as_posix()

    for _, raw_url in ATTR_RE.findall(doc):
        target, fragment = local_target(page, raw_url)
        if target is None:
            continue
        CHECKED += 1

        # Do not allow traversal outside the repository.
        try:
            rel_target = target.relative_to(ROOT)
        except ValueError:
            fail(f"Repo dışına çıkan link: {rel_page} -> {raw_url}")
            continue

        if not target.exists():
            fail(f"Kırık yerel hedef: {rel_page} -> {raw_url} ({rel_target.as_posix()})")
            continue

        if fragment and target.suffix.lower() in {".html", ".htm"}:
            if fragment not in anchors(target):
                fail(f"Eksik fragment: {rel_page} -> {raw_url}")

# Explicitly prohibit anchors from the retired single-page architecture.
LEGACY_FRAGMENTS = ("#faaliyet-alanlari", "#hakkimizda", "#pinar-karakas", "#iletisim")
for page in pages:
    rel_page = page.relative_to(ROOT).as_posix()
    doc = page.read_text(encoding="utf-8")
    if rel_page in {"index.html", "en/index.html"}:
        continue
    for marker in LEGACY_FRAGMENTS:
        if marker in doc:
            fail(f"Eski tek-sayfa anchor'ı kaldı: {rel_page} -> {marker}")

if ERRORS:
    print(f"LINK AUDIT FAILED — {len(ERRORS)} sorun")
    for problem in ERRORS:
        print("  -", problem)
    sys.exit(1)

print(f"LINK AUDIT OK — {len(pages)} HTML sayfası, {CHECKED} yerel hedef/asset kontrol edildi")
