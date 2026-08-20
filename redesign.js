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

  /* Contact map: lock the embed to the exact Armesa İş Merkezi building and
     keep Google's native, full-colour roadmap. The office is D:32 inside the
     building, so the public map pin intentionally targets the building itself. */
  var mapFrame=document.querySelector('.locate__map iframe');
  if(mapFrame){
    mapFrame.src='https://www.google.com/maps?q=Armesa%20%C4%B0%C5%9F%20Merkezi%2C%20Akdeniz%2C%201353.%20Sk.%20No%3A2%2C%2035210%20Konak%2F%C4%B0zmir%2C%20T%C3%BCrkiye&z=18&output=embed';
    mapFrame.style.filter='none';
    mapFrame.style.webkitFilter='none';
    mapFrame.title='Karakaş Hukuk Bürosu — Armesa İş Merkezi, Akdeniz Mah. 1353 Sk. No:2, Konak / İzmir';
  }

  var directions=document.querySelector('.locate__actions .btn[href*="google.com/maps/dir"]');
  if(directions){
    directions.href='https://www.google.com/maps/dir/?api=1&destination=Armesa%20%C4%B0%C5%9F%20Merkezi%2C%20Akdeniz%20Mah.%201353%20Sk.%20No%3A2%2C%2035210%20Konak%2F%C4%B0zmir%2C%20T%C3%BCrkiye&destination_place_id=ChIJie8JKfrYuxQRCkBc1UVEnuQ';
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
