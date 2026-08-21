#!/usr/bin/env python3
"""Normalize metadata for hand-written bilingual core pages.

Article drafts remain permanently noindex until the lawyer expressly approves
publication.
"""
from __future__ import annotations

import re

from seo_postprocess import FIRM, ROOT, SITE, patch_social, set_canonical, set_hreflang, set_robots, set_title

EN_PAGES = [
    {
        "path": "en/index.html",
        "title": "Karakaş Law Firm | İzmir",
        "description": "Karakaş Law Firm was founded in İzmir by Attorney Pınar Karakaş. Office information and fields of legal practice.",
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
    ("iletisim/index.html", f"{SITE}/iletisim/", f"{SITE}/en/contact/"),
]

DRAFT_PAGES = [
    "makaleler/index.html",
    "makaleler/kira-sozlesmelerinde-tahliye-surecleri/index.html",
    "makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/index.html",
    "makaleler/is-hukukunda-kidem-tazminati-sartlari/index.html",
    "en/articles/index.html",
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


def force_noindex(path_str: str) -> None:
    path = ROOT / path_str
    if not path.exists():
        return
    doc = path.read_text(encoding="utf-8")
    doc = re.sub(r'<meta\s+name=["\']robots["\'][^>]*>\s*', "", doc, flags=re.I)
    doc = doc.replace("</head>", '<meta name="robots" content="noindex, nofollow">\n</head>', 1)
    path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> None:
    for page in EN_PAGES:
        patch_en_page(page)
    for path_str, tr_url, en_url in TR_CORE:
        patch_tr_core(path_str, tr_url, en_url)
    for path_str in DRAFT_PAGES:
        force_noindex(path_str)
    print(
        "Core metadata tamamlandı: "
        f"{len(EN_PAGES)} EN public + {len(TR_CORE)} TR public + "
        f"{len(DRAFT_PAGES)} article draft noindex"
    )


if __name__ == "__main__":
    main()
