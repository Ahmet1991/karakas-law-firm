#!/usr/bin/env python3
"""Write the final bilingual sitemap after all page generators have run."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "content.json").read_text(encoding="utf-8"))
SITE = DATA["firm"].get("siteUrl", "https://www.karakaslawfirm.com").rstrip("/")
AREAS = DATA["areas"]
TODAY = date.today().isoformat()


def main() -> None:
    urls: list[tuple[str, str | None]] = [
        ("", TODAY),
        ("hakkimizda/", TODAY),
        ("uzmanlik-alanlari/", TODAY),
        ("makaleler/", "2026-08-21"),
        ("makaleler/kira-sozlesmelerinde-tahliye-surecleri/", "2026-08-21"),
        ("makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/", "2026-08-21"),
        ("makaleler/is-hukukunda-kidem-tazminati-sartlari/", "2026-08-21"),
        ("iletisim/", TODAY),
        ("kvkk/", None),
        ("en/", TODAY),
        ("en/about/", TODAY),
        ("en/articles/", "2026-08-21"),
        ("en/articles/lease-eviction-processes/", "2026-08-21"),
        ("en/articles/commercial-contracts-key-considerations/", "2026-08-21"),
        ("en/articles/severance-pay-conditions/", "2026-08-21"),
        ("en/contact/", TODAY),
        ("en/practice-areas/", TODAY),
        ("en/privacy/", None),
    ]

    for area in AREAS:
        urls.append((f"faaliyet-alanlari/{area['slug']['tr']}/", TODAY))
        urls.append((f"en/practice-areas/{area['slug']['en']}/", TODAY))

    rows = []
    for slug, modified in urls:
        lastmod = f"<lastmod>{modified}</lastmod>" if modified else ""
        rows.append(f"  <url><loc>{SITE}/{slug}</loc>{lastmod}</url>")

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")
    print(f"Final sitemap yazıldı: {len(urls)} URL")


if __name__ == "__main__":
    main()
