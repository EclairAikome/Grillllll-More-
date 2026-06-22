#!/usr/bin/env python3
"""
render_post.py — house-style Instagram post renderer (Ajinomoto dry food).

Deterministic Pillow engine. Reads ONE post spec (JSON) and writes a PORTRAIT PNG.
Canvas is ALWAYS 4:5 portrait (Instagram feed): 1080x1350 web / 4320x5400 print.
Guarantees the fixed brand "frame" + bundled fonts across every post, while the spec
controls the variety (background, watermark, layout archetype, packshot placement,
headline, photo placeholders).

  python render_post.py <spec.json> [--w 1080] [--out output/foo.png]

Coordinate convention: every box is [x, y, w, h] in FRACTIONS, where x & w are fractions
of canvas WIDTH and y & h are fractions of canvas HEIGHT. Text positions "at":[fx,fy] are
likewise (width-fraction, height-fraction). Font sizes are fractions of canvas WIDTH.

*** MANDATORY, NON-OVERRIDABLE BRAND RULE ***
The Ajinomoto "Eat Well, Live Well." + Aj + AJINOMOTO lockup is locked to a fixed top-right
box on EVERY post (see LOGO_BOX). Measured from the user's reference creative. A spec cannot
move or resize it. Supply the real lockup PNG at assets/brand/eat-well-aji.png; until then a
typographic stand-in is drawn in the exact same locked box.
"""
import argparse, json, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
FONTS = os.path.join(SKILL, "assets", "fonts")

FONT_FILES = {
    "brush":     os.path.join(FONTS, "UID Deep sea.ttf"),
    "condensed": os.path.join(FONTS, "DINCondensed-VF.ttf"),
    "body":      os.path.join(FONTS, "MyriadPro-Regular.otf"),
}

# Canvas: 4:5 portrait, always.
ASPECT_W, ASPECT_H = 4, 5

# --- LOCKED Ajinomoto logo lockup placement (fractions of canvas) --------------
# Measured from the reference Seri-Aji creative (1080x1350): lockup ~230x150 px,
# right edge ~60 px from the right, top ~63 px from the top.
# Anchored TOP-RIGHT. Width is locked; height follows the artwork's own aspect.
# THIS IS A HARD REQUIREMENT — render_furniture ignores any spec override.
LOGO_BOX = {
    "width":        0.213,  # fraction of canvas WIDTH
    "right_margin": 0.055,  # fraction of canvas WIDTH (gap from right edge)
    "top_margin":   0.047,  # fraction of canvas HEIGHT (gap from top edge)
    "fallback_aspect": 230.0 / 150.0,  # w:h used only by the typographic stand-in
}

# ---------- helpers ----------------------------------------------------------

