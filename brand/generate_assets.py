#!/usr/bin/env python3
"""
CoreTrust System Inc. — brand asset generator.

Builds the full logo kit from the existing raster icon + live vector text:
  - layouts:      icon / horizontal / vertical
  - backgrounds:  transparent / dark navy (#0f172a)
  - PNG:          multiple sizes per layout
  - Vector:       PDF + AI (PDF-compatible), wordmark = live editable text

Run:  /tmp/ctlogo-venv/bin/python brand/generate_assets.py
"""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
ICON_SRC = os.path.join(REPO, "images", "logo-icon.png")

# ---- brand constants ---------------------------------------------------------
AMBER       = (251, 191, 36)      # #fbbf24
NAVY_TEXT   = (15, 23, 42)        # #0f172a
WHITE       = (255, 255, 255)
DARK_BG     = (15, 23, 42)        # #0f172a
SUB_LIGHT   = (100, 116, 139)     # slate-500
SUB_DARK    = (148, 163, 184)     # slate-400

F_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
F_REG   = "/System/Library/Fonts/Supplemental/Arial.ttf"
assert os.path.exists(F_BLACK), F_BLACK
assert os.path.exists(F_REG), F_REG

# ---- icon master (tight-cropped, transparent) --------------------------------
_icon = Image.open(ICON_SRC).convert("RGBA")
_icon = _icon.crop(_icon.getbbox())
ICON_W, ICON_H = _icon.size  # ~207 x 252

def icon_at(height):
    w = round(ICON_W * height / ICON_H)
    return _icon.resize((w, height), Image.LANCZOS)

# ---- tracked text rendering --------------------------------------------------
def _tracked(draw_img, text, font, fill, tracking):
    """Return (advance_width). tracking in px added between glyphs (can be <0)."""
    x = 0
    d = ImageDraw.Draw(draw_img)
    for ch in text:
        d.text((x, 0), ch, font=font, fill=fill)
        bb = font.getbbox(ch)
        x += (bb[2] - bb[0]) + tracking
    return x

def _seg_width(text, font, tracking):
    x = 0
    for ch in text:
        bb = font.getbbox(ch)
        x += (bb[2] - bb[0]) + tracking
    return x

def wordmark(cap_px, core_color, trust_color, sub_color, with_sub=True):
    """Render 'CORETRUST' (+ optional 'SYSTEM INC.') -> tight RGBA image."""
    fsize = round(cap_px / 0.715)          # Arial Black cap height ≈ 0.715*em
    font  = ImageFont.truetype(F_BLACK, fsize)
    track = round(-fsize * 0.02)           # slightly tight
    asc, desc = font.getmetrics()
    line_h = asc + desc

    w_core  = _seg_width("CORE",  font, track)
    w_trust = _seg_width("TRUST", font, track)
    kern    = round(fsize * 0.0)           # gap between CORE|TRUST
    total_w = w_core + kern + w_trust

    sub_h = 0
    sub_font = None
    sub_track = 0
    sub_text = "SYSTEM INC."
    if with_sub:
        sub_size  = round(cap_px * 0.30)
        sub_font  = ImageFont.truetype(F_REG, sub_size)
        sub_track = round(sub_size * 0.42)
        sub_w     = _seg_width(sub_text, sub_font, sub_track)
        sa, sd    = sub_font.getmetrics()
        sub_h     = sa + sd
        gap_sub   = round(cap_px * 0.18)
        total_w   = max(total_w, sub_w)
    else:
        gap_sub = 0

    img = Image.new("RGBA", (total_w + 8, line_h + (gap_sub + sub_h if with_sub else 0) + 8), (0,0,0,0))
    # wordmark
    seg = Image.new("RGBA", (total_w + 8, line_h + 8), (0,0,0,0))
    d = ImageDraw.Draw(seg)
    x = 0
    for ch in "CORE":
        d.text((x, 0), ch, font=font, fill=core_color)
        bb = font.getbbox(ch); x += (bb[2]-bb[0]) + track
    x += kern
    for ch in "TRUST":
        d.text((x, 0), ch, font=font, fill=trust_color)
        bb = font.getbbox(ch); x += (bb[2]-bb[0]) + track
    img.paste(seg, (0, 0), seg)

    if with_sub:
        ss = Image.new("RGBA", (total_w + 8, sub_h + 8), (0,0,0,0))
        ds = ImageDraw.Draw(ss)
        xx = 0
        for ch in sub_text:
            ds.text((xx, 0), ch, font=sub_font, fill=sub_color)
            bb = sub_font.getbbox(ch); xx += (bb[2]-bb[0]) + sub_track
        img.paste(ss, (0, line_h + gap_sub), ss)

    return img.crop(img.getbbox())

