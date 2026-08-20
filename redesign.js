(function(){
  "use strict";

  var sharedScript=document.currentScript;
  var baseUrl=sharedScript&&sharedScript.src?sharedScript.src:window.location.href;
  var asset=function(name){return new URL('assets/'+name,baseUrl).href;};
  var isHome=!!document.querySelector('.hero');

  /* Nested pages still need the WebP article assets. Keep these URLs absolute
     because CSS created inside a <style> element resolves relative to the page. */
  if(!isHome){
    var assetStyle=document.createElement('style');
    assetStyle.setAttribute('data-karakas-assets','webp');
    assetStyle.textContent=[
      '.article-media.one{background-image:linear-gradient(180deg,transparent,rgba(0,0,0,.08)),url("'+asset('makale-kira-sozlesmeleri.webp')+'")!important}',
      '.article-media.two{background-image:linear-gradient(180deg,transparent,rgba(0,0,0,.08)),url("'+asset('makale-ticari-sozlesmeler.webp')+'")!important}',
      '.article-media.three{background-image:linear-gradient(180deg,transparent,rgba(0,0,0,.08)),url("'+asset('makale-is-hukuku.webp')+'")!important}'
    ].join('\n');
    document.head.appendChild(assetStyle);
  }

  /* Visual-QA pass for the homepage. The reference uses a taller logo zone,
     a two-line hero headline and a less dominant justice image. */
  if(isHome){
    var homeTune=document.createElement('style');
    homeTune.setAttribute('data-karakas-home-tune','true');
    homeTune.textContent='\
@media (min-width:1181px){\
  .site-header{height:112px!important}\
  .brand img{width:142px!important}\
  .main-nav{gap:clamp(22px,2vw,34px)!important}\
  .hero{height:720px!important;min-height:720px!important;max-height:720px!important}\
  .hero::before{background:linear-gradient(90deg,#080807 0%,rgba(8,8,7,.995) 28%,rgba(8,8,7,.94) 40%,rgba(8,8,7,.62) 53%,rgba(8,8,7,.12) 70%,rgba(8,8,7,.02) 100%) 0 0/100% 100% no-repeat,linear-gradient(180deg,rgba(0,0,0,.06),rgba(0,0,0,.28)) 0 0/100% 100% no-repeat,url("'+asset('hero-adalet-premium.webp')+'") 97% center/auto 94% no-repeat!important}\
  .hero__inner{padding-top:82px!important}\
  .hero__copy{width:min(620px,46vw)!important;transform:translateY(4px)!important}\
  .hero h1{font-size:clamp(56px,4.1vw,68px)!important;max-width:16ch!important;line-height:1.03!important;letter-spacing:-.025em!important}\
  .hero__lead{max-width:50ch!important}\
}\
@media (min-width:921px) and (max-width:1180px){\
  .site-header{height:100px!important}\
  .brand img{width:122px!important}\
  .main-nav{gap:15px!important}\
  .hero{min-height:680px!important;height:680px!important}\
  .hero__inner{padding-top:76px!important}\
  .hero__copy{width:min(570px,50vw)!important}\
  .hero h1{font-size:56px!important;max-width:16ch!important}\
  .hero::before{background:linear-gradient(90deg,#080807 0%,rgba(8,8,7,.99) 30%,rgba(8,8,7,.88) 43%,rgba(8,8,7,.42) 58%,rgba(8,8,7,.06) 77%) 0 0/100% 100% no-repeat,url("'+asset('hero-adalet-premium.webp')+'") 100% center/auto 90% no-repeat!important}\
}\
@media (max-width:920px){\
  .brand img{width:90px!important}\
}\
@media (max-width:640px){\
  .brand img{width:82px!important}\
  .hero h1{max-width:12ch!important}\
}\
';
    document.head.appendChild(homeTune);
  }

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
