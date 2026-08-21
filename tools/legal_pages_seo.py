#!/usr/bin/env python3
"""Normalize SEO metadata for the generated TR/EN legal pages."""
from __future__ import annotations

from seo_postprocess import FIRM, ROOT, SITE, patch_social, set_canonical, set_hreflang, set_robots, set_title

PAGES = [
    {
        "path": "kvkk/index.html",
        "lang": "tr",
        "title": "Aydınlatma Metni | Karakaş Hukuk Bürosu",
        "description": "6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında, bu internet sitesi üzerinden iletilen kişisel verilerin işlenmesine ilişkin bilgilendirme.",
        "url": f"{SITE}/kvkk/",
        "tr": f"{SITE}/kvkk/",
        "en": f"{SITE}/en/privacy/",
        "locale": "tr_TR",
        "site_name": FIRM["name"],
    },
    {
        "path": "en/privacy/index.html",
        "lang": "en",
        "title": "Privacy Notice | Karakaş Law Firm",
        "description": "Information on how personal data submitted through the Karakaş Law Firm website is processed under Turkish Personal Data Protection Law No. 6698.",
        "url": f"{SITE}/en/privacy/",
        "tr": f"{SITE}/kvkk/",
        "en": f"{SITE}/en/privacy/",
        "locale": "en_GB",
        "site_name": FIRM.get("nameEn", "Karakaş Law Firm"),
    },
]


def patch_page(cfg: dict[str, str]) -> None:
    path = ROOT / cfg["path"]
    if not path.exists():
        return
    doc = path.read_text(encoding="utf-8")
    doc = set_title(doc, cfg["title"])
    doc = set_robots(doc)
    doc = set_canonical(doc, cfg["url"])
    doc = set_hreflang(doc, cfg["tr"], cfg["en"], cfg["lang"])
    doc = patch_social(
        doc,
        title=cfg["title"],
        description=cfg["description"],
        url=cfg["url"],
        locale=cfg["locale"],
        site_name=cfg["site_name"],
    )
    path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> None:
    for page in PAGES:
        patch_page(page)
    print(f"Legal SEO tamamlandı: {len(PAGES)} sayfa")


if __name__ == "__main__":
    main()
