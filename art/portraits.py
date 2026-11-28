#!/usr/bin/env python3
"""Portraits, black paper, own attributes, in the prologue's style
(art/render.py: greyscale + ink hints, Bayer dither). Each has its own
size in characters (v0.9): Isobel and Kate are 10 x 12 (80 x 96 pixels),
the trial's witnesses 16 x 14 (128 x 112).

Each portrait is drawn at the screen's top left, rendered with render.Pic,
then cut out as a block: db width, height (characters), then 8 x height
pixel rows of width bytes (top to bottom), then height rows of width
attributes. Packed with ZX0 by the build (src/port_NAME.inc).

A witness can also falter (v0.9): drawn a second time with the eyes and
mouth changed, and the cells that differ written to art/NAME_falter.bin:
db cells, then each cell as db row, col (in the portrait), 8 pixel bytes
as it falters, 8 as it was. The attributes never change, so swapping the
cells in at once can't clash. The engine swaps them straight to the screen.

  isobel : Isobel Halliday, 18, by candlelight on the night the clerk
           first sees her. Well bred, a stranger to the island; drawn as a
           young woman, tired and watchful. Not a monster, not a saint.
  kate   : Kate Rankin, Janet Boyd's daughter, a spinner, fetched from her
           wheel (v0.7). The light comes cold from the right (the door she
           is brought through), the other side from Isobel's candle. A plain
           linen kerchief, a grey woollen shawl; younger and rounder in the
           face; she looks down and away, not at the clerk. Ordinary.

  lowry  : Margaret Lowry, servant at Braehead House, in the witness box
           at six in the morning (v0.9). A plain linen cap, a brown
           woollen bodice, a white kerchief; the candle on the box's ledge,
           low on the left. She looks up at the bench, holding to the story
           she has told so often; when she falters her eyes drop and go
           aside, her brows lift and her mouth opens a little. Ordinary,
           frightened of the court, not of anyone in the dock.

Writes art/<name>.bin (the raw block), art/<name>.png (preview, x4) and,
for a witness, art/<name>_falter.bin and art/<name>_falter.png.
"""
import os
from PIL import Image, ImageDraw
from render import Pic, scr_preview, K, RED, YELLOW, WHITE, BR

HERE = os.path.dirname(os.path.abspath(__file__))
PW, PHC = 10, 12               # the night portraits' size, in characters
PWX, PHX = PW * 8, PHC * 8     # in pixels


S = 4                          # drawn at 4x, then scaled down before dithering


class Canvas:
    """A 4x canvas in portrait units (80 x 96). Shapes are filled with a
    value or with fn(x, y) -> 0..1 (x, y in portrait units)."""

    def __init__(self, pw=PW, ph=PHC):
        self.pw, self.ph = pw, ph
        self.lum = Image.new("L", (pw * 8 * S, ph * 8 * S), 0)
        self.hint = Image.new("L", (pw * 8 * S, ph * 8 * S), 0)

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
        p = Pic((0, self.ph), ink=YELLOW, seed=seed)
        wx, hx = self.pw * 8, self.ph * 8
        small = self.lum.resize((wx, hx), Image.BOX)
        n = levels - 1
        p.lum.paste(small.point(lambda v: min(255, int(round(v / 255 * n) * 255 / n))), (0, 0))
        p.hint.paste(self.hint.resize((wx, hx), Image.NEAREST), (0, 0))
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


