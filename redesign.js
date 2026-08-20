(function(){
  "use strict";

  /* Asset filenames in the local /assets folder are WebP. Keep the visual
     system resilient by overriding only the image URLs here; no layout rules
     are duplicated. */
  var assetStyle=document.createElement('style');
  assetStyle.setAttribute('data-karakas-assets','webp');
  assetStyle.textContent=[
    '.hero::before{background:linear-gradient(90deg,#080807 0%,rgba(8,8,7,.98) 31%,rgba(8,8,7,.76) 47%,rgba(8,8,7,.08) 69%),linear-gradient(180deg,rgba(0,0,0,.12),rgba(0,0,0,.46)),url("assets/hero-adalet-premium.webp") center right/cover no-repeat!important}',
    '.about-media{background:linear-gradient(90deg,#0a0a09 0%,rgba(10,10,9,.55) 20%,transparent 52%),linear-gradient(180deg,transparent 56%,rgba(0,0,0,.38)),url("assets/hakkimizda-terazi-masa.webp") center/cover no-repeat!important}',
    '.article-media.one{background-image:linear-gradient(180deg,transparent,rgba(0,0,0,.08)),url("assets/makale-kira-sozlesmeleri.webp")!important}',
    '.article-media.two{background-image:linear-gradient(180deg,transparent,rgba(0,0,0,.08)),url("assets/makale-ticari-sozlesmeler.webp")!important}',
    '.article-media.three{background-image:linear-gradient(180deg,transparent,rgba(0,0,0,.08)),url("assets/makale-is-hukuku.webp")!important}'
  ].join('\n');
  document.head.appendChild(assetStyle);

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
