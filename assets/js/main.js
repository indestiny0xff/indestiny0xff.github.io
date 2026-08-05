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

/* ---------- HuntingBadGuys interactive scan console (simulated) ---------- */
(function () {
  'use strict';

  var consoleEl = document.getElementById('hbgConsole');
  var input = document.getElementById('demoInput');
  var runBtn = document.getElementById('demoRun');
  var stream = document.getElementById('demoStream');
  var results = document.getElementById('demoResults');
  if (!consoleEl || !input || !runBtn || !stream || !results) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  var MODULES = ['DNS', 'WHOIS', 'HTTP', 'TLS', 'CT LOGS', 'BGP/ASN', 'GEOIP', 'SCREENSHOT', 'CRAWLER', 'EFI'];

  // Each scenario: stream log lines + structured result blocks. All data is synthetic.
  var SCENARIOS = {
    phish: {
      target: 'secure-paypa1-login.com',
      lines: [
        '<span class="t-ok">[+]</span> DNS: A 203.0.113.42 · NS ns1.fastregistrar.example',
        '<span class="t-ok">[+]</span> WHOIS: registered <span class="t-warn">4 days ago</span> · privacy-protected registrant',
        '<span class="t-ok">[+]</span> HTTP chain: 302 → hxxps://secure-paypa1-login[.]com/signin <span class="t-dim">(200)</span>',
        '<span class="t-ok">[+]</span> TLS: issuer R3 · cert age 3 days',
        '<span class="t-ok">[+]</span> CT logs: 1 certificate · SAN login.secure-paypa1-login.com',
        '<span class="t-ok">[+]</span> screenshot captured · <span class="t-info">pHash matches 6 known phishing pages</span>',
        '<span class="t-ok">[+]</span> crawler: kit files found at /assets/js/gate.js · MinHash cluster #12',
        '<span class="t-warn">[!]</span> feeds: listed on <span class="t-warn">OpenPhish</span> and <span class="t-warn">URLhaus</span>',
        '<span class="t-warn">[!]</span> EFI: 3 IOCs extracted from page source and kit files'
      ],
      feeds: ['OpenPhish · listed 2026-08-01', 'URLhaus · phishing kit'],
      iocs: ['@fake_support_tg', 'bc1qxy2k...phish', '/gate.php exfil endpoint'],
      verdict: { cls: 'bad', en: '◉ VERDICT: ACTIVE PHISHING · confidence high', fr: '◉ VERDICT : PHISHING ACTIF · confiance élevée' }
    },
    ransom: {
      target: 'leaksblog7xq4v.onion',
      lines: [
        '<span class="t-info">[i]</span> .onion target detected · routing through Tor SOCKS5 proxy',
        '<span class="t-ok">[+]</span> HTTP 200 · title <span class="t-dim">"Leaked Data | victims list"</span>',
        '<span class="t-ok">[+]</span> screenshot captured through Tor',
        '<span class="t-ok">[+]</span> crawler: 30 linked resources fetched · 14 victim entries parsed',
        '<span class="t-ok">[+]</span> file fingerprinting: SHA-1 + MinHash on every published archive',
        '<span class="t-warn">[!]</span> feeds: matches a tracked <span class="t-warn">ransomware leak site</span>',
        '<span class="t-warn">[!]</span> EFI: TOX ID, BTC wallet and 3 mirror .onion domains extracted',
        '<span class="t-info">[i]</span> monitoring alert armed: new victim post triggers an e-mail'
      ],
      feeds: ['Ransomware tracker · active leak site', 'ThreatFox · related C2 infra'],
      iocs: ['TOX 56A1E6C3...', 'bc1qransom...', 'mirror2xk4.onion ×3'],
      verdict: { cls: 'warn', en: '◉ VERDICT: RANSOMWARE LEAK SITE · under monitoring', fr: '◉ VERDICT : SITE DE FUITE RANSOMWARE · sous surveillance' }
    },
    c2: {
      target: '203.0.113.42',
      lines: [
        '<span class="t-ok">[+]</span> BGP/ASN: AS64512 <span class="t-dim">"BulletHost LLC"</span> · prefix 203.0.113.0/24',
        '<span class="t-ok">[+]</span> GeoIP: NL · Amsterdam · hosting provider',
        '<span class="t-ok">[+]</span> HE.net: 12 PTR records in prefix · 4 sibling domains found',
        '<span class="t-ok">[+]</span> TLS on :443 · self-signed cert CN=srv01 · cert reused on 2 other IPs',
        '<span class="t-warn">[!]</span> feeds: <span class="t-warn">ThreatFox: Lumma Stealer C2</span> (2026-07-28)',
        '<span class="t-warn">[!]</span> correlation: shared certificate and ASN with cluster #7',
        '<span class="t-info">[i]</span> graph updated: 2 domains · 3 IPs · 1 ASN linked'
      ],
      feeds: ['ThreatFox · Lumma Stealer C2', 'Abuse feed · brute-force source'],
      iocs: ['cert CN=srv01 (reused ×3)', 'AS64512 cluster #7', 'panel path /login'],
      verdict: { cls: 'bad', en: '◉ VERDICT: ACTIVE C2 SERVER · cluster #7', fr: '◉ VERDICT : SERVEUR C2 ACTIF · cluster #7' }
    },
    generic: {
      lines: [
        '<span class="t-ok">[+]</span> DNS: resolved · A record found',
        '<span class="t-ok">[+]</span> WHOIS: registrar and creation date collected',
        '<span class="t-ok">[+]</span> HTTP chain traced · final status 200',
        '<span class="t-ok">[+]</span> CT logs: certificates indexed and queryable',
        '<span class="t-ok">[+]</span> BGP/ASN and GeoIP enrichment complete',
        '<span class="t-ok">[+]</span> screenshot captured · pHash computed',
        '<span class="t-info">[i]</span> feeds: no match in OpenPhish, URLhaus or ThreatFox',
        '<span class="t-info">[i]</span> EFI: 65 patterns executed · 1 low-confidence IOC'
      ],
      feeds: ['No feed match'],
      iocs: ['contact@ handle (low confidence)'],
      verdict: { cls: 'watch', en: '◉ VERDICT: NO KNOWN THREAT · kept queryable in store', fr: '◉ VERDICT : AUCUNE MENACE CONNUE · conservé dans le store' }
    }
  };

  var presets = consoleEl.querySelectorAll('.preset');
  var selectedKey = null;
  presets.forEach(function (btn) {
    btn.addEventListener('click', function () {
      presets.forEach(function (b) { b.classList.remove('sel'); });
      btn.classList.add('sel');
      selectedKey = btn.getAttribute('data-key');
      input.value = SCENARIOS[selectedKey].target;
      input.focus();
    });
  });
  input.addEventListener('input', function () {
    selectedKey = null;
    presets.forEach(function (b) { b.classList.remove('sel'); });
  });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') runScan(); });
  runBtn.addEventListener('click', runScan);

  var running = false;
  function runScan() {
    if (running) return;
    var raw = input.value.trim();
    if (!raw && !selectedKey) { input.focus(); return; }

    var key = selectedKey;
    if (!key) {
      key = 'generic';
      for (var k in SCENARIOS) {
        if (SCENARIOS[k].target && SCENARIOS[k].target === raw) key = k;
      }
    }
    var sc = SCENARIOS[key];
    var target = esc(raw || sc.target);
    var lang = document.documentElement.getAttribute('data-lang') === 'fr' ? 'fr' : 'en';

    running = true;
    runBtn.setAttribute('disabled', '');
    consoleEl.classList.add('scanning');
    stream.innerHTML = '';
    results.innerHTML = '<span class="res-title">' + (lang === 'fr' ? 'RÉSULTATS' : 'RESULTS') + '</span>';

    var queue = [];
    queue.push({ t: 'log', html: '<span class="t-prompt">hbg</span><span class="t-dim">://scan$</span> <span class="t-cmd">analyse ' + target + '</span>' });
    queue.push({ t: 'log', html: '<span class="t-dim">dispatching ' + MODULES.length + ' modules concurrently…</span>' });
    queue.push({ t: 'mods' });
    sc.lines.forEach(function (l) { queue.push({ t: 'log', html: l }); });
    queue.push({ t: 'feeds' });
    queue.push({ t: 'iocs' });
    queue.push({ t: 'log', html: '<span class="t-ok">[✓]</span> report ready · HTML + SVG graph + STIX 2.1 bundle' });
    queue.push({ t: 'verdict' });

    var modBoard = null;
    var i = 0;
    function step() {
      if (i >= queue.length) {
        running = false;
        runBtn.removeAttribute('disabled');
        consoleEl.classList.remove('scanning');
        return;
      }
      var item = queue[i++];
      if (item.t === 'log') {
        var el = document.createElement('span');
        el.className = 'ln';
        el.innerHTML = item.html;
        stream.appendChild(el);
        stream.scrollTop = stream.scrollHeight;
      } else if (item.t === 'mods') {
        modBoard = document.createElement('div');
        modBoard.className = 'mod-board';
        MODULES.forEach(function (m, idx) {
          var d = document.createElement('span');
          d.className = 'mod';
          d.innerHTML = m + ' <b>✓</b>';
          if (!reduced) d.style.animationDelay = (idx * 55) + 'ms';
          modBoard.appendChild(d);
        });
        results.appendChild(modBoard);
      } else if (item.t === 'feeds') {
        sc.feeds.forEach(function (f) {
          var d = document.createElement('div');
          d.className = 'feed-hit';
          d.textContent = '⚑ ' + f;
          results.appendChild(d);
        });
      } else if (item.t === 'iocs') {
        var box = document.createElement('div');
        box.className = 'ioc-chips';
        sc.iocs.forEach(function (c) {
          var d = document.createElement('span');
          d.className = 'ioc';
          d.textContent = c;
          box.appendChild(d);
        });
        results.appendChild(box);
      } else if (item.t === 'verdict') {
        var v = document.createElement('div');
        v.className = 'verdict ' + sc.verdict.cls;
        v.textContent = lang === 'fr' ? sc.verdict.fr : sc.verdict.en;
        results.appendChild(v);
      }
      setTimeout(step, reduced ? 0 : 200 + Math.random() * 240);
    }
    step();
  }
})();