def kate():
    c = Canvas()
    R = lambda x, lo, hi, g=0.8: side(x, 80, 0, lo, hi, g)   # lit from the right
    # the shawl, grey wool, pulled round the shoulders and crossed in front
    c.poly([(0, 96), (2, 84), (14, 72), (30, 66), (50, 66), (66, 72), (79, 82), (79, 96)],
           lambda x, y: R(x, 0.05, 0.50, 1.4), WHITE)
    c.line([(22, 74), (34, 86), (40, 96)], 0.02, 1.0)                # where it crosses
    c.line([(60, 72), (50, 84), (46, 96)], 0.30, 0.8)
    c.line([(12, 82), (18, 92)], 0.02, 0.6)                          # a fold in the dark
    # a glimpse of the bodice where the shawl parts, plain brown-red
    c.poly([(34, 66), (48, 66), (44, 78), (38, 78)], lambda x, y: R(x, 0.05, 0.35), RED)
    # neck
    c.poly([(34, 54), (47, 54), (47, 67), (34, 67)],
           lambda x, y: side(x, 47, 34, 0.0, 0.6, 1.2) * (0.4 if y < 61 else 0.8), YELLOW)
    # the kerchief, linen tied at the nape: lit on the right, the left side
    # lost in the dark, so it never makes a ring round the face
    c.poly([(19, 40), (18, 24), (24, 12), (36, 6), (48, 7), (58, 14), (62, 26), (62, 42),
            (58, 54), (55, 44), (55, 30), (50, 21), (40, 18), (30, 21), (25, 30), (24, 44)],
           lambda x, y: R(x, 0.0, 1.0, 1.0) * min(1.0, max(0.0, (x - 34) / 14.0)), WHITE)
    c.line([(26, 22), (34, 16), (46, 15), (56, 22)], 0.4, 0.8)         # its edge over the brow
    c.line([(52, 9), (58, 20)], 0.5, 0.6)                             # a fold
    # the face, rounder, turned a little to her right (our left), away from the light
    face = [(26, 30), (30, 22), (40, 19), (50, 21), (55, 29), (56, 38), (54, 47), (50, 54),
            (44, 58), (38, 58), (32, 54), (28, 47), (26, 39)]

    def face_lum(x, y):
        v = side(x, 58, 26, 0.38, 1.0, 1.0)
        if x < 31:
            v *= 0.75                                    # the far cheek, in shadow
        if y > 53:
            v *= 0.8
        return v
    c.poly(face, face_lum, YELLOW)
    c.poly([(44, 19), (57, 22), (57, 50), (46, 58)], None, YELLOW + BR)   # lit side bright
    # hair at the brow, light brown, a loose strand on the lit side
    c.poly([(27, 30), (30, 23), (40, 21), (50, 22), (55, 29), (55, 33), (50, 26), (41, 25),
            (33, 26), (28, 31)], lambda x, y: R(x, 0.0, 0.5, 1.2))
    c.line([(54, 30), (56, 38), (55, 46)], 0.35, 0.6)
    c.ellipse((30, 34, 37, 39), 0.5)                     # the eyes, lowered
    c.ellipse((43, 34, 50, 39), 0.75)
    c.ellipse((46, 42, 54, 49), 0.9)                     # the near cheek
    c.poly([(42, 36), (40, 44), (42, 47)], 0.9)          # light down the nose
    p = c.to_pic(1711)
    # The features a pixel at a time. Her eyes are down and to the side:
    # she has been sent for, and doesn't know why it is her.
    px = p.lum.load()

    def put(pts, v):
        for (x, y) in pts:
            px[x, y] = int(v * 255)
    put([(x, 32) for x in range(31, 36)], 0.25)                            # brows, raised a
    put([(x, 31) for x in range(44, 50)] + [(43, 32), (50, 32)], 0.5)       # little: worried
    put([(x, 36) for x in range(43, 50)], 0.0)                             # near eye: a lid,
    put([(x, 37) for x in range(43, 50)], 0.75)                            # lowered
    put([(44, 37), (45, 37)], 0.0)                                         # looking down, aside
    put([(x, 36) for x in range(31, 36)], 0.0)                             # far eye
    put([(31, 37), (32, 37)], 0.0)
    put([(x, 38) for x in range(43, 49)], 0.5)                             # lower lid
    put([(40, y) for y in range(38, 45)], 0.5)                              # nose shadow
    put([(39, 46), (42, 46)], 0.0)                                         # nostrils
    put([(x, 51) for x in range(37, 44)], 0.0)                             # the mouth, closed,
    put([(36, 52), (44, 51)], 0.5)                                         # pressed a little
    put([(x, 52) for x in range(38, 44)], 0.75)
    return p


