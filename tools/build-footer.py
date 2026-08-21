# -*- coding: utf-8 -*-
"""Tum yeniden tasarlanan sayfalara ayni zengin footer'i yazar.

  python tools/build-footer.py

Dort sutun: marka + sosyal, site haritasi, uzmanlik alanlari, iletisim.
Uzmanlik sutunu onemli: 12 detay sayfasi aksi hâlde tek bir sayfadan
erisilebiliyor. Alt seritte telif, baro kaydi ve bilgilendirme ibaresi.
"""
import io, os, re

LI = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 5.5a2.06 2.06 0 1 1-4.12 0 '
      '2.06 2.06 0 0 1 4.12 0ZM3.16 8.98h3.54V21H3.16V8.98Zm5.79 0h3.39v1.64h.05c.47-.89 1.63-1.83 3.35-1.83 3.58 0 '
      '4.24 2.36 4.24 5.42V21h-3.54v-5.85c0-1.4-.03-3.2-1.95-3.2-1.95 0-2.25 1.52-2.25 3.1V21H8.95V8.98Z"/></svg>')
IG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17'
      '.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 '
      '3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41'
      '-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68'
      '-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23'
      '.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16Zm0 1.98c-3.14 '
      '0-3.51.01-4.75.07-1.15.05-1.77.24-2.18.4-.55.22-.94.47-1.35.88-.41.41-.66.8-.88 1.35-.16.41-.35 1.03-.4 2.18'
      '-.06 1.24-.07 1.61-.07 4.75s.01 3.51.07 4.75c.05 1.15.24 1.77.4 2.18.22.55.47.94.88 1.35.41.41.8.66 1.35.88.41'
      '.16 1.03.35 2.18.4 1.24.06 1.61.07 4.75.07s3.51-.01 4.75-.07c1.15-.05 1.77-.24 2.18-.4.55-.22.94-.47 1.35-.88'
      '.41-.41.66-.8.88-1.35.16-.41.35-1.03.4-2.18.06-1.24.07-1.61.07-4.75s-.01-3.51-.07-4.75c-.05-1.15-.24-1.77-.4'
      '-2.18a3.6 3.6 0 0 0-.88-1.35 3.6 3.6 0 0 0-1.35-.88c-.41-.16-1.03-.35-2.18-.4-1.24-.06-1.61-.07-4.75-.07Zm0 '
      '3.37a5.49 5.49 0 1 1 0 10.98 5.49 5.49 0 0 1 0-10.98Zm0 9.06a3.57 3.57 0 1 0 0-7.14 3.57 3.57 0 0 0 0 7.14Zm6'
      '.99-9.28a1.28 1.28 0 1 1-2.57 0 1.28 1.28 0 0 1 2.57 0Z"/></svg>')
FB = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 '
      '2 12.06c0 5.02 3.66 9.18 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.52 1.49-3.91 3.77-3.91 1.09 0 2.24.2 2.24.2'
      'v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.44 2.91h-2.34V22c4.78-.76 8.44-4.92 8.44-9.94Z"/></svg>')
PHONE = ('<svg viewBox="0 0 24 24"><path d="M6.6 3h-2A1.6 1.6 0 0 0 3 4.6C3 12.6 11.4 21 19.4 21a1.6 1.6 0 0 0 1.6'
         '-1.6v-2a1 1 0 0 0-.8-1l-3.2-.7a1 1 0 0 0-1 .4l-1 1.3a13.6 13.6 0 0 1-5.4-5.4l1.3-1a1 1 0 0 0 .4-1l-.7-3.2a1 '
         '1 0 0 0-1-.8Z"/></svg>')
MAIL = '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14"/><path d="m3 6 9 6.5L21 6"/></svg>'
PIN = ('<svg viewBox="0 0 24 24"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/>'
       '<circle cx="12" cy="10" r="2.6"/></svg>')

