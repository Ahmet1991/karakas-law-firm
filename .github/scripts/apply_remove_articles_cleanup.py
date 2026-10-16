#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def save(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8", newline="\n")


def replace_file(rel: str, pairs: list[tuple[str, str]]) -> None:
    text = load(rel)
    for old, new in pairs:
        text = text.replace(old, new)
    save(rel, text)


# ------------------------------------------------------------------ generators
replace_file(
    "tools/build.py",
    [
        ('            ("makaleler/", "Makaleler"),\n', ""),
        ('            ("articles/", "Articles"),\n', ""),
        ("elle yazılan sayfalarla (hakkimizda, iletisim, makaleler)", "elle yazılan sayfalarla (hakkimizda, iletisim)"),
    ],
)

replace_file(
    "tools/build-footer.py",
    [
        ("          ('makaleler/', 'Makaleler'), ", ""),
        ("          ('articles/', 'Articles'), ", ""),
        ("  ('uzmanlik-alanlari/index.html', TR, 1, 1), ('makaleler/index.html', TR, 1, 1),\n", "  ('uzmanlik-alanlari/index.html', TR, 1, 1),\n"),
        ("  ('en/practice-areas/index.html', EN, 2, 1), ('en/articles/index.html', EN, 2, 1),\n", "  ('en/practice-areas/index.html', EN, 2, 1),\n"),
    ],
)

replace_file(
    "tools/en_template.py",
    [
        ("NAV = [('', 'Home'), ('about/', 'About'), ('practice-areas/', 'Practice Areas'),\n       ('articles/', 'Articles'), ('contact/', 'Contact')]", "NAV = [('', 'Home'), ('about/', 'About'), ('practice-areas/', 'Practice Areas'),\n       ('contact/', 'Contact')]"),
        ("        '<a href=\"' + en_root + 'articles/\">Articles</a>'\n", ""),
    ],
)

# build-en.py is a legacy/manual generator; remove all article generation paths
# so it cannot re-introduce the retired section if someone runs it later.
text = load("tools/build-en.py")
text = re.sub(r"\nARTICLES = \[\n.*?\n\]\n\n# ---------------------------------------------------------------- homepage --", "\n# ---------------------------------------------------------------- homepage --", text, flags=re.S)
text = re.sub(r"\nart = ''\n.*?\n\ns = head\(", "\n\ns = head(", text, flags=re.S)
text = re.sub(
    r"\n  '<section class=\\\"section section--deep\\\"><div class=\\\"shell\\\"><div class=\\\"section-head reveal\\\">'.*?'<div class=\\\"article-grid\\\">' \+ art \+ '</div></div></section>\\n'",
    "",
    text,
    flags=re.S,
)
article_head = "s = head('Articles | Karakaş Law Firm'"
if article_head in text:
    start = text.rfind("\n#", 0, text.index(article_head))
    end_marker = "# ---------------------------------------------------------------- contact --"
    end = text.find(end_marker, text.index(article_head))
    if start != -1 and end != -1:
        text = text[:start] + "\n" + text[end:]
text = text.replace("print('yazildi: en/index.html, en/about/, en/practice-areas/, en/articles/, en/contact/')", "print('yazildi: en/index.html, en/about/, en/practice-areas/, en/contact/')")
save("tools/build-en.py", text)

# Final sitemap no longer advertises retired article URLs.
text = load("tools/sitemap_finalize.py")
text = "\n".join(line for line in text.splitlines() if '"makaleler/' not in line and '"en/articles/' not in line) + "\n"
save("tools/sitemap_finalize.py", text)

# Core SEO metadata now covers only pages that still exist.
text = load("tools/core_pages_seo.py")
text = text.replace("hand-written bilingual core and article pages", "hand-written bilingual core pages")
text = re.sub(r"\n    \{\n        \"path\": \"en/articles/index\.html\",.*?\n    \},", "", text, flags=re.S)
text = "\n".join(line for line in text.splitlines() if '("makaleler/index.html"' not in line) + "\n"
text = re.sub(r"\nARTICLE_PAIRS = \[.*?\n\]\n", "\n", text, flags=re.S)
text = re.sub(r"\n\ndef patch_article_pair\(.*?(?=\n\ndef main\(\))", "", text, flags=re.S)
text = re.sub(r"\n    for pair in ARTICLE_PAIRS:\n        patch_article_pair\(\*pair\)", "", text)
text = re.sub(
    r"    print\(\n        \"Core metadata tamamlandı: \"\n        f\"\{len\(EN_PAGES\)\} EN public \+ \{len\(TR_CORE\)\} TR public \+ \"\n        f\"\{len\(ARTICLE_PAIRS\)\} bilingual article pairs\"\n    \)",
    '    print(f"Core metadata tamamlandı: {len(EN_PAGES)} EN public + {len(TR_CORE)} TR public")',
    text,
)
save("tools/core_pages_seo.py", text)