def lowry():
    """Margaret Lowry in the witness box (16 x 14). Returns (steady, faltering)."""
    def paint():
        c = Canvas(16, 14)
        L = lambda x, lo, hi, g=0.9: side(x, 20, 112, lo, hi, g)   # the candle, low left
        # the bodice, brown wool, plain: dark, catching the light on the left
        c.poly([(0, 112), (4, 94), (22, 80), (44, 74), (84, 74), (106, 80), (124, 94), (127, 112)],
               lambda x, y: L(x, 0.03, 0.40, 1.4), YELLOW)
        # the kerchief, white linen crossed over the breast, a servant's,
        # tucked in plainly
        c.poly([(38, 78), (52, 74), (64, 88), (76, 74), (90, 78), (80, 96), (70, 112), (58, 112),
                (48, 96)], lambda x, y: L(x, 0.15, 0.95, 0.8), WHITE)
        c.line([(64, 88), (63, 112)], 0.1, 0.8)
        c.line([(50, 78), (56, 92), (60, 106)], 0.45, 0.6)
        # neck, in shadow under the jaw
        c.poly([(52, 64), (76, 64), (78, 78), (50, 78)],
               lambda x, y: L(x, 0.08, 0.6) * (0.4 if y < 76 else 0.75), YELLOW)
        # hair, dark, under the cap
        c.ellipse((36, 16, 92, 72), lambda x, y: L(x, 0.02, 0.25, 1.5), YELLOW)
        # the cap: plain linen over the crown, lit on the left, lost in the
        # dark on the right so it never rings her face
        c.poly([(36, 34), (38, 20), (48, 10), (62, 6), (78, 8), (90, 18), (94, 32), (90, 44),
                (86, 34), (80, 26), (64, 22), (50, 24), (42, 30)],
               lambda x, y: L(x, 0.0, 1.0, 1.4), WHITE)
        c.line([(37, 33), (46, 25), (60, 22), (76, 23), (86, 31)], 0.4, 0.8)   # its edge
        c.line([(52, 9), (55, 20)], 0.55, 0.6)                                  # a fold
        # the face, nearly full on, turned a little to the light
        face = [(40, 36), (44, 28), (54, 24), (70, 24), (82, 29), (86, 40), (85, 52), (80, 62),
                (72, 70), (62, 72), (52, 68), (44, 60), (40, 48)]

        def face_lum(x, y):
            v = L(x, 0.42, 1.0, 0.6)
            if x > 80:
                v *= 0.75
            if y > 66:
                v *= 0.8
            return v
        c.poly(face, face_lum, YELLOW)
        c.poly([(38, 24), (62, 24), (60, 72), (38, 60)], None, YELLOW + BR)   # lit half bright
        # hair at the brow, parted under the cap's edge
        c.poly([(40, 36), (44, 28), (54, 25), (62, 27), (70, 25), (82, 29), (86, 38),
                (80, 31), (70, 30), (62, 31), (54, 30), (46, 33)], 0.05)
        c.ellipse((45, 38, 61, 48), 0.85)        # the eyes, lit enough to read
        c.ellipse((65, 38, 80, 48), 0.6)
        c.poly([(61, 44), (64, 38), (65, 56), (61, 58)], 1.0)   # light down the nose
        c.ellipse((44, 50, 56, 60), 1.0)         # the near cheek
        return c.to_pic(1711_3)

    def features(p, falter):
        px = p.lum.load()

        def put(pts, v):
            for (x, y) in pts:
                px[x, y] = int(v * 255)
        if not falter:
            # steady: up at the bench, brows level, the mouth set: she has
            # told this so often she can say it without thinking
            put([(x, 38) for x in range(48, 58)], 0.25)                       # brows
            put([(x, 38) for x in range(68, 77)], 0.25)
            put([(x, y) for x in range(48, 58) for y in (42, 43)], 1.0)       # near eye
            put([(x, 41) for x in range(48, 58)] + [(47, 42), (58, 42)], 0.0)
            put([(x, y) for x in (52, 53) for y in (41, 42, 43)], 0.0)       # iris, up
            put([(52, 42)], 1.0)
            put([(x, 44) for x in range(49, 57)], 0.5)
            put([(x, y) for x in range(68, 77) for y in (42, 43)], 0.75)      # far eye
            put([(x, 41) for x in range(68, 77)] + [(67, 42), (77, 42)], 0.0)
            put([(x, y) for x in (71, 72) for y in (41, 42, 43)], 0.0)
            put([(x, 63) for x in range(56, 70)], 0.0)                       # mouth, set
            put([(x, 64) for x in range(57, 69)], 1.0)
        else:
            # faltering: the brows lift, the eyes drop and go aside, the
            # mouth opens a little: she has lost her place in the story
            put([(x, 36 - (1 if 51 <= x <= 55 else 0)) for x in range(48, 58)], 0.25)
            put([(x, 36 - (1 if 70 <= x <= 74 else 0)) for x in range(68, 77)], 0.25)
            put([(x, y) for x in range(48, 58) for y in (42, 43)], 1.0)
            put([(x, 41) for x in range(48, 58)] + [(47, 42), (58, 42)], 0.0)
            put([(x, 42) for x in range(48, 58)], 0.5)                       # lid lowered
            put([(x, y) for x in (49, 50) for y in (43, 44)], 0.0)           # down, aside
            put([(x, 45) for x in range(49, 57)], 0.5)
            put([(x, y) for x in range(68, 77) for y in (42, 43)], 0.75)
            put([(x, 41) for x in range(68, 77)] + [(67, 42), (77, 42)], 0.0)
            put([(x, 42) for x in range(68, 77)], 0.5)
            put([(x, y) for x in (68, 69) for y in (43, 44)], 0.0)
            put([(x, 62) for x in range(58, 68)], 0.0)                       # mouth, open
            put([(x, 63) for x in range(58, 68)], 0.0)
            put([(x, 64) for x in range(59, 67)], 0.0)
            put([(57, 63), (68, 63)], 0.5)
            put([(x, 65) for x in range(59, 67)], 1.0)
        put([(65, y) for y in range(48, 57)], 0.5)                           # nose shadow
        put([(61, 58), (65, 58)], 0.0)                                       # nostrils
        return p
    return features(paint(), False), features(paint(), True)