TR = {
  'tag': 'Hukuki süreçlerde açık, ölçülü ve özenli bir yaklaşım.',
  'nav_h': 'Site Haritası',
  'nav': [('', 'Ana Sayfa'), ('hakkimizda/', 'Hakkımızda'), ('uzmanlik-alanlari/', 'Uzmanlık Alanlarımız'),
          ('makaleler/', 'Makaleler'), ('iletisim/', 'İletişim'), ('kvkk/', 'Aydınlatma Metni')],
  'areas_h': 'Uzmanlık Alanları',
  'areas_base': 'faaliyet-alanlari/',
  'areas': [('ticaret-ve-sirketler-hukuku', 'Ticaret ve Şirketler Hukuku'),
            ('deniz-ticareti-hukuku', 'Deniz Ticareti Hukuku'),
            ('sigorta-hukuku', 'Sigorta Hukuku'), ('maden-hukuku', 'Maden Hukuku'),
            ('saglik-hukuku', 'Sağlık Hukuku'), ('banka-ve-finans-hukuku', 'Banka ve Finans Hukuku'),
            ('gayrimenkul-ve-insaat-hukuku', 'Gayrimenkul ve İnşaat Hukuku'),
            ('fikri-mulkiyet-hukuku', 'Fikri Mülkiyet Hukuku'),
            ('idare-ve-vergi-hukuku', 'İdare ve Vergi Hukuku'), ('is-hukuku', 'İş Hukuku'),
            ('icra-ve-iflas-hukuku', 'İcra ve İflas Hukuku'), ('dava-ve-tahkim', 'Dava ve Tahkim')],
  'contact_h': 'İletişim', 'social_h': 'Sosyal Medya',
  'addr': 'Akdeniz Mah. 1353 Sk. No:2<br>Armesa İş Merkezi D:32<br>Konak / İzmir',
  'bar': 'İzmir Barosu’na kayıtlıdır.',
  'legal': 'Bu sitedeki içerikler genel bilgilendirme amaçlıdır; hukuki görüş veya tavsiye niteliği taşımaz.',
  'rights': 'Tüm hakları saklıdır.', 'kvkk': ('kvkk/', 'Aydınlatma Metni'),
  'ig': 'Instagram hesabı yakında', 'fb': 'Facebook sayfası yakında',
}
EN = {
  'tag': 'A clear, measured and careful approach to legal matters.',
  'nav_h': 'Site Map',
  'nav': [('', 'Home'), ('about/', 'About'), ('practice-areas/', 'Practice Areas'),
          ('articles/', 'Articles'), ('contact/', 'Contact'), ('privacy/', 'Privacy Notice')],
  'areas_h': 'Practice Areas',
  'areas_base': 'practice-areas/',
  'areas': [('corporate-and-commercial-law', 'Corporate &amp; Commercial Law'),
            ('maritime-law', 'Maritime Law'), ('insurance-law', 'Insurance Law'),
            ('mining-law', 'Mining Law'), ('healthcare-law', 'Healthcare Law'),
            ('banking-and-finance-law', 'Banking &amp; Finance'),
            ('real-estate-and-construction-law', 'Real Estate &amp; Construction'),
            ('intellectual-property-law', 'Intellectual Property'),
            ('administrative-and-tax-law', 'Administrative &amp; Tax Law'),
            ('employment-law', 'Employment Law'),
            ('enforcement-and-insolvency-law', 'Enforcement &amp; Insolvency'),
            ('litigation-and-arbitration', 'Litigation &amp; Arbitration')],
  'contact_h': 'Contact', 'social_h': 'Social',
  'addr': 'Akdeniz Mah. 1353 Sk. No:2<br>Armesa İş Merkezi D:32<br>Konak / İzmir, Türkiye',
  'bar': 'Registered with the İzmir Bar Association.',
  'legal': 'Content on this site is for general information only and does not constitute legal advice.',
  'rights': 'All rights reserved.', 'kvkk': ('privacy/', 'Privacy Notice'),
  'ig': 'Instagram coming soon', 'fb': 'Facebook coming soon',
}

