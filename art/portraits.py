#!/usr/bin/env python3
"""Portraits: 10 x 12 characters (80 x 96 pixels), black paper, own
attributes, in the prologue's style (art/render.py: greyscale + ink hints,
Bayer dither).

Each portrait is drawn at the screen's top left, rendered with render.Pic,
then cut out as a block: 96 pixel rows of 10 bytes (top to bottom), then
12 rows of 10 attributes. 1080 bytes raw, packed with ZX0 by the build.

  isobel : Isobel Halliday, 18, by candlelight on the night the clerk
           first sees her. Well bred, a stranger to the island; drawn as a
           young woman, tired and watchful. Not a monster, not a saint.

Writes art/<name>.bin (the raw block) and art/<name>.png (preview, x4).
"""
import os
from PIL import Image, ImageDraw
from render import Pic, scr_preview, K, RED, YELLOW, WHITE, BR

HERE = os.path.dirname(os.path.abspath(__file__))
PW, PHC = 10, 12               # width and height in characters
PWX, PHX = PW * 8, PHC * 8     # in pixels


S = 4                          # drawn at 4x, then scaled down before dithering


class Canvas:
    """A 4x canvas in portrait units (80 x 96). Shapes are filled with a
    value or with fn(x, y) -> 0..1 (x, y in portrait units)."""

    def __init__(self):
        self.lum = Image.new("L", (PWX * S, PHX * S), 0)
        self.hint = Image.new("L", (PWX * S, PHX * S), 0)

    def fill(self, draw_mask, v, ink=None):
        m = Image.new("L", self.lum.size, 0)
        draw_mask(ImageDraw.Draw(m))
        mp, lp, hp = m.load(), self.lum.load(), self.hint.load()
        W, H = self.lum.size
        for y in range(H):
            for x in range(W):
                if mp[x, y]:
                    if v is not None:
                        f = v(x / S, y / S) if callable(v) else v
                        lp[x, y] = max(0, min(255, int(f * 255)))
                    if ink is not None:
                        hp[x, y] = ink

    def poly(self, pts, v, ink=None):
        self.fill(lambda d: d.polygon([(x * S, y * S) for x, y in pts], fill=1), v, ink)

    def ellipse(self, box, v, ink=None):
        self.fill(lambda d: d.ellipse([c * S for c in box], fill=1), v, ink)

    def line(self, pts, v, width=1.0, ink=None):
        self.fill(lambda d: d.line([(x * S, y * S) for x, y in pts], fill=1,
                                   width=max(1, int(width * S))), v, ink)

    def to_pic(self, seed, levels=5):
        """Scale down and quantise to a few clean dither patterns (0, 1/4,
        1/2, 3/4, 1 with five levels): flat, readable tones, no grain."""
        p = Pic((0, PHC), ink=YELLOW, seed=seed)
        small = self.lum.resize((PWX, PHX), Image.BOX)
        n = levels - 1
        p.lum.paste(small.point(lambda v: min(255, int(round(v / 255 * n) * 255 / n))), (0, 0))
        p.hint.paste(self.hint.resize((PWX, PHX), Image.NEAREST), (0, 0))
        return p


def side(x, x0, x1, lo, hi, g=0.8):
    """lo..hi across a shape: hi on the candle side (x0), lo at x1."""
    t = min(1.0, max(0.0, (x - x0) / float(x1 - x0)))
    return lo + (hi - lo) * (1 - t) ** g


