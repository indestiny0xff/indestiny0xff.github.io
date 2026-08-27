"""Regenerate favicon.ico from the red spider lily design in assets/favicon.svg.

The .ico must always match the .svg: this script redraws the same shapes
(same 64-unit coordinates) with PIL at high resolution, then saves a
multi-size icon (16/32/48/64) at the repo root. Run from the repo root:

    python scripts/gen_favicon.py
"""

import math

from PIL import Image, ImageDraw

BASE = 64          # design space of assets/favicon.svg
S = 512            # master render size
F = S / BASE

BG_TOP = (0x15, 0x0A, 0x2E)
BG_BOT = (0x03, 0x05, 0x0A)
PETAL = (0xBE, 0x12, 0x3C, 255)
PETAL_GLOW = (0xFB, 0x71, 0x85, 255)
STAMEN = (0xFD, 0xA4, 0xAF, 255)
ANTHER = (0xFE, 0xCD, 0xD3, 255)
STEM = (0x9F, 0x12, 0x39, 255)
CORE = (0x88, 0x13, 0x37, 255)

C = (32.0, 32.0)   # flower center


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


def quad(p0, p1, p2, n=32):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((
            u**2 * p0[0] + 2 * u * t * p1[0] + t**2 * p2[0],
            u**2 * p0[1] + 2 * u * t * p1[1] + t**2 * p2[1],
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


def px(pts):
    return [(x * F, y * F) for x, y in pts]


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
d = ImageDraw.Draw(img)

# Stem
d.line(px(cubic((32, 33), (31, 42), (33, 50), (32, 58))), fill=STEM, width=round(2.2 * F), joint="curve")

# Stamens with anthers (behind the petals)
stamen = quad((32, 32), (27, 17), (18, 5))
for ang in (-52, -26, 0, 26, 52):
    pts = rot(stamen, ang)
    d.line(px(pts), fill=STAMEN, width=round(1.1 * F), joint="curve")
    tx, ty = pts[-1]
    r = 1.3
    d.ellipse([(tx - r) * F, (ty - r) * F, (tx + r) * F, (ty + r) * F], fill=ANTHER)

# Petals: fan of six, outer tone with a lighter inner glow
petal = (
    cubic((32, 33), (28.5, 26), (27, 15), (31, 8))
    + cubic((31, 8), (34.5, 14), (35.5, 25), (32, 33))[1:]
)
for ang in (-80, -48, -16, 16, 48, 80):
    poly = px(rot(petal, ang))
    d.polygon(poly, fill=PETAL)
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    d.polygon([(cx + (x - cx) * 0.55, cy + (y - cy) * 0.55) for x, y in poly], fill=PETAL_GLOW)

# Flower core
r = 2
d.ellipse([(32 - r) * F, (32 - r) * F, (32 + r) * F, (32 + r) * F], fill=CORE)

img.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("favicon.ico written")
