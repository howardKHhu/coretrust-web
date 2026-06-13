# CLAUDE.md — CoreTrust Web

This file provides guidance for AI assistants working on this codebase.

---

## Project Overview

**CoreTrust System Inc.** is a cybersecurity and AI monitoring company. This repository is a static marketing website that showcases their products (Privileged Access Management and AI Tool Monitoring) and allows visitors to book a product demo.

---

## Repository Structure

```
coretrust-web/
├── index.html          # Entire website — all HTML, CSS (inline), and JS in one file
├── favicon.png         # Site favicon (PNG)
├── robots.txt          # SEO: crawler directives + sitemap pointer
├── sitemap.xml         # SEO: hreflang sitemap for zh-Hant / en / ja
└── images/
    ├── logo.png        # Full brand logo (used in OG/Twitter meta tags)
    ├── logo-icon.png   # Icon-only logo (transparent bg, used in <nav>)
    ├── pam.jpg         # Product image: Privileged Access Management
    ├── ai-monitor.jpg  # Product image: AI Tool Monitoring
    └── keep            # Placeholder to keep the images/ directory tracked by git
```

There is no build system, package manager, or backend. This is a **pure static site**.

---

## Technology Stack

| Concern     | Solution                                     |
|-------------|----------------------------------------------|
| Markup      | HTML5                                        |
| Styling     | Tailwind CSS (CDN: `cdn.tailwindcss.com`)    |
| Scripting   | Vanilla JavaScript (ES6+, inline in HTML)    |
| Forms       | Formspree (`https://formspree.io/f/xvzgkeww`) |
| i18n        | Custom `data-lang` attribute pattern         |
| State       | `localStorage` (language preference only)   |
| SEO         | Meta tags, Open Graph, Twitter Card, JSON-LD, sitemap.xml, robots.txt |

No npm, no Node.js, no bundler, no framework.

---

## Development Workflow

### Running locally

Open `index.html` directly in a browser, or serve it with any static file server:

```bash
# Python
python3 -m http.server 8080

# Node (npx)
npx serve .
```

### Making changes

All site content, styles, and logic live in `index.html`. Edit that file directly.

There are **no build steps** — changes are immediately reflected on reload.

### Committing and pushing

Branch convention: feature branches follow the `claude/<description>` pattern.

```bash
git add index.html              # or specific files
git commit -m "Descriptive message"
git push -u origin <branch-name>
```

---

## Codebase Conventions

### i18n (Multi-language support)

The site supports three languages:

| Code | Language             |
|------|----------------------|
| `zh` | Traditional Chinese  |
| `en` | English              |
| `ja` | Japanese             |

**Pattern:** Any element that should vary by language uses `data-lang="<code>"` as an attribute. All such elements are hidden by default (`[data-lang] { display: none; }`). The `changeLang()` function shows only elements matching the active language.

```html
<!-- Example: text that changes per language -->
<span data-lang="zh">繁體中文內容</span>
<span data-lang="en">English content</span>
<span data-lang="ja">日本語コンテンツ</span>
```

- The active language is persisted in `localStorage` under the key `preferredLang`.
- On page load, the script reads `preferredLang`, falling back to browser language detection (`navigator.language`), then to `'en'`.
- `changeLang()` also updates `document.documentElement.lang` and `document.title` using the `LANG_META` map (helps SEO and accessibility):

```js
const LANG_META = {
    zh: { htmlLang: 'zh-Hant', title: '...' },
    en: { htmlLang: 'en',      title: '...' },
    ja: { htmlLang: 'ja',      title: '...' }
};
```

- Display type: `<span>` and `<option>` elements use `display: inline`; all others use `display: block`.

### Styling

- **Tailwind CSS utility classes** are used for most layout/spacing/typography.
- Custom global CSS lives in a `<style>` block in `<head>`:
  - `.hero-bg` — dark blue radial gradient header background
  - `.warm-accent` — amber (#fbbf24) text colour for brand accents
  - `.warm-bg` — amber (#fbbf24) background
  - `.warm-btn` — amber CTA button with hover lift effect
  - `.lang-active-btn` — amber highlight for the active language button

- Primary brand colour: **amber (#fbbf24 / Tailwind `amber-500`)**
- Dark background colour: **slate-800 / #0f172a**
- Responsive breakpoint used: `md:` (768 px) from Tailwind defaults

### Navigation Logo

The `<nav>` uses a two-part logo:
1. `<img src="images/logo-icon.png">` — transparent icon (height `h-8 md:h-10`)
2. A text wordmark: `CORE<span class="text-amber-500">TRUST</span>`

Do not replace the `<img>` with a different asset without also updating the `og:image` and `twitter:image` meta tags (which reference `images/logo.png`).

### Animations

Scroll-triggered entrance animations are implemented with the **Intersection Observer API**. Product cards (`.product-card`) start as `opacity-0 translate-y-8` and transition to `opacity-100 translate-y-0` when they enter the viewport. No animation library is used.

### Product Cards — Expandable Detail

The **AI Tool Monitoring** card includes an expandable detail section:

- Toggle button `id="ai-toggle-btn"` calls `toggleAiDetail()`
- Detail panel `id="ai-detail"` uses `max-height` CSS transition (`0` ↔ `scrollHeight`) for smooth open/close
- Arrow icon `id="ai-toggle-icon"` rotates 180° when open
- State is tracked via the `aiDetailOpen` boolean
- **The PAM card does not have an expandable section.** Add one following the same pattern if needed.

Card order (left → right on desktop): AI Tool Monitoring, then Privileged Access Management.

### Form

The contact/demo form (section id `#demo`) POSTs to Formspree. The form ID is `xvzgkeww`. No client-side form validation library is used — only native HTML `required` attributes.

### SEO Files

- `robots.txt` — allows all crawlers and points to `https://coretrustsystem.com/sitemap.xml`
- `sitemap.xml` — single URL entry with `hreflang` alternates for `zh-Hant`, `en`, `ja`, and `x-default`; update `<lastmod>` when making significant content changes

---

## Page Sections (in order)

1. **`<nav>`** — Sticky top bar with logo image + wordmark, language switcher, and "Demo" CTA
2. **`<header>` (hero)** — Headline, sub-headline, and "Products" anchor CTA
3. **`#products`** — Two product cards: AI Tool Monitoring (left) and PAM (right); AI card has expandable detail
4. **`#advantages`** — 4-column grid of key differentiators (AI Analysis, Modular Deployment, Intuitive UI, Hybrid Cloud)
5. **`#about`** — Company background blurb
6. **`#demo`** — Contact/demo booking form (Formspree)
7. **`<footer>`** — Copyright and tagline

---

## Key Constraints

- **No npm / no build step** — do not introduce package.json, webpack, vite, or similar tooling unless explicitly requested.
- **No external JS libraries** — all interactivity is vanilla JS; keep it that way unless asked otherwise.
- **Single-file architecture** — all HTML, CSS, and JS remain in `index.html`; do not split into separate files unless explicitly requested.
- **CDN Tailwind only** — the project uses the Tailwind CDN play script, not a PostCSS build; custom Tailwind config can be added via the inline `tailwind.config` object if needed.
- **Images stay in `/images`** — any new image assets should be placed in the `images/` directory.

---

## No Tests, No CI

There is currently no test suite, no linting configuration, and no CI/CD pipeline. Manual browser testing is the current workflow.
