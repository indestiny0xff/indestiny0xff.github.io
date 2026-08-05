# indestiny0xff.github.io — CLAUDE.md

## What this is

Bilingual (EN/FR) portfolio + research blog hosted on **GitHub Pages** (Jekyll, no external theme — all layouts are custom). Two parts:

- `/` — portfolio showcase ("vitrine") selling the owner's profile to employers: hero with animated terminal, about, **HuntingBadGuys flagship section**, experience timeline, projects, skills, education, publications, contact.
- `/blog/` — research blog (posts in `_posts/`, layout `post`).

## PRIVACY RULES — NON-NEGOTIABLE

Never introduce any of the following anywhere on the site:

- **Full last name** — use only "othmaneb" / "Othmane B."
- **Phone number** — never.
- **Personal email** — the ONLY contact email allowed is `ada.moonstone746@passmail.com`.
- **LinkedIn profile / article URLs** — they contain the full name in the slug. Do not link them.
- **Photos** — none.
- CV PDFs must never be committed to this repo.

Public handles that ARE allowed: GitHub `indestiny0xff`, X/Twitter `indestiny_cti`, `huntingbadguys.online`.

## Architecture

```
_config.yml            — Jekyll config (no theme; jekyll-feed, jekyll-sitemap, jemoji)
_layouts/default.html  — shell: nav, EN/FR switch, dark/light toggle, footer
_layouts/post.html     — blog article (loads local highlight.js: powershell, plaintext, tsql)
index.html             — the whole portfolio one-pager (bilingual)
blog/index.html        — post list
404.html               — themed 404
assets/css/main.css    — entire design system
assets/js/main.js      — theme/lang persistence (localStorage), mobile nav, reveal-on-scroll, hero terminal typing
_posts/                — blog posts (markdown, front matter: layout post, title, tags)
js/highlightjs/        — vendored highlight.js core + 3 language packs
```

## Conventions

- **i18n**: duplicated content blocks with classes `.lang-en` / `.lang-fr`; CSS hides the inactive one via `html[data-lang]`. Every user-visible string must exist in both languages. Default is EN; choice persisted in `localStorage.lang`.
- **Themes**: `html[data-theme="dark"]` (default) = black/purple, matching HuntingBadGuys (`#03050a` bg, `#7c3aed`/`#a855f7` accents). `light` = cream (`#f5f0e8` bg, `#6d28d9` accent). All colors via CSS variables in `main.css` — never hardcode colors in HTML except via `var(--*)`.
- Fonts: Inter (UI) + JetBrains Mono (accents/code), loaded from Google Fonts in `default.html`.
- Code blocks in posts stay dark in BOTH themes (`--code-bg`); hljs colors are overridden at the bottom of `main.css`.
- New blog post: `_posts/YYYY-MM-DD-Title.md` with front matter `layout: post`, `title`, `tags: [..]`.

## HuntingBadGuys facts used on the site

Source of truth: local repo `C:\Users\othma\Desktop\Code\HuntingBadGuys` (do NOT scrape huntingbadguys.online — the owner does not allow scraping). Key numbers shown: 16+ collection modules, 65 IOC regex patterns, 10 categories, STIX 2.1 export. Links point to `/demo`, `/features`, `/public`.

## Deploy

Push to `main` → GitHub Pages builds automatically. No local build required; if testing locally: `bundle exec jekyll serve` (needs github-pages gem).
