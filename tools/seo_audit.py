#!/usr/bin/env python3
"""Static SEO regression audit for the Karakaş Law Firm site.

Run after tools/build_site.py. Exits non-zero when metadata, sitemap, hreflang,
preview/production indexing state or article schema regresses.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "content.json").read_text(encoding="utf-8"))
FIRM = DATA["firm"]
AREAS = DATA["areas"]
SITE = FIRM.get("siteUrl", "https://www.karakaslawfirm.com").rstrip("/")
PREVIEW = FIRM.get("preview", True)

ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: str) -> str:
    full = ROOT / path
    if not full.exists():
        fail(f"Eksik dosya: {path}")
        return ""
    return full.read_text(encoding="utf-8")


def canonical(doc: str) -> str | None:
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', doc, re.I)
    return m.group(1) if m else None


def meta(doc: str, key: str, *, prop: bool = False) -> str | None:
    kind = "property" if prop else "name"
    m = re.search(
        rf'<meta\s+{kind}=["\']{re.escape(key)}["\'][^>]*content=["\']([^"\']*)',
        doc,
        re.I,
    )
    if not m:
        m = re.search(
            rf'<meta\s+content=["\']([^"\']*)["\'][^>]*{kind}=["\']{re.escape(key)}["\']',
            doc,
            re.I,
        )
    return m.group(1) if m else None


def has_noindex(doc: str) -> bool:
    robots = meta(doc, "robots") or ""
    return "noindex" in robots.lower()


def has_hreflang(doc: str, lang: str, url: str) -> bool:
    pattern = (
        rf'<link\s+rel=["\']alternate["\'][^>]*hreflang=["\']{re.escape(lang)}["\']'
        rf'[^>]*href=["\']{re.escape(url)}["\']'
    )
    reverse = (
        rf'<link\s+rel=["\']alternate["\'][^>]*href=["\']{re.escape(url)}["\']'
        rf'[^>]*hreflang=["\']{re.escape(lang)}["\']'
    )
    return bool(re.search(pattern, doc, re.I) or re.search(reverse, doc, re.I))


CORE: list[tuple[str, str]] = [
    ("index.html", f"{SITE}/"),
    ("hakkimizda/index.html", f"{SITE}/hakkimizda/"),
    ("uzmanlik-alanlari/index.html", f"{SITE}/uzmanlik-alanlari/"),
    ("makaleler/index.html", f"{SITE}/makaleler/"),
    ("makaleler/kira-sozlesmelerinde-tahliye-surecleri/index.html", f"{SITE}/makaleler/kira-sozlesmelerinde-tahliye-surecleri/"),
    ("makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/index.html", f"{SITE}/makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/"),
    ("makaleler/is-hukukunda-kidem-tazminati-sartlari/index.html", f"{SITE}/makaleler/is-hukukunda-kidem-tazminati-sartlari/"),
    ("iletisim/index.html", f"{SITE}/iletisim/"),
    ("kvkk/index.html", f"{SITE}/kvkk/"),
    ("en/index.html", f"{SITE}/en/"),
    ("en/about/index.html", f"{SITE}/en/about/"),
    ("en/articles/index.html", f"{SITE}/en/articles/"),
    ("en/contact/index.html", f"{SITE}/en/contact/"),
    ("en/practice-areas/index.html", f"{SITE}/en/practice-areas/"),
    ("en/privacy/index.html", f"{SITE}/en/privacy/"),
]

DETAILS: list[tuple[str, str]] = []
DETAIL_PAIRS: list[tuple[str, str, str, str]] = []
for area in AREAS:
    tr_slug = area["slug"]["tr"]
    en_slug = area["slug"]["en"]
    tr_path = f"faaliyet-alanlari/{tr_slug}/index.html"
    en_path = f"en/practice-areas/{en_slug}/index.html"
    tr_url = f"{SITE}/faaliyet-alanlari/{tr_slug}/"
    en_url = f"{SITE}/en/practice-areas/{en_slug}/"
    DETAILS.extend([(tr_path, tr_url), (en_path, en_url)])
    DETAIL_PAIRS.append((tr_path, tr_url, en_path, en_url))

EXPECTED = CORE + DETAILS

# ------------------------------------------------------------------ files/meta
for path, expected_url in EXPECTED:
    doc = read(path)
    if not doc:
        continue

    got_canonical = canonical(doc)
    if got_canonical != expected_url:
        fail(f"Canonical hatası {path}: {got_canonical!r} != {expected_url!r}")

    title = re.search(r"<title>(.*?)</title>", doc, re.I | re.S)
    if not title or not re.sub(r"\s+", " ", title.group(1)).strip():
        fail(f"Title eksik: {path}")

    description = meta(doc, "description")
    if not description or len(description.strip()) < 45:
        fail(f"Meta description kısa/eksik: {path}")

    og_image = meta(doc, "og:image", prop=True)
    if not og_image or not og_image.startswith(f"{SITE}/"):
        fail(f"Absolute OG image eksik: {path} -> {og_image!r}")

    if PREVIEW and not has_noindex(doc):
        fail(f"Preview sayfasında noindex eksik: {path}")
    if not PREVIEW and has_noindex(doc):
        fail(f"Production sayfasında noindex kalmış: {path}")

# -------------------------------------------------------------- hreflang pairs
CORE_PAIRS = [
    ("index.html", f"{SITE}/", "en/index.html", f"{SITE}/en/"),
    ("hakkimizda/index.html", f"{SITE}/hakkimizda/", "en/about/index.html", f"{SITE}/en/about/"),
    ("uzmanlik-alanlari/index.html", f"{SITE}/uzmanlik-alanlari/", "en/practice-areas/index.html", f"{SITE}/en/practice-areas/"),
    ("makaleler/index.html", f"{SITE}/makaleler/", "en/articles/index.html", f"{SITE}/en/articles/"),
    ("iletisim/index.html", f"{SITE}/iletisim/", "en/contact/index.html", f"{SITE}/en/contact/"),
    ("kvkk/index.html", f"{SITE}/kvkk/", "en/privacy/index.html", f"{SITE}/en/privacy/"),
]

for tr_path, tr_url, en_path, en_url in CORE_PAIRS + DETAIL_PAIRS:
    tr_doc = read(tr_path)
    en_doc = read(en_path)
    if tr_doc:
        if not has_hreflang(tr_doc, "tr", tr_url):
            fail(f"TR self hreflang eksik: {tr_path}")
        if not has_hreflang(tr_doc, "en", en_url):
            fail(f"TR -> EN hreflang eksik: {tr_path}")
    if en_doc:
        if not has_hreflang(en_doc, "en", en_url):
            fail(f"EN self hreflang eksik: {en_path}")
        if not has_hreflang(en_doc, "tr", tr_url):
            fail(f"EN -> TR hreflang eksik: {en_path}")

# ------------------------------------------------------------------- articles
ARTICLE_PATHS = [
    "makaleler/kira-sozlesmelerinde-tahliye-surecleri/index.html",
    "makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/index.html",
    "makaleler/is-hukukunda-kidem-tazminati-sartlari/index.html",
]
for path in ARTICLE_PATHS:
    doc = read(path)
    if '"@type":"Article"' not in doc and '"@type": "Article"' not in doc:
        fail(f"Article JSON-LD eksik: {path}")
    if "Pınar Karakaş" not in doc:
        fail(f"Makale yazar bilgisi eksik: {path}")

# -------------------------------------------------------------------- sitemap
sitemap = read("sitemap.xml")
expected_urls = [url for _, url in EXPECTED]
for url in expected_urls:
    if f"<loc>{url}</loc>" not in sitemap:
        fail(f"Sitemap URL eksik: {url}")
legacy_index = f"{SITE}/faaliyet-alanlari/"
if f"<loc>{legacy_index}</loc>" in sitemap:
    fail("Eski /faaliyet-alanlari/ genel dizini sitemap'te olmamalı")

# --------------------------------------------------------------------- robots
robots = read("robots.txt")
if PREVIEW:
    if "Disallow: /" not in robots:
        fail("Preview robots.txt Disallow: / içermiyor")
    if "Sitemap:" in robots:
        fail("Preview robots.txt production sitemap ilan etmemeli")
else:
    if "Allow: /" not in robots:
        fail("Production robots.txt Allow: / içermiyor")
    if f"Sitemap: {SITE}/sitemap.xml" not in robots:
        fail("Production robots.txt sitemap satırı eksik")

# --------------------------------------------------------------- special pages
legacy = read("faaliyet-alanlari/index.html")
if canonical(legacy) != f"{SITE}/uzmanlik-alanlari/":
    fail("Legacy faaliyet-alanlari canonical yönlendirmesi hatalı")
if not has_noindex(legacy):
    fail("Legacy faaliyet-alanlari genel sayfası noindex olmalı")

not_found = read("404.html")
if not has_noindex(not_found):
    fail("404.html noindex olmalı")

for path in ("en/index.html", "en/articles/index.html"):
    doc = read(path)
    if "2024-05" in doc or "May 2024" in doc or "Mayıs 2024" in doc:
        fail(f"Eski 2024 makale tarihi kaldı: {path}")

# --------------------------------------------------------------------- report
if ERRORS:
    print(f"SEO AUDIT FAILED — {len(ERRORS)} sorun")
    for problem in ERRORS:
        print("  -", problem)
    sys.exit(1)

print(
    "SEO AUDIT OK — "
    f"{len(EXPECTED)} canonical sayfa, {len(CORE_PAIRS) + len(DETAIL_PAIRS)} hreflang çifti, "
    f"{len(expected_urls)} sitemap URL'si; mode={'preview' if PREVIEW else 'production'}"
)
