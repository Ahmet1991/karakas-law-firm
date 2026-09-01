# -*- coding: utf-8 -*-
"""Ingilizce sayfalari yeni tasarimda uretir.  python tools/build-en.py"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from en_template import (head, header, wa_float, inner_footer, home_footer, script, ARROW)

W = lambda p, s: (os.makedirs(os.path.dirname(p), exist_ok=True), io.open(p, 'w', encoding='utf-8').write(s))

PRACTICE = [
 ('corporate-and-commercial-law', 'Corporate &amp; Commercial Law',
  'The full corporate lifecycle, from incorporation and share transfers to governance and director liability.',
  ['Articles of association and shareholders&rsquo; agreements',
   'Capital increases, share transfers, conversions and public offerings',
   'General assembly and board resolutions',
   'Domestic and foreign consortia and joint ventures',
   'Corporate governance, regulatory compliance and day-to-day counsel',
   'Civil and criminal liability of directors and officers']),
 ('litigation-and-arbitration', 'Litigation &amp; Arbitration',
  'Domestic and cross-border disputes, pursued through the courts, arbitration or settlement.',
  ['Disputes arising from commercial contracts',
   'Enforcement of foreign arbitral awards in T&uuml;rkiye',
   'Settlement options assessed before proceedings are filed',
   'Arbitration and mediation run through an international network of correspondent firms']),
 ('maritime-law', 'Maritime Law',
  'Every stage of the vessel, cargo and carriage chain, at home and abroad.',
  ['Arrest, salvage and collision',
   'Cargo and charterparty disputes',
   'Matters involving liability underwriters',
   'Problems arising during and after carriage',
   'Ship registration, marine finance and contract negotiation']),
 ('insurance-law', 'Insurance Law',
  'Counsel and representation on both sides of the insurance relationship, from policy to subrogation.',
  ['Representation in subrogation claims',
   'Advice on relationships with insurers',
   'Regulatory compliance in motor insurance operations',
   'Compensation claims arising from road, air and sea transport accidents',
   'Policy-related services']),
 ('mining-law', 'Mining Law',
  'The legal and compliance side of mining, from licensing through to investment.',
  ['Legal counsel through the licensing stages',
   'All matters under Mining Law No. 3213 and related legislation',
   'Advice and representation in proceedings and transactional work',
   'Technical counsel on tax processes',
   'Advice to foreign mining companies investing in T&uuml;rkiye']),
 ('healthcare-law', 'Healthcare Law',
  'Contracts, financing and liability for hospital groups and healthcare professionals.',
  ['Hospital formation and transfer agreements',
   'Negotiation of financing agreements with international credit institutions',
   'Clinical trial and confidentiality agreements',
   'Representation of practitioners and hospitals in malpractice claims',
   'Domestic and international collection and enforcement']),
 ('banking-and-finance-law', 'Banking &amp; Finance',
  'From the workings of credit institutions through to structured finance.',
  ['Counsel on the structure and operation of banks and credit institutions',
   'Credit agreements, leasing and corporate finance',
   'Asset, project and structured finance',
   'Capital markets and asset-backed securities',
   'International trade finance and Islamic finance']),
 ('real-estate-and-construction-law', 'Real Estate &amp; Construction',
  'Every stage of acquiring and building, from project development to zoning.',
  ['Real estate development projects and project counsel',
   'Title and registration procedures',
   'Negotiation of international acquisition and construction agreements',
   'Citizenship processes following property acquisition',
   'Lease agreements, mortgages and real estate finance',
   'Urban regeneration and zoning disputes']),
 ('intellectual-property-law', 'Intellectual Property',
  'Protecting trademarks, patents and copyright, and the licensing and assignment around them.',
  ['IP work across telecoms, internet, advertising, media and healthcare',
   'Counsel on portfolio transfers and acquisitions',
   'Representation in patent, trademark, copyright, unfair competition and trade secret actions',
   'Licence, assignment and transfer agreements',
   'International trademark, patent and design filings']),
 ('administrative-and-tax-law', 'Administrative &amp; Tax Law',
  'Challenges to administrative acts, alongside domestic and international tax structuring.',
  ['Counsel on dealings with public authorities',
   'Annulment actions against fines, licence and permit revocations',
   'Administrative applications, objections and dispute resolution',
   'Customs matters and tax offences and penalties',
   'Domestic tax counsel and international tax structuring',
   'International corporate structuring, mergers and acquisitions']),
 ('employment-law', 'Employment Law',
  'The legal frame of the employment relationship, from hiring through to termination.',
  ['Individual and collective employment agreements',
   'Termination, written warnings and notices',
   'Representation in reinstatement and wage claims',
   'Employee and workplace safety, and tracking legislative change',
   'Work and residence permits']),
 ('enforcement-and-insolvency-law', 'Enforcement &amp; Insolvency',
  'Representation on either side of the debt relationship, from recovery to composition.',
  ['Recovery for domestic and foreign clients, attachment and realisation',
   'Enforcement of court judgments',
   'Collection of cheques, notes and other negotiable instruments',
   'Halting enforcement and bankruptcy petitions, negative declaratory actions',
   'Preparation and management of restructuring and composition projects']),
]

HOME_SIX = [
 ('corporate-and-commercial-law', 'Corporate &amp; Commercial Law',
  'Incorporation, agreements, share structure and corporate process.',
  '<path d="M5 41h38M9 41V21m10 20V21m10 20V21m10 20V21M5 20 24 8l19 12Z"/>'),
 ('litigation-and-arbitration', 'Litigation &amp; Arbitration',
  'Disputes resolved through the courts, arbitration or negotiation.',
  '<path d="M24 7v34M13 41h22M9 15h30M9 15 4 27h10ZM39 15l-5 12h10Z"/>'
  '<path d="M4 27c0 4 10 4 10 0M34 27c0 4 10 4 10 0"/>'),
 ('maritime-law', 'Maritime Law',
  'Carriage, vessels, cargo, finance and maritime trade.',
  '<circle cx="24" cy="10" r="4"/><path d="M24 14v28M16 22h16M8 28c0 8 7 14 16 14s16-6 16-14M8 28H4m36 0h4"/>'),
 ('real-estate-and-construction-law', 'Real Estate &amp; Construction',
  'Transactions, projects, agreements and zoning process.',
  '<path d="M7 42h34M11 42V20l13-10 13 10v22M18 42V29h12v13"/>'),
 ('banking-and-finance-law', 'Banking &amp; Finance',
  'Credit, project finance and the legal structure of financial transactions.',
  '<path d="M5 41h38M9 41V23m10 18V23m10 18V23m10 18V23M5 22 24 10l19 12Z"/><circle cx="24" cy="31" r="3"/>'),
 ('employment-law', 'Employment Law',
  'Working relationships, agreements, termination and disputes.',
  '<circle cx="17" cy="16" r="6"/><circle cx="34" cy="19" r="5"/>'
  '<path d="M6 40c0-8 5-13 11-13s11 5 11 13M28 31c7-2 13 2 14 9"/>'),
]

ARTICLES = [
 ('kira-sozlesmelerinde-tahliye-surecleri', 'one', '20 May 2024',
  'Eviction Under a Lease: How the Process Actually Runs',
  'The grounds, the deadlines and the points that decide the outcome in practice.'),
 ('ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar', 'two', '12 May 2024',
  'Allocating Risk in Commercial Contracts',
  'Where liability sits, which safeguards hold, and what tends to be left unsaid.'),
 ('is-hukukunda-kidem-tazminati-sartlari', 'three', '05 May 2024',
  'When Severance Pay Is Owed',
  'The conditions that trigger entitlement, and how it is calculated in practice.'),
]

# ---------------------------------------------------------------- homepage --
cards = ''
for slug, title, desc, icon in HOME_SIX:
    cards += ('<a class="practice-card reveal" href="practice-areas/' + slug + '/">'
        '<span class="practice-icon"><svg viewBox="0 0 48 48">' + icon + '</svg></span>'
        '<h3>' + title + '</h3><p>' + desc + '</p><span class="arrow">&rarr;</span></a>')

art = ''
for slug, cls, date, title, _ in ARTICLES:
    art += ('<article class="article-card reveal"><div class="article-media ' + cls + '"></div>'
        '<div class="article-body"><time datetime="2024-05-20">' + date + '</time><h3>' + title + '</h3>'
        '<a class="text-link" href="articles/">Read More <span>&rarr;</span></a></div></article>')

s = head('Karakaş Law Firm | İzmir',
         'Karakaş Law Firm provides advocacy and legal counsel to companies and individuals from İzmir, Türkiye.',
         1, '../', 'redesign-home-polish.css',
         '<link rel="preload" as="image" href="../assets/hero-adalet-base.webp" media="(min-width:921px)">'
         '<link rel="preload" as="image" href="../assets/hero-adalet-mobil.webp" media="(max-width:920px)">')
s += '<a class="skip-link" href="#main">Skip to content</a>\n'
s += header(1, '', '../', 'contact/', 'Get in Touch', stuck=False)
s += ('<main id="main">\n'
  '<section class="hero">\n'
  '<div class="hero__scales" aria-hidden="true"><picture>'
  '<source media="(max-width:920px)" srcset="../assets/hero-terazi-mobil.webp">'
  '<img src="../assets/hero-terazi.webp" alt="" width="1672" height="941"></picture></div>\n'
  '<div class="shell hero__inner"><div class="hero__copy reveal">'
  '<p class="eyebrow">Karakaş Law Firm · İzmir</p>'
  '<h1>Complex Matters, Clear Counsel.</h1><div class="hero__rule"></div>'
  '<p class="hero__lead">We read a legal question not only against the statute but against its commercial and '
  'personal consequences, and work in a way that stays open, measured and deliberate.</p>'
  '<div class="hero__actions"><a class="btn" href="practice-areas/">Explore Our Practice' + ARROW + '</a></div>'
  '</div></div></section>\n'
  '<section class="section section--deep" aria-labelledby="areas-title"><div class="shell">'
  '<p class="section-label reveal" id="areas-title">Practice Areas</p>'
  '<div class="practice-grid">' + cards + '</div>'
  '<div style="text-align:center;margin-top:28px"><a class="text-link" href="practice-areas/">'
  'See all practice areas <span>&rarr;</span></a></div></div></section>\n'
  '<section class="section"><div class="shell about-grid reveal">'
  '<div class="about-copy"><p class="mini">About</p>'
  '<h2>A practice that works from inside commercial life.</h2><div class="gold-rule"></div>'
  '<p>Karakaş Law Firm was founded in İzmir by Att. Pınar Karakaş. The firm handles the legal needs of '
  'companies and individuals with an eye on the commercial and practical consequences of the process.</p>'
  '<a class="text-link" href="about/">About Us <span>&rarr;</span></a></div>'
  '<div class="about-media" role="img" aria-label="Karakaş Law Firm"></div></div></section>\n'
  '<section class="section section--deep"><div class="shell"><div class="section-head reveal">'
  '<div><p class="section-label" style="justify-content:flex-start;margin-bottom:18px">Insights</p>'
  '<h2>Notes on legal developments.</h2></div>'
  '<a class="text-link" href="articles/">All Articles <span>&rarr;</span></a></div>'
  '<div class="article-grid">' + art + '</div></div></section>\n'
  '</main>\n')
s += wa_float() + home_footer(1)
W('en/index.html', s)

# ------------------------------------------------------------------ about --
s = head('About | Karakaş Law Firm', 'The approach, outlook and founding lawyer of Karakaş Law Firm.',
         2, '../../hakkimizda/', 'redesign-pages.css')
s += header(2, 'about/', '../../hakkimizda/', 'contact/', 'Get in Touch')
s += ('<main>\n'
  '<section class="subhero"><div class="shell reveal"><p class="page-kicker">Karakaş Law Firm</p>'
  '<h1 class="page-title">About</h1><div class="page-rule"></div>'
  '<p class="page-lead">A measured way of working that treats a legal question not as a file but as something '
  'with commercial, personal and long-term consequences.</p></div></section>\n'
  '<section class="page-shell"><div class="shell"><div class="about-page-grid">'
  '<div class="about-page-copy reveal"><p class="page-kicker">Approach</p>'
  '<h2>A practice that works from inside commercial life.</h2>'
  '<p>Karakaş Law Firm was founded in İzmir by Att. Pınar Karakaş. The firm acts for companies and '
  'individuals across advocacy and legal counsel.</p>'
  '<p>Across corporate and commercial law, dispute resolution, maritime, healthcare, real estate, finance and '
  'employment, the work rests on open communication, predictable process management and close attention to '
  'the file.</p>'
  '<a class="text-link" href="../practice-areas/">See our practice areas <span>&rarr;</span></a></div>'
  '<div class="about-page-media reveal" role="img" aria-label="Karakaş Law Firm"></div>'
  '</div></div></section>\n'
  # Av. Pınar Karakaş fotoğrafının yayınlanmasını istemedi; portre bloğu
  # bilinçli olarak kaldırıldı, bölüm tek sütuna düşüyor.
  '<section class="founder" aria-labelledby="founder-title">'
  '<div class="shell founder__grid founder__grid--no-portrait">'
  '<div class="founder__copy reveal"><p class="page-kicker">Founding Lawyer</p>'
  '<h2 id="founder-title">Pınar Karakaş</h2><div class="gold-rule"></div>'
  '<p>Pınar Karakaş is the founding partner of Karakaş Law Firm. After graduating from İstanbul Bilgi '
  'University Faculty of Law, she completed her master&rsquo;s degree in international trade law with honours '
  'at Coventry University in the United Kingdom.</p>'
  '<p>Following experience at a well-regarded İstanbul law firm and as counsel to a group of companies '
  'reporting directly to the Turkish Savings Deposit Insurance Fund (TMSF), she founded Karakaş Law Firm in '
  'İzmir. She acts today for leading companies and hospital groups in the healthcare, chemicals, marble, '
  'machinery, engineering, fuel and furniture sectors, including on matters with an international dimension.</p>'
  '<p>A member of the İzmir Bar Association, she works predominantly for domestic and foreign companies.</p>'
  '<ul class="founder__facts">'
  '<li><small>Law Degree</small><strong>İstanbul Bilgi University<br>Faculty of Law</strong></li>'
  '<li><small>Master&rsquo;s</small><strong>Coventry University<br>International Trade Law (with honours)</strong></li>'
  '<li><small>Bar</small><strong>İzmir Bar Association<br>Registered Advocate</strong></li></ul>'
  '<div class="founder__areas"><h3>Practice</h3><ul class="founder__tags">'
  + ''.join('<li>' + t + '</li>' for _, t, _, _ in PRACTICE) +
  '</ul></div></div></div></section>\n'
  '<section class="page-shell page-shell--tight"><div class="shell"><div class="values-grid">'
  '<div class="value-card reveal"><span>01</span><h3>Clarity</h3><p>We set out the options, the risks and the '
  'likely outcomes in language that can be acted on.</p></div>'
  '<div class="value-card reveal"><span>02</span><h3>Proportion</h3><p>Each file is handled at the scale it '
  'needs, without manufactured complexity.</p></div>'
  '<div class="value-card reveal"><span>03</span><h3>Care</h3><p>We weigh the commercial and personal effects '
  'of a matter as closely as its legal detail.</p></div>'
  '</div></div></section>\n</main>\n')
s += wa_float() + inner_footer(2)
W('en/about/index.html', s)

# --------------------------------------------------------- practice areas --
cards = ''
for i, (slug, title, lead, items) in enumerate(PRACTICE, 1):
    cards += ('<a class="expertise-card reveal" href="' + slug + '/">'
        '<span class="expertise-no">%02d</span>' % i +
        '<h2>' + title + '</h2><p>' + lead + '</p>'
        '<ul class="expertise-list">' + ''.join('<li>' + x + '</li>' for x in items) + '</ul>'
        '<span class="text-link">See details <span>&rarr;</span></span></a>\n')

s = head('Practice Areas | Karakaş Law Firm',
         'The areas in which Karakaş Law Firm advises domestic and foreign companies and individuals.',
         2, '../../uzmanlik-alanlari/', 'redesign-pages.css')
s += header(2, 'practice-areas/', '../../uzmanlik-alanlari/', 'contact/', 'Get in Touch')
s += ('<main>\n'
  '<section class="subhero"><div class="shell reveal"><p class="page-kicker">What We Do</p>'
  '<h1 class="page-title">Practice Areas</h1><div class="page-rule"></div>'
  '<p class="page-lead">Karakaş Law Firm advises domestic and foreign individuals and companies across a wide '
  'field, from commercial law through to arbitration.</p></div></section>\n'
  '<section class="page-shell"><div class="shell"><div class="expertise-grid">\n' + cards +
  '</div></div></section>\n</main>\n')
s += wa_float() + inner_footer(2)
W('en/practice-areas/index.html', s)

# --------------------------------------------------------------- articles --
cards = ''
for slug, cls, date, title, desc in ARTICLES:
    cards += ('<article class="article-page-card reveal"><div class="article-media ' + cls + '"></div>'
        '<div class="article-body"><time datetime="2024-05-20">' + date + '</time>'
        '<h2>' + title + '</h2><p>' + desc + '</p>'
        '<a class="text-link" href="../../makaleler/' + slug + '/">Read in Turkish <span>&rarr;</span></a>'
        '</div></article>\n')

s = head('Articles | Karakaş Law Firm', 'Short notes on legal developments, contracts and practice.',
         2, '../../makaleler/', 'redesign-pages.css')
s += header(2, 'articles/', '../../makaleler/', 'contact/', 'Get in Touch')
s += ('<main>\n'
  '<section class="subhero"><div class="shell reveal"><p class="page-kicker">Insights</p>'
  '<h1 class="page-title">Articles</h1><div class="page-rule"></div>'
  '<p class="page-lead">Short notes on legal developments, contracts and practice. Full texts are currently '
  'published in Turkish.</p></div></section>\n'
  '<section class="page-shell"><div class="shell"><div class="article-page-grid">\n' + cards +
  '</div></div></section>\n</main>\n')
s += wa_float() + inner_footer(2)
W('en/articles/index.html', s)

# ---------------------------------------------------------------- contact --
CH = [('tel:+905305493090', 'Phone', '+90 530 549 30 90',
       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">'
       '<path d="M6.6 3h-2A1.6 1.6 0 0 0 3 4.6C3 12.6 11.4 21 19.4 21a1.6 1.6 0 0 0 1.6-1.6v-2a1 1 0 0 '
       '0-.8-1l-3.2-.7a1 1 0 0 0-1 .4l-1 1.3a13.6 13.6 0 0 1-5.4-5.4l1.3-1a1 1 0 0 0 .4-1l-.7-3.2a1 1 0 0 '
       '0-1-.8Z"/></svg>', False),
      ('https://wa.me/905305493090', 'WhatsApp', '+90 530 549 30 90', None, True),
      ('mailto:avpinarkarakas@gmail.com', 'Email', 'avpinarkarakas@gmail.com',
       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">'
       '<rect x="3" y="5" width="18" height="14"/><path d="m3 6 9 6.5L21 6"/></svg>', False),
      ('https://www.linkedin.com/company/karakas-law-firm/', 'LinkedIn', 'Karakaş Law Firm', None, True)]
from en_template import WA_SVG, LI_SVG
chans = ''
for href, label, val, icon, ext in CH:
    ic = icon or (WA_SVG if label == 'WhatsApp' else LI_SVG)
    tgt = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
    chans += ('<a class="channel" href="' + href + '"' + tgt + '>'
        '<span class="channel__icon">' + ic + '</span>'
        '<span class="channel__body"><small>' + label + '</small><strong>' + val + '</strong></span>'
        '<span class="channel__go" aria-hidden="true">&rarr;</span></a>\n')

MAP = ('https://www.google.com/maps?q=Armesa%20%C4%B0%C5%9F%20Merkezi%2C%20Akdeniz%20Mah.%201353%20Sk.%20No%3A2'
       '%2C%20Konak%2C%20%C4%B0zmir&amp;z=16&amp;output=embed')
DIR = ('https://www.google.com/maps/dir/?api=1&amp;destination=Armesa%20%C4%B0%C5%9F%20Merkezi%2C%20Akdeniz%20'
       'Mah.%201353%20Sk.%20No%3A2%2C%20Konak%2C%20%C4%B0zmir')

s = head('Contact | Karakaş Law Firm', 'Contact details for Karakaş Law Firm in İzmir, Türkiye.',
         2, '../../iletisim/', 'redesign-pages.css')
s += header(2, 'contact/', '../../iletisim/', 'tel:+905305493090', 'Call Us')
s += ('<main>\n'
  '<section class="subhero subhero--izmir"><div class="shell reveal"><p class="page-kicker">Karakaş Law Firm</p>'
  '<h1 class="page-title">Contact</h1><div class="page-rule"></div>'
  '<p class="page-lead">To discuss your matter or reach the office, use any of the channels below.</p>'
  '<p class="subhero__place">İzmir · Konak · Kordon</p></div></section>\n'
  '<section class="page-shell"><div class="shell contact-layout">'
  '<div class="contact-lead reveal"><p class="page-kicker">İzmir · Konak</p>'
  '<h2>Let&rsquo;s start the conversation here.</h2>'
  '<p>A short outline of what your matter involves helps the first conversation go further. Depending on the '
  'file, we can meet in person, speak by phone or arrange a video call.</p>'
  '<ul class="contact-notes">'
  '<li>The first conversation covers the scope of the matter and the likely route ahead.</li>'
  '<li>Anything you share is covered by an advocate&rsquo;s duty of confidentiality.</li></ul></div>'
  '<div class="contact-channels reveal">\n' + chans + '</div></div></section>\n'
  '<section class="locate" aria-labelledby="locate-title"><div class="locate__copy">'
  '<p class="page-kicker">Office</p><h2 id="locate-title">Armesa İş Merkezi</h2><div class="gold-rule"></div>'
  '<address>Akdeniz Mah. 1353 Sk. No:2<br>Armesa İş Merkezi D:32<br>Konak / İzmir, Türkiye</address>'
  '<p class="locate__note">If you need help finding the office, call ahead of your appointment and we will '
  'talk you in.</p>'
  '<div class="locate__actions"><a class="btn" href="' + DIR + '" target="_blank" rel="noopener">Get Directions'
  + ARROW + '</a><a class="text-link" href="tel:+905305493090">Call Us <span>&rarr;</span></a></div></div>'
  '<div class="locate__map"><iframe src="' + MAP + '" title="Karakaş Law Firm office location — Armesa İş '
  'Merkezi, Konak / İzmir" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen>'
  '</iframe></div></section>\n</main>\n')
s += wa_float() + inner_footer(2)
W('en/contact/index.html', s)

print('yazildi: en/index.html, en/about/, en/practice-areas/, en/articles/, en/contact/')
