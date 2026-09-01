#!/usr/bin/env python3
"""Generate the practice-area pages from tools/content.json.

    python tools/build.py

Writes plain static HTML into the repo. The generated files are committed, so
deployment stays a straight push to GitHub Pages — no build step in CI, and no
Node toolchain. Re-run this only when content.json changes.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import icons

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "tools", "content.json")

with open(CONTENT, encoding="utf-8") as fh:
    DATA = json.load(fh)

FIRM = DATA["firm"]
AREAS = DATA["areas"]
SITE_URL = FIRM.get("siteUrl", "https://www.karakaslawfirm.com").rstrip("/")

# Preview mode keeps the staging copy out of search results so it cannot
# compete with the firm's live site. Flip to False at launch.
PREVIEW = FIRM.get("preview", True)

ARROW = (
    '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
    '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.3"/></svg>'
)

# --------------------------------------------------------------------------
# Per-language chrome
# --------------------------------------------------------------------------
L = {
    "tr": {
        "code": "tr",
        "htmlLang": "tr",
        "ogLocale": "tr_TR",
        "areasDir": "faaliyet-alanlari",
        "skip": "İçeriğe geç",
        "brandAria": "Karakaş Hukuk Bürosu — ana sayfa",
        "menuOpen": "Menüyü aç",
        "navAria": "Ana menü",
        "nav": [
            ("", "Ana Sayfa"),
            ("hakkimizda/", "Hakkımızda"),
            ("uzmanlik-alanlari/", "Uzmanlık Alanlarımız"),
            ("makaleler/", "Makaleler"),
            ("iletisim/", "İletişim"),
        ],
        "contactHref": "iletisim/",
        "activeHref": "uzmanlik-alanlari/",
        "cta": "Danışmanlık Al",
        "home": "Ana Sayfa",
        "areasTitle": "Faaliyet Alanları",
        "areaKicker": "Faaliyet Alanı",
        "scopeLabel": "Kapsam",
        "indexLabel": "Tüm Faaliyet Alanları",
        "prev": "Önceki",
        "next": "Sonraki",
        "ctaHeading": "Bu alandaki bir mesele için görüşelim.",
        "ctaBody": (
            "Dosyanızın kapsamını kısaca aktarın; ilk değerlendirme için uygun "
            "bir görüşme zamanı belirleyelim."
        ),
        "ctaMail": "E-posta Gönder",
        "footerSite": "Site",
        "footerSocial": "Sosyal Medya",
        "footerContact": "İletişim",
        "footerBlurb": (
            "İzmir merkezli, yerli ve yabancı şirketlere kurumsal hukuk ve "
            "uyuşmazlık çözümü alanlarında hizmet veren bağımsız hukuk bürosu."
        ),
        "footerLegal": (
            "Bu internet sitesindeki bilgiler yalnızca genel bilgilendirme "
            "amaçlıdır; hukuki görüş, tavsiye veya danışmanlık niteliği taşımaz "
            "ve avukat–müvekkil ilişkisi doğurmaz. Site içeriği Türkiye Barolar "
            "Birliği Reklam Yasağı Yönetmeliği çerçevesinde hazırlanmıştır."
        ),
        "toTop": "Yukarı ↑",
        "otherLangLabel": "English",
        "areasIndexLead": (
            "Büronun çalışma alanları aşağıda topluca yer alır. Başlıklar genel "
            "bilgilendirme amaçlıdır ve uzmanlık iddiası niteliğinde değildir."
        ),
        "areasIndexHeading": "Hukuki çalışma alanları",
        "detail": "İncele",
        "legalSlug": "kvkk",
        "legalTitle": "Aydınlatma Metni",
        "legalLead": (
            "6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında, bu "
            "internet sitesi üzerinden iletilen kişisel verilerin nasıl "
            "işlendiğine ilişkin bilgilendirme."
        ),
        "legalUpdated": "Bu metin site yayına alınmadan önce güncellenecektir.",
        "waAria": "WhatsApp ile yazın",
        "barAria": "Hızlı iletişim",
        "barCall": "Ara",
        "barWrite": "Yazın",
        "linkedinAria": "Karakaş Hukuk Bürosu LinkedIn sayfası",
    },
    "en": {
        "code": "en",
        "htmlLang": "en",
        "ogLocale": "en_GB",
        "areasDir": "practice-areas",
        "skip": "Skip to content",
        "brandAria": "Karakaş Law Firm — home",
        "menuOpen": "Open menu",
        "navAria": "Main menu",
        "nav": [
            ("", "Home"),
            ("about/", "About"),
            ("practice-areas/", "Practice Areas"),
            ("articles/", "Articles"),
            ("contact/", "Contact"),
        ],
        "contactHref": "contact/",
        "activeHref": "practice-areas/",
        "cta": "Get in Touch",
        "home": "Home",
        "areasTitle": "Practice Areas",
        "areaKicker": "Practice Area",
        "scopeLabel": "Scope",
        "indexLabel": "All Practice Areas",
        "prev": "Previous",
        "next": "Next",
        "ctaHeading": "Let's discuss a matter in this area.",
        "ctaBody": (
            "Outline the scope of your matter and we will arrange a suitable "
            "time for an initial assessment."
        ),
        "ctaMail": "Send an Email",
        "footerSite": "Site",
        "footerSocial": "Social Media",
        "footerContact": "Contact",
        "footerBlurb": (
            "An independent law firm based in İzmir, advising domestic and "
            "international companies on corporate law and dispute resolution."
        ),
        "footerLegal": (
            "The information on this website is provided for general "
            "information only. It does not constitute legal opinion or advice "
            "and does not create an attorney–client relationship. The content "
            "has been prepared in accordance with the Advertising Restrictions "
            "Regulation of the Union of Turkish Bar Associations."
        ),
        "toTop": "Back to top ↑",
        "otherLangLabel": "Türkçe",
        "areasIndexLead": (
            "The firm's areas of practice are set out below. These headings are "
            "for general information and do not constitute a claim of "
            "specialisation."
        ),
        "areasIndexHeading": "Areas of legal practice",
        "detail": "Read more",
        "legalSlug": "privacy",
        "legalTitle": "Privacy Notice",
        "legalLead": (
            "How personal data submitted through this website is processed "
            "under Turkish Personal Data Protection Law No. 6698."
        ),
        "legalUpdated": "This text will be updated before the site goes live.",
        "waAria": "Message us on WhatsApp",
        "barAria": "Quick contact",
        "barCall": "Call",
        "barWrite": "Write",
        "linkedinAria": "Karakaş Law Firm on LinkedIn",
    },
}


def e(text):
    return html.escape(text, quote=False)


def paths(lang, depth):
    """Relative links out of a page nested `depth` folders below the root."""
    root = "../" * depth
    return {
        "root": root,
        "home_tr": root,
        "home_en": root + "en/",
        "areas_tr": root + "faaliyet-alanlari/",
        "areas_en": root + "en/practice-areas/",
        "home": root if lang == "tr" else root + "en/",
        "areas": root + ("faaliyet-alanlari/" if lang == "tr" else "en/practice-areas/"),
        "legal": root + ("kvkk/" if lang == "tr" else "en/privacy/"),
        "assets": root + "assets/",
        "css": root + "redesign.css",
        "css_pages": root + "redesign-pages.css",
        "css_theme": root + "theme-light.css",
        "js": root + "redesign.js",
    }


def head(lang, depth, title, description, canonical_path, alternate_path):
    t = L[lang]
    p = paths(lang, depth)
    robots = (
        '<meta name="robots" content="noindex, nofollow">\n'
        if PREVIEW
        else f'<link rel="canonical" href="{SITE_URL}/{canonical_path}">\n'
    )
    alt_lang = "en" if lang == "tr" else "tr"
    return f"""<!doctype html>
