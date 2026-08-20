(function(){
  "use strict";

  var header=document.querySelector('.site-header');
  var toggle=document.querySelector('.menu-toggle');
  var nav=document.querySelector('.main-nav');

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
    toggle.setAttribute('aria-label',open?'Menüyü kapat':'Menüyü aç');
    document.body.style.overflow=open?'hidden':'';
  }
  if(toggle&&nav){
    toggle.addEventListener('click',function(){setMenu(toggle.getAttribute('aria-expanded')!=='true');});
    nav.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('is-open')){setMenu(false);toggle.focus();}});
  }

  /* Contact map — precise single-location treatment for Armesa İş Merkezi. */
  var mapFrame=document.querySelector('.locate__map iframe');
  if(mapFrame){
    var mapWrap=mapFrame.parentElement;

    /* A coordinate query forces a single map marker instead of Google's
       multi-result business search. The coordinate is the Armesa İş Merkezi
       building on 1353. Sokak. */
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
      '.locate{max-width:1420px;margin:54px auto 76px;border:1px solid rgba(195,148,82,.30);background:#090908;overflow:hidden}',
      '.locate__copy{position:relative;background:radial-gradient(90% 120% at 0% 0%,rgba(195,148,82,.07),transparent 52%),linear-gradient(110deg,#080807,#0b0a09)}',
      '.locate__copy:after{content:"";position:absolute;inset:18px;border:1px solid rgba(195,148,82,.08);pointer-events:none}',
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
    directions.href='https://www.google.com/maps/dir/?api=1&destination=38.426121%2C27.135384&destination_place_id=ChIJie8JKfrYuxQRCkBc1UVEnuQ';
  }

  var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items=document.querySelectorAll('.reveal');
  if(reduced||!('IntersectionObserver' in window)){
    items.forEach(function(el){el.classList.add('is-in');});
  }else{
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){entry.target.classList.add('is-in');io.unobserve(entry.target);}
      });
    },{threshold:.08,rootMargin:'0px 0px -5% 0px'});
    items.forEach(function(el){io.observe(el);});
  }

  var year=document.getElementById('year');
  if(year)year.textContent=new Date().getFullYear();
})();