def witness(spec):
    """A witness in the box (16 x 14), from a spec (v1.0). Returns (steady,
    faltering). The same build as Lowry's: the body, the head, the face lit
    from one side (the candle on the box's ledge), then the features put a
    pixel at a time so the scaling doesn't smear them. Faltering moves only
    the brows, eyes and mouth, so the delta stays small and the colours
    never change.

    spec: light 'left'/'right'; dress: 'woman', 'farmer', 'elder',
    'minister', 'mayor'; head: 'hood', 'hair', 'bald', 'skullcap', 'wig';
    hair (0-1, how light); face (width, top, bottom); age (lines);
    look: (x offset of the eyes steady, faltering); mouth: 'set',
    'pressed', 'smug'; seed."""
    left = spec["light"] == "left"
    fw, ft, fb = spec.get("face", (22, 24, 72))
    cx = 64
    x0, x1 = cx - fw, cx + fw

    def L(x, lo, hi, g=0.9):
        return side(x, 20, 112, lo, hi, g) if left else side(x, 108, 16, lo, hi, g)

    def paint():
        c = Canvas(16, 14)
        dress = spec["dress"]
        # the body: shoulders, a coat or a gown, dark, lit on the candle side
        coat_ink = WHITE if dress in ("minister", "woman") else YELLOW
        top = 74 if dress != "mayor" else 72
        c.poly([(0, 112), (4, 94), (22, 80), (44, top), (84, top), (106, 80), (124, 94), (127, 112)],
               lambda x, y: L(x, 0.02, 0.36 if dress != "minister" else 0.24, 1.4), coat_ink)
        if dress == "mayor":
            # a laced coat: braid down the front, a chain of office
            c.line([(46, 76), (40, 112)], 0.9, 1.2, YELLOW + BR)
            c.line([(82, 76), (88, 112)], 0.5, 1.2, YELLOW)
            c.line([(44, 80), (54, 98), (64, 104), (74, 98), (84, 80)], 1.0, 1.5, YELLOW + BR)
            c.ellipse((60, 100, 68, 110), 1.0, YELLOW + BR)
            # the lace cravat, falling white
            c.poly([(54, 72), (74, 72), (72, 86), (68, 96), (60, 96), (56, 86)],
                   lambda x, y: L(x, 0.3, 1.0, 0.7), WHITE)
            c.line([(64, 74), (64, 94)], 0.45, 0.6)
        elif dress == "minister":
            # black gown, the white bands at the throat
            c.poly([(57, 74), (63, 74), (62, 92), (56, 92)], lambda x, y: L(x, 0.5, 1.0), WHITE)
            c.poly([(65, 74), (71, 74), (72, 92), (66, 92)], lambda x, y: L(x, 0.4, 0.9), WHITE)
        elif dress == "woman":
            # a dark gown, a falling band of linen at the neck
            c.poly([(42, 78), (54, 74), (64, 84), (74, 74), (86, 78), (80, 92), (64, 98), (48, 92)],
                   lambda x, y: L(x, 0.2, 0.95, 0.8), WHITE)
            c.line([(64, 84), (64, 98)], 0.15, 0.8)
        else:
            # a farmer's or an elder's coat, a plain shirt and neckcloth
            c.poly([(52, 74), (64, 86), (76, 74), (72, 92), (56, 92)],
                   lambda x, y: L(x, 0.2, 0.9, 0.8), WHITE)
            c.line([(46, 76), (58, 112)], 0.0, 1.0)              # the coat's edge
            c.line([(82, 76), (70, 112)], 0.0, 1.0)
            if dress == "elder":
                c.line([(64, 80), (64, 96)], 0.3, 0.6)
        # the neck, in shadow under the jaw
        c.poly([(cx - 12, fb - 8), (cx + 12, fb - 8), (cx + 14, 78), (cx - 14, 78)],
               lambda x, y: L(x, 0.06, 0.55) * (0.4 if y < 76 else 0.7), YELLOW)
        head = spec["head"]
        hv = spec.get("hair", 0.2)
        if head == "wig":
            # a full-bottomed periwig over the shoulders: lit on the candle
            # side, lost in the dark on the other, so it never rings the face
            c.ellipse((cx - 44, ft - 18, cx + 44, fb + 6), lambda x, y: L(x, 0.0, 0.7, 1.6), WHITE)
            c.poly([(cx - 46, 40), (cx - 30, 40), (cx - 24, 96), (cx - 42, 100)],
                   lambda x, y: L(x, 0.0, 0.65, 1.6), WHITE)
            c.poly([(cx + 30, 40), (cx + 46, 40), (cx + 42, 100), (cx + 24, 96)],
                   lambda x, y: L(x, 0.0, 0.65, 1.6), WHITE)
            for k in range(7):                                   # its curls, row on row
                y = 14 + k * 12
                c.line([(cx - 44, y), (cx - 36, y + 5), (cx - 28, y)], 0.2, 1.2)
                c.line([(cx + 28, y), (cx + 36, y + 5), (cx + 44, y)], 0.05, 1.2)
        elif head == "hood":
            # a black silk hood, the edge of a white cap just showing
            c.ellipse((cx - 34, ft - 18, cx + 34, fb + 8), lambda x, y: L(x, 0.04, 0.4, 1.4), WHITE)
            c.poly([(cx - 34, 50), (cx - 26, 90), (cx - 40, 100)], lambda x, y: L(x, 0.02, 0.3), WHITE)
            c.poly([(cx + 34, 50), (cx + 26, 90), (cx + 40, 100)], lambda x, y: L(x, 0.02, 0.3), WHITE)
        elif head == "hair":
            # his own hair, worn long, uncovered for the court
            c.ellipse((cx - 28, ft - 12, cx + 28, fb), lambda x, y: L(x, 0.02, 0.15 + hv * 0.5, 1.5), YELLOW)
            c.poly([(cx - 28, 40), (cx - 20, 40), (cx - 18, 78), (cx - 30, 74)],
                   lambda x, y: L(x, 0.02, 0.1 + hv * 0.4, 1.5), YELLOW)
            c.poly([(cx + 20, 40), (cx + 28, 40), (cx + 30, 74), (cx + 18, 78)],
                   lambda x, y: L(x, 0.02, 0.1 + hv * 0.4, 1.5), YELLOW)
        elif head == "bald":
            # thin white hair at the sides only
            c.ellipse((cx - 26, ft - 6, cx + 26, fb - 10), lambda x, y: L(x, 0.03, 0.55, 1.4), WHITE)
        elif head == "skullcap":
            c.ellipse((cx - 24, ft - 8, cx + 24, fb - 12), lambda x, y: L(x, 0.02, 0.2, 1.4), YELLOW)
        # the face
        face = [(x0 + 2, ft + 12), (x0 + 6, ft + 4), (x0 + 14, ft), (x1 - 14, ft), (x1 - 6, ft + 4),
                (x1 - 2, ft + 12), (x1 - 1, ft + 26), (x1 - 6, ft + 36), (cx + 8, fb - 2),
                (cx - 2, fb), (cx - 10, fb - 4), (x0 + 4, ft + 36), (x0, ft + 24)]

        def face_lum(x, y):
            v = L(x, 0.42, 1.0, 0.6)
            if y > fb - 6:
                v *= 0.8
            return v
        c.poly(face, face_lum, YELLOW)
        lit = [(x0 - 2, ft), (cx - 2, ft), (cx - 4, fb), (x0 - 2, fb - 12)] if left else \
              [(cx + 2, ft), (x1 + 2, ft), (x1 + 2, fb - 12), (cx + 4, fb)]
        c.poly(lit, None, YELLOW + BR)                            # the lit half bright
        if head == "skullcap":
            c.poly([(x0 + 2, ft + 10), (x0 + 6, ft - 4), (cx, ft - 8), (x1 - 6, ft - 4), (x1 - 2, ft + 10),
                    (cx, ft + 2)], 0.04)
        elif head == "bald":
            c.poly([(x0 + 4, ft + 8), (x0 + 10, ft - 4), (cx, ft - 8), (x1 - 10, ft - 4), (x1 - 4, ft + 8)],
                   lambda x, y: L(x, 0.35, 0.95, 0.7), YELLOW)
        elif head in ("hair", "wig", "hood"):
            hl = 0.04 if head != "wig" else 0.6
            c.poly([(x0 + 2, ft + 12), (x0 + 6, ft + 2), (x0 + 16, ft - 2), (x1 - 16, ft - 2), (x1 - 6, ft + 2),
                    (x1 - 2, ft + 12), (x1 - 8, ft + 6), (cx, ft + 4), (x0 + 8, ft + 6)],
                   (lambda x, y: L(x, 0.0, hl)) if head == "wig" else 0.04 + hv * 0.2,
                   WHITE if head == "wig" else None)
        ey = ft + 18
        c.ellipse((cx - 19, ey - 4, cx - 3, ey + 6), 0.85 if left else 0.6)     # the eyes, lit enough
        c.ellipse((cx + 1, ey - 4, cx + 16, ey + 6), 0.6 if left else 0.85)
        nx = cx - 2 if left else cx + 1
        c.poly([(nx - 3, ey + 2), (nx, ey - 4), (nx + 1, ey + 14), (nx - 3, ey + 16)], 1.0)
        ck = (cx - 17, ey + 8, cx - 7, ey + 17) if left else (cx + 6, ey + 8, cx + 16, ey + 17)
        c.ellipse(ck, 1.0)                                       # the near cheek
        if spec["dress"] == "mayor":
            c.ellipse((cx - 14, fb - 6, cx + 14, fb + 4), lambda x, y: L(x, 0.3, 0.9), YELLOW)  # a second chin
        return c.to_pic(spec["seed"])

    def features(p, falter):
        px = p.lum.load()

        def put(pts, v):
            for (x, y) in pts:
                if 0 <= x < 128 and 0 <= y < 112:
                    px[x, y] = int(v * 255)
        ey = ft + 18
        ex0, ex1 = (cx - 16, cx - 6), (cx + 4, cx + 13)          # the eyes' spans
        look = spec.get("look", (0, -3))[1 if falter else 0]
        lift = 2 if falter else 0
        bro = spec.get("brows", 0)                               # + lower, a frown
        # brows
        for (a, b), v in ((ex0, 0.25), (ex1, 0.25)):
            put([(x, ey - 4 + bro - lift - (1 if falter and a + 3 <= x <= b - 3 else 0))
                 for x in range(a, b + 1)], v)
        # eyes: a lid, the white, the iris (moved by look), the lower lid
        lid = spec.get("lids", 0) + (1 if falter else 0)         # heavy-lidded
        for (a, b), w in ((ex0, 1.0 if left else 0.75), (ex1, 0.75 if left else 1.0)):
            put([(x, y) for x in range(a, b + 1) for y in (ey, ey + 1)], w)
            put([(x, ey - 1) for x in range(a, b + 1)] + [(a - 1, ey), (b + 1, ey)], 0.0)
            if lid:
                put([(x, ey) for x in range(a, b + 1)], 0.5)
            m = (a + b) // 2 + look
            put([(x, y) for x in (m, m + 1) for y in (ey - 1 + lid, ey, ey + 1)], 0.0)
            put([(x, ey + 2) for x in range(a + 1, b)], 0.5)
        # nose shadow and nostrils
        nx = cx + 1 if left else cx - 2
        put([(nx, y) for y in range(ey + 6, ey + 15)], 0.5)
        put([(cx - 3, ey + 16), (cx + 1, ey + 16)], 0.0)
        my = ey + 21
        mouth = spec.get("mouth", "set")
        if not falter:
            if mouth == "smug":                                  # the Mayor, pleased
                put([(x, my) for x in range(cx - 7, cx + 6)], 0.0)
                put([(cx + 6, my - 1), (cx + 7, my - 2)], 0.0)
                put([(x, my + 1) for x in range(cx - 6, cx + 5)], 1.0)
            elif mouth == "pressed":
                put([(x, my) for x in range(cx - 6, cx + 5)], 0.0)
                put([(cx - 7, my + 1), (cx + 5, my + 1)], 0.25)  # turned down
                put([(x, my + 1) for x in range(cx - 5, cx + 4)], 1.0)
            else:
                put([(x, my) for x in range(cx - 7, cx + 6)], 0.0)
                put([(x, my + 1) for x in range(cx - 6, cx + 5)], 1.0)
        else:
            o = 3 if mouth == "smug" else 2                      # the Mayor's mouth falls open wider
            w = 4 if mouth == "smug" else 5
            for k in range(o):
                put([(x, my - 1 + k) for x in range(cx - w, cx + w)], 0.0)
            put([(cx - w - 1, my), (cx + w, my)], 0.5)
            put([(x, my - 1 + o) for x in range(cx - w + 1, cx + w - 1)], 1.0)
        for (x, y) in spec.get("lines", []):                     # age
            put([(x, y), (x, y + 1), (x, y + 2)], 0.5)
        return p
    return features(paint(), False), features(paint(), True)