<html lang="{t['htmlLang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0a0f1a">

<title>{e(title)}</title>
<meta name="description" content="{html.escape(description)}">
{robots}
<meta property="og:type" content="article">
<meta property="og:locale" content="{t['ogLocale']}">
<meta property="og:site_name" content="{e(FIRM['name'])}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="{p['assets']}og-image.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="alternate" hreflang="{lang}" href="{SITE_URL}/{canonical_path}">
<link rel="alternate" hreflang="{alt_lang}" href="{SITE_URL}/{alternate_path}">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{canonical_path if lang == 'tr' else alternate_path}">

<link rel="icon" href="{p['assets']}favicon.ico" sizes="32x32">
<link rel="icon" href="{p['assets']}icon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="{p['assets']}apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p['css']}">
<link rel="stylesheet" href="{p['css_pages']}">
<link rel="stylesheet" href="{p['css_theme']}">
<noscript><style>.reveal{{opacity:1!important;transform:none!important}}</style></noscript>
</head>
"""


def header(lang, depth, alternate_href):
    t = L[lang]
    p = paths(lang, depth)
    other = "en" if lang == "tr" else "tr"
    nav_links = "\n      ".join(
        '<a class="main-nav__link{}" href="{}{}">{}</a>'.format(
            " is-active" if href and href == t["activeHref"] else "",
            p["home"], href,
            e(label),
        )
        for href, label in t["nav"]
    )
    tr_href = p["home_tr"] if lang == "en" else "./"
    en_href = p["home_en"] if lang == "tr" else "./"
    # On a subpage the language switch should land on the matching translation.
    if alternate_href:
        if lang == "tr":
            en_href = alternate_href
            tr_href = "./"
        else:
            tr_href = alternate_href
            en_href = "./"

    return f"""<body>
