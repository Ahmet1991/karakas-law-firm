#!/usr/bin/env python3
"""One-command build for Karakaş Law Firm.

Generates only legacy-owned practice/legal pages, then applies the persistent
SEO layer, bilingual core/legal metadata, final sitemap and environment-aware
robots. The redesigned homepages are never rewritten by the legacy generator.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "tools" / script)], cwd=ROOT, check=True)


def main() -> None:
    run("generate_practice_pages.py")
    run("seo_postprocess.py")
    run("core_pages_seo.py")
    run("legal_pages_seo.py")
    run("sitemap_finalize.py")
    run("robots_finalize.py")
    print("\nTam site üretimi tamamlandı: faaliyet + TR/EN core/legal SEO + sitemap + robots.")


if __name__ == "__main__":
    main()
