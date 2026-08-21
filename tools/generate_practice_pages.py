#!/usr/bin/env python3
"""Generate only pages still owned by the legacy content generator.

The redesigned homepages and TR/EN privacy pages are hand-written. This wrapper
therefore generates only the practice-area indexes/details plus preview robots;
persistent SEO passes run afterwards from build_site.py.
"""
from __future__ import annotations

import build


def main() -> None:
    written: list[str] = []

    for lang in ("tr", "en"):
        written.append(build.write(*build.build_areas_index(lang)))
        for i in range(len(build.AREAS)):
            written.append(build.write(*build.build_area_page(lang, i)))

    # Hand-written pages intentionally NOT regenerated here:
    #   index.html / en/index.html
    #   kvkk/index.html / en/privacy/index.html
    # sitemap is also omitted; sitemap_finalize.py owns the final bilingual file.
    written.append(build.build_robots())

    print(f"{len(written)} legacy-owned sayfa/dosya üretildi:")
    for path in written:
        print("  " + path)


if __name__ == "__main__":
    main()