# ---- composition -------------------------------------------------------------
def compose_horizontal(dark):
    core = WHITE if dark else NAVY_TEXT
    sub  = SUB_DARK if dark else SUB_LIGHT
    ih = 300
    icon = icon_at(ih)
    wm   = wordmark(cap_px=170, core_color=core, trust_color=AMBER, sub_color=sub)
    gap  = round(ih * 0.22)
    pad  = round(ih * 0.30)
    cw = pad + icon.width + gap + wm.width + pad
    ch = pad + max(icon.height, wm.height) + pad
    canvas = Image.new("RGBA", (cw, ch), (0,0,0,0))
    iy = (ch - icon.height)//2
    canvas.paste(icon, (pad, iy), icon)
    wy = (ch - wm.height)//2
    canvas.paste(wm, (pad + icon.width + gap, wy), wm)
    return _bg(canvas, dark)

def compose_vertical(dark):
    core = WHITE if dark else NAVY_TEXT
    sub  = SUB_DARK if dark else SUB_LIGHT
    ih = 340
    icon = icon_at(ih)
    wm   = wordmark(cap_px=150, core_color=core, trust_color=AMBER, sub_color=sub)
    gap  = round(ih * 0.16)
    pad  = round(ih * 0.26)
    cw = pad + max(icon.width, wm.width) + pad
    ch = pad + icon.height + gap + wm.height + pad
    canvas = Image.new("RGBA", (cw, ch), (0,0,0,0))
    canvas.paste(icon, ((cw-icon.width)//2, pad), icon)
    canvas.paste(wm, ((cw-wm.width)//2, pad + icon.height + gap), wm)
    return _bg(canvas, dark)

def compose_icon(dark, square_pad=0.14):
    icon = icon_at(420)
    side = round(max(icon.width, icon.height) * (1 + square_pad*2))
    canvas = Image.new("RGBA", (side, side), (0,0,0,0))
    canvas.paste(icon, ((side-icon.width)//2, (side-icon.height)//2), icon)
    return _bg(canvas, dark)

def _bg(rgba, dark):
    if not dark:
        return rgba
    base = Image.new("RGBA", rgba.size, DARK_BG + (255,))
    base.alpha_composite(rgba)
    return base

def save_widths(img, path_no_ext, widths):
    out = []
    for w in widths:
        h = round(img.height * w / img.width)
        im = img.resize((w, h), Image.LANCZOS)
        p = f"{path_no_ext}-{w}.png"
        im.save(p)
        out.append(p)
    return out

def save_sizes_sq(img, path_no_ext, sizes):
    out = []
    for s in sizes:
        im = img.resize((s, s), Image.LANCZOS)
        p = f"{path_no_ext}-{s}.png"
        im.save(p)
        out.append(p)
    return out

# ---- generate PNGs -----------------------------------------------------------
made = []
P = os.path.join(ROOT, "png")
for dark, tag in [(False, "transparent"), (True, "dark")]:
    made += save_sizes_sq(compose_icon(dark),
                          os.path.join(P, "icon", f"coretrust-icon-{tag}"), [64,128,256,512])
    made += save_widths(compose_horizontal(dark),
                        os.path.join(P, "horizontal", f"coretrust-horizontal-{tag}"), [400,800,1600])
    made += save_widths(compose_vertical(dark),
                        os.path.join(P, "vertical", f"coretrust-vertical-{tag}"), [400,800])

# ---- vector (PDF + AI) -------------------------------------------------------
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("ArialBlk", F_BLACK))
pdfmetrics.registerFont(TTFont("ArialReg", F_REG))

def _icon_reader(px_h):
    return ImageReader(icon_at(px_h))

def rgb01(c): return (c[0]/255, c[1]/255, c[2]/255)

def vector_horizontal(path, dark):
    core = WHITE if dark else NAVY_TEXT
    sub  = SUB_DARK if dark else SUB_LIGHT
    ih = 120.0
    iw = ICON_W * ih / ICON_H
    cap = 70.0
    fsize = cap/0.715
    track = -fsize*0.02
    pdfmetrics.registerFont(TTFont("ArialBlk", F_BLACK))
    def seg_w(t,fs,tr):
        return sum(pdfmetrics.stringWidth(ch,"ArialBlk",fs)+tr for ch in t)
    w_core = seg_w("CORE",fsize,track); w_trust = seg_w("TRUST",fsize,track)
    wm_w = w_core + w_trust
    sub_size = cap*0.30; sub_tr = sub_size*0.42
    sub_w = sum(pdfmetrics.stringWidth(ch,"ArialReg",sub_size)+sub_tr for ch in "SYSTEM INC.")
    block_w = max(wm_w, sub_w)
    gap = ih*0.22; pad = ih*0.30
    W = pad + iw + gap + block_w + pad
    H = pad + ih + pad
    c = pdfcanvas.Canvas(path, pagesize=(W,H))
    if dark:
        c.setFillColorRGB(*rgb01(DARK_BG)); c.rect(0,0,W,H,fill=1,stroke=0)
    c.drawImage(_icon_reader(round(ih*3)), pad, (H-ih)/2, iw, ih, mask='auto')
    # wordmark baseline
    tx = pad + iw + gap
    sub_gap = cap*0.18
    total_text_h = cap + sub_gap + sub_size
    ty = (H - total_text_h)/2 + sub_size + sub_gap   # baseline of wordmark
    def draw_seg(text, fs, tr, color, x, y):
        c.setFont("ArialBlk", fs); c.setFillColorRGB(*rgb01(color))
        for ch in text:
            c.drawString(x, y, ch); x += pdfmetrics.stringWidth(ch,"ArialBlk",fs)+tr
        return x
    xend = draw_seg("CORE", fsize, track, core, tx, ty)
    draw_seg("TRUST", fsize, track, AMBER, xend, ty)
    # subtitle below wordmark
    c.setFont("ArialReg", sub_size); c.setFillColorRGB(*rgb01(sub))
    sy = ty - sub_gap - sub_size
    sx = tx
    for ch in "SYSTEM INC.":
        c.drawString(sx, sy, ch); sx += pdfmetrics.stringWidth(ch,"ArialReg",sub_size)+sub_tr
    c.showPage(); c.save()

def vector_vertical(path, dark):
    core = WHITE if dark else NAVY_TEXT
    sub  = SUB_DARK if dark else SUB_LIGHT
    ih = 150.0
    iw = ICON_W * ih / ICON_H
    cap = 64.0; fsize = cap/0.715; track=-fsize*0.02
    def seg_w(t,fs,tr): return sum(pdfmetrics.stringWidth(ch,"ArialBlk",fs)+tr for ch in t)
    wm_w = seg_w("CORE",fsize,track)+seg_w("TRUST",fsize,track)
    sub_size=cap*0.30; sub_tr=sub_size*0.42
    sub_w = sum(pdfmetrics.stringWidth(ch,"ArialReg",sub_size)+sub_tr for ch in "SYSTEM INC.")
    block_w = max(iw, wm_w, sub_w)
    pad = ih*0.26; gap = ih*0.16; sub_gap=cap*0.20
    W = pad + block_w + pad
    H = pad + ih + gap + cap + sub_gap + sub_size + pad
    c = pdfcanvas.Canvas(path, pagesize=(W,H))
    if dark:
        c.setFillColorRGB(*rgb01(DARK_BG)); c.rect(0,0,W,H,fill=1,stroke=0)
    c.drawImage(_icon_reader(round(ih*3)), (W-iw)/2, H-pad-ih, iw, ih, mask='auto')
    ty = H - pad - ih - gap - cap
    x = (W - wm_w)/2
    c.setFont("ArialBlk", fsize)
    c.setFillColorRGB(*rgb01(core))
    for ch in "CORE":
        c.drawString(x,ty,ch); x += pdfmetrics.stringWidth(ch,"ArialBlk",fsize)+track
    c.setFillColorRGB(*rgb01(AMBER))
    for ch in "TRUST":
        c.drawString(x,ty,ch); x += pdfmetrics.stringWidth(ch,"ArialBlk",fsize)+track
    sy = ty - sub_gap - sub_size
    sx = (W - sub_w)/2
    c.setFont("ArialReg", sub_size); c.setFillColorRGB(*rgb01(sub))
    for ch in "SYSTEM INC.":
        c.drawString(sx,sy,ch); sx += pdfmetrics.stringWidth(ch,"ArialReg",sub_size)+sub_tr
    c.showPage(); c.save()

def vector_icon(path, dark):
    ih = 300.0; iw = ICON_W*ih/ICON_H
    padf = 0.14
    side = max(iw, ih)*(1+padf*2)
    c = pdfcanvas.Canvas(path, pagesize=(side, side))
    if dark:
        c.setFillColorRGB(*rgb01(DARK_BG)); c.rect(0,0,side,side,fill=1,stroke=0)
    c.drawImage(_icon_reader(round(ih*3)), (side-iw)/2, (side-ih)/2, iw, ih, mask='auto')
    c.showPage(); c.save()

V = os.path.join(ROOT, "vector")
vec_specs = [
    ("coretrust-icon",            lambda p: vector_icon(p, False)),
    ("coretrust-horizontal",      lambda p: vector_horizontal(p, False)),
    ("coretrust-horizontal-dark", lambda p: vector_horizontal(p, True)),
    ("coretrust-vertical",        lambda p: vector_vertical(p, False)),
]
for name, fn in vec_specs:
    pdf = os.path.join(V, name + ".pdf")
    fn(pdf)
    shutil.copyfile(pdf, os.path.join(V, name + ".ai"))   # AI = PDF-compatible
    made.append(pdf); made.append(os.path.join(V, name + ".ai"))

print(f"icon source content: {ICON_W}x{ICON_H}px")
print(f"generated {len(made)} files")
