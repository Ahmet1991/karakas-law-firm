#!/usr/bin/env python3
"""Normalize metadata for hand-written bilingual core and article pages."""
from __future__ import annotations

from seo_postprocess import FIRM, ROOT, SITE, patch_social, set_canonical, set_hreflang, set_robots, set_title

EN_PAGES = [
    {
        "path": "en/index.html",
        "title": "Karakaş Law Firm | İzmir",
        "description": "Karakaş Law Firm was founded in İzmir by Attorney Pınar Karakaş. Office information, practice areas and legal articles.",
        "url": f"{SITE}/en/",
        "tr": f"{SITE}/",
    },
    {
        "path": "en/about/index.html",
        "title": "Pınar Karakaş | Karakaş Law Firm",
        "description": "Professional and educational information about Attorney Pınar Karakaş, founder of Karakaş Law Firm in İzmir.",
        "url": f"{SITE}/en/about/",
        "tr": f"{SITE}/hakkimizda/",
    },
    {
        "path": "en/articles/index.html",
        "title": "Legal Articles | Karakaş Law Firm",
        "description": "Articles from Karakaş Law Firm on lease law, commercial contracts, employment law and related legal topics.",
        "url": f"{SITE}/en/articles/",
        "tr": f"{SITE}/makaleler/",
    },
    {
        "path": "en/contact/index.html",
        "title": "Contact | Karakaş Law Firm",
        "description": "Address, telephone and email information for Karakaş Law Firm in Konak, İzmir.",
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

ARTICLE_PAIRS = [
    (
        "makaleler/kira-sozlesmelerinde-tahliye-surecleri/index.html",
        f"{SITE}/makaleler/kira-sozlesmelerinde-tahliye-surecleri/",
        "en/articles/lease-eviction-processes/index.html",
        f"{SITE}/en/articles/lease-eviction-processes/",
    ),
    (
        "makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/index.html",
        f"{SITE}/makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/",
        "en/articles/commercial-contracts-key-considerations/index.html",
        f"{SITE}/en/articles/commercial-contracts-key-considerations/",
    ),
    (
        "makaleler/is-hukukunda-kidem-tazminati-sartlari/index.html",
        f"{SITE}/makaleler/is-hukukunda-kidem-tazminati-sartlari/",
        "en/articles/severance-pay-conditions/index.html",
        f"{SITE}/en/articles/severance-pay-conditions/",
    ),
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


def patch_article_pair(tr_path_str: str, tr_url: str, en_path_str: str, en_url: str) -> None:
    tr_path = ROOT / tr_path_str
    en_path = ROOT / en_path_str
    if tr_path.exists():
        doc = tr_path.read_text(encoding="utf-8")
        doc = set_robots(doc)
        doc = set_canonical(doc, tr_url)
        doc = set_hreflang(doc, tr_url, en_url, "tr")
        tr_path.write_text(doc, encoding="utf-8", newline="\n")
    if en_path.exists():
        doc = en_path.read_text(encoding="utf-8")
        doc = set_robots(doc)
        doc = set_canonical(doc, en_url)
        doc = set_hreflang(doc, tr_url, en_url, "en")
        en_path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> None:
    for page in EN_PAGES:
        patch_en_page(page)
    for path_str, tr_url, en_url in TR_CORE:
        patch_tr_core(path_str, tr_url, en_url)
    for pair in ARTICLE_PAIRS:
        patch_article_pair(*pair)
    print(
        "Core metadata tamamlandı: "
        f"{len(EN_PAGES)} EN public + {len(TR_CORE)} TR public + "
        f"{len(ARTICLE_PAIRS)} bilingual article pairs"
    )


if __name__ == "__main__":
    main()
