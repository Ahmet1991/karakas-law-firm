const root = document.documentElement;
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
const langToggle = document.querySelector('.lang-toggle');
const languageNodes = document.querySelectorAll('[data-tr][data-en]');

let currentLang = localStorage.getItem('karakas-lang') || 'tr';

function applyLanguage(lang) {
  currentLang = lang;
  root.lang = lang;
  languageNodes.forEach((node) => {
    node.textContent = node.dataset[lang];
  });
  langToggle?.classList.toggle('is-en', lang === 'en');
  document.title = lang === 'tr'
    ? 'Karakaş Hukuk Bürosu | İzmir'
    : 'Karakaş Law Firm | Izmir';
  localStorage.setItem('karakas-lang', lang);
}

applyLanguage(currentLang);

// The source site does not state a graduation year, so the visual label stays factual.
const educationLabels = document.querySelectorAll('.education > div > span');
if (educationLabels[0]) educationLabels[0].textContent = 'LL.B.';

langToggle?.addEventListener('click', () => {
  applyLanguage(currentLang === 'tr' ? 'en' : 'tr');
});

menuToggle?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(open));
});

nav?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    nav.classList.remove('open');
    menuToggle?.setAttribute('aria-expanded', 'false');
  });
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
document.getElementById('year').textContent = new Date().getFullYear();