<a class="skip-link" href="#main">{e(t['skip'])}</a>

<header class="site-header" id="top">
  <div class="shell nav-wrap">

    <a class="brand" href="{p['home']}" aria-label="{e(t['brandAria'])}">
      <img src="{p['assets']}logo-horizontal-ondark.webp" width="1287" height="436" alt="{e(FIRM['name'] if lang == 'tr' else FIRM['nameEn'])}" fetchpriority="high">
    </a>

    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="{e(t['menuOpen'])}">
      <i></i><i></i>
    </button>

    <nav class="main-nav" id="main-nav" aria-label="{e(t['navAria'])}">
      {nav_links}
      <a class="nav-cta" href="{p['home']}{t['contactHref']}">
        {e(t['cta'])}
        {ARROW}
      </a>
      <span class="lang-switch">
        <a href="{tr_href}" hreflang="tr"{' aria-current="true"' if lang == 'tr' else ''}>TR</a>
        <i aria-hidden="true"></i>
        <a href="{en_href}" hreflang="en"{' aria-current="true"' if lang == 'en' else ''}>EN</a>
      </span>
    </nav>

  </div>
</header>
"""


WA_ICON = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 '
    "2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 "
    "0 9.9-4.45 9.9-9.91S17.5 2 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.19 "
    "8.19 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.23 8.23 0 0 1 0 16.47Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.71-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.44.13-.15.17-.25.25-.42.09-.16.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.84-.2-.49-.4-.42-.56-.43h-.47c-.16 "
    '0-.43.06-.65.31-.23.24-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.2 3.72.59.25 1.05.4 1.4.52.59.18 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>'
)

PHONE_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
    '<path d="M6.6 3h-2A1.6 1.6 0 0 0 3 4.6C3 12.6 11.4 21 19.4 21a1.6 1.6 0 0 0 1.6-1.6v-2a1 1 0 0 '
    '0-.8-1l-3.2-.7a1 1 0 0 0-1 .4l-1 1.3a13.6 13.6 0 0 1-5.4-5.4l1.3-1a1 1 0 0 0 .4-1l-.7-3.2a1 1 0 0 0-1-.8Z"/></svg>'
)

LINKEDIN_ICON = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 5.5a2.06 '
    "2.06 0 1 1-4.12 0 2.06 2.06 0 0 1 4.12 0ZM7 9H3v12h4V9Zm6.32 0H9.34v12h3.94v-6.3c0-3.67 "
    '4.77-3.97 4.77 0V21H22v-7.66c0-6.15-7.02-5.92-8.72-2.9V9Z"/></svg>'
)

MAIL_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
    '<rect x="3" y="5" width="18" height="14"/><path d="m3 6 9 6.5L21 6"/></svg>'
)


def floating(lang, depth):
    """WhatsApp button (desktop) and sticky action bar (mobile)."""
    t = L[lang]
    p = paths(lang, depth)
    wa = "https://wa.me/" + FIRM["phoneHref"].lstrip("+")
    contact_anchor = p["home"] + t["contactHref"]
    return f"""
<a class="wa-float" href="{wa}" target="_blank" rel="noopener" aria-label="{e(t['waAria'])}">
  {WA_ICON}
