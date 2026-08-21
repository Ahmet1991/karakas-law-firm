#!/usr/bin/env python3
"""Normalize generated TR/EN practice pages and preserve the redesigned
/uzmanlik-alanlari/ page as the Turkish overview.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "content.json").read_text(encoding="utf-8"))
FIRM = DATA["firm"]
AREAS = DATA["areas"]
SITE = FIRM.get("siteUrl", "https://www.karakaslawfirm.com").rstrip("/")
PREVIEW = FIRM.get("preview", True)
OG_IMAGE = f"{SITE}/assets/og-image.jpg"


def attr(value: str) -> str:
    return html.escape(value, quote=True)


def clamp(text: str, limit: int = 158) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return cut + "…"


def set_title(doc: str, value: str) -> str:
    value = html.escape(value)
    if re.search(r"<title>.*?</title>", doc, flags=re.S | re.I):
        return re.sub(r"<title>.*?</title>", f"<title>{value}</title>", doc, count=1, flags=re.S | re.I)
    return doc.replace("</head>", f"<title>{value}</title>\n</head>", 1)


def set_meta(doc: str, key: str, value: str, *, prop: bool = False) -> str:
    kind = "property" if prop else "name"
    pattern = rf'<meta\s+{kind}=["\']{re.escape(key)}["\'][^>]*>'
    replacement = f'<meta {kind}="{attr(key)}" content="{attr(value)}">'
    if re.search(pattern, doc, flags=re.I):
        return re.sub(pattern, replacement, doc, count=1, flags=re.I)
    return doc.replace("</head>", replacement + "\n</head>", 1)


def set_canonical(doc: str, url: str) -> str:
    doc = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>\s*', "", doc, flags=re.I)
    link = f'<link rel="canonical" href="{attr(url)}">\n'
    anchor = re.search(r'<link\s+rel=["\']alternate["\']', doc, flags=re.I)
    if anchor:
        return doc[: anchor.start()] + link + doc[anchor.start() :]
    return doc.replace("</head>", link + "</head>", 1)


def set_robots(doc: str) -> str:
    doc = re.sub(r'<meta\s+name=["\']robots["\'][^>]*>\s*', "", doc, flags=re.I)
    if PREVIEW:
        return doc.replace("</head>", '<meta name="robots" content="noindex, nofollow">\n</head>', 1)
    return doc


def set_hreflang(doc: str, tr_url: str, en_url: str, current: str) -> str:
    doc = re.sub(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\'][^"\']+["\'][^>]*>\s*', "", doc, flags=re.I)
    links = (
        f'<link rel="alternate" hreflang="tr" href="{attr(tr_url)}">\n'
        f'<link rel="alternate" hreflang="en" href="{attr(en_url)}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{attr(tr_url)}">\n'
    )
    icon = re.search(r'<link\s+rel=["\']icon["\']', doc, flags=re.I)
    if icon:
        return doc[: icon.start()] + links + doc[icon.start() :]
    return doc.replace("</head>", links + "</head>", 1)


def patch_social(doc: str, *, title: str, description: str, url: str, locale: str, site_name: str) -> str:
    doc = set_meta(doc, "description", description)
    doc = set_meta(doc, "og:type", "website", prop=True)
    doc = set_meta(doc, "og:locale", locale, prop=True)
    doc = set_meta(doc, "og:site_name", site_name, prop=True)
    doc = set_meta(doc, "og:title", title, prop=True)
    doc = set_meta(doc, "og:description", description, prop=True)
    doc = set_meta(doc, "og:url", url, prop=True)
    doc = set_meta(doc, "og:image", OG_IMAGE, prop=True)
    doc = set_meta(doc, "og:image:alt", f"{title} — Karakaş", prop=True)
    doc = set_meta(doc, "twitter:card", "summary_large_image")
    doc = set_meta(doc, "twitter:title", title)
    doc = set_meta(doc, "twitter:description", description)
    doc = set_meta(doc, "twitter:image", OG_IMAGE)
    return doc


def patch_detail(lang: str, area: dict) -> None:
    tr_slug = area["slug"]["tr"]
    en_slug = area["slug"]["en"]

    if lang == "tr":
        path = ROOT / "faaliyet-alanlari" / tr_slug / "index.html"
        title = f"{area['title']['tr']} | Karakaş Hukuk Bürosu"
        short = area["short"]["tr"].rstrip(".")
        description = clamp(f"Karakaş Hukuk Bürosu — {area['title']['tr']}: {short}.")
        url = f"{SITE}/faaliyet-alanlari/{tr_slug}/"
        tr_url = url
        en_url = f"{SITE}/en/practice-areas/{en_slug}/"
        locale = "tr_TR"
        site_name = FIRM["name"]
    else:
        path = ROOT / "en" / "practice-areas" / en_slug / "index.html"
        title = f"{area['title']['en']} | Karakaş Law Firm"
        short = area["short"]["en"].rstrip(".")
        description = clamp(f"Karakaş Law Firm — {area['title']['en']}: {short}.")
        url = f"{SITE}/en/practice-areas/{en_slug}/"
        tr_url = f"{SITE}/faaliyet-alanlari/{tr_slug}/"
        en_url = url
        locale = "en_GB"
        site_name = FIRM.get("nameEn", "Karakaş Law Firm")

    if not path.exists():
        return

    doc = path.read_text(encoding="utf-8")
    doc = set_title(doc, title)
    doc = set_robots(doc)
    doc = set_canonical(doc, url)
    doc = set_hreflang(doc, tr_url, en_url, lang)
    doc = patch_social(doc, title=title, description=description, url=url, locale=locale, site_name=site_name)

    if lang == "tr":
        doc = doc.replace('href="../../faaliyet-alanlari/">Faaliyet Alanları</a>', 'href="../../uzmanlik-alanlari/">Uzmanlık Alanlarımız</a>')
        doc = doc.replace('href="../../faaliyet-alanlari/">Çalışma Alanları</a>', 'href="../../uzmanlik-alanlari/">Uzmanlık Alanlarımız</a>')
        doc = doc.replace(f'"item":"{SITE}/faaliyet-alanlari/"', f'"item":"{SITE}/uzmanlik-alanlari/"')
        doc = doc.replace('"name":"Faaliyet Alanları"', '"name":"Uzmanlık Alanlarımız"')
        doc = doc.replace('"name":"Çalışma Alanları"', '"name":"Uzmanlık Alanlarımız"')

    path.write_text(doc, encoding="utf-8", newline="\n")


def patch_en_index() -> None:
    path = ROOT / "en" / "practice-areas" / "index.html"
    if not path.exists():
        return
    doc = path.read_text(encoding="utf-8")
    title = "Practice Areas | Karakaş Law Firm"
    desc = "Karakaş Law Firm practice areas including corporate, disputes, maritime, real estate, finance and employment matters."
    url = f"{SITE}/en/practice-areas/"
    doc = set_title(doc, title)
    doc = set_robots(doc)
    doc = set_canonical(doc, url)
    doc = set_hreflang(doc, f"{SITE}/uzmanlik-alanlari/", url, "en")
    doc = patch_social(doc, title=title, description=clamp(desc), url=url, locale="en_GB", site_name=FIRM.get("nameEn", "Karakaş Law Firm"))
    path.write_text(doc, encoding="utf-8", newline="\n")


def write_legacy_overview_redirect() -> None:
    """Keep /faaliyet-alanlari/ detail URLs, but send the old overview URL to
    the redesigned /uzmanlik-alanlari/ page."""
    path = ROOT / "faaliyet-alanlari" / "index.html"
    target = f"{SITE}/uzmanlik-alanlari/"
    doc = f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Uzmanlık Alanlarımız | Karakaş Hukuk Bürosu</title><meta name="robots" content="noindex, follow">
<link rel="canonical" href="{target}"><meta http-equiv="refresh" content="0;url={target}">
<script>location.replace({json.dumps(target)});</script></head>
<body><p><a href="{target}">Uzmanlık Alanlarımız sayfasına geçin.</a></p></body></html>'''
    path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> None:
    for area in AREAS:
        patch_detail("tr", area)
        patch_detail("en", area)
    patch_en_index()
    write_legacy_overview_redirect()
    print(f"SEO post-process tamamlandı: {len(AREAS) * 2} faaliyet detayı + Uzmanlık overview eşlemesi")


if __name__ == "__main__":
    main()