# SEO audit must stop requiring pages and Article JSON-LD that are intentionally removed.
text = load("tools/seo_audit.py")
text = text.replace("preview/production indexing state or article schema regresses.", "preview/production indexing state regresses.")
text = "\n".join(
    line for line in text.splitlines()
    if '"makaleler/' not in line and '"en/articles/' not in line
) + "\n"
text = re.sub(r"\n# ------------------------------------------------------------------- articles\n.*?(?=\n# -------------------------------------------------------------------- sitemap)", "", text, flags=re.S)
text = text.replace('for path in ("en/index.html", "en/articles/index.html"):', 'for path in ("en/index.html",):')
save("tools/seo_audit.py", text)

# Documentation and CI should describe only the current site structure.
text = load("README.md")
filtered = []
for line in text.splitlines():
    if any(marker in line for marker in ("`makaleler/", "`en/articles/", "`assets/makale-", "`Article`")):
        continue
    filtered.append(line)
save("README.md", "\n".join(filtered) + "\n")

text = load(".github/workflows/seo-build.yml")
text = text.replace(" uzmanlik-alanlari makaleler iletisim", " uzmanlik-alanlari iletisim")
save(".github/workflows/seo-build.yml", text)

# ---------------------------------------------------------------- legal sources
text = load("tools/legal-tr.html")
text = re.sub(r'^<p class="notice">.*?</p>\n', "", text, count=1, flags=re.S)
text = text.replace(" Kullanılan sağlayıcılar ve aktarım mekanizmaları yayına alınmadan önce ayrıca doğrulanmalıdır.", "")
text = text.replace(" Başvuru yöntemi ve kimlik doğrulama usulü yayına alınmadan önce nihai metinde açıkça belirtilmelidir.", "")
save("tools/legal-tr.html", text)

text = load("tools/legal-en.html")
text = re.sub(r'^<p class="notice">.*?</p>\n', "", text, count=1, flags=re.S)
text = text.replace(" The provider and relevant transfer mechanism should be confirmed before launch.", "")
text = text.replace(" The final notice should specify the application method and identity-verification procedure before launch.", "")
save("tools/legal-en.html", text)

# -------------------------------------------------------------- public pages
# Remove the English homepage Insights/articles section as one visual block.
path = ROOT / "en/index.html"
text = path.read_text(encoding="utf-8")
text = re.sub(
    r'\s*<section class="section section--deep"><div class="shell"><div class="section-head reveal"><div><p class="section-label"[^>]*>Insights</p>.*?</section>\s*',
    "\n",
    text,
    flags=re.S,
)
path.write_text(text, encoding="utf-8", newline="\n")

# Remove menu/footer anchors to the retired TR/EN article routes from every remaining HTML page.
article_anchor = re.compile(r'<a\b[^>]*href=["\'][^"\']*(?:makaleler|articles)/[^"\']*["\'][^>]*>.*?</a>', re.I | re.S)
for path in ROOT.rglob("*.html"):
    if "makaleler" in path.parts or "articles" in path.parts:
        continue
    doc = path.read_text(encoding="utf-8")
    updated = article_anchor.sub("", doc)
    if updated != doc:
        path.write_text(updated, encoding="utf-8", newline="\n")

# Remove internal draft/review language from the public privacy notices only;
# the substantive KVKK/privacy provisions remain unchanged.
tr = load("kvkk/index.html")
tr = re.sub(r'<p class="legal-notice">.*?</p>\s*', "", tr, count=1, flags=re.S)
tr = tr.replace("6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında internet sitesi ve iletişim kanallarına ilişkin taslak bilgilendirme.", "6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında internet sitesi ve iletişim kanallarına ilişkin bilgilendirme.")
tr = tr.replace(" Kullanılan sağlayıcılar ve aktarım mekanizmaları yayına alınmadan önce doğrulanmalıdır.", "")
tr = tr.replace(" Başvuru yöntemi ve kimlik doğrulama usulü yayına alınmadan önce nihai metinde açıkça belirtilmelidir.", "")
tr = re.sub(r'<p class="legal-note">.*?</p>', '<p class="legal-note">Son güncelleme: 16 Ekim 2026</p>', tr, count=1, flags=re.S)
save("kvkk/index.html", tr)

en = load("en/privacy/index.html")
en = re.sub(r'<p class="legal-notice">.*?</p>\s*', "", en, count=1, flags=re.S)
en = en.replace("Draft information concerning the website and communication channels under Turkish Personal Data Protection Law No. 6698.", "Information concerning the website and communication channels under Turkish Personal Data Protection Law No. 6698.")
en = en.replace(" The provider and mechanism should be confirmed before launch.", "")
en = en.replace(" The final notice should specify the application method and identity-verification procedure before launch.", "")
en = re.sub(r'<p class="legal-note">.*?</p>', '<p class="legal-note">Last updated: 16 October 2026</p>', en, count=1, flags=re.S)
save("en/privacy/index.html", en)

# --------------------------------------------------------------------- delete
for rel in ("makaleler", "en/articles"):
    target = ROOT / rel
    if target.exists():
        shutil.rmtree(target)

for rel in (
    "article-detail.css",
    "assets/makale-is-hukuku.webp",
    "assets/makale-kira-sozlesmeleri.webp",
    "assets/makale-ticari-sozlesmeler.webp",
    "assets/makaleler-hero.webp",
    "assets/_source/makalelerhero.png",
):
    target = ROOT / rel
    if target.exists():
        target.unlink()

print("Article section and draft privacy-review language removed.")