</a>
"""


def footer(lang, depth):
    """Elle yazılan sayfalarla (hakkimizda, iletisim, makaleler) birebir aynı
    footer söz dizimi: .footer-grid / .footer-col / .social-row. Eski
    .footer__* sınıflarının yeni CSS'te karşılığı yok."""
    t = L[lang]
    p = paths(lang, depth)
    a = FIRM["address"]
    other_home = p["home_en"] if lang == "tr" else p["home_tr"]
    site_links = "\n          ".join(
        f'<li><a href="{p["home"]}{href}">{e(label)}</a></li>'
        for href, label in t["nav"]
    )
    area_links = "\n          ".join(
        f'<li><a href="{p["areas"]}{area["slug"][lang]}/">{e(area["title"][lang])}</a></li>'
        for area in AREAS
    )
    maps = (
        "https://www.google.com/maps/search/?api=1&amp;query="
        + html.escape(f"{a['street']} {a['district']} {a['city']}".replace(" ", "%20"))
    )
    return f"""
<footer class="site-footer">
  <div class="shell">
    <div class="footer-grid">

      <div class="footer-brand">
        <img src="{p['assets']}logo-lockup-ondark-420.webp" width="420" height="338" loading="lazy" alt="{e(FIRM['name'])}">
        <p>{e(t['footerBlurb'])}</p>
        <h3>{e(t['footerSocial'])}</h3>
        <div class="social-row">
          <a href="{FIRM['linkedin']}" target="_blank" rel="noopener" aria-label="{e(t['linkedinAria'])}">{LINKEDIN_ICON}</a>
        </div>
      </div>

      <nav class="footer-col" aria-label="{e(t['footerSite'])}">
        <h3>{e(t['footerSite'])}</h3>
        <ul class="footer-nav">
          {site_links}
          <li><a href="{p['legal']}">{e(t['legalTitle'])}</a></li>
          <li><a href="{other_home}">{e(t['otherLangLabel'])}</a></li>
        </ul>
      </nav>

      <nav class="footer-col footer-col--areas" aria-label="{e(t['areasTitle'])}">
        <h3>{e(t['areasTitle'])}</h3>
        <ul class="footer-nav">
          {area_links}
        </ul>
      </nav>

      <div class="footer-col">
        <h3>{e(t['footerContact'])}</h3>
        <ul class="footer-contact">
          <li><a href="{maps}" target="_blank" rel="noopener">{e(a['street'])}<br>{e(a['district'])} / {e(a['city'])}</a></li>
          <li><a href="tel:{FIRM['phoneHref']}">{e(FIRM['phone'])}</a></li>
          <li><a href="mailto:{FIRM['email']}">{e(FIRM['email'])}</a></li>
        </ul>
      </div>

    </div>

    <p class="footer-legal">{e(t['footerLegal'])}</p>

    <div class="footer-bottom">
      <span>© <span id="year">2026</span> {e(FIRM['name'])}</span>
      <span><a href="{p['legal']}">{e(t['legalTitle'])}</a></span>
    </div>
  </div>
</footer>
{floating(lang, depth)}
<script src="{p['js']}" defer></script>
</body>
</html>
"""


def jsonld(lang, depth, blocks):
    return (
        '<script type="application/ld+json">'
        + json.dumps({"@context": "https://schema.org", "@graph": blocks},
                     ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )


def firm_node(lang):
    a = FIRM["address"]
    return {
        "@type": "LegalService",
        "@id": f"{SITE_URL}/#firm",
        "name": FIRM["name"] if lang == "tr" else FIRM["nameEn"],
        "url": SITE_URL + ("/" if lang == "tr" else "/en/"),
        "telephone": FIRM["phone"],
        "email": FIRM["email"],
        "image": f"{SITE_URL}/assets/og-image.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": a["street"],
            "addressLocality": a["district"],
            "addressRegion": a["city"],
            "addressCountry": a["country"],
        },
        "areaServed": {"@type": "Country", "name": "Türkiye"},
        "founder": {"@type": "Person", "name": "Pınar Karakaş", "jobTitle": "Avukat"},
        "availableLanguage": ["tr", "en"],
    }


# --------------------------------------------------------------------------
# Page builders
# --------------------------------------------------------------------------
def area_index_html(lang, current_slug, depth):
    """Sidebar list of every practice area."""
    t = L[lang]
    p = paths(lang, depth)
    items = []
    for area in AREAS:
        slug = area["slug"][lang]
        current = slug == current_slug
        attr = ' aria-current="page"' if current else ""
        items.append(
            f'<li><a href="{p["areas"]}{slug}/"{attr}>'
            f'<span>{area["no"]}</span>{e(area["title"][lang])}</a></li>'
        )
    return (
        f'<aside class="area-index">\n'
        f"  <h2>{e(t['indexLabel'])}</h2>\n"
        f"  <ol>\n    " + "\n    ".join(items) + "\n  </ol>\n</aside>"
    )


