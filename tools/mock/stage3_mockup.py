"""Mockup of the stage 3 cross-examination screen, at 256x192 with the
game's own 6-pixel font (art/font.py). Three frames: testimony, the
record (ENTER), HOLD, SIR!. The portrait is a placeholder."""
import sys
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "..", "..", "art"))
from font import G, FONTW
from PIL import Image, ImageDraw

K = (0, 0, 0)
YEL, BYEL = (0xD7, 0xD7, 0), (0xFF, 0xFF, 0)
WHT, BWHT = (0xD7, 0xD7, 0xD7), (0xFF, 0xFF, 0xFF)
BRED = (0xFF, 0, 0)
RED = (0xD7, 0, 0)


def text(px, row, col, s, ink, tall=False, spacing=0):
    x = col * FONTW
    for ch in s:
        rows = G.get(ch, G[" "])
        for gy, r in enumerate(rows):
            for gx, c in enumerate(r):
                if c == "#":
                    if tall:
                        for dy in (0, 1):
                            px[x + gx, row * 8 + gy * 2 + dy] = ink
                    else:
                        px[x + gx, row * 8 + gy] = ink
        x += FONTW + spacing
    assert x <= 256, (s, x)


def wrap(s, width=40):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + (1 if line else 0) > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w) if line else w
    out.append(line)
    return out


def rule(px, row, label, ink=YEL):
    y = row * 8 + 4
    for x in range(6, 250, 2):
        px[x, y] = ink
    w = len(label) * FONTW
    x0 = (256 - w) // 2
    for x in range(x0 - 4, x0 + w + 4):
        px[x, y] = K
    text(px, row, x0 / FONTW, label, ink)


def marks(px, struck):
    # eight hour marks, top right: little upright candles; struck ones crossed
    for i in range(8):
        x = 204 + i * 6
        for y in range(1, 7):
            px[x + 2, y] = BYEL if i >= struck else YEL
            px[x + 3, y] = BYEL if i >= struck else YEL
        if i < struck:
            for d in range(6):
                px[x + d, 6 - d] = K
                px[x + d, 1 + d] = RED if False else K


def portrait(px, falter):
    # placeholder face, 128x112 at columns 8-23 (x 64-191), rows 2-15 (y 16-127)
    ox, oy = 64, 16
    im = Image.new("L", (128, 112), 0)
    d = ImageDraw.Draw(im)
    d.polygon([(0, 112), (8, 92), (34, 80), (94, 80), (120, 92), (127, 112)], fill=90)  # shawl
    d.polygon([(44, 80), (64, 96), (84, 80), (78, 112), (50, 112)], fill=200)           # kerchief
    d.rectangle([54, 66, 74, 82], fill=110)                                             # neck
    d.ellipse([34, 14, 94, 64], fill=40)                                                # cap shadow
    d.polygon([(34, 34), (40, 14), (64, 6), (88, 14), (94, 34), (86, 24), (64, 18), (42, 24)],
              fill=230)                                                                 # linen cap
    d.ellipse([40, 22, 88, 76], fill=170)                                               # face
    d.ellipse([40, 22, 60, 76], fill=230)                                               # lit side
    bayer = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    p = im.load()
    for y in range(112):
        for x in range(128):
            v = p[x, y] / 255 * 16
            if v > bayer[y % 4][x % 4]:
                ink = BWHT if 40 <= x < 88 and 22 <= y < 78 and v > 9 else (WHT if v > 6 else YEL)
                px[ox + x, oy + y] = ink
    # features, a pixel at a time
    def put(pts, c):
        for (x, y) in pts:
            px[ox + x, oy + y] = c
    eye_y = 44 if falter else 42
    for ex in (50, 70):
        put([(ex + i, 40) for i in range(7)], K)                 # brows
        put([(ex + i, eye_y) for i in range(7)], K)              # lids
        if falter:
            put([(ex + 2, eye_y + 1), (ex + 3, eye_y + 1)], K)   # looking down
        else:
            put([(ex + 3, eye_y - 1), (ex + 3, eye_y + 1), (ex + 2, eye_y), (ex + 4, eye_y)], K)
    put([(63, y) for y in range(46, 55)], K)                     # nose
    if falter:
        put([(58 + i, 63) for i in range(10)] + [(60 + i, 65) for i in range(6)]
            + [(58, 64), (67, 64)], K)                           # mouth open, unsure
    else:
        put([(57 + i, 64) for i in range(12)], K)                # mouth level


