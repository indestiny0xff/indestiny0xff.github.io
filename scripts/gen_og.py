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
gd.ellipse([850, 40, 1190, 390], fill=(0x2A, 0x14, 0x52))
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

# butterfly (same 64-unit geometry as the favicon), centered right
F = 4.9
OX, OY = 1020 - 32 * F, 215 - 32 * F


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


outline = (
    cubic((29, 30), (24, 12), (10, 6), (7, 13))
    + cubic((7, 13), (4, 20), (10, 30), (17, 33))[1:]
    + cubic((17, 33), (9, 35), (8, 45), (13, 51))[1:]
    + cubic((13, 51), (18, 56), (27, 50), (29, 38))[1:]
)
for mirror in (False, True):
    wing = px(outline, mirror)
    d.polygon(wing, fill=ACCENT_DK)
    cx = sum(p[0] for p in wing) / len(wing)
    cy = sum(p[1] for p in wing) / len(wing)
    d.polygon([(cx + (x - cx) * 0.55, cy + (y - cy) * 0.55) for x, y in wing], fill=ACCENT)
    for (mx, my, r) in [(13, 20, 1.8), (16, 45, 1.4)]:
        if mirror:
            mx = 64 - mx
        d.ellipse([OX + (mx - r) * F, OY + (my - r) * F, OX + (mx + r) * F, OY + (my + r) * F], fill=CYAN)
d.ellipse([OX + (32 - 2.4) * F, OY + (36 - 10.5) * F, OX + (32 + 2.4) * F, OY + (36 + 10.5) * F], fill=BODY)
d.ellipse([OX + (32 - 3) * F, OY + (22.5 - 3) * F, OX + (32 + 3) * F, OY + (22.5 + 3) * F], fill=BODY)
for a in (quad((30.5, 20.5), (27, 13), (22, 11)), quad((33.5, 20.5), (37, 13), (42, 11))):
    d.line(px(a), fill=BODY, width=round(1.7 * F), joint="curve")

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
