#!/usr/bin/env python3
"""Generate only pages still owned by the legacy content generator.

Hand-written pages are preserved: TR/EN homepages, TR practice landing and
TR/EN privacy pages. The legacy generator owns only 24 practice detail pages,
the EN practice index and preview robots; persistent post-processes run after.
"""
from __future__ import annotations

import build


def main() -> None:
    written: list[str] = []

    # TR /faaliyet-alanlari/ is a hand-written compliance-conscious landing.
    # EN /practice-areas/ remains generated.
    written.append(build.write(*build.build_areas_index("en")))

    for lang in ("tr", "en"):
        for i in range(len(build.AREAS)):
            written.append(build.write(*build.build_area_page(lang, i)))

    # Hand-written pages intentionally NOT regenerated here:
    #   index.html / en/index.html
    #   faaliyet-alanlari/index.html
    #   kvkk/index.html / en/privacy/index.html
    # sitemap is omitted; sitemap_finalize.py owns the final bilingual file.
    written.append(build.build_robots())

    print(f"{len(written)} legacy-owned sayfa/dosya üretildi:")
    for path in written:
        print("  " + path)


if __name__ == "__main__":
    main()
