/* othmaneb : theme, language, nav, motion, hero terminal, embedded HBG demo */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Theme toggle ---------- */
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  }

  /* ---------- Language toggle ---------- */
  var btnEn = document.getElementById('langEn');
  var btnFr = document.getElementById('langFr');
  function setLang(lang) {
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang);
    localStorage.setItem('lang', lang);
    if (btnEn) btnEn.classList.toggle('on', lang === 'en');
    if (btnFr) btnFr.classList.toggle('on', lang === 'fr');
  }
  if (btnEn && btnFr) {
    btnEn.addEventListener('click', function () { setLang('en'); });
    btnFr.addEventListener('click', function () { setLang('fr'); });
    setLang(root.getAttribute('data-lang') || 'en');
  }

  /* ---------- Nav: mobile menu, scrolled state, scrollspy ---------- */
  var nav = document.querySelector('.nav');
  var burger = document.getElementById('navBurger');
  var links = document.getElementById('navLinks');
  if (burger && links) {
    burger.addEventListener('click', function () { links.classList.toggle('open'); });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) links.classList.remove('open');
    });
  }
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 10); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
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
        navAnchors.forEach(function (a) { a.classList.remove('active'); });
        var link = byId[en.target.id];
        if (link) link.classList.add('active');
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

  /* ---------- Embedded HuntingBadGuys demo: load on click ---------- */
  var facade = document.getElementById('hbgFacade');
  var frame = document.getElementById('hbgFrame');
  if (facade && frame) {
    var note = document.createElement('span');
    note.className = 'f-load';
    facade.appendChild(note);
    facade.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); facade.click(); }
    });
    facade.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      if (facade.classList.contains('loading')) return;
      facade.classList.add('loading');
      var fr = root.getAttribute('data-lang') === 'fr';
      note.textContent = fr ? 'Chargement de la plateforme…' : 'Loading the platform…';
      frame.addEventListener('load', function () {
        facade.classList.add('off');
      }, { once: true });
      frame.src = frame.getAttribute('data-src');
      // If the platform refuses to be embedded, guide the user to a new tab.
      setTimeout(function () {
        if (!facade.classList.contains('off')) {
          note.innerHTML = fr
            ? 'Si la fenêtre reste vide, <a href="' + frame.getAttribute('data-src') +
              '" target="_blank" rel="noopener" style="color:#a855f7">ouvrez la démo dans un nouvel onglet ↗</a>'
            : 'If the window stays empty, <a href="' + frame.getAttribute('data-src') +
              '" target="_blank" rel="noopener" style="color:#a855f7">open the demo in a new tab ↗</a>';
        }
      }, 6000);
    });
  }

  /* ---------- Hero terminal typing ---------- */
  var term = document.getElementById('termBody');
  if (!term) return;

  var SCRIPT = [
    { html: '<span class="t-prompt">othmaneb@hbg</span><span class="t-dim">:~$</span> <span class="t-cmd">whoami</span>', type: true },
    { html: '<span class="t-info">CTI analyst · malware analysis · detection engineering</span>' },
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
