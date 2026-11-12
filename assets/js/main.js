/* othmaneb : theme, language, nav, motion, hero terminal */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function store(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* private mode */ }
  }
  // Cross-fade the whole page when the browser supports view transitions
  function swap(apply) {
    if (!reduced && document.startViewTransition) document.startViewTransition(apply);
    else apply();
  }

  /* ---------- Theme toggle ---------- */
  var themeBtn = document.getElementById('themeBtn');
  var themeMeta = document.querySelector('meta[name="theme-color"]');
  function syncTheme() {
    var dark = root.getAttribute('data-theme') !== 'light';
    if (themeMeta) themeMeta.setAttribute('content', dark ? '#03050a' : '#f5f0e8');
    if (themeBtn) themeBtn.setAttribute('aria-pressed', String(!dark));
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      swap(function () { root.setAttribute('data-theme', next); syncTheme(); });
      store('theme', next);
    });
  }
  syncTheme();

  /* ---------- Language toggle ---------- */
  var btnEn = document.getElementById('langEn');
  var btnFr = document.getElementById('langFr');
  function setLang(lang) {
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang);
    if (btnEn) { btnEn.classList.toggle('on', lang === 'en'); btnEn.setAttribute('aria-pressed', String(lang === 'en')); }
    if (btnFr) { btnFr.classList.toggle('on', lang === 'fr'); btnFr.setAttribute('aria-pressed', String(lang === 'fr')); }
  }
  function pickLang(lang) {
    if (root.getAttribute('data-lang') === lang) return;
    swap(function () { setLang(lang); });
    store('lang', lang);
  }
  if (btnEn && btnFr) {
    btnEn.addEventListener('click', function () { pickLang('en'); });
    btnFr.addEventListener('click', function () { pickLang('fr'); });
    setLang(root.getAttribute('data-lang') || 'en');
  }

  /* ---------- Nav: mobile menu, scrolled state, scrollspy ---------- */
  var nav = document.querySelector('.nav');
  var burger = document.getElementById('navBurger');
  var links = document.getElementById('navLinks');
  function setMenu(open) {
    links.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
  }
  if (burger && links) {
    burger.addEventListener('click', function () { setMenu(!links.classList.contains('open')); });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('open')) { setMenu(false); burger.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (links.classList.contains('open') && !nav.contains(e.target)) setMenu(false);
    });
  }
  if (nav) {
    var prog = document.getElementById('scrollProgress');
    var ticking = false;
    var paint = function () {
      ticking = false;
      nav.classList.toggle('scrolled', window.scrollY > 10);
      if (prog) {
        var h = root.scrollHeight - window.innerHeight;
        prog.style.setProperty('--progress', h > 0 ? Math.min(1, window.scrollY / h) : 0);
      }
    };
    var onScroll = function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(paint); }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    paint();
  }
  // Scrollspy: highlight the nav link of the section in view (home page only)
  var sections = document.querySelectorAll('section.block[id], header.hero');
  var navAnchors = links ? links.querySelectorAll('a[href*="#"]') : [];
  if (sections.length && navAnchors.length && 'IntersectionObserver' in window) {
    var byId = {};
    navAnchors.forEach(function (a) {
      var m = a.getAttribute('href').split('#')[1];
      if (m) byId[m] = a;
    });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        navAnchors.forEach(function (a) { a.classList.remove('active'); a.removeAttribute('aria-current'); });
        var link = byId[en.target.id];
        if (link) { link.classList.add('active'); link.setAttribute('aria-current', 'true'); }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Reveal on scroll, with stagger ---------- */
  var revealed = document.querySelectorAll('.reveal');
  if (revealed.length && 'IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      var batch = 0;
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.style.setProperty('--stagger', (batch++ * 80) + 'ms');
        en.target.classList.add('vis');
        io.unobserve(en.target);
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });
    revealed.forEach(function (el) { io.observe(el); });
  } else {
    revealed.forEach(function (el) { el.classList.add('vis'); });
  }

  /* ---------- Project cards: fold long descriptions behind "Read more" ---------- */
  var CHEV = '<svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 9l7 7 7-7"/></svg>';
  document.querySelectorAll('.proj > p').forEach(function (p) {
    p.classList.add('clamp');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'proj-more';
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML =
      '<span class="more"><span class="lang-en">Read more</span><span class="lang-fr">Lire la suite</span></span>' +
      '<span class="less"><span class="lang-en">Show less</span><span class="lang-fr">Réduire</span></span>' + CHEV;
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', String(open));
      p.classList.toggle('clamp', !open);
    });
    p.insertAdjacentElement('afterend', btn);
  });

  /* ---------- Hero terminal typing ---------- */
  var term = document.getElementById('termBody');
  if (!term) return;

  var SCRIPT = [
    { html: '<span class="t-prompt">othmaneb@hbg</span><span class="t-dim">:~$</span> <span class="t-cmd">whoami</span>', type: true },
    { html: '<span class="t-info">security engineer - CSIRT L3 @ BNP Paribas CIB · forensics · malware analysis · detection engineering</span>' },
    { html: '&nbsp;' },
    { html: '<span class="t-prompt">othmaneb@hbg</span><span class="t-dim">:~$</span> <span class="t-cmd">./hunt --target suspicious-domain.tld --full</span>', type: true },
    { html: '<span class="t-ok">[+]</span> DNS <span class="t-ok">✓</span>  WHOIS <span class="t-ok">✓</span>  HTTP chain <span class="t-ok">✓</span>  CT logs <span class="t-ok">✓</span>  BGP/ASN <span class="t-ok">✓</span>' },
    { html: '<span class="t-ok">[+]</span> screenshot captured · pHash clustered <span class="t-dim">(3 look-alikes)</span>' },
    { html: '<span class="t-warn">[!]</span> EFI: 65 patterns → <span class="t-warn">12 IOCs extracted</span> <span class="t-dim">(wallets, C2, tokens)</span>' },
    { html: '<span class="t-ok">[+]</span> EFA: static analysis · entropy 7.2, PE32 identified' },
    { html: '<span class="t-info">[i]</span> report ready → <span class="t-cmd">investigation_report.html</span> · STIX 2.1 bundle' },
    { html: '&nbsp;' },
    { html: '<span class="t-prompt">othmaneb@hbg</span><span class="t-dim">:~$</span> <span class="t-caret"></span>' }
  ];

  if (reduced) {
    term.innerHTML = SCRIPT.map(function (l) { return '<span class="ln">' + l.html + '</span>'; }).join('');
    return;
  }

  var li = 0;
  function nextLine() {
    if (li >= SCRIPT.length) return;
    var line = SCRIPT[li++];
    var el = document.createElement('span');
    el.className = 'ln';
    term.appendChild(el);
    if (line.type) {
      var tmp = document.createElement('div');
      tmp.innerHTML = line.html;
      var txt = tmp.textContent;
      var i = 0;
      (function typeCh() {
        el.textContent = txt.slice(0, ++i);
        if (i < txt.length) { setTimeout(typeCh, 22); }
        else { el.innerHTML = line.html; setTimeout(nextLine, 240); }
      })();
    } else {
      el.innerHTML = line.html;
      setTimeout(nextLine, li < 4 ? 300 : 170);
    }
  }
  if ('IntersectionObserver' in window) {
    var tio = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { tio.disconnect(); setTimeout(nextLine, 350); }
    });
    tio.observe(term);
  } else { nextLine(); }
})();