WITNESSES = {
    # Margaret Wylie: a gentlewoman, Hugh Wylie's sister, in a black hood;
    # she looks straight at the bench, lips pressed; faltering, her eyes go
    # to the side, towards the house's people in the gallery
    "wylie": dict(light="left", dress="woman", head="hood", face=(20, 26, 72),
                  look=(0, 3), brows=1, mouth="pressed", seed=1720,
                  lines=[(50, 66), (77, 66)]),
    # William Dickey: a farmer, his own hair, frank; he has told this in
    # every kitchen on the island
    "dickey": dict(light="left", dress="farmer", head="hair", hair=0.35, face=(23, 24, 72),
                   look=(0, -3), seed=1721),
    # John Wilson: younger, thinner, lit from the other side; even steady,
    # his eyes slide towards Dickey in the court; faltering, they drop
    "wilson": dict(light="right", dress="farmer", head="hair", hair=0.15, face=(20, 25, 72),
                   look=(2, -3), seed=1722),
    # Hugh Gilmour: an elder, bald, white at the sides, lined; careful
    "gilmour": dict(light="left", dress="elder", head="bald", face=(22, 26, 72), lids=1,
                    look=(0, -3), seed=1723, lines=[(46, 52), (82, 52), (49, 68), (79, 68)]),
    # Mr Gordon: the minister, black skullcap, white bands, earnest
    "gordon": dict(light="right", dress="minister", head="skullcap", face=(21, 24, 72),
                   look=(0, -3), brows=-1, seed=1724, lines=[(52, 64), (75, 64)]),
    # Mayor Ellis: a full periwig, the chain of office, a second chin,
    # heavy-lidded and pleased with himself; faltering, his eyes come wide
    # open and his mouth falls open. The humour is his.
    "ellis": dict(light="left", dress="mayor", head="wig", face=(25, 26, 74), lids=1,
                  look=(0, 3), mouth="smug", seed=1725),
}