def build_area_page(lang, idx):
    area = AREAS[idx]
    t = L[lang]
    depth = 2 if lang == "tr" else 3
    p = paths(lang, depth)
    slug = area["slug"][lang]
    other = "en" if lang == "tr" else "tr"
    other_slug = area["slug"][other]

    canonical = (
        f"faaliyet-alanlari/{slug}/" if lang == "tr" else f"en/practice-areas/{slug}/"
    )
    alternate = (
        f"en/practice-areas/{other_slug}/"
        if lang == "tr"
        else f"faaliyet-alanlari/{other_slug}/"
    )
    alternate_href = (
        f'{p["areas_en"]}{other_slug}/' if lang == "tr" else f'{p["areas_tr"]}{other_slug}/'
    )

    title = f"{area['title'][lang]} | {FIRM['name'] if lang == 'tr' else FIRM['nameEn']}"
    description = area["lead"][lang][:300]

    # The diamond marker is drawn by .scope li::before, which occupies the
    # first grid column — no extra element belongs here.
    scope_items = "\n        ".join(
        f"<li>{e(item)}</li>" for item in area["items"][lang]
    )

    prev_area = AREAS[idx - 1] if idx > 0 else AREAS[-1]
    next_area = AREAS[(idx + 1) % len(AREAS)]

    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home"],
             "item": SITE_URL + ("/" if lang == "tr" else "/en/")},
            {"@type": "ListItem", "position": 2, "name": t["areasTitle"],
             "item": f"{SITE_URL}/{'faaliyet-alanlari' if lang == 'tr' else 'en/practice-areas'}/"},
            {"@type": "ListItem", "position": 3, "name": area["title"][lang],
             "item": f"{SITE_URL}/{canonical}"},
        ],
    }
    service = {
        "@type": "Service",
        "name": area["title"][lang],
        "serviceType": area["title"][lang],
        "description": area["lead"][lang],
        "provider": {"@id": f"{SITE_URL}/#firm"},
        "areaServed": {"@type": "Country", "name": "Türkiye"},
    }

    body = f"""
<main id="main">

  <section class="subhero subhero--area">
    <div class="shell">
      <ol class="breadcrumb">
        <li><a href="{p['home']}">{e(t['home'])}</a></li>
        <li><a href="{p['areas']}">{e(t['areasTitle'])}</a></li>
        <li aria-current="page">{e(area['title'][lang])}</li>
      </ol>

      <p class="page-kicker">{area['no']} · {e(t['areaKicker']).upper()}</p>
      <h1 class="page-title">{e(area['title'][lang])}</h1>
      <div class="page-rule"></div>
      <p class="page-lead">{e(area['lead'][lang])}</p>
    </div>
  </section>

  <section class="page-shell">
    <div class="shell area-layout">
      {area_index_html(lang, slug, depth)}

      <div class="scope reveal">
        <h2>{e(t['scopeLabel'])}</h2>
        <ul>
        {scope_items}
        </ul>

        <div class="area-cta">
          <h2>{e(t['ctaHeading'])}</h2>
          <p>{e(t['ctaBody'])}</p>
          <div class="area-cta__actions">
            <a class="btn" href="mailto:{FIRM['email']}">{e(t['ctaMail'])} {ARROW}</a>
            <a class="btn btn--ghost" href="tel:{FIRM['phoneHref']}">{e(FIRM['phone'])}</a>
          </div>
        </div>

        <nav class="area-nav" aria-label="{e(t['areasTitle'])}">
          <a href="{p['areas']}{prev_area['slug'][lang]}/">
            <small>{e(t['prev'])}</small>
            <strong>{e(prev_area['title'][lang])}</strong>
          </a>
          <a href="{p['areas']}{next_area['slug'][lang]}/">
            <small>{e(t['next'])}</small>
            <strong>{e(next_area['title'][lang])}</strong>
          </a>
        </nav>
      </div>
    </div>
  </section>

</main>
"""

    doc = (
        head(lang, depth, title, description, canonical, alternate)
        + header(lang, depth, alternate_href)
        + body
        + jsonld(lang, depth, [firm_node(lang), service, breadcrumb])
        + footer(lang, depth)
    )
    out = os.path.join(
        ROOT,
        *(["faaliyet-alanlari", slug] if lang == "tr" else ["en", "practice-areas", slug]),
        "index.html",
    )
    return out, doc


