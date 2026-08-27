"""Regenerate favicon.ico from the red spider lily design in assets/favicon.svg.

The .ico must always match the .svg: this script redraws the same shapes
(same 64-unit coordinates) with PIL at high resolution, then saves a
multi-size icon (16/32/48/64) at the repo root. Run from the repo root:

    python scripts/gen_favicon.py
"""

import math

from PIL import Image, ImageDraw, ImageFilter

BASE = 64          # design space of assets/favicon.svg
S = 512            # master render size
F = S / BASE

BG_TOP = (0x15, 0x0A, 0x2E)
BG_BOT = (0x03, 0x05, 0x0A)
HALO = (0xE1, 0x1D, 0x48)
OUTER_BASE = (0x88, 0x13, 0x37)
OUTER_MID = (0xBE, 0x12, 0x3C)
OUTER_TIP = (0xF4, 0x3F, 0x5E)
INNER_BASE = (0xBE, 0x12, 0x3C)
INNER_MID = (0xE1, 0x1D, 0x48)
INNER_TIP = (0xFD, 0xA4, 0xAF)
STAMEN = (0xFE, 0xCD, 0xD3, 255)
ANTHER = (0xFF, 0xF1, 0xF2, 255)
STEM = (0x9F, 0x12, 0x39, 255)
CORE = (0xFE, 0xCD, 0xD3, 255)

C = (32.0, 32.0)   # flower center
PB = (32.0, 33.0)  # petal base


def cubic(p0, p1, p2, p3, n=48):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((
            u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1],
        ))
    return pts


def rot(pts, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [
        (C[0] + (x - C[0]) * ca - (y - C[1]) * sa,
         C[1] + (x - C[0]) * sa + (y - C[1]) * ca)
        for x, y in pts
    ]


def scale_about(pts, f, o):
    return [(o[0] + (x - o[0]) * f, o[1] + (y - o[1]) * f) for x, y in pts]


def px(pts):
    return [(x * F, y * F) for x, y in pts]


def draw_petal(d, poly, base_c, mid_c, tip_c):
    """Approximate the base-to-tip gradient with three nested tones."""
    d.polygon(poly, fill=base_c)
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    d.polygon([(cx + (x - cx) * 0.8, cy + (y - cy) * 0.8) for x, y in poly], fill=mid_c)
    # tip highlight: shrink toward a point 70% of the way to the tip
    tip = min(poly, key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2 * 0)  # placeholder
    tip = poly[len(poly) // 2]
    tx, ty = cx + (tip[0] - cx) * 0.7, cy + (tip[1] - cy) * 0.7
    d.polygon([(tx + (x - tx) * 0.45, ty + (y - ty) * 0.45) for x, y in poly], fill=tip_c)


# Background: rounded tile with a vertical approximation of the diagonal gradient
grad = Image.new("RGBA", (S, S))
gd = ImageDraw.Draw(grad)
for y in range(S):
    t = y / (S - 1)
    col = tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT)) + (255,)
    gd.line([(0, y), (S, y)], fill=col)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=round(14 * F), fill=255)
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
img.paste(grad, (0, 0), mask)

# Soft red halo behind the flower
halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
hd.ellipse([(32 - 19) * F, (29 - 19) * F, (32 + 19) * F, (29 + 19) * F], fill=HALO + (95,))
halo = halo.filter(ImageFilter.GaussianBlur(40))
img.alpha_composite(halo)
img = Image.composite(img, Image.new("RGBA", (S, S), (0, 0, 0, 0)), mask)
d = ImageDraw.Draw(img)

# Stem
d.line(px(cubic((32, 33), (30, 40), (34, 49), (32, 58))), fill=STEM, width=round(2 * F), joint="curve")

# Stamens: long arcs with glowing anthers (behind the petals)
stamen = cubic((32, 32), (30.5, 24), (29, 14), (31, 4))
for ang in (-64, -32, 0, 32, 64):
    pts = rot(stamen, ang)
    d.line(px(pts), fill=STAMEN, width=round(0.9 * F), joint="curve")
    tx, ty = pts[-1]
    r = 1.2
    d.ellipse([(tx - r) * F, (ty - r) * F, (tx + r) * F, (ty + r) * F], fill=ANTHER)

# Petals: curved, swirling; outer fan of six, inner brighter fan of five
petal = (
    cubic((32, 33), (27.5, 27), (26, 16.5), (29.5, 8))
    + cubic((29.5, 8), (30.6, 5.2), (33.4, 5.2), (32.6, 8.6))[1:]
    + cubic((32.6, 8.6), (31.6, 14.5), (31.6, 25), (32, 33))[1:]
)
for ang in (-80, -48, -16, 16, 48, 80):
    draw_petal(d, px(rot(petal, ang)), OUTER_BASE, OUTER_MID, OUTER_TIP)
inner = scale_about(petal, 0.62, PB)
for ang in (-64, -32, 0, 32, 64):
    draw_petal(d, px(rot(inner, ang)), INNER_BASE, INNER_MID, INNER_TIP)

# Flower core
r = 1.7
d.ellipse([(32 - r) * F, (32 - r) * F, (32 + r) * F, (32 + r) * F], fill=CORE)

img.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("favicon.ico written")