def _w(name):
    return lambda: witness(WITNESSES[name])


def block(p, pw, ph):
    """Cut the portrait out of a rendered screen: its size, pixels row by
    row, then attributes row by row."""
    scr = p.to_scr()
    out = bytearray([pw, ph])
    for y in range(ph * 8):
        a = ((y & 0xC0) << 5) | ((y & 7) << 8) | ((y & 0x38) << 2)
        out += scr[a:a + pw]
    for r in range(ph):
        out += scr[6144 + r * 32:6144 + r * 32 + pw]
    return bytes(out), scr


def falter_delta(scr0, scr1, pw, ph):
    """The cells that differ between the two renders, pixels only: the
    steady face's attributes stay (a render may make a changed cell
    BRIGHT or not; the swap must never touch colour, or it would clash)."""
    cells = []
    for r in range(ph):
        for c in range(pw):
            old, new = bytearray(), bytearray()
            for y in range(r * 8, r * 8 + 8):
                a = ((y & 0xC0) << 5) | ((y & 7) << 8) | ((y & 0x38) << 2) | c
                old.append(scr0[a])
                new.append(scr1[a])
            if old != new:
                cells.append((r, c, bytes(new), bytes(old)))
    out = bytearray([len(cells)])
    for r, c, new, old in cells:
        out += bytes([r, c]) + new + old
    return bytes(out), len(cells)


