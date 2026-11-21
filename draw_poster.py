#!/usr/bin/env python3
"""SOLMARA — travel poster for a place that does not exist.

Draws a vintage art-deco travel poster (1024x1024) procedurally with PIL.
Fully deterministic: fixed palette, fixed geometry, no randomness, no
network, no clock. The only text in the image is the invented place name
"SOLMARA".

Concept: the bay where the sun is wound by hand. A great brass sun, low
over a calm teal bay at golden dawn, is being wound by a tiny keeper on a
ladder from a winding tower on the cliff. One landmark, one promise:
golden dawn, calm warm water.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

# Palette
PEACH_TOP = (232, 106, 74)      # coral dawn top
PEACH_MID = (247, 178, 102)     # warm peach
CREAM_HORIZON = (253, 235, 208) # pale cream at horizon
GOLD = (245, 185, 66)           # brass sun
GOLD_DEEP = (214, 138, 32)
BRASS_DARK = (122, 74, 18)
TEAL_DEEP = (8, 59, 68)         # sea deep
TEAL = (14, 90, 99)             # sea
TEAL_LIGHT = (38, 138, 138)     # sea light band
CLIFF = (16, 62, 66)            # cliff silhouette
CREAM = (255, 246, 224)         # type
INK = (24, 48, 52)              # outlines

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, x0, y0, x1, y1, c_top, c_bot):
    """Vertical gradient band."""
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / h
        draw.line([(x0, y), (x1, y)], fill=lerp(c_top, c_bot, t))


def draw_poster():
    img = Image.new("RGB", (W, H), CREAM_HORIZON)
    d = ImageDraw.Draw(img)

    # ---- sky: coral top -> peach -> cream horizon (0..640) ----
    vgrad(d, 0, 0, W, 340, PEACH_TOP, PEACH_MID)
    vgrad(d, 0, 340, W, 660, PEACH_MID, CREAM_HORIZON)

    # ---- thin deco sun rays fanning behind the sun ----
    import math
    cx, cy, r = 512, 470, 195
    for k in range(-7, 8):
        ang = math.radians(-90 + k * 9)
        x0 = cx + int(math.cos(ang) * (r + 8))
        y0 = cy + int(math.sin(ang) * (r + 8))
        x1 = cx + int(math.cos(ang) * (r + 120))
        y1 = cy + int(math.sin(ang) * (r + 120))
        if y1 < 660:  # keep rays in the sky
            d.line([(x0, y0), (x1, y1)], fill=(247, 200, 130), width=5)

    # ---- sun: brass clockwork disc ----
    # gear teeth around the rim
    for k in range(36):
        ang = math.radians(k * 10)
        x0 = cx + int(math.cos(ang) * (r - 2))
        y0 = cy + int(math.sin(ang) * (r - 2))
        x1 = cx + int(math.cos(ang) * (r + 16))
        y1 = cy + int(math.sin(ang) * (r + 16))
        d.line([(x0, y0), (x1, y1)], fill=GOLD_DEEP, width=10)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD, outline=BRASS_DARK, width=6)
    # clockwork rings + tick marks
    d.ellipse([cx - 152, cy - 152, cx + 152, cy + 152], outline=BRASS_DARK, width=4)
    d.ellipse([cx - 106, cy - 106, cx + 106, cy + 106], outline=(176, 112, 26), width=3)
    for k in range(12):
        ang = math.radians(k * 30)
        x0 = cx + int(math.cos(ang) * 115)
        y0 = cy + int(math.sin(ang) * 115)
        x1 = cx + int(math.cos(ang) * 145)
        y1 = cy + int(math.sin(ang) * 145)
        d.line([(x0, y0), (x1, y1)], fill=BRASS_DARK, width=6)
    # centre hub + hands (a clock face in the sun)
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=CREAM, outline=BRASS_DARK, width=4)
    d.line([(cx, cy), (cx, cy - 62)], fill=BRASS_DARK, width=7)   # minute hand up
    d.line([(cx, cy), (cx + 40, cy + 14)], fill=BRASS_DARK, width=7)  # hour hand
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=BRASS_DARK)

    # ---- sea: deep teal, horizon at y=660 ----
    vgrad(d, 0, 660, W, H, TEAL, TEAL_DEEP)
    # light bands on the water
    for y, wdt in ((700, 3), (760, 4), (830, 3), (910, 4), (980, 3)):
        d.line([(0, y), (W, y)], fill=TEAL_LIGHT, width=wdt)

    # ---- sun reflection: soft broken gold dashes on the water ----
    for yy, half in ((672, 62), (700, 48), (726, 66), (754, 44),
                     (784, 58), (816, 40), (850, 52), (886, 38),
                     (924, 46), (962, 34)):
        d.rectangle([cx - half, yy, cx + half, yy + 7], fill=(238, 178, 90))

    # ---- cliff + winding tower (far right edge, narrow) ----
    d.polygon([(862, 1024), (862, 640), (900, 606), (962, 590),
               (1024, 606), (1024, 1024)], fill=CLIFF)
    # tower on the cliff top
    d.rectangle([888, 452, 924, 600], fill=INK)
    d.rectangle([878, 440, 934, 454], fill=INK)          # platform
    d.polygon([(882, 440), (930, 440), (906, 414)], fill=GOLD_DEEP)  # roof
    d.rectangle([900, 474, 914, 492], fill=GOLD)         # lit window
    d.rectangle([900, 508, 914, 526], fill=GOLD)

    # ---- winding key in the sun's right side (clear of the cliff) ----
    kx, ky = 702, 470
    d.line([(kx - 6, ky), (kx + 34, ky)], fill=BRASS_DARK, width=12)  # stem
    d.ellipse([kx + 30, ky - 34, kx + 78, ky + 10], outline=BRASS_DARK, width=10)  # bow loop 1
    d.ellipse([kx + 30, ky - 10, kx + 78, ky + 34], outline=BRASS_DARK, width=10)  # bow loop 2
    d.ellipse([kx + 30, ky - 34, kx + 78, ky + 34], outline=GOLD_DEEP, width=3)

    # ---- ladder from tower platform to the key ----
    import math as _m
    x0, y0, x1, y1 = 884, 452, 766, 470
    d.line([(x0, y0), (x1, y1)], fill=BRASS_DARK, width=6)
    d.line([(x0, y0 + 14), (x1, y1 + 14)], fill=BRASS_DARK, width=6)
    for t in [i / 7 for i in range(1, 7)]:
        rx = int(x0 + (x1 - x0) * t)
        ry = int(y0 + (y1 - y0) * t)
        d.line([(rx, ry), (rx, ry + 14)], fill=BRASS_DARK, width=4)

    # ---- tiny keeper on the ladder, turning the key ----
    kx2, ky2 = 776, 440
    d.line([(kx2, ky2 + 8), (kx2, ky2 + 26)], fill=INK, width=7)      # body
    d.ellipse([kx2 - 7, ky2 - 6, kx2 + 7, ky2 + 8], fill=INK)         # head
    d.line([(kx2, ky2 + 12), (kx2 + 16, ky2 + 2)], fill=INK, width=5)  # arm to key
    d.line([(kx2, ky2 + 26), (kx2 - 8, ky2 + 38)], fill=INK, width=5)  # legs
    d.line([(kx2, ky2 + 26), (kx2 + 8, ky2 + 38)], fill=INK, width=5)

    # ---- sailboats on the bay ----
    def boat(bx, by, s):
        d.polygon([(bx - 34 * s, by), (bx + 34 * s, by), (bx, by + 12 * s)],
                  fill=INK)
        d.line([(bx, by), (bx, by - 46 * s)], fill=INK, width=4)
        d.polygon([(bx + 2, by - 44 * s), (bx + 2, by - 4 * s), (bx + 30 * s, by - 4 * s)],
                  fill=CREAM)
        d.polygon([(bx - 2, by - 40 * s), (bx - 2, by - 4 * s), (bx - 24 * s, by - 4 * s)],
                  fill=GOLD)
    boat(330, 800, 1.0)
    boat(620, 900, 0.7)

    # ---- gulls ----
    def gull(gx, gy, s):
        d.line([(gx - 13 * s, gy + 5 * s), (gx, gy - 3 * s), (gx + 13 * s, gy + 5 * s)],
               fill=INK, width=3, joint="curve")
    gull(300, 330, 1.0)
    gull(368, 296, 0.8)
    gull(700, 330, 0.9)

    # ---- place name: SOLMARA, large across the upper sky ----
    font = ImageFont.truetype(FONT_BOLD, 128)
    word = "SOLMARA"
    tracking = 26
    widths = [d.textlength(ch, font=font) for ch in word]
    total = sum(widths) + tracking * (len(word) - 1)
    x = (W - total) // 2
    y = 96
    # soft shadow, then cream letters with a thin dark outline
    for ch, wch in zip(word, widths):
        d.text((x + 5, y + 6), ch, font=font, fill=(176, 84, 40))
        x += wch + tracking
    x = (W - total) // 2
    for ch, wch in zip(word, widths):
        d.text((x, y), ch, font=font, fill=CREAM,
               stroke_width=2, stroke_fill=INK)
        x += wch + tracking
    # deco rule lines flanking a small sun mark under the name
    d.line([(300, 268), (452, 268)], fill=CREAM, width=4)
    d.line([(572, 268), (724, 268)], fill=CREAM, width=4)
    d.ellipse([498, 254, 526, 282], fill=GOLD, outline=CREAM, width=3)

    # ---- art-deco double border ----
    d.rectangle([22, 22, W - 23, H - 23], outline=CREAM, width=5)
    d.rectangle([36, 36, W - 37, H - 37], outline=CREAM, width=2)

    img.save(OUT, "PNG", optimize=True)
    print("Wrote %s" % OUT)


if __name__ == "__main__":
    draw_poster()
