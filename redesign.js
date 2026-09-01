(function(){
  "use strict";

  var header=document.querySelector('.site-header');
  var toggle=document.querySelector('.menu-toggle');
  var nav=document.querySelector('.main-nav');
  var pageLang=document.documentElement.lang==='en'?'en':'tr';
  var sharedScript=document.currentScript;
  var siteRoot=sharedScript&&sharedScript.src?new URL('./',sharedScript.src):new URL('./',window.location.href);

  /* Keep Articles/Makaleler in the shared navigation on every redesigned page.
     Older hand-written pages may not contain the item in their static markup. */
  if(nav&&!nav.querySelector('a[href*="makaleler"],a[href*="articles"]')){
    var articleNav=document.createElement('a');
    articleNav.className='main-nav__link';
    articleNav.textContent=pageLang==='en'?'Articles':'Makaleler';
    articleNav.href=new URL(pageLang==='en'?'en/articles/':'makaleler/',siteRoot).href;
    var contactLink=Array.prototype.find.call(nav.querySelectorAll('.main-nav__link'),function(a){
      var text=(a.textContent||'').trim().toLowerCase();
      return text==='iletişim'||text==='contact';
    });
    if(contactLink)nav.insertBefore(articleNav,contactLink);
    else{
      var langSwitch=nav.querySelector('.lang-switch');
      if(langSwitch)nav.insertBefore(articleNav,langSwitch);else nav.appendChild(articleNav);
    }
  }

  /* Article language pairs. A reader switching language on a detail article
     lands on the same article, not merely the article index. */
  var articlePairs={
    'kira-sozlesmelerinde-tahliye-surecleri':'lease-eviction-processes',
    'ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar':'commercial-contracts-key-considerations',
    'is-hukukunda-kidem-tazminati-sartlari':'severance-pay-conditions'
  };
  var path=window.location.pathname.replace(/\/+$/,'');
  Object.keys(articlePairs).forEach(function(trSlug){
    var enSlug=articlePairs[trSlug];
    var trNeedle='/makaleler/'+trSlug;
    var enNeedle='/en/articles/'+enSlug;
    if(path.indexOf(trNeedle)!==-1){
      var enSwitch=document.querySelector('.lang-switch a[hreflang="en"]');
      var enUrl=new URL('en/articles/'+enSlug+'/',siteRoot).href;
      if(enSwitch)enSwitch.href=enUrl;
      if(!document.head.querySelector('link[rel="alternate"][hreflang="en"]')){
        var enAlt=document.createElement('link');enAlt.rel='alternate';enAlt.hreflang='en';enAlt.href=enUrl;document.head.appendChild(enAlt);
      }
    }
    if(path.indexOf(enNeedle)!==-1){
      var trSwitch=document.querySelector('.lang-switch a[hreflang="tr"]');
      var trUrl=new URL('makaleler/'+trSlug+'/',siteRoot).href;
      if(trSwitch)trSwitch.href=trUrl;
      if(!document.head.querySelector('link[rel="alternate"][hreflang="tr"]')){
        var trAlt=document.createElement('link');trAlt.rel='alternate';trAlt.hreflang='tr';trAlt.href=trUrl;document.head.appendChild(trAlt);
      }
    }
  });

  /* Restore the three-article block on both homepages without duplicating it
     if the markup is later added statically. */
  var isHome=(path.endsWith('/karakas-law-firm')||path.endsWith('/karakas-law-firm/index.html')||path===''||path==='/'||path.endsWith('/en'));
  if(isHome&&!document.querySelector('.home-articles-restored')&&!document.querySelector('.article-grid')){
    var main=document.getElementById('main')||document.querySelector('main');
    if(main){
      var section=document.createElement('section');
      section.className='section section--deep home-articles-restored';
      if(pageLang==='en'){
        section.innerHTML='<div class="shell"><div class="section-head reveal"><div><p class="section-label" style="justify-content:flex-start;margin-bottom:18px">Articles</p><h2>Notes on legal developments.</h2></div><a class="text-link" href="'+new URL('en/articles/',siteRoot).href+'">All Articles <span>→</span></a></div><div class="article-grid">'+
          '<article class="article-card reveal"><a href="'+new URL('en/articles/lease-eviction-processes/',siteRoot).href+'"><div class="article-media one" style="background:none"><img src="'+new URL('assets/makale-kira-sozlesmeleri.webp',siteRoot).href+'" alt="Lease agreements and eviction proceedings" width="1200" height="800" loading="lazy" decoding="async" style="display:block;width:100%;height:100%;object-fit:cover"></div></a><div class="article-body"><time datetime="2026-08-21">21 August 2026</time><h3><a href="'+new URL('en/articles/lease-eviction-processes/',siteRoot).href+'">Eviction Under a Lease: How the Process Works</a></h3><a class="text-link" href="'+new URL('en/articles/lease-eviction-processes/',siteRoot).href+'">Read More <span>→</span></a></div></article>'+
          '<article class="article-card reveal"><a href="'+new URL('en/articles/commercial-contracts-key-considerations/',siteRoot).href+'"><div class="article-media two" style="background:none"><img src="'+new URL('assets/makale-ticari-sozlesmeler.webp',siteRoot).href+'" alt="Commercial contract legal review" width="1200" height="800" loading="lazy" decoding="async" style="display:block;width:100%;height:100%;object-fit:cover"></div></a><div class="article-body"><time datetime="2026-08-21">21 August 2026</time><h3><a href="'+new URL('en/articles/commercial-contracts-key-considerations/',siteRoot).href+'">Key Considerations in Commercial Contracts</a></h3><a class="text-link" href="'+new URL('en/articles/commercial-contracts-key-considerations/',siteRoot).href+'">Read More <span>→</span></a></div></article>'+
          '<article class="article-card reveal"><a href="'+new URL('en/articles/severance-pay-conditions/',siteRoot).href+'"><div class="article-media three" style="background:none"><img src="'+new URL('assets/makale-is-hukuku.webp',siteRoot).href+'" alt="Employment law and severance pay" width="1200" height="800" loading="lazy" decoding="async" style="display:block;width:100%;height:100%;object-fit:cover"></div></a><div class="article-body"><time datetime="2026-08-21">21 August 2026</time><h3><a href="'+new URL('en/articles/severance-pay-conditions/',siteRoot).href+'">When Is Severance Pay Owed?</a></h3><a class="text-link" href="'+new URL('en/articles/severance-pay-conditions/',siteRoot).href+'">Read More <span>→</span></a></div></article></div></div>';
      }else{
        section.innerHTML='<div class="shell"><div class="section-head reveal"><div><p class="section-label" style="justify-content:flex-start;margin-bottom:18px">Güncel Makaleler</p><h2>Hukuki gelişmelere dair notlar.</h2></div><a class="text-link" href="'+new URL('makaleler/',siteRoot).href+'">Tüm Makaleler <span>→</span></a></div><div class="article-grid">'+
          '<article class="article-card reveal"><a href="'+new URL('makaleler/kira-sozlesmelerinde-tahliye-surecleri/',siteRoot).href+'"><div class="article-media one" style="background:none"><img src="'+new URL('assets/makale-kira-sozlesmeleri.webp',siteRoot).href+'" alt="Kira sözleşmeleri ve tahliye süreçleri" width="1200" height="800" loading="lazy" decoding="async" style="display:block;width:100%;height:100%;object-fit:cover"></div></a><div class="article-body"><time datetime="2026-08-21">21 Ağustos 2026</time><h3><a href="'+new URL('makaleler/kira-sozlesmelerinde-tahliye-surecleri/',siteRoot).href+'">Kira Sözleşmelerinde Tahliye Süreçleri Nelerdir?</a></h3><a class="text-link" href="'+new URL('makaleler/kira-sozlesmelerinde-tahliye-surecleri/',siteRoot).href+'">Devamını Oku <span>→</span></a></div></article>'+
          '<article class="article-card reveal"><a href="'+new URL('makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/',siteRoot).href+'"><div class="article-media two" style="background:none"><img src="'+new URL('assets/makale-ticari-sozlesmeler.webp',siteRoot).href+'" alt="Ticari sözleşmelerin hukuki değerlendirmesi" width="1200" height="800" loading="lazy" decoding="async" style="display:block;width:100%;height:100%;object-fit:cover"></div></a><div class="article-body"><time datetime="2026-08-21">21 Ağustos 2026</time><h3><a href="'+new URL('makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/',siteRoot).href+'">Ticari Sözleşmelerde Dikkat Edilmesi Gereken Hususlar</a></h3><a class="text-link" href="'+new URL('makaleler/ticari-sozlesmelerde-dikkat-edilmesi-gereken-hususlar/',siteRoot).href+'">Devamını Oku <span>→</span></a></div></article>'+
          '<article class="article-card reveal"><a href="'+new URL('makaleler/is-hukukunda-kidem-tazminati-sartlari/',siteRoot).href+'"><div class="article-media three" style="background:none"><img src="'+new URL('assets/makale-is-hukuku.webp',siteRoot).href+'" alt="İş hukuku ve kıdem tazminatı" width="1200" height="800" loading="lazy" decoding="async" style="display:block;width:100%;height:100%;object-fit:cover"></div></a><div class="article-body"><time datetime="2026-08-21">21 Ağustos 2026</time><h3><a href="'+new URL('makaleler/is-hukukunda-kidem-tazminati-sartlari/',siteRoot).href+'">İş Hukukunda Kıdem Tazminatı Şartları</a></h3><a class="text-link" href="'+new URL('makaleler/is-hukukunda-kidem-tazminati-sartlari/',siteRoot).href+'">Devamını Oku <span>→</span></a></div></article></div></div>';
      }
      main.appendChild(section);
    }
  }

  function syncHeader(){
    if(!header)return;
    header.classList.toggle('is-stuck',window.scrollY>24);
  }
  syncHeader();
  window.addEventListener('scroll',syncHeader,{passive:true});

  function setMenu(open){
    if(!toggle||!nav)return;
    nav.classList.toggle('is-open',open);
    toggle.setAttribute('aria-expanded',String(open));
    toggle.setAttribute('aria-label',open?(pageLang==='en'?'Close menu':'Menüyü kapat'):(pageLang==='en'?'Open menu':'Menüyü aç'));
    document.body.style.overflow=open?'hidden':'';
  }
  if(toggle&&nav){
    toggle.addEventListener('click',function(){setMenu(toggle.getAttribute('aria-expanded')!=='true');});
    nav.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('is-open')){setMenu(false);toggle.focus();}});
  }

  var waPath='M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.9-4.45 9.9-9.91S17.5 2 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.19 8.19 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.23 8.23 0 0 1 0 16.47Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.71-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.44.13-.15.17-.25.25-.42.09-.16.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.84-.2-.49-.4-.42-.56-.43h-.47c-.16 0-.43.06-.65.31-.23.24-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.2 3.72.59.25 1.05.4 1.4.52.59.18 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.28Z';
  document.querySelectorAll('.wa-float svg path,.channel[href*="wa.me"] svg path').forEach(function(p){p.setAttribute('d',waPath);});

  var mapFrame=document.querySelector('.locate__map iframe');
  if(mapFrame){
    var mapWrap=mapFrame.parentElement;
    mapFrame.src='https://www.google.com/maps?q=38.426121,27.135384&z=18&output=embed';
    mapFrame.style.filter='none';
    mapFrame.style.webkitFilter='none';
    mapFrame.title='Karakaş Hukuk Bürosu — Armesa İş Merkezi, D:32, Konak / İzmir';
    mapWrap.classList.add('map-premium');
    if(!mapWrap.querySelector('.map-office-badge')){
      var badge=document.createElement('div');
      badge.className='map-office-badge';
      badge.innerHTML='<span class="map-office-badge__mark">K</span><span><strong>Karakaş Hukuk Bürosu</strong><small>Armesa İş Merkezi · D:32</small></span>';
      mapWrap.appendChild(badge);
    }
    var mapStyle=document.createElement('style');
    mapStyle.setAttribute('data-karakas-map-polish','true');
    mapStyle.textContent=[
      '.locate{max-width:1420px;margin:54px auto 76px;border:1px solid var(--line);border-radius:var(--radius,0);background:var(--panel,#090908);box-shadow:var(--shadow-md,none);overflow:hidden}',
      '.locate__copy{position:relative;background:radial-gradient(90% 120% at 0% 0%,rgba(203,174,114,.10),transparent 55%),var(--panel,#080807)}',
      '.locate__copy:after{content:"";position:absolute;inset:18px;border:1px solid var(--line-soft,rgba(195,148,82,.08));pointer-events:none}',
      '.locate__map.map-premium{position:relative;min-height:520px;margin:18px 18px 18px 0;border:1px solid rgba(224,189,131,.38);overflow:hidden;background:#efe9df;box-shadow:inset 0 0 0 1px rgba(255,255,255,.025)}',
      '.locate__map.map-premium iframe{position:absolute;inset:0;width:100%;height:100%;filter:none!important;-webkit-filter:none!important}',
      '.map-office-badge{position:absolute;z-index:3;left:18px;top:18px;display:flex;align-items:center;gap:11px;padding:11px 14px 11px 10px;background:rgba(7,7,6,.94);border:1px solid rgba(195,148,82,.55);box-shadow:0 10px 28px rgba(0,0,0,.28);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);pointer-events:none}',
      '.map-office-badge__mark{width:34px;height:34px;border:1px solid #c39452;border-radius:50%;display:grid;place-items:center;color:#e0bd83;font-family:"Bodoni Moda",Georgia,serif;font-size:18px}',
      '.map-office-badge strong{display:block;color:#f3efe8;font-family:"Bodoni Moda",Georgia,serif;font-size:15px;font-weight:400;line-height:1.15}',
      '.map-office-badge small{display:block;margin-top:3px;color:#b1aaa0;font-size:9px;letter-spacing:.09em;text-transform:uppercase}',
      '@media(max-width:980px){.locate{margin:36px 18px 58px}.locate__map.map-premium{margin:0 18px 18px;min-height:410px;border-left:1px solid rgba(224,189,131,.38)}}',
      '@media(max-width:680px){.locate{margin:28px 14px 44px}.locate__map.map-premium{margin:0 12px 12px;min-height:340px}.map-office-badge{left:10px;top:10px;padding:9px 11px 9px 8px}.map-office-badge__mark{width:30px;height:30px}.map-office-badge strong{font-size:13px}.map-office-badge small{font-size:8px}}'
    ].join('\n');
    document.head.appendChild(mapStyle);
  }

  var directions=document.querySelector('.locate__actions .btn[href*="google.com/maps/dir"]');
  if(directions){
    directions.href='https://www.google.com/maps/dir/?api=1&destination=Armesa%20%C4%B0%C5%9F%20Merkezi&destination_place_id=ChIJie8JKfrYuxQRCkBc1UVEnuQ&travelmode=driving';
    directions.target='_blank';
    directions.rel='noopener noreferrer';
  }

  var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items=document.querySelectorAll('.reveal');
  function show(el){el.classList.add('is-in');}

  if(reduced||!('IntersectionObserver' in window)){
    items.forEach(show);
  }else{
    // threshold 0: bir pikseli bile gorunur olunca tetiklenir. Onceki .08
    // degeri, ekrandan cok daha uzun bir ogede (ornegin makale govdesinin
    // tamami tek bir .reveal ise) hicbir zaman saglanamiyor ve icerik kalici
    // olarak gorunmez kaliyordu.
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){show(entry.target);io.unobserve(entry.target);}
      });
    },{threshold:0,rootMargin:'0px 0px -8% 0px'});
    items.forEach(function(el){io.observe(el);});

    // Ilk ekranda duran ogeler kaydirma beklemeden acilir.
    requestAnimationFrame(function(){
      items.forEach(function(el){
        if(el.getBoundingClientRect().top < window.innerHeight)show(el);
      });
    });

    // Emniyet agi: gozlemci herhangi bir sebeple calismazsa icerik
    // gorunmez kalmasin.
    window.setTimeout(function(){items.forEach(show);},2500);
  }

  // --- Sayfalar arasi morph gecisi -----------------------------------
  // Bir karta tiklandiginda kartin basligina, detay sayfasindaki
  // .page-title ile AYNI view-transition adi verilir; tarayici ikisini
  // eslestirip aralarinda akitir. Ad ayni anda tek ogede olabilecegi
  // icin once sayfanin kendi basligindan aliniyor.
  if(!reduced && 'startViewTransition' in document){
    document.addEventListener('click',function(ev){
      var t=ev.target;
      if(!t||!t.closest)return;
      var card=t.closest('.expertise-card,.article-page-card,.article-card,.practice-card');
      if(!card)return;
      var title=card.querySelector('h2,h3');
      if(!title)return;
      var own=document.querySelector('.subhero .page-title');
      if(own)own.style.viewTransitionName='none';
      title.style.viewTransitionName='page-title';
    },true);

    // Geri donuldugunde (bfcache) ad uzerinde kalmasin.
    window.addEventListener('pageshow',function(){
      var m=document.querySelector('[style*="view-transition-name"]');
      if(m)m.style.viewTransitionName='';
      var own=document.querySelector('.subhero .page-title');
      if(own)own.style.viewTransitionName='';
    });
  }

  // --- Makale okuma ilerleme cizgisi ---------------------------------
  // Dolgusu CSS'te scroll() zaman cizgisiyle yapiliyor; burada yalnizca
  // ogeyi ekliyoruz. Destek yoksa cizgi eklenmiyor.
  if(!reduced && document.querySelector('.article-content') &&
     window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()')){
    var bar=document.createElement('div');
    bar.className='read-progress';
    bar.setAttribute('aria-hidden','true');
    document.body.appendChild(bar);
  }

  var year=document.getElementById('year');
  if(year)year.textContent=new Date().getFullYear();
})();