def hex2rgb(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

def shade(rgb, f):
    r, g, b = rgb[:3]
    c = lambda v: max(0, min(255, int(v * f)))
    out = (c(r), c(g), c(b))
    return out + (rgb[3],) if len(rgb) == 4 else out

def font(kind, px):
    return ImageFont.truetype(FONT_FILES[kind], max(1, int(px)))

def tsize(draw, s, fnt, stroke=0):
    b = draw.textbbox((0, 0), s, font=fnt, stroke_width=stroke)
    return b[2] - b[0], b[3] - b[1]

def _abs(p):
    if not p: return p
    return p if os.path.isabs(p) else os.path.join(SKILL, p)

def _load(path):
    p = _abs(path)
    if p and os.path.exists(p):
        try: return Image.open(p).convert("RGBA")
        except Exception: return None
    return None

def _fit(im, bw, bh):
    s = min(bw / im.width, bh / im.height)
    return im.resize((max(1, int(im.width*s)), max(1, int(im.height*s))), Image.LANCZOS)

# px helpers: x,w scale by W ; y,h scale by H
def PX(box, W, H):
    x, y, w, h = box
    return int(x*W), int(y*H), int(w*W), int(h*H)

# ---------- layers -----------------------------------------------------------

def draw_background(img, spec, W, H):
    img.paste(hex2rgb(spec.get("bg", "#D02329"))[:3], (0, 0, W, H))

def draw_pattern(img, spec, W, H):
    pat = spec.get("pattern", {}); kind = pat.get("kind", "none")
    base = hex2rgb(spec.get("bg", "#D02329"))
    tone = shade(base, pat.get("contrast", 1.12))[:3]
    ov = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(ov)
    if kind == "dots":
        step = int(W * pat.get("step", 0.13)); r = int(step*0.30)
        for y in range(step//2, H, step):
            for x in range(step//2, W, step):
                d.ellipse([x-r,y-r,x+r,y+r], fill=tone+(255,))
    elif kind == "diagonal":
        dk = shade(base, 0.86)[:3]; m = int(W * pat.get("margin", 0.30))
        d.polygon([(0,0),(m,0),(0,m)], fill=dk+(255,))
        d.polygon([(W,H),(W-m,H),(W,H-m)], fill=dk+(255,))
    elif kind == "ground":
        gc = hex2rgb(pat.get("color", "#F4D21E")); h = int(H * pat.get("height", 0.32))
        d.rectangle([0, H-h, W, H], fill=gc)
    elif kind == "glyphs":
        g = pat.get("glyph", "Aji"); step = int(W * pat.get("step", 0.18))
        f = font("brush", step*0.42)
        gly = Image.new("RGBA", (step*2, step*2), (0,0,0,0))
        ImageDraw.Draw(gly).text((step,step), g, font=f, fill=tone+(255,), anchor="mm")
        gly = gly.rotate(18, expand=False)
        for j, y in enumerate(range(0, H, step)):
            xoff = (step//2) if j % 2 else 0
            for x in range(-step, W, step):
                ov.alpha_composite(gly, (x+xoff-step, y-step))
    img.alpha_composite(ov)

def place_image(img, W, H, el):
    x, y, w, h = PX(el["box"], W, H)
    im = None if el.get("placeholder", False) else _load(el.get("file"))
    if im is not None:
        im = _fit(im, w, h)
        px = x + (w-im.width)//2; py = y + (h-im.height)//2
        if el.get("shadow", True):
            sh = Image.new("RGBA", (W,H), (0,0,0,0))
            blob = Image.new("RGBA", im.size, (0,0,0,120))
            sh.paste(blob, (px+int(W*0.008), py+int(H*0.011)), im.split()[-1])
            img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(int(W*0.012))))
        img.alpha_composite(im, (px, py))
    else:
        draw_placeholder(img, W, H, (x,y,w,h), el.get("label","PHOTO"))

def draw_placeholder(img, W, H, xywh, label):
    x, y, w, h = xywh
    ov = Image.new("RGBA", (W,H), (0,0,0,0)); d = ImageDraw.Draw(ov)
    d.rectangle([x,y,x+w,y+h], fill=(255,255,255,38))
    dash = int(W*0.012); gap = int(dash*0.7); col=(255,255,255,225); wd=max(2,int(W*0.003))
    def dl(x0,y0,x1,y1):
        ln = math.hypot(x1-x0,y1-y0); n = max(1,int(ln//(dash+gap)))
        for i in range(n):
            t0=i*(dash+gap)/ln; t1=min(1,(i*(dash+gap)+dash)/ln)
            d.line([x0+(x1-x0)*t0,y0+(y1-y0)*t0,x0+(x1-x0)*t1,y0+(y1-y0)*t1], fill=col, width=wd)
    dl(x,y,x+w,y); dl(x+w,y,x+w,y+h); dl(x+w,y+h,x,y+h); dl(x,y+h,x,y)
    f = font("condensed", W*0.022)
    lines=[]; cur=""
    for word in label.split():
        t=(cur+" "+word).strip()
        if tsize(d,t,f)[0] > w*0.86 and cur: lines.append(cur); cur=word
        else: cur=t
    lines.append(cur)
    lh = tsize(d,"Ag",f)[1]*1.25; ty = y+h/2-lh*len(lines)/2
    for ln in lines:
        tw = tsize(d,ln,f)[0]; d.text((x+w/2-tw/2, ty), ln, font=f, fill=col); ty+=lh
    img.alpha_composite(ov)

def draw_highlight(img, W, H, el):
    x,y,w,h = PX(el["box"], W, H)
    ov = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    r = int(min(w,h)*el.get("radius",0.35))
    d.rounded_rectangle([x,y,x+w,y+h], radius=r, fill=hex2rgb(el.get("color","#5FD0E0")))
    if el.get("rotate"): ov = ov.rotate(el["rotate"], center=(x+w/2,y+h/2), expand=False)
    img.alpha_composite(ov)

def draw_text(img, W, H, t):
    kind = t.get("font","brush"); cap = int(t["size"]*W); f = font(kind, cap)
    s = t["text"].upper() if t.get("upper", kind=="brush" and t.get("role")=="headline") else t["text"]
    fill = hex2rgb(t.get("color","#FFFFFF"))
    stroke = int(cap*t.get("stroke",0.04)); sfill = hex2rgb(t.get("stroke_color","#3A1A12"))
    cx, cy = t["at"][0]*W, t["at"][1]*H
    ov = Image.new("RGBA",(W,H),(0,0,0,0)); d = ImageDraw.Draw(ov)
    maxw = t.get("maxw",0.84)*W; lines=[]; cur=""
    for word in s.split():
        tt=(cur+" "+word).strip()
        if tsize(d,tt,f,stroke)[0] > maxw and cur: lines.append(cur); cur=word
        else: cur=tt
    if cur: lines.append(cur)
    lh = tsize(d,"Ag",f,stroke)[1]*t.get("leading",1.18); ty = cy-lh*len(lines)/2
    for ln in lines:
        tw = tsize(d,ln,f,stroke)[0]
        d.text((cx-tw/2,ty), ln, font=f, fill=fill, stroke_width=stroke,
               stroke_fill=sfill, anchor="la"); ty+=lh
    if t.get("rotate"): ov = ov.rotate(t["rotate"], center=(cx,cy), expand=False)
    if t.get("shadow", True):
        img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(int(cap*0.03))))
    img.alpha_composite(ov)

def draw_locked_logo(img, W, H, spec):
    """MANDATORY top-right Ajinomoto lockup at the locked box. Not spec-overridable."""
    lw = int(LOGO_BOX["width"]*W)
    rm = int(LOGO_BOX["right_margin"]*W)
    tm = int(LOGO_BOX["top_margin"]*H)
    x = W - rm - lw; y = tm
    asset = spec.get("furniture", {}).get("top_right", {}).get("file") or "assets/brand/eat-well-aji.png"
    im = _load(asset)
    if im is not None:
        s = lw / im.width
        im = im.resize((lw, max(1, int(im.height*s))), Image.LANCZOS)
        img.alpha_composite(im, (x, y))
    else:
        # Typographic stand-in on a white plaque so the LOCKED box is always visible,
        # regardless of background colour. (Real PNG replaces this entirely.)
        lh = int(lw / LOGO_BOX["fallback_aspect"])
        ov = Image.new("RGBA",(W,H),(0,0,0,0)); d = ImageDraw.Draw(ov)
        pad = int(lw*0.05)
        d.rounded_rectangle([x-pad, y-pad, x+lw+pad, y+lh+pad],
                            radius=int(lw*0.06), fill=(255,255,255,235))
        f1 = font("brush", lh*0.20); f2 = font("brush", lh*0.42)
        t1 = "Eat Well, Live Well."; w1 = tsize(d,t1,f1)[0]
        d.text((x+lw-w1, y), t1, font=f1, fill=hex2rgb("#E20A17"))
        t2 = "AJINOMOTO"; w2 = tsize(d,t2,f2)[0]
        d.text((x+lw-w2, y+lh*0.42), t2, font=f2, fill=hex2rgb("#E20A17"))
        img.alpha_composite(ov)

def draw_other_furniture(img, W, H, spec):
    fr = spec.get("furniture", {}); M = int(W*0.055)
    tl = fr.get("top_left")
    if tl and _load(tl.get("file")):
        im = _fit(_load(tl["file"]), int(W*0.30), int(H*0.11)); img.alpha_composite(im,(M,int(H*0.045)))
    elif tl and tl.get("text"):
        ov = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); f=font("brush", W*0.045)
        d.text((M,int(H*0.045)), tl["text"], font=f, fill=hex2rgb(tl.get("color","#FFFFFF")),
               stroke_width=int(W*0.0025), stroke_fill=hex2rgb("#333333"))
        img.alpha_composite(ov)
    bl = fr.get("bottom_left")
    if bl and _load(bl.get("file")):
        im = _fit(_load(bl["file"]), int(W*0.18), int(H*0.07)); img.alpha_composite(im,(M, H-int(H*0.045)-im.height))

# ---------- main -------------------------------------------------------------

def render(spec, W, H):
    img = Image.new("RGBA", (W, H), (255,255,255,255))
    draw_background(img, spec, W, H)
    draw_pattern(img, spec, W, H)
    for el in spec.get("elements", []):
        ty = el.get("type")
        if ty == "image":      place_image(img, W, H, el)
        elif ty == "highlight": draw_highlight(img, W, H, el)
        elif ty == "text":      draw_text(img, W, H, el)
    draw_other_furniture(img, W, H, spec)
    draw_locked_logo(img, W, H, spec)   # LAST + LOCKED, always on top
    return img.convert("RGB")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--w", type=int, default=1080, help="canvas width; height = width*5/4")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    W = a.w; H = a.w * ASPECT_H // ASPECT_W
    spec = json.load(open(a.spec, encoding="utf-8"))
    img = render(spec, W, H)
    out = a.out or os.path.join(SKILL, "output",
            os.path.splitext(os.path.basename(a.spec))[0] + f"_{W}x{H}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, quality=95)
    print(f"wrote {out}  ({W}x{H})")

if __name__ == "__main__":
    main()
