#!/usr/bin/env python3
"""One-command build for Karakaş Law Firm.

Runs the content generator, generated-page SEO, hand-written English core SEO,
and the final bilingual sitemap writer. Use this instead of build.py directly.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "tools" / script)], cwd=ROOT, check=True)


def main() -> None:
    run("build.py")
    run("seo_postprocess.py")
    run("core_pages_seo.py")
    run("sitemap_finalize.py")
    print("\nTam site üretimi tamamlandı: içerik + TR/EN SEO + final sitemap.")


if __name__ == "__main__":
    main()
