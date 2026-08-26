"""Regenerate favicon.ico from the butterfly design in assets/favicon.svg.

The .ico must always match the .svg: this script redraws the same shapes
(same 64-unit coordinates) with PIL at high resolution, then saves a
multi-size icon (16/32/48/64) at the repo root. Run from the repo root:

    python scripts/gen_favicon.py
"""

from PIL import Image, ImageDraw

BASE = 64          # design space of assets/favicon.svg
S = 512            # master render size
F = S / BASE

BG_TOP = (0x15, 0x0A, 0x2E)
BG_BOT = (0x03, 0x05, 0x0A)
WING = (0xA8, 0x55, 0xF7, 255)
WING_GLOW = (0xC0, 0x84, 0xFC, 255)
CYAN = (0x67, 0xE8, 0xF9, 255)
BODY = (0xC4, 0xB5, 0xFD, 255)


def cubic(p0, p1, p2, p3, n=48):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def quad(p0, p1, p2, n=32):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**2 * p0[0] + 2 * u * t * p1[0] + t**2 * p2[0]
        y = u**2 * p0[1] + 2 * u * t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


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

# Left wing on its own layer, mirrored for the right side
wing_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
wd = ImageDraw.Draw(wing_layer)
outline = (
    cubic((29, 30), (24, 12), (10, 6), (7, 13))
    + cubic((7, 13), (4, 20), (10, 30), (17, 33))[1:]
    + cubic((17, 33), (9, 35), (8, 45), (13, 51))[1:]
    + cubic((13, 51), (18, 56), (27, 50), (29, 38))[1:]
)
wing_px = px(outline)
wd.polygon(wing_px, fill=WING)
cx = sum(p[0] for p in wing_px) / len(wing_px)
cy = sum(p[1] for p in wing_px) / len(wing_px)
wd.polygon([(cx + (x - cx) * 0.55, cy + (y - cy) * 0.55) for x, y in wing_px], fill=WING_GLOW)
for (dx, dy, r) in [(13, 20, 1.8), (16, 45, 1.4)]:
    wd.ellipse([(dx - r) * F, (dy - r) * F, (dx + r) * F, (dy + r) * F], fill=CYAN)
img.alpha_composite(wing_layer)
img.alpha_composite(wing_layer.transpose(Image.FLIP_LEFT_RIGHT))

# Body, head, antennae
d = ImageDraw.Draw(img)
d.ellipse([(32 - 2.4) * F, (36 - 10.5) * F, (32 + 2.4) * F, (36 + 10.5) * F], fill=BODY)
d.ellipse([(32 - 3) * F, (22.5 - 3) * F, (32 + 3) * F, (22.5 + 3) * F], fill=BODY)
for a in (quad((30.5, 20.5), (27, 13), (22, 11)), quad((33.5, 20.5), (37, 13), (42, 11))):
    d.line(px(a), fill=BODY, width=round(1.7 * F), joint="curve")
for (tx, ty) in [(22, 11), (42, 11)]:
    r = 1.2
    d.ellipse([(tx - r) * F, (ty - r) * F, (tx + r) * F, (ty + r) * F], fill=BODY)

img.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("favicon.ico written")
