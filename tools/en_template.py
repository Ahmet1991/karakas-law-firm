# -*- coding: utf-8 -*-
"""Ingilizce sayfalarin ortak parcalari.

Turkce sayfalarla ayni bilesenleri ve ayni CSS'i kullanir; sadece metin ve
baglantilar degisir. `up` degeri sayfanin kok dizine uzakligidir (en/ icin 1,
en/about/ icin 2) ve butun goreli yollar ondan turetilir.
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500'
         '&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">')

ARROW = ('<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.3"/></svg>')

WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 '
    '11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.9-4.45 9.9-9.91S17.5 2 12.04 '
    '2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.19 8.19 0 0 1-1.26-4.38c0-4.54 '
    '3.7-8.23 8.25-8.23a8.23 8.23 0 0 1 0 16.47Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24'
    '-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.71-.14-.25-.01-.38.11-.5'
    '.11-.11.25-.29.37-.44.13-.15.17-.25.25-.42.09-.16.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.84-.2-.49-.4-.42-.56'
    '-.43h-.47c-.16 0-.43.06-.65.31-.23.24-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.2 3.72.59.25 1.05.4 '
    '1.4.52.59.18 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.28Z"/></svg>')

LI_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 5.5a2.06 2.06 0 1 1-4.12 0 '
    '2.06 2.06 0 0 1 4.12 0ZM3.16 8.98h3.54V21H3.16V8.98Zm5.79 0h3.39v1.64h.05c.47-.89 1.63-1.83 3.35-1.83 3.58 0 '
    '4.24 2.36 4.24 5.42V21h-3.54v-5.85c0-1.4-.03-3.2-1.95-3.2-1.95 0-2.25 1.52-2.25 3.1V21H8.95V8.98Z"/></svg>')

IG_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 '
    '1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 '
    '3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27'
    '.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9'
    '-1.38-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48'
    '-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16Zm0 1.98c-3.14 0-3.51.01'
    '-4.75.07-1.15.05-1.77.24-2.18.4-.55.22-.94.47-1.35.88-.41.41-.66.8-.88 1.35-.16.41-.35 1.03-.4 2.18-.06 1.24'
    '-.07 1.61-.07 4.75s.01 3.51.07 4.75c.05 1.15.24 1.77.4 2.18.22.55.47.94.88 1.35.41.41.8.66 1.35.88.41.16 1.03'
    '.35 2.18.4 1.24.06 1.61.07 4.75.07s3.51-.01 4.75-.07c1.15-.05 1.77-.24 2.18-.4.55-.22.94-.47 1.35-.88.41-.41.66'
    '-.8.88-1.35.16-.41.35-1.03.4-2.18.06-1.24.07-1.61.07-4.75s-.01-3.51-.07-4.75c-.05-1.15-.24-1.77-.4-2.18a3.6 3.6 '
    '0 0 0-.88-1.35 3.6 3.6 0 0 0-1.35-.88c-.41-.16-1.03-.35-2.18-.4-1.24-.06-1.61-.07-4.75-.07Zm0 3.37a5.49 5.49 0 '
    '1 1 0 10.98 5.49 5.49 0 0 1 0-10.98Zm0 9.06a3.57 3.57 0 1 0 0-7.14 3.57 3.57 0 0 0 0 7.14Zm6.99-9.28a1.28 1.28 '
    '0 1 1-2.57 0 1.28 1.28 0 0 1 2.57 0Z"/></svg>')

FB_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 '
    '6.5 2 12.06c0 5.02 3.66 9.18 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.52 1.49-3.91 3.77-3.91 1.09 0 2.24.2 2.24.2'
    'v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.44 2.91h-2.34V22c4.78-.76 8.44-4.92 8.44-9.94Z"/></svg>')

PHONE_SVG = ('<svg viewBox="0 0 24 24"><path d="M6.6 3h-2A1.6 1.6 0 0 0 3 4.6C3 12.6 11.4 21 19.4 21a1.6 1.6 0 0 0 '
    '1.6-1.6v-2a1 1 0 0 0-.8-1l-3.2-.7a1 1 0 0 0-1 .4l-1 1.3a13.6 13.6 0 0 1-5.4-5.4l1.3-1a1 1 0 0 0 .4-1l-.7-3.2a1 1 '
    '0 0 0-1-.8Z"/></svg>')
MAIL_SVG = '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14"/><path d="m3 6 9 6.5L21 6"/></svg>'
PIN_SVG = ('<svg viewBox="0 0 24 24"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/>'
           '<circle cx="12" cy="10" r="2.6"/></svg>')

NAV = [('', 'Home'), ('about/', 'About'), ('practice-areas/', 'Practice Areas'),
       ('articles/', 'Articles'), ('contact/', 'Contact')]


def head(title, desc, up, tr_url, extra_css, preload=''):
    root = '../' * up
    return ('<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="theme-color" content="#080807">\n'
        '<title>' + title + '</title><meta name="description" content="' + desc + '">'
        '<meta name="robots" content="noindex, nofollow">\n'
        '<link rel="alternate" hreflang="tr" href="' + tr_url + '">'
        '<link rel="alternate" hreflang="en" href="./">\n'
        '<link rel="icon" href="' + root + 'assets/favicon.ico" sizes="32x32">\n'
        + preload + FONTS + '\n'
        '<link rel="stylesheet" href="' + root + 'redesign.css">'
        '<link rel="stylesheet" href="' + root + extra_css + '">\n'
        '</head>\n<body>\n')


def header(up, active, tr_url, cta_href, cta_label, stuck=True):
    root = '../' * up            # site kokune (varliklar, css)
    en_root = '../' * (up - 1)   # ingilizce kokune (gezinme)
    home = en_root or './'
    links = ''
    for slug, label in NAV:
        href = home if slug == '' else en_root + slug
        cur = ' is-active" aria-current="page' if slug == active else ''
        links += '<a class="main-nav__link' + cur + '" href="' + href + '">' + label + '</a>'
    href = cta_href if cta_href.startswith('tel:') else en_root + cta_href
    return ('<header class="site-header' + (' is-stuck' if stuck else '') + '" id="top">'
        '<div class="shell nav-wrap">'
        '<a class="brand" href="' + home + '" aria-label="Karakaş Law Firm home">'
        '<img src="' + root + 'assets/logo-horizontal-ondark.webp" alt="Karakaş Law Firm" '
        'width="1287" height="436"></a>'
        '<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav" '
        'aria-label="Open menu"><i></i><i></i></button>'
        '<nav class="main-nav" id="main-nav" aria-label="Main menu">' + links +
        '<span class="lang-switch"><a href="' + tr_url + '" hreflang="tr">TR</a><i></i>'
        '<a href="./" hreflang="en" aria-current="true">EN</a></span>'
        '<a class="nav-cta" href="' + href + '">' + cta_label + ARROW + '</a>'
        '</nav></div></header>\n')


def wa_float():
    return ('\n<a class="wa-float" href="https://wa.me/905305493090" target="_blank" rel="noopener" '
            'aria-label="Message us on WhatsApp">' + WA_SVG + '</a>\n')


def script(up):
    return '<script src="' + ('../' * up) + 'redesign.js" defer></script>\n</body></html>\n'


def inner_footer(up):
    root = '../' * up
    en_root = '../' * (up - 1)
    return ('<footer class="inner-footer"><div class="shell"><div class="inner-footer__grid">'
        '<div class="inner-footer__brand">'
        '<img src="' + root + 'assets/logo-lockup-ondark-420.webp" alt="Karakaş Law Firm">'
        '<p>A clear, measured and careful approach to legal matters.</p></div>'
        '<div class="inner-footer__links">'
        '<a href="' + en_root + 'about/">About</a>'
        '<a href="' + en_root + 'practice-areas/">Practice Areas</a>'
        '<a href="' + en_root + 'articles/">Articles</a>'
        '<a href="' + en_root + 'privacy/">Privacy Notice</a></div></div>'
        '<div class="inner-footer__bottom">© <span id="year">2026</span> Karakaş Law Firm</div>'
        '</div></footer>' + script(up))


def home_footer(up):
    root = '../' * up                 # site kokune (varliklar)
    en = ('../' * (up - 1)) or './'   # ingilizce kokune (gezinme)
    return ('<footer class="site-footer"><div class="shell"><div class="footer-grid">'
        '<div class="footer-brand">'
        '<img src="' + root + 'assets/logo-lockup-ondark-420.webp" alt="Karakaş Law Firm">'
        '<p>A clear, measured and careful approach to legal matters.</p></div>'
        '<ul class="footer-contact">'
        '<li>' + PHONE_SVG + '<a href="tel:+905305493090">+90 530 549 30 90</a></li>'
        '<li>' + MAIL_SVG + '<a href="mailto:avpinarkarakas@gmail.com">avpinarkarakas@gmail.com</a></li>'
        '<li>' + PIN_SVG + '<span>Akdeniz Mah. 1353 Sk. No:2, Armesa İş Merkezi D:32<br>'
        'Konak / İzmir, Türkiye</span></li></ul>'
        '<div class="footer-social"><h3>Social</h3><div class="social-row">'
        '<a href="https://www.linkedin.com/company/karakas-law-firm/" target="_blank" rel="noopener" '
        'aria-label="LinkedIn">' + LI_SVG + '</a>'
        '<a class="is-soon" title="Instagram coming soon" aria-label="Instagram — coming soon">' + IG_SVG + '</a>'
        '<a class="is-soon" title="Facebook coming soon" aria-label="Facebook — coming soon">' + FB_SVG + '</a>'
        '</div></div></div>'
        '<div class="footer-bottom">'
        '<span>© <span id="year">2026</span> Karakaş Law Firm. All rights reserved.</span>'
        '<span><a href="' + en + 'privacy/">Privacy Notice</a></span></div></div></footer>' + script(up))