# sayfa -> (dil, site kokune uzaklik, gezinme kokune uzaklik)
PAGES = [
  ('index.html', TR, 0, 0), ('hakkimizda/index.html', TR, 1, 1),
  ('uzmanlik-alanlari/index.html', TR, 1, 1), ('makaleler/index.html', TR, 1, 1),
  ('iletisim/index.html', TR, 1, 1),
  ('en/index.html', EN, 1, 0), ('en/about/index.html', EN, 2, 1),
  ('en/practice-areas/index.html', EN, 2, 1), ('en/articles/index.html', EN, 2, 1),
  ('en/contact/index.html', EN, 2, 1),
]


def footer(L, up, nav_up):
    root = '../' * up          # varliklar ve TR icin gezinme kokü
    nav = '../' * nav_up       # dilin kokü
    home = nav or './'
    # TR'de uzmanlik alanlari site kokunde, EN'de dil kokunde
    areas_root = root if L is TR else nav

    links = ''.join('<li><a href="%s">%s</a></li>' % ((home if s == '' else nav + s), t) for s, t in L['nav'])
    areas = ''.join('<li><a href="%s%s%s/">%s</a></li>' % (areas_root, L['areas_base'], s, t) for s, t in L['areas'])

    return (
      '<footer class="site-footer"><div class="shell">'
      '<div class="footer-grid">'
        '<div class="footer-brand">'
          '<img src="' + root + 'assets/logo-lockup-ondark-420.webp" alt="Karakaş Hukuk Bürosu">'
          '<p>' + L['tag'] + '</p>'
          '<h3>' + L['social_h'] + '</h3><div class="social-row">'
          '<a href="https://www.linkedin.com/company/karakas-law-firm/" target="_blank" rel="noopener" '
          'aria-label="LinkedIn">' + LI + '</a>'
          '<a class="is-soon" title="' + L['ig'] + '" aria-label="Instagram">' + IG + '</a>'
          '<a class="is-soon" title="' + L['fb'] + '" aria-label="Facebook">' + FB + '</a>'
          '</div>'
        '</div>'
        '<nav class="footer-col" aria-label="' + L['nav_h'] + '"><h3>' + L['nav_h'] + '</h3>'
          '<ul class="footer-nav">' + links + '</ul></nav>'
        '<nav class="footer-col footer-col--areas" aria-label="' + L['areas_h'] + '">'
          '<h3>' + L['areas_h'] + '</h3><ul class="footer-nav">' + areas + '</ul></nav>'
        '<div class="footer-col"><h3>' + L['contact_h'] + '</h3>'
          '<ul class="footer-contact">'
          '<li>' + PIN + '<span>' + L['addr'] + '</span></li>'
          '<li>' + PHONE + '<a href="tel:+905305493090">+90 530 549 30 90</a></li>'
          '<li>' + MAIL + '<a href="mailto:avpinarkarakas@gmail.com">avpinarkarakas@gmail.com</a></li>'
          '</ul></div>'
      '</div>'
      '<p class="footer-legal">' + L['legal'] + '</p>'
      '<div class="footer-bottom">'
        '<span>© <span id="year">2026</span> Karakaş Hukuk Bürosu. ' + L['rights'] + ' ' + L['bar'] + '</span>'
        '<span><a href="' + (nav if L is EN else root) + L['kvkk'][0] + '">' + L['kvkk'][1] + '</a></span>'
      '</div></div></footer>')


changed = 0
for path, L, up, nav_up in PAGES:
    if not os.path.isfile(path):
        print('yok:', path); continue
    doc = io.open(path, encoding='utf-8').read()
    new = re.sub(r'<footer class="(?:site-footer|inner-footer)">.*?</footer>',
                 lambda _: footer(L, up, nav_up), doc, count=1, flags=re.S)
    if new == doc:
        print('footer bulunamadi:', path); continue
    io.open(path, 'w', encoding='utf-8', newline='\n').write(new)
    changed += 1
    print('guncellendi:', path)
print('toplam %d sayfa' % changed)