def preview(scr, pw, ph, path):
    tmp = os.path.join(HERE, "_tmp.png")
    scr_preview(scr, tmp, scale=1)
    Image.open(tmp).crop((0, 0, pw * 8, ph * 8)).resize((pw * 32, ph * 32), Image.NEAREST).save(path)
    os.remove(tmp)


# Kate (v0.7) is no longer shown (v1.0: out of the build; kate() kept)
PORTRAITS = [("isobel", isobel, 10, 12), ("lowry", lowry, 16, 14)] + \
    [(n, _w(n), 16, 14) for n in ("wylie", "dickey", "wilson", "gilmour", "gordon", "ellis")]

if __name__ == "__main__":
    import zx0
    for name, fn, pw, ph in PORTRAITS:
        pics = fn()
        if not isinstance(pics, tuple):
            pics = (pics,)
        raw, scr = block(pics[0], pw, ph)
        open(os.path.join(HERE, name + ".bin"), "wb").write(raw)
        preview(scr, pw, ph, os.path.join(HERE, name + ".png"))
        extra = ""
        if len(pics) > 1:
            _, scr1 = block(pics[1], pw, ph)
            scr1 = scr1[:6144] + scr[6144:]          # as the game shows it: the steady colours
            delta, n = falter_delta(scr, scr1, pw, ph)
            open(os.path.join(HERE, name + "_falter.bin"), "wb").write(delta)
            preview(scr1, pw, ph, os.path.join(HERE, name + "_falter.png"))
            extra = "; falters in %d cells (%d bytes)" % (n, len(delta))
        print("%s: %d x %d, %d bytes raw, %d packed%s" % (name, pw, ph, len(raw),
                                                          len(zx0.compress(raw)), extra))
