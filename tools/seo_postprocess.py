#!/usr/bin/env python3
"""Post-process generated Karakaş practice pages for safe, factual metadata.

The site may describe the fields in which the office works, but the generated
pages must not imply specialisation or use repetitive search-ranking phrasing.
Run after the legacy practice-page generator.
"""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "content.json").read_text(encoding="utf-8"))
FIRM = DATA["firm"]
AREAS = DATA["areas"]
SITE = FIRM.get("siteUrl", "https://www.karakaslawfirm.com").rstrip("/")
PREVIEW = FIRM.get("preview", True)
OG_IMAGE = f"{SITE}/assets/og-image.jpg"
TODAY = date.today().isoformat()


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
    pattern = r'<link\s+rel=["\']canonical["\'][^>]*>\s*'
    doc = re.sub(pattern, "", doc, flags=re.I)
    link = f'<link rel="canonical" href="{attr(url)}">\n'
    anchor = re.search(r'<link\s+rel=["\']alternate["\']', doc, flags=re.I)
    if anchor:
        return doc[: anchor.start()] + link + doc[anchor.start() :]
    return doc.replace("</head>", link + "</head>", 1)


def set_robots(doc: str) -> str:
    pattern = r'<meta\s+name=["\']robots["\'][^>]*>\s*'
    doc = re.sub(pattern, "", doc, flags=re.I)
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
        description = clamp(
            f"Karakaş Hukuk Bürosu'nun {area['title']['tr'].lower()} alanındaki çalışma konuları hakkında genel bilgi: {short[:1].lower() + short[1:]}."
        )
        url = f"{SITE}/faaliyet-alanlari/{tr_slug}/"
        tr_url = url
        en_url = f"{SITE}/en/practice-areas/{en_slug}/"
        locale = "tr_TR"
        site_name = FIRM["name"]
        index_href = "../../faaliyet-alanlari/"
        index_schema = f"{SITE}/faaliyet-alanlari/"
    else:
        path = ROOT / "en" / "practice-areas" / en_slug / "index.html"
        title = f"{area['title']['en']} | Karakaş Law Firm"
        short = area["short"]["en"].rstrip(".")
        description = clamp(
            f"General information on the areas in which Karakaş Law Firm works in {area['title']['en'].lower()}: {short[:1].lower() + short[1:]}."
        )
        url = f"{SITE}/en/practice-areas/{en_slug}/"
        tr_url = f"{SITE}/faaliyet-alanlari/{tr_slug}/"
        en_url = url
        locale = "en_GB"
        site_name = FIRM.get("nameEn", "Karakaş Law Firm")
        index_href = "../"
        index_schema = f"{SITE}/en/practice-areas/"

    if not path.exists():
        return
    doc = path.read_text(encoding="utf-8")
    doc = set_title(doc, title)
    doc = set_robots(doc)
    doc = set_canonical(doc, url)
    doc = set_hreflang(doc, tr_url, en_url, lang)
    doc = patch_social(doc, title=title, description=description, url=url, locale=locale, site_name=site_name)

    if lang == "tr":
        doc = doc.replace(
            'href="../../faaliyet-alanlari/">Faaliyet Alanları</a>',
            f'href="{index_href}">Çalışma Alanları</a>',
        )
        doc = doc.replace(f'"item":"{SITE}/uzmanlik-alanlari/"', f'"item":"{index_schema}"')
        doc = doc.replace('"name":"Uzmanlık Alanlarımız"', '"name":"Çalışma Alanları"')
        doc = doc.replace('"name":"Faaliyet Alanları"', '"name":"Çalışma Alanları"')

    path.write_text(doc, encoding="utf-8", newline="\n")


def patch_en_index() -> None:
    path = ROOT / "en" / "practice-areas" / "index.html"
    if not path.exists():
        return
    doc = path.read_text(encoding="utf-8")
    title = "Practice Areas | Karakaş Law Firm"
    desc = "General information on the fields in which Karakaş Law Firm works, including corporate, disputes, maritime, real estate, finance and employment matters."
    url = f"{SITE}/en/practice-areas/"
    doc = set_title(doc, title)
    doc = set_robots(doc)
    doc = set_canonical(doc, url)
    doc = set_hreflang(doc, f"{SITE}/faaliyet-alanlari/", url, "en")
    doc = patch_social(doc, title=title, description=clamp(desc), url=url, locale="en_GB", site_name=FIRM.get("nameEn", "Karakaş Law Firm"))
    doc = doc.replace('../../uzmanlik-alanlari/', '../../faaliyet-alanlari/')
    doc = doc.replace(f'"item":"{SITE}/uzmanlik-alanlari/"', f'"item":"{SITE}/faaliyet-alanlari/"')
    path.write_text(doc, encoding="utf-8", newline="\n")


def write_specialisation_redirect() -> None:
    path = ROOT / "uzmanlik-alanlari" / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    target = f"{SITE}/faaliyet-alanlari/"
    doc = f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Çalışma Alanları | Karakaş Hukuk Bürosu</title><meta name="robots" content="noindex, follow">
<link rel="canonical" href="{target}"><meta http-equiv="refresh" content="0;url={target}">
<script>location.replace({json.dumps(target)});</script></head>
<body><p><a href="{target}">Çalışma Alanları sayfasına geçin.</a></p></body></html>'''
    path.write_text(doc, encoding="utf-8", newline="\n")


def patch_robots() -> None:
    path = ROOT / "robots.txt"
    if PREVIEW:
        doc = "# Hazırlık aşaması: staging kopyası arama motorlarına kapalıdır.\nUser-agent: *\nDisallow: /\n"
    else:
        doc = f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"
    path.write_text(doc, encoding="utf-8", newline="\n")


def build_sitemap() -> None:
    urls: list[tuple[str, str | None]] = [
        ("", TODAY),
        ("hakkimizda/", TODAY),
        ("faaliyet-alanlari/", TODAY),
        ("iletisim/", TODAY),
        ("kvkk/", None),
        ("en/", TODAY),
        ("en/about/", TODAY),
        ("en/contact/", TODAY),
        ("en/practice-areas/", TODAY),
        ("en/privacy/", None),
    ]
    for area in AREAS:
        urls.append((f"faaliyet-alanlari/{area['slug']['tr']}/", TODAY))
        urls.append((f"en/practice-areas/{area['slug']['en']}/", TODAY))

    rows = []
    for slug, lastmod in urls:
        extra = f"<lastmod>{lastmod}</lastmod>" if lastmod else ""
        rows.append(f"  <url><loc>{SITE}/{slug}</loc>{extra}</url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")


def main() -> None:
    for area in AREAS:
        patch_detail("tr", area)
        patch_detail("en", area)
    patch_en_index()
    write_specialisation_redirect()
    build_sitemap()
    patch_robots()
    print(f"Compliance-aware SEO post-process tamamlandı: {len(AREAS) * 2} faaliyet detayı + EN index/redirect/sitemap/robots")


if __name__ == "__main__":
    main()
