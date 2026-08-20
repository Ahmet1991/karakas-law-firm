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

  /* Keep the WhatsApp glyph identical even on pages whose inline SVG came
     from an older/minified template. */
  var waPath='M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.9-4.45 9.9-9.91S17.5 2 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.19 8.19 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.23 8.23 0 0 1 0 16.47Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.71-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.44.13-.15.17-.25.25-.42.09-.16.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.84-.2-.49-.4-.42-.56-.43h-.47c-.16 0-.43.06-.65.31-.23.24-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.2 3.72.59.25 1.05.4 1.4.52.59.18 1.13.16 1.55.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.28Z';
  document.querySelectorAll('.wa-float svg path,.channel[href*="wa.me"] svg path').forEach(function(path){path.setAttribute('d',waPath);});

  /* Contact map — precise single-location treatment for Armesa İş Merkezi. */
  var mapFrame=document.querySelector('.locate__map iframe');
  if(mapFrame){
    var mapWrap=mapFrame.parentElement;

    /* A coordinate query forces a single map marker instead of Google's
       multi-result business search. */
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

  /* Use Google's canonical Directions URL format. Keep the destination name
     and verified Place ID together; do not mix a lat/lng destination with a
     different place identifier. */
  var directions=document.querySelector('.locate__actions .btn[href*="google.com/maps/dir"]');
  if(directions){
    directions.href='https://www.google.com/maps/dir/?api=1&destination=Armesa%20%C4%B0%C5%9F%20Merkezi&destination_place_id=ChIJie8JKfrYuxQRCkBc1UVEnuQ&travelmode=driving';
    directions.target='_blank';
    directions.rel='noopener noreferrer';
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