def frame(kind):
    im = Image.new("RGB", (256, 192), K)
    px = im.load()
    text(px, 0, 1, "MARGARET LOWRY, servant", BWHT)
    marks(px, 1)
    text(px, 1, 1, "A quarter past seven", YEL)
    line = ("It was rolled up close, my lord, and tied hard with "
            "nine strange knots.")
    if kind == "record":
        text(px, 2, 1, "THE COURT RECORD", BWHT)
        facts = ["The apron: five knots.",
                 "Lowry found the apron on the floor.",
                 "None would loose the knots but she.",
                 "The apron: nine knots, she found it.",
                 "She never saw them before.",
                 "A fit as soon as she saw them.",
                 "Wilson's words are Dickey's.",
                 "Thirty women brought in: no fit.",
                 "None knew Janet Moore was coming.",
                 "Mr Gordon sent for Janet Moore."]
        for i, f in enumerate(facts):
            sel = i == 0
            text(px, 4 + i, 1, ">" if sel else " ", BWHT)
            text(px, 4 + i, 3, "%d" % ((i + 1) % 10), BWHT if sel else YEL)
            text(px, 4 + i, 5, f, BWHT if sel else YEL)
        text(px, 15, 5, "Sworn by Margaret Lowry, 3rd March.", WHT)
    else:
        portrait(px, falter=(kind == "hold"))
    rule(px, 16, "3 of 6")
    if kind == "hold":
        text(px, 17, 11, "HOLD, SIR!", BRED, tall=True, spacing=3)
        for i, l in enumerate(wrap("On the 3rd of March you swore five knots. "
                                   "How came you to swear nine?")):
            text(px, 19 + i, 1, l, BWHT)
        text(px, 21, 1, "Justice Ormsby puts down his pen.", YEL)
        text(px, 22, 1, "SPACE  on", WHT)
    else:
        for i, l in enumerate(wrap("'" + line + "'")):
            text(px, 17 + i, 1, l, WHT)
        text(px, 21, 1, "Justice Ormsby writes steadily.", YEL)
        if kind == "record":
            text(px, 22, 1, "Q A  a fact   ENTER  present   X  back", WHT)
        else:
            text(px, 22, 1, "O P  lines   SPACE  press   ENTER  record", WHT)
    text(px, 23, 1, "'Go on, Mrs Lowry.'", YEL)
    return im


def bordered(im, colour, b=24):
    out = Image.new("RGB", (256 + 2 * b, 192 + 2 * b), colour)
    out.paste(im, (b, b))
    return out


frames = [bordered(frame("testimony"), K), bordered(frame("record"), K),
          bordered(frame("hold"), BRED)]
S = 3
W, H = frames[0].size
sheet = Image.new("RGB", (W * S * 3 + 40, H * S + 60), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for i, (f, cap) in enumerate(zip(frames, ["1  Testimony", "2  The record (ENTER)",
                                         "3  HOLD, SIR! (border flash)"])):
    sheet.paste(f.resize((W * S, H * S), Image.NEAREST), (10 + i * (W * S + 10), 50))
    d.text((10 + i * (W * S + 10), 15), cap, fill=(220, 220, 220))
sheet.save("docs/stage3_mockup.png")
for i, f in enumerate(frames):
    f.resize((W * S, H * S), Image.NEAREST).save("/tmp/frame%d.png" % (i + 1))
print("ok")
