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

// Replace the temporary monogram with the supplied professional portrait.
const portrait = document.querySelector('.portrait-placeholder');
if (portrait) {
  portrait.classList.add('has-photo');
  portrait.innerHTML = '<img src="assets/pinar-karakas-original-lossless.webp" alt="Pınar Karakaş" width="357" height="376" loading="lazy" decoding="async">';

  const portraitStyle = document.createElement('style');
  portraitStyle.textContent = `
    .profile-visual {
      width: min(100%, 330px);
      justify-self: center;
    }
    .portrait-placeholder.has-photo {
      width: 100%;
      aspect-ratio: 357 / 376;
      background: #fff;
      border: 1px solid rgba(10,15,26,.10);
    }
    .portrait-placeholder.has-photo::before,
    .portrait-placeholder.has-photo::after {
      display: none;
    }
    .portrait-placeholder.has-photo img {
      width: 100%;
      height: auto;
      display: block;
      object-fit: contain;
    }
    @media (max-width: 720px) {
      .profile-visual {
        width: min(82vw, 310px);
        justify-self: start;
      }
    }
  `;
  document.head.appendChild(portraitStyle);
}

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
