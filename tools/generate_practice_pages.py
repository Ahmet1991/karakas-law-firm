#!/usr/bin/env python3
"""Generate only the pages still owned by the legacy content generator.

The redesigned TR/EN homepages are hand-written and no longer contain the
AREAS:START/END markers expected by build.py's sync_home(). Import the generator
as a module and call only the page builders we still need.
"""
from __future__ import annotations

import build


def main() -> None:
    written: list[str] = []

    for lang in ("tr", "en"):
        written.append(build.write(*build.build_areas_index(lang)))
        for i in range(len(build.AREAS)):
            written.append(build.write(*build.build_area_page(lang, i)))
        written.append(build.write(*build.build_legal_page(lang)))

    # sitemap is deliberately omitted here. sitemap_finalize.py owns the final
    # bilingual sitemap after all SEO post-processing is complete.
    written.append(build.build_robots())

    print(f"{len(written)} legacy-owned sayfa/dosya üretildi:")
    for path in written:
        print("  " + path)


if __name__ == "__main__":
    main()
