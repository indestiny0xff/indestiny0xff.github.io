/* othmaneb — theme, language, nav, reveal & hero terminal */
(function () {
  'use strict';

  var root = document.documentElement;

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

  /* ---------- Mobile nav ---------- */
  var burger = document.getElementById('navBurger');
  var links = document.getElementById('navLinks');
  if (burger && links) {
    burger.addEventListener('click', function () { links.classList.toggle('open'); });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) links.classList.remove('open');
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealed = document.querySelectorAll('.reveal');
  if (revealed.length && 'IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('vis'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    revealed.forEach(function (el) { io.observe(el); });
  } else {
    revealed.forEach(function (el) { el.classList.add('vis'); });
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
    { html: '<span class="t-ok">[+]</span> screenshot captured — pHash clustered <span class="t-dim">(3 look-alikes)</span>' },
    { html: '<span class="t-warn">[!]</span> EFI: 65 patterns → <span class="t-warn">12 IOCs extracted</span> <span class="t-dim">(wallets, C2, tokens)</span>' },
    { html: '<span class="t-ok">[+]</span> EFA: static analysis — entropy 7.2, PE32 identified' },
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
      // type the visible text progressively, then swap in the rich HTML
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
  // start once visible
  if ('IntersectionObserver' in window) {
    var tio = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { tio.disconnect(); setTimeout(nextLine, 350); }
    });
    tio.observe(term);
  } else { nextLine(); }
})();
