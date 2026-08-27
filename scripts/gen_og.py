"""Generate assets/og.png, the 1200x630 social share image.

Brand: dark background with a faint grid, terminal-style title
(othmaneb@cti:~$), dim subtitle, purple corner targeting brackets, and
the butterfly from the favicon on the right. Run from the repo root:

    python scripts/gen_og.py
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
BG_TOP = (0x0B, 0x07, 0x1C)
BG_BOT = (0x03, 0x05, 0x0A)
GRID = (0x18, 0x24, 0x3A)
TEXT = (0xE4, 0xEC, 0xF8)
DIM = (0x84, 0x97, 0xB0)
ACCENT = (0xA8, 0x55, 0xF7)
ACCENT_DK = (0x7C, 0x3A, 0xED)
GLOW_IN = (0xC0, 0x84, 0xFC, 255)
CYAN = (0x67, 0xE8, 0xF9, 255)
BODY = (0xC4, 0xB5, 0xFD, 255)

FONTS = r"C:\Windows\Fonts"
title_f = ImageFont.truetype(FONTS + r"\consolab.ttf", 84)
sub_f = ImageFont.truetype(FONTS + r"\consola.ttf", 33)
url_f = ImageFont.truetype(FONTS + r"\consolab.ttf", 28)

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
for y in range(H):
    t = y / (H - 1)
    d.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT)))

# faint grid
for x in range(0, W, 56):
    d.line([(x, 0), (x, H)], fill=GRID, width=1)
for y in range(0, H, 56):
    d.line([(0, y), (W, y)], fill=GRID, width=1)
# darken the grid softly
img = Image.blend(img, img.point(lambda p: p), 0)  # no-op, keep pipeline simple
overlay = Image.new("L", (W, H), 0)
img = img.convert("RGB")

# purple glow behind the butterfly
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([850, 40, 1190, 390], fill=(0x38, 0x0B, 0x1C))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img = Image.blend(img, Image.blend(img, glow, 0.0), 0)
from PIL import ImageChops
img = ImageChops.add(img, glow)

d = ImageDraw.Draw(img)

# corner targeting brackets
L, IN, WID = 30, 26, 4
for (cx, cy, sx, sy) in [(IN, IN, 1, 1), (W - IN, IN, -1, 1), (IN, H - IN, 1, -1), (W - IN, H - IN, -1, -1)]:
    d.line([(cx, cy), (cx + L * sx, cy)], fill=ACCENT, width=WID)
    d.line([(cx, cy), (cx, cy + L * sy)], fill=ACCENT, width=WID)

# red spider lily (same 64-unit geometry as the favicon), centered right
import math

F = 4.9
OX, OY = 1020 - 32 * F, 215 - 32 * F
OUTER_BASE = (0x88, 0x13, 0x37)
OUTER_MID = (0xDC, 0x26, 0x26)
OUTER_TIP = (0xF4, 0x3F, 0x5E)
INNER_BASE = (0xBE, 0x12, 0x3C)
INNER_MID = (0xEF, 0x44, 0x44)
INNER_TIP = (0xFD, 0xA4, 0xAF)
STAMEN = (0xFE, 0xCD, 0xD3)
ANTHER = (0xFF, 0xF1, 0xF2)
STEM = (0x9F, 0x12, 0x39)
CORE = (0xFE, 0xCD, 0xD3)


def scale_about(pts, f, o):
    return [(o[0] + (x - o[0]) * f, o[1] + (y - o[1]) * f) for x, y in pts]


def draw_petal(dd, poly, base_c, mid_c, tip_c):
    dd.polygon(poly, fill=base_c)
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    dd.polygon([(cx + (x - cx) * 0.8, cy + (y - cy) * 0.8) for x, y in poly], fill=mid_c)
    tip = poly[len(poly) // 2]
    tx, ty = cx + (tip[0] - cx) * 0.7, cy + (tip[1] - cy) * 0.7
    dd.polygon([(tx + (x - tx) * 0.45, ty + (y - ty) * 0.45) for x, y in poly], fill=tip_c)


def rot(pts, deg, c=(32.0, 32.0)):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [
        (c[0] + (x - c[0]) * ca - (y - c[1]) * sa,
         c[1] + (x - c[0]) * sa + (y - c[1]) * ca)
        for x, y in pts
    ]


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


def px(pts, mirror=False):
    out = []
    for x, y in pts:
        if mirror:
            x = 64 - x
        out.append((OX + x * F, OY + y * F))
    return out


d.line(px(cubic((32, 33), (30, 42), (34, 52), (32, 64))), fill=STEM, width=round(2 * F), joint="curve")
stamen = cubic((32, 32), (30, 23), (28.5, 12), (30.5, 1.5))
for ang in (-68, -34, 0, 34, 68):
    pts = rot(stamen, ang)
    d.line(px(pts), fill=STAMEN, width=round(0.9 * F), joint="curve")
    tx, ty = pts[-1]
    r = 1.2
    d.ellipse([OX + (tx - r) * F, OY + (ty - r) * F, OX + (tx + r) * F, OY + (ty + r) * F], fill=ANTHER)
petal = (
    cubic((32, 33), (28.5, 26), (26.5, 15), (30.3, 4.5))
    + cubic((30.3, 4.5), (31.6, 12), (31.5, 23), (32, 33))[1:]
)
for ang, sc in ((-85, 1), (-59, .9), (-36, 1), (-13, .94), (11, .9), (34, 1), (57, .94), (83, 1)):
    draw_petal(d, px(rot(scale_about(petal, sc, (32.0, 33.0)), ang)), OUTER_BASE, OUTER_MID, OUTER_TIP)
inner = scale_about(petal, 0.6, (32.0, 33.0))
for ang in (-70, -35, 0, 35, 70):
    draw_petal(d, px(rot(inner, ang)), INNER_BASE, INNER_MID, INNER_TIP)
r = 1.7
d.ellipse([OX + (32 - r) * F, OY + (32 - r) * F, OX + (32 + r) * F, OY + (32 + r) * F], fill=CORE)

# text block, left
x = 90
d.text((x, 200), "othmaneb", font=title_f, fill=TEXT)
w = d.textlength("othmaneb", font=title_f)
d.text((x + w, 200), "@cti:~$", font=title_f, fill=ACCENT)
d.text((x, 330), "Cyber Threat Intelligence · Malware Analysis", font=sub_f, fill=DIM)
d.text((x, 378), "Detection Engineering · HuntingBadGuys", font=sub_f, fill=DIM)
d.line([(x + 2, 452), (x + 62, 452)], fill=ACCENT, width=4)
d.text((x, 490), "indestiny0xff.github.io", font=url_f, fill=ACCENT)

img.save("assets/og.png", optimize=True)
print("assets/og.png written", img.size)