def build_areas_index(lang):
    t = L[lang]
    depth = 1 if lang == "tr" else 2
    p = paths(lang, depth)
    other = "en" if lang == "tr" else "tr"
    canonical = "faaliyet-alanlari/" if lang == "tr" else "en/practice-areas/"
    alternate = "en/practice-areas/" if lang == "tr" else "faaliyet-alanlari/"
    alternate_href = p["areas_en"] if lang == "tr" else p["areas_tr"]

    cards = []
    for area in AREAS:
        cards.append(f"""        <a class="expertise-card reveal" href="{p['areas']}{area['slug'][lang]}/">
          <span class="expertise-no">{area['no']}</span>
          <h2>{e(area['title'][lang])}</h2>
          <p>{e(area['card'][lang])}</p>
          <span class="text-link">{e(t['detail'])} {ARROW}</span>
        </a>""")

    title = f"{t['areasTitle']} | {FIRM['name'] if lang == 'tr' else FIRM['nameEn']}"

    body = f"""
<main id="main">

  <section class="subhero subhero--area">
    <div class="shell">
      <ol class="breadcrumb">
        <li><a href="{p['home']}">{e(t['home'])}</a></li>
        <li aria-current="page">{e(t['areasTitle'])}</li>
      </ol>

      <p class="page-kicker">{e(t['areasTitle']).upper()}</p>
      <h1 class="page-title">{e(t['areasIndexHeading'])}</h1>
      <div class="page-rule"></div>
      <p class="page-lead">{e(t['areasIndexLead'])}</p>
    </div>
  </section>

  <section class="page-shell">
    <div class="shell">
      <div class="expertise-grid">
{chr(10).join(cards)}
      </div>
    </div>
  </section>

</main>
"""

    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home"],
             "item": SITE_URL + ("/" if lang == "tr" else "/en/")},
            {"@type": "ListItem", "position": 2, "name": t["areasTitle"],
             "item": f"{SITE_URL}/{canonical}"},
        ],
    }

    doc = (
        head(lang, depth, title, t["areasIndexLead"], canonical, alternate)
        + header(lang, depth, alternate_href)
        + body
        + jsonld(lang, depth, [firm_node(lang), breadcrumb])
        + footer(lang, depth)
    )
    out = os.path.join(
        ROOT, *(["faaliyet-alanlari"] if lang == "tr" else ["en", "practice-areas"]),
        "index.html",
    )
    return out, doc


def build_legal_page(lang):
    """KVKK / privacy notice. Body copy lives in tools/legal-<lang>.html."""
    t = L[lang]
    depth = 1 if lang == "tr" else 2
    p = paths(lang, depth)
    canonical = "kvkk/" if lang == "tr" else "en/privacy/"
    alternate = "en/privacy/" if lang == "tr" else "kvkk/"
    alternate_href = (
        p["root"] + "en/privacy/" if lang == "tr" else p["root"] + "kvkk/"
    )

    fragment_path = os.path.join(ROOT, "tools", f"legal-{lang}.html")
    with open(fragment_path, encoding="utf-8") as fh:
        fragment = fh.read().strip()

    title = f"{t['legalTitle']} | {FIRM['name'] if lang == 'tr' else FIRM['nameEn']}"

    body = f"""
<main id="main">

  <section class="page-hero">
    <div class="shell">
      <ol class="breadcrumb">
        <li><a href="{p['home']}">{e(t['home'])}</a></li>
        <li>{e(t['legalTitle'])}</li>
      </ol>

      <h1 class="display-l">{e(t['legalTitle'])}</h1>
      <p class="page-hero__lead lead">{e(t['legalLead'])}</p>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <div class="prose reveal">
{fragment}
        <p class="prose__updated">{e(t['legalUpdated'])}</p>
      </div>
    </div>
  </section>

</main>
"""

    doc = (
        head(lang, depth, title, t["legalLead"], canonical, alternate)
        + header(lang, depth, alternate_href)
        + body
        + footer(lang, depth)
    )
    return os.path.join(
        ROOT, *(["kvkk"] if lang == "tr" else ["en", "privacy"]), "index.html"
    ), doc


