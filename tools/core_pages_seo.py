#!/usr/bin/env python3
"""Normalize SEO metadata for hand-written bilingual core pages."""
from __future__ import annotations

from seo_postprocess import FIRM, ROOT, SITE, patch_social, set_canonical, set_hreflang, set_robots, set_title

EN_PAGES = [
    {
        "path": "en/index.html",
        "title": "Karakaş Law Firm | İzmir Corporate & Commercial Law",
        "description": "Karakaş Law Firm is an İzmir-based law firm advising companies and individuals on corporate, disputes, maritime, real estate, finance, employment and related matters.",
        "url": f"{SITE}/en/",
        "tr": f"{SITE}/",
    },
    {
        "path": "en/about/index.html",
        "title": "About Pınar Karakaş | Karakaş Law Firm İzmir",
        "description": "Learn about Karakaş Law Firm's approach and founding attorney Pınar Karakaş, including her education, professional background and areas of practice in İzmir.",
        "url": f"{SITE}/en/about/",
        "tr": f"{SITE}/hakkimizda/",
    },
    {
        "path": "en/articles/index.html",
        "title": "Legal Articles & Insights | Karakaş Law Firm İzmir",
        "description": "Legal articles and practical notes from Karakaş Law Firm in İzmir on leases, commercial contracts, employment law and related legal developments.",
        "url": f"{SITE}/en/articles/",
        "tr": f"{SITE}/makaleler/",
    },
    {
        "path": "en/contact/index.html",
        "title": "Contact & Office Location | Karakaş Law Firm İzmir",
        "description": "Contact Karakaş Law Firm in Konak, İzmir. View the Armesa İş Merkezi office address, phone, WhatsApp, email and directions.",
        "url": f"{SITE}/en/contact/",
        "tr": f"{SITE}/iletisim/",
    },
]

TR_CORE = [
    ("index.html", f"{SITE}/", f"{SITE}/en/"),
    ("hakkimizda/index.html", f"{SITE}/hakkimizda/", f"{SITE}/en/about/"),
    ("uzmanlik-alanlari/index.html", f"{SITE}/uzmanlik-alanlari/", f"{SITE}/en/practice-areas/"),
    ("makaleler/index.html", f"{SITE}/makaleler/", f"{SITE}/en/articles/"),
    ("iletisim/index.html", f"{SITE}/iletisim/", f"{SITE}/en/contact/"),
]

# These pages have no full English translation yet, so they should not get a
# fake hreflang pair. They do still need preview/live robots state controlled
# by firm.preview.
TR_ARTICLE_PAGES = [
    "makaleler/kira-sozlesmelerinde-tahliye-surecleri/index.html",
    "makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/index.html",
    "makaleler/is-hukukunda-kidem-tazminati-sartlari/index.html",
]


def patch_en_page(cfg: dict[str, str]) -> None:
    path = ROOT / cfg["path"]
    if not path.exists():
        return
    doc = path.read_text(encoding="utf-8")
    doc = set_title(doc, cfg["title"])
    doc = set_robots(doc)
    doc = set_canonical(doc, cfg["url"])
    doc = set_hreflang(doc, cfg["tr"], cfg["url"], "en")
    doc = patch_social(
        doc,
        title=cfg["title"],
        description=cfg["description"],
        url=cfg["url"],
        locale="en_GB",
        site_name=FIRM.get("nameEn", "Karakaş Law Firm"),
    )
    path.write_text(doc, encoding="utf-8", newline="\n")


def patch_tr_core(path_str: str, tr_url: str, en_url: str) -> None:
    path = ROOT / path_str
    if not path.exists():
        return
    doc = path.read_text(encoding="utf-8")
    doc = set_robots(doc)
    doc = set_hreflang(doc, tr_url, en_url, "tr")
    path.write_text(doc, encoding="utf-8", newline="\n")


def patch_robots_only(path_str: str) -> None:
    path = ROOT / path_str
    if not path.exists():
        return
    doc = path.read_text(encoding="utf-8")
    doc = set_robots(doc)
    path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> None:
    for page in EN_PAGES:
        patch_en_page(page)
    for path_str, tr_url, en_url in TR_CORE:
        patch_tr_core(path_str, tr_url, en_url)
    for path_str in TR_ARTICLE_PAGES:
        patch_robots_only(path_str)
    print(
        "Core SEO tamamlandı: "
        f"{len(EN_PAGES)} EN metadata + {len(TR_CORE)} TR core + "
        f"{len(TR_ARTICLE_PAGES)} TR article robots"
    )


if __name__ == "__main__":
    main()
