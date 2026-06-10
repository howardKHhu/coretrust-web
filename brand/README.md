# CoreTrust System Inc. — Brand Assets

Logo kit for CoreTrust System Inc., generated from the master logo.
Three layouts × two backgrounds, in PNG (multiple sizes) and vector (PDF + AI).

## Folder layout

```
brand/
├── png/
│   ├── icon/         coretrust-icon-{transparent|dark}-{64,128,256,512}.png
│   ├── horizontal/   coretrust-horizontal-{transparent|dark}-{400,800,1600}.png
│   └── vertical/     coretrust-vertical-{transparent|dark}-{400,800}.png
├── vector/
│   ├── coretrust-icon.pdf / .ai
│   ├── coretrust-horizontal.pdf / .ai
│   ├── coretrust-horizontal-dark.pdf / .ai
│   └── coretrust-vertical.pdf / .ai
├── generate_assets.py   # reproducible generator
└── README.md
```

## Layouts

| Layout | Description | Best for |
|--------|-------------|----------|
| **icon** | Gold hexagonal mark only, square | favicon, app icon, avatar, social profile |
| **horizontal** | Icon + `CORETRUST` + `SYSTEM INC.` side by side | website header, email signature, letterhead |
| **vertical** | Icon stacked above wordmark | business cards, posters, square placements |

## Backgrounds

- **transparent** — for placing on white / light surfaces (wordmark `CORE` is navy `#0f172a`).
- **dark** — solid navy `#0f172a` background baked in (wordmark `CORE` is white).
  In both, `TRUST` is brand amber `#fbbf24`.

## Brand colors

| Token | Hex | Use |
|-------|-----|-----|
| Amber (accent) | `#fbbf24` | `TRUST`, highlights |
| Navy (primary) | `#0f172a` | `CORE` on light, dark backgrounds |
| White | `#ffffff` | `CORE` on dark |
| Slate (subtitle) | `#64748b` / `#94a3b8` | `SYSTEM INC.` on light / dark |

Wordmark typeface: **Arial Black** (heavy geometric sans, matches the website's
`font-black tracking-tighter` style and is available across platforms).

## Vector files (PDF / AI)

- The `.ai` files are **PDF-compatible** — open and edit them directly in Adobe
  Illustrator (or any PDF-capable vector editor). They are identical to the `.pdf`.
- The **wordmark is live, editable vector text** (Arial Black embedded), so it stays
  razor-sharp at any size and can be recolored or re-typed.
- The **icon is an embedded raster** image (see resolution note below), not vector —
  the original mark was supplied as raster artwork.

## ⚠️ Icon resolution note

The source icon artwork is raster at ~207×252px. As a result:

- PNG icon up to **256px** and all lockups up to **800px** wide are crisp.
- Icon **512px** and horizontal **1600px** involve mild upscaling of the icon
  (text remains perfectly crisp).
- For large-format print, re-export the icon from the original Canva design at higher
  resolution, drop it into `images/logo-icon.png`, and re-run `generate_assets.py`.

## Regenerating

```bash
python3 -m venv .venv && .venv/bin/pip install Pillow reportlab
.venv/bin/python brand/generate_assets.py
```