ARROW_WIDE = (
    '<svg viewBox="0 0 24 14" fill="none" aria-hidden="true">'
    '<path d="M1 7h20M16 2l5 5-5 5" stroke="currentColor" stroke-width="1.15" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

NL = "\n"


def home_area_row(lang):
    """The practice-area icon row that sits on the homepage."""
    base = "faaliyet-alanlari/" if lang == "tr" else "practice-areas/"
    detail = L[lang]["detail"]
    tiles = []
    for area in AREAS:
        slug = area["slug"][lang]
        tiles.append(
            '        <a class="area-tile reveal" href="{base}{slug}/" aria-label="{aria}">{nl}'
            '          <span class="area-tile__icon">{icon}</span>{nl}'
            "          <h3>{title}</h3>{nl}"
            "          <p>{short}</p>{nl}"
            '          <span class="area-tile__arrow">{arrow}</span>{nl}'
            "        </a>".format(
                base=base,
                slug=slug,
                aria=e("{} — {}".format(area["title"][lang], detail)),
                icon=icons.icon(area["slug"]["tr"]),
                title=e(area["title"][lang]),
                short=e(area["short"][lang]),
                arrow=ARROW_WIDE,
                nl=NL,
            )
        )
    return '      <div class="area-row">' + NL + NL.join(tiles) + NL + "      </div>"


def sync_home(lang):
    """Rewrite the marked block inside the hand-written homepage."""
    path = os.path.join(
        ROOT, "index.html" if lang == "tr" else os.path.join("en", "index.html")
    )
    with open(path, encoding="utf-8") as fh:
        src = fh.read()

    pattern = re.compile(r"(<!-- AREAS:START[^>]*-->)(.*?)(<!-- AREAS:END -->)", re.S)
    if not pattern.search(src):
        raise SystemExit(path + ": AREAS isaretleri bulunamadi")

    block = home_area_row(lang)
    out = pattern.sub(
        lambda m: m.group(1) + NL + block + NL + "      " + m.group(3), src, count=1
    )

    with open(path, "w", encoding="utf-8", newline=NL) as fh:
        fh.write(out)
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def write(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(doc)
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def build_sitemap():
    urls = ["", "en/", "faaliyet-alanlari/", "en/practice-areas/", "kvkk/", "en/privacy/"]
    for area in AREAS:
        urls.append(f"faaliyet-alanlari/{area['slug']['tr']}/")
        urls.append(f"en/practice-areas/{area['slug']['en']}/")

    entries = []
    for u in urls:
        entries.append(f"  <url>\n    <loc>{SITE_URL}/{u}</loc>\n  </url>")
    doc = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    return write(os.path.join(ROOT, "sitemap.xml"), doc)


def build_robots():
    if PREVIEW:
        doc = (
            "# Hazırlık aşaması: site canlı alan adına taşınana kadar arama\n"
            "# motorlarına kapalı. Yayına alırken content.json içindeki\n"
            '# firm.preview değerini false yapıp bu dosyayı yeniden üretin.\n'
            "User-agent: *\nDisallow: /\n"
        )
    else:
        doc = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    return write(os.path.join(ROOT, "robots.txt"), doc)


def main():
    """Dogrudan calistirmaya kapali.

    Bu jenerator eskiden kvkk/ ve en/privacy/ sayfalarini da uretiyordu; o
    sayfalar artik elle bakiliyor ve burada uretilirse eski .page-hero /
    .display-l soz dizimiyle uzerine yazilir. Sahiplik listesi
    generate_practice_pages.py icindedir; tek dogru giris noktasi
    build_site.py'dir.
    """
    raise SystemExit(
        "build.py dogrudan calistirilmamalidir; elle bakilan sayfalari ezer.\n"
        "Dogru komut: python tools/build_site.py"
    )


def _legacy_main_unused():
    written = []
    for lang in ("tr", "en"):
        written.append(write(*build_areas_index(lang)))
        for i in range(len(AREAS)):
            written.append(write(*build_area_page(lang, i)))
        written.append(write(*build_legal_page(lang)))

    for lang in ("tr", "en"):
        written.append(sync_home(lang))

    written.append(build_sitemap())
    written.append(build_robots())

    print(f"{len(written)} dosya üretildi:")
    for path in written:
        print("  " + path)
    if PREVIEW:
        print("\nUYARI: preview modu açık — sayfalar noindex ve robots.txt kapalı.")


if __name__ == "__main__":
    sys.exit(main())