def isobel():
    c = Canvas()
    # The candle is low on the left, out of the frame; the wall is black.
    # gown: a dark red bodice, good cloth, catching the light on the left
    c.poly([(0, 96), (3, 82), (16, 71), (34, 66), (54, 68), (68, 74), (79, 86), (79, 96)],
           lambda x, y: side(x, 0, 80, 0.04, 0.55, 1.3), RED)
    # the neckerchief, fine white linen crossed over the breast
    c.poly([(15, 74), (29, 66), (40, 75), (51, 66), (62, 71), (52, 86), (45, 96), (35, 96), (25, 85)],
           lambda x, y: side(x, 15, 64, 0.25, 1.0, 0.7), WHITE)
    c.line([(40, 75), (39, 96)], 0.12, 0.8)              # where it crosses
    c.line([(29, 67), (33, 77), (36, 90)], 0.45, 0.6)    # a fold
    c.line([(51, 67), (49, 78)], 0.10, 0.6)
    # neck, in shadow under the jaw
    c.poly([(33, 52), (47, 52), (48, 68), (32, 68)],
           lambda x, y: side(x, 32, 48, 0.10, 0.62) * (0.45 if y < 61 else 0.8), YELLOW)
    # hair, dark brown, pinned up: it shows at the brow and behind the ear
    c.ellipse((21, 12, 61, 58), lambda x, y: side(x, 21, 61, 0.03, 0.30, 1.5), YELLOW)
    # the cap (a linen coif) over the crown and back of the head: lit on the
    # left, lost in the dark on the right, so it never makes a ring
    c.poly([(23, 25), (25, 14), (33, 7), (45, 5), (55, 9), (61, 17), (62, 28), (59, 38),
            (55, 29), (51, 22), (43, 19), (33, 19), (27, 22)],
           lambda x, y: side(x, 23, 62, 0.0, 1.0, 1.3) * (0.85 + 0.15 * (y > 10)), WHITE)
    c.line([(24, 24), (30, 19), (40, 17), (50, 19), (55, 26)], 0.45, 0.8)   # the frill's edge
    c.line([(33, 9), (36, 16)], 0.55, 0.6)                                  # a fold
    # the face: three-quarters, turned a little towards the light
    face = [(26, 27), (30, 21), (38, 19), (48, 20), (53, 25), (54, 34), (52, 44), (48, 52),
            (43, 57), (38, 57), (32, 53), (27, 46), (25, 37)]

    def face_lum(x, y):
        v = side(x, 25, 54, 0.42, 1.0, 0.55)
        if x > 49:
            v *= 0.75                                    # the far cheek turns away
        if y > 52:
            v *= 0.8                                     # under the chin
        return v
    c.poly(face, face_lum, YELLOW)
    c.poly([(24, 20), (44, 20), (40, 58), (24, 50)], None, YELLOW + BR)   # lit half bright
    c.poly([(23, 24), (27, 23), (26.5, 36), (25, 44), (22.5, 36)], 0.25)  # hair at the temple
    c.ellipse((28, 31, 39, 39), 0.50)                    # the eyes sit in shadow
    c.ellipse((43, 31, 51, 39), 0.25)
    c.poly([(37, 40), (40, 33), (41, 44), (38, 46)], 1.0)   # light down the nose
    c.ellipse((27, 40, 35, 47), 1.0)                    # the near cheek
    # hair at the brow, parted, under the frill
    c.poly([(26, 27), (30, 21), (38, 20), (40, 23), (48, 20), (53, 25), (54, 30),
            (49, 25), (41, 25), (33, 24), (28, 27)], 0.06)
    p = c.to_pic(1727)
    # The features go on afterwards, a pixel at a time, so the scaling
    # does not smear them. She looks at you, steadily, giving nothing away.
    px = p.lum.load()

    def put(pts, v):
        for (x, y) in pts:
            px[x, y] = int(v * 255)
    put([(x, 30) for x in range(30, 36)] + [(29, 31), (36, 31)], 0.5)       # brows, soft
    put([(x, 30) for x in range(45, 50)] + [(44, 31)], 0.25)
    put([(x, y) for x in range(30, 37) for y in (34, 35)], 1.0)             # near eye
    put([(29, 34), (37, 34)] + [(x, 33) for x in range(30, 37)], 0.0)       # its lid
    put([(x, y) for x in (32, 33) for y in (33, 34, 35, 36)], 0.0)          # iris: on you
    put([(32, 34)], 1.0)                                                    # catchlight
    put([(x, 36) for x in range(30, 37) if x not in (32, 33)], 0.5)         # lower lid
    put([(x, y) for x in range(44, 50) for y in (34, 35)], 0.75)            # far eye
    put([(43, 34), (50, 34)] + [(x, 33) for x in range(44, 50)], 0.0)
    put([(x, y) for x in (45, 46) for y in (33, 34, 35, 36)], 0.0)
    put([(x, 39) for x in range(31, 36)], 0.75)                             # tired
    put([(42, y) for y in range(38, 45)], 0.5)                              # nose shadow
    put([(39, 46), (42, 46)], 0.0)                                # nostrils
    put([(36, 51), (44, 51)], 0.5)                                          # the mouth,
    put([(x, 51) for x in range(37, 44)], 0.0)                              # closed
    put([(x, 52) for x in range(37, 43)], 1.0)
    put([(x, 50) for x in range(38, 42)], 0.75)
    return p


def block(p):
    """Cut the portrait out of a rendered screen: pixels row by row, then
    attributes row by row."""
    scr = p.to_scr()
    out = bytearray()
    for y in range(PHX):
        a = ((y & 0xC0) << 5) | ((y & 7) << 8) | ((y & 0x38) << 2)
        out += scr[a:a + PW]
    for r in range(PHC):
        out += scr[6144 + r * 32:6144 + r * 32 + PW]
    return bytes(out), scr


PORTRAITS = [("isobel", isobel)]

if __name__ == "__main__":
    import zx0
    for name, fn in PORTRAITS:
        raw, scr = block(fn())
        open(os.path.join(HERE, name + ".bin"), "wb").write(raw)
        tmp = os.path.join(HERE, "_tmp.png")
        scr_preview(scr, tmp, scale=1)
        Image.open(tmp).crop((0, 0, PWX, PHX)).resize((PWX * 4, PHX * 4), Image.NEAREST) \
            .save(os.path.join(HERE, name + ".png"))
        os.remove(tmp)
        print("%s: %d bytes raw, %d packed" % (name, len(raw), len(zx0.compress(raw))))
