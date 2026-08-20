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
