#!/usr/bin/env python3
"""Write the final robots.txt according to firm.preview."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "content.json").read_text(encoding="utf-8"))
FIRM = DATA["firm"]
SITE = FIRM.get("siteUrl", "https://www.karakaslawfirm.com").rstrip("/")
PREVIEW = FIRM.get("preview", True)


def main() -> None:
    if PREVIEW:
        doc = (
            "# Hazırlık aşaması: staging kopyası arama motorlarına kapalıdır.\n"
            "# Production domain bu repoya geçtiğinde firm.preview=false yapıp\n"
            "# python tools/build_site.py çalıştırın.\n"
            "User-agent: *\n"
            "Disallow: /\n"
        )
    else:
        doc = (
            "User-agent: *\n"
            "Allow: /\n\n"
            f"Sitemap: {SITE}/sitemap.xml\n"
        )
    (ROOT / "robots.txt").write_text(doc, encoding="utf-8", newline="\n")
    print("robots.txt:", "preview / blocked" if PREVIEW else "production / open")


if __name__ == "__main__":
    main()
