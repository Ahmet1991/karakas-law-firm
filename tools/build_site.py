#!/usr/bin/env python3
"""One-command build for Karakaş Law Firm.

Runs the existing content generator, the persistent SEO post-process and the
final bilingual sitemap writer. Use this instead of calling build.py directly.
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
    run("sitemap_finalize.py")
    print("\nTam site üretimi tamamlandı: içerik + kalıcı SEO + final sitemap.")


if __name__ == "__main__":
    main()
