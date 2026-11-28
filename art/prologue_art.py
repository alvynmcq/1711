#!/usr/bin/env python3
"""The prologue pictures. Each fills character rows 0-13 (112 pixels);
the game prints the story text underneath.

  house  : Braehead House at night, one lit kitchen window
  window : the kitchen window from inside, a pane broken, the boy's arm
           through it holding the book open
  grave  : the gable end at dusk, the boy digging with a sword
v1.0, the trial:
  court     : the court from the gallery at six in the morning
  dock      : the accused in the dock, eight ordinary women
  isobel_in : Isobel brought in, held up between two women
  pillory   : the market place, the castle, the pillory far off
Writes art/<name>.scr and art/<name>.png (preview).
"""
import os
from render import Pic, scr_preview, K, RED, YELLOW, WHITE, BR

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = (0, 14)
PH = 112                     # picture height in pixels


def house():
    p = Pic(ROWS, ink=WHITE, seed=1710)
    for y in range(PH):                                  # night sky, faintly lighter low down
        p.line([(0, y), (255, y)], 0.03 + 0.30 * (y / 70) ** 1.5 if y < 70 else 0.33)
    for _ in range(40):
        x, y = p.rng.randrange(256), p.rng.randrange(2, 50)
        p.lum.putpixel((x, y), 255)
    p.ellipse((206, 10, 220, 24), 1.0, WHITE + BR)       # moon behind thin cloud
    p.rect(194, 15, 238, 17, 0.0)
    p.poly([(0, 80), (40, 72), (110, 76), (220, 70), (256, 74), (256, PH), (0, PH)], 0.0)  # hills
    # the house: long, two storeys, a chimney at each gable
    x0, x1, eaves, ridge, ground = 58, 196, 52, 36, 96
    p.rect(x0, eaves, x1, ground, 0.0)
    p.poly([(x0 - 4, eaves), (x0 + 14, ridge), (x1 - 14, ridge), (x1 + 4, eaves)], 0.0)
    for cx in (x0 + 6, x1 - 16):
        p.rect(cx, ridge - 12, cx + 10, ridge + 2, 0.0)
        p.rect(cx - 1, ridge - 14, cx + 11, ridge - 11, 0.0)
    p.line([(x0 + 14, ridge), (x1 - 14, ridge)], 0.8)               # moonlit ridge
    p.line([(x1 - 14, ridge), (x1 + 4, eaves)], 0.6)
    p.glow(103, 82, 40, 0.6, YELLOW, squash=0.6)                    # the kitchen window's light
    p.rect(x0, eaves, x1, eaves + 1, 0.0)
    for wx in (76, 108, 146, 172):                                  # dark upper windows
        p.rect(wx, 58, wx + 9, 68, 0.0)
    p.rect(98, 76, 108, 87, 1.0, YELLOW + BR)
    p.line([(103, 76), (103, 87)], 0.0)
    p.line([(98, 81), (108, 81)], 0.0)
    # dry-stone wall in front, its top stones catching the moon
    p.rect(0, 97, 255, PH - 1, 0.0)
    for x in range(0, 256, 6):
        if 118 <= x <= 136:
            continue
        p.line([(x + 1, 96 + (x * 7) % 3), (x + 4, 96 + (x * 7) % 3)], 0.7)
    for gx in range(120, 136, 4):                                   # the gate
        p.line([(gx, 94), (gx, 102)], 0.5)
    p.line([(118, 97), (136, 97)], 0.5)
    p.grain(4)
    return p


def window():
    p = Pic(ROWS, ink=YELLOW, seed=1711)
    p.rect(0, 0, 255, PH - 1, 0.0)
    ox0, oy0, ox1, oy1 = 60, 18, 196, 92                            # the window opening
    for y in range(oy0, oy1):                                       # outside: moonlit sky
        p.line([(ox0, y), (ox1, y)], 0.30 + 0.35 * ((y - oy0) / (oy1 - oy0)), ink=WHITE)
    # the boy beyond the glass, close: bonnet, hunched shoulders, blanket
    p.ellipse((140, 26, 176, 56), 0.0, WHITE)
    p.poly([(124, 92), (132, 60), (148, 48), (170, 48), (186, 62), (194, 92)], 0.0, WHITE)
    p.poly([(150, 40), (168, 38), (172, 60), (146, 62)], 0.0, WHITE)  # arm across his face
    # leaded panes ("quarries"): a diamond lattice in the opening only
    for k in range(-160, 200, 14):
        p.line([(ox0 + k, oy0), (ox0 + k + 74, oy1)], 0.0, 1)
        p.line([(ox1 - k, oy0), (ox1 - k - 74, oy1)], 0.0, 1)
    p.rect(126, oy0, 129, oy1, 0.0)                                  # mullion
    # walls and reveals over the lattice's ends
    p.poly([(0, 0), (256, 0), (220, 0), (196, oy0), (ox0, oy0), (36, 0)], 0.0)
    p.poly([(0, 0), (36, 0), (ox0, oy0), (ox0, oy1), (30, PH), (0, PH)], 0.0)
    p.poly([(36, 0), (ox0, oy0), (ox0, oy1), (30, PH)], 0.22)        # left reveal
    p.poly([(256, 0), (220, 0), (ox1, oy0), (ox1, oy1), (226, PH), (256, PH)], 0.0)
    p.poly([(220, 0), (ox1, oy0), (ox1, oy1), (226, PH)], 0.12)      # right reveal
    p.poly([(36, 0), (220, 0), (ox1, oy0), (ox0, oy0)], 0.16)        # lintel
    p.poly([(30, PH), (ox0, oy1), (ox1, oy1), (226, PH)], 0.3)       # the sill
    # the broken quarry, jagged, and the arm reaching through it
    p.poly([(110, 50), (122, 40), (134, 52), (122, 64)], 0.0)
    for (a, b) in (((110, 50), (114, 47)), ((122, 40), (120, 45)), ((134, 52), (129, 52)), ((122, 64), (123, 59))):
        p.line([a, b], 1.0, 1, WHITE + BR)
    p.poly([(150, 62), (128, 50), (112, 58), (92, 70), (98, 78), (118, 66), (140, 70)], 0.12, WHITE)  # ragged sleeve
    p.poly([(96, 68), (86, 70), (86, 78), (96, 78)], 0.55, WHITE)   # hand
    # the book, held open towards the room
    p.poly([(62, 78), (80, 70), (90, 80), (72, 88)], 0.95, WHITE + BR)
    p.poly([(80, 70), (98, 66), (106, 76), (90, 80)], 0.85, WHITE + BR)
    p.line([(80, 70), (90, 80)], 0.1)
    for i in range(4):                                              # lines of print
        p.line([(66 + 2 * i, 79 + 2 * i), (80 + 2 * i, 73 + 2 * i)], 0.2)
        p.line([(84 + 2 * i, 72 + 2 * i), (98 + 2 * i, 69 + 2 * i)], 0.2)
    for (x, y) in ((140, 98), (152, 101), (166, 96), (132, 103)):   # glass on the sill
        p.poly([(x, y), (x + 5, y - 2), (x + 3, y + 2)], 1.0, WHITE + BR)
    # the candle on the sill, left
    p.glow(44, 86, 40, 0.8, YELLOW, squash=0.9)
    p.rect(41, 88, 47, 106, 0.9, WHITE)
    p.ellipse((41, 77, 47, 87), 1.0, YELLOW + BR)
    p.grain(6)
    return p


def grave():
    p = Pic(ROWS, ink=WHITE, seed=1712)
    hz = 84
    for y in range(hz):                                  # dusk sky, pale low down
        p.line([(0, y), (255, y)], 0.06 + 0.62 * (y / hz) ** 2)
    p.rect(0, hz, 255, PH - 1, 0.0)                      # the garden, black
    # the gable end of the house, right; a broken window glowing
    p.poly([(168, PH), (168, 30), (214, 4), (256, 26), (256, PH)], 0.0)
    p.rect(220, 0, 232, 12, 0.0)                                    # chimney
    p.rect(196, 50, 212, 66, 0.95, YELLOW + BR)                     # the parlour window, lit
    p.line([(204, 50), (204, 66)], 0.0)
    p.line([(196, 58), (212, 58)], 0.0)
    p.poly([(206, 51), (211, 51), (211, 57), (208, 54)], 0.0)       # its broken quarry
    # the garden wall, left, black against the sky
    p.poly([(0, 66), (96, 70), (96, hz), (0, hz)], 0.0)
    for x in range(0, 96, 5):
        p.rect(x, 64 + (x * 3) % 4, x + 4, 70, 0.0)
    # the boy, a silhouette against the last light, digging
    bx, by = 128, 92
    p.poly([(bx - 13, by), (bx - 8, by - 34), (bx + 8, by - 38), (bx + 14, by - 6), (bx + 26, by + 2), (bx + 2, by + 4)], 0.0)
    p.ellipse((bx - 6, by - 52, bx + 10, by - 34), 0.0)             # bonnet
    p.line([(bx + 6, by - 30), (bx + 30, by - 2)], 0.0, 4)          # arm
    p.line([(bx + 28, by - 6), (bx + 46, by + 14)], 1.0, 2, WHITE + BR)   # the sword, catching light
    # the turned earth, a grave's length, faint
    p.poly([(bx + 36, by + 8), (bx + 92, by + 6), (bx + 96, by + 12), (bx + 34, by + 14)], 0.22)
    p.grain(4)
    return p


# ---- the trial (v1.0) ----

def court():
    """The court from the gallery at six in the morning: the three judges
    at the bench, candles along it; the clerk's table, the witness box on
    the left with its candle, the dock on the right; the gallery's rail
    across the foreground."""
    p = Pic(ROWS, ink=YELLOW, seed=1731)
    p.rect(0, 0, 255, PH - 1, 0.0)
    # the tall windows behind the bench, the first grey of the morning
    for wx in (40, 112, 184):
        p.rect(wx, 4, wx + 30, 34, 0.14, WHITE)
        p.line([(wx + 15, 4), (wx + 15, 34)], 0.0)
        p.line([(wx, 18), (wx + 30, 18)], 0.0)
    # the bench, high and long, panelled
    p.rect(24, 50, 232, 62, 0.20)
    for x in range(30, 232, 16):
        p.rect(x, 52, x + 11, 60, 0.10)
    # three judges: wigs catching the light, dark gowns; Lyle on the left
    for jx in (88, 128, 168):
        p.poly([(jx - 13, 50), (jx - 9, 36), (jx + 9, 36), (jx + 13, 50)], 0.06)
        p.ellipse((jx - 10, 22, jx + 10, 42), 0.55, WHITE)              # the wig
        p.ellipse((jx - 5, 26, jx + 5, 38), 0.7, YELLOW)                # the face
        p.rect(jx - 2, 41, jx + 2, 46, 0.9, WHITE + BR)                 # the bands
    # candles along the bench
    for cx in (52, 108, 148, 204):
        p.rect(cx - 1, 42, cx + 1, 49, 0.9, WHITE)
        p.glow(cx, 40, 16, 0.75, YELLOW, squash=0.8)
        p.ellipse((cx - 1, 37, cx + 1, 41), 1.0, YELLOW + BR)
    # the clerk's table, papers on it
    p.rect(92, 72, 164, 78, 0.18)
    for (x, y) in ((100, 70), (118, 71), (138, 70)):
        p.poly([(x, y), (x + 12, y - 1), (x + 13, y + 3), (x + 1, y + 4)], 0.9, WHITE)
    # the witness box, left, with its candle (where Lowry stood)
    p.rect(14, 70, 50, 92, 0.14)
    p.ellipse((26, 58, 38, 70), 0.4, YELLOW)
    p.glow(46, 66, 18, 0.6, YELLOW)
    p.ellipse((45, 61, 47, 65), 1.0, YELLOW + BR)
    # the dock, right: a row of heads behind the rail, in the dark
    p.rect(186, 76, 250, 92, 0.12)
    for hx in range(192, 248, 8):
        p.ellipse((hx - 3, 66, hx + 3, 74), 0.25, WHITE)
    # the gallery's rail and balusters across the foreground
    p.rect(0, 96, 255, 99, 0.3)
    for x in range(4, 256, 12):
        p.rect(x, 100, x + 4, PH - 1, 0.12)
    p.grain(4)
    return p


def dock():
    """The accused in the dock: eight women, ordinary, in their own caps and
    shawls, lit from below by the dock's candle; a mother and daughter side
    by side. Faces, not monsters: no one is marked out."""
    p = Pic(ROWS, ink=WHITE, seed=1732)
    p.rect(0, 0, 255, PH - 1, 0.0)
    xs = [22, 50, 80, 110, 142, 172, 202, 232]
    hs = [36, 40, 30, 38, 34, 42, 36, 38]          # heights differ: tall, small, old, young
    for i, (x, top) in enumerate(zip(xs, hs)):
        # a shawl over the shoulders
        p.poly([(x - 15, 96), (x - 12, top + 34), (x, top + 28), (x + 12, top + 34), (x + 15, 96)],
               0.16 + 0.06 * (i % 3), WHITE)
        # the face
        p.ellipse((x - 8, top + 6, x + 8, top + 26), 0.62, YELLOW)
        p.ellipse((x - 7, top + 8, x + 1, top + 24), 0.85, YELLOW + BR)  # lit from the left, below
        # a linen cap, lit on the left only, so it never rings the face
        p.poly([(x - 10, top + 12), (x - 9, top + 2), (x, top - 2), (x + 8, top + 1), (x + 4, top + 6),
                (x - 4, top + 5), (x - 7, top + 12)], 0.75, WHITE)
        # eyes and mouth, a stroke each: they look at the bench
        p.line([(x - 5, top + 14), (x - 2, top + 14)], 0.1)
        p.line([(x + 2, top + 14), (x + 5, top + 14)], 0.15)
        p.line([(x - 3, top + 21), (x + 2, top + 21)], 0.2)
    # the dock's rail, and its candle on the ledge
    p.rect(0, 90, 255, 95, 0.35)
    p.rect(0, 96, 255, PH - 1, 0.08)
    p.glow(128, 92, 70, 0.35, YELLOW, squash=0.5)
    p.rect(127, 82, 129, 89, 0.9, WHITE)
    p.ellipse((126, 78, 130, 82), 1.0, YELLOW + BR)
    p.grain(4)
    return p


def isobel_in():
    """Isobel brought in: held up between two women of the house in the
    middle of the court floor, her head fallen to one side, eyes closed. A
    frightened young woman, small in the room."""
    p = Pic(ROWS, ink=YELLOW, seed=1733)
    p.rect(0, 0, 255, PH - 1, 0.0)
    # the bench, far behind, its candles
    p.rect(40, 18, 216, 28, 0.12)
    for cx in (70, 128, 186):
        p.glow(cx, 14, 12, 0.5, YELLOW)
        p.ellipse((cx - 1, 11, cx + 1, 15), 1.0, YELLOW + BR)
    # the floor: flagstones, in the light of the box's candle
    for y in (60, 72, 88, 108):
        p.line([(0, y), (255, y)], 0.08)
    # the two women, dark, holding her by the arms
    for wx, lit in ((96, 0.3), (160, 0.12)):
        p.poly([(wx - 14, PH), (wx - 10, 54), (wx, 46), (wx + 10, 54), (wx + 14, PH)], lit * 0.6, WHITE)
        p.ellipse((wx - 7, 30, wx + 7, 48), lit + 0.2, YELLOW)
        p.poly([(wx - 9, 36), (wx - 8, 28), (wx, 26), (wx + 8, 28), (wx + 6, 32), (wx - 6, 32)], lit, WHITE)
    # Isobel between them, in a pale gown, smaller, her head to one side
    p.poly([(116, PH), (118, 60), (128, 52), (138, 60), (142, PH)], 0.55, WHITE)
    p.line([(118, 62), (104, 70)], 0.5, 4, WHITE)                    # her arms, held
    p.line([(138, 62), (152, 70)], 0.4, 4, WHITE)
    p.ellipse((121, 34, 135, 52), 0.85, YELLOW + BR)                # the face, tilted
    p.poly([(120, 40), (122, 32), (130, 30), (137, 34), (134, 36), (124, 37)], 0.15)  # dark hair
    p.line([(124, 43), (127, 44)], 0.1)                             # eyes closed
    p.line([(130, 44), (133, 43)], 0.1)
    p.line([(126, 48), (130, 48)], 0.35)
    p.glow(128, 60, 40, 0.25, YELLOW)
    p.grain(4)
    return p


def pillory():
    """The market place at Carrickfergus, a grey morning: the castle on the
    shore, far off; the pillory on its platform above the crowd, two
    figures bent in it, small and far, no faces; the crowd dark and still.
    Distant and plain."""
    p = Pic(ROWS, ink=WHITE, seed=1734)
    hz = 76
    for y in range(hz):                                              # a low grey sky
        p.line([(0, y), (255, y)], 0.10 + 0.22 * (y / hz) ** 1.5)
    p.rect(0, hz, 255, PH - 1, 0.0)
    # the castle on the shore, left: the keep, battlements, the curtain wall
    p.rect(16, 30, 44, hz, 0.0)
    for x in range(16, 44, 6):
        p.rect(x, 26, x + 3, 30, 0.0)
    p.poly([(0, hz), (0, 56), (16, 54), (16, hz)], 0.0)
    p.poly([(44, hz), (44, 52), (84, 58), (84, hz)], 0.0)
    for x in range(44, 84, 6):
        p.rect(x, 50 + (x - 44) // 7, x + 3, 54 + (x - 44) // 7, 0.0)
    # roofs of the town, right
    for (x, w, h) in ((168, 26, 12), (196, 24, 18), (222, 34, 10)):
        p.poly([(x, hz), (x, hz - h), (x + w // 2, hz - h - 8), (x + w, hz - h), (x + w, hz)], 0.0)
    # the pillory: the platform, the post, the board with two heads in it
    p.rect(108, 62, 152, hz, 0.0)
    p.rect(128, 30, 131, 62, 0.0)
    p.rect(112, 40, 148, 44, 0.0)
    for hx in (118, 140):
        p.ellipse((hx - 3, 36, hx + 3, 42), 0.0)                    # a head through the board
        p.poly([(hx - 2, 44), (hx + 6 if hx < 128 else hx - 6, 46), (hx + 6 if hx < 128 else hx - 6, 62),
                (hx - 1, 62)], 0.0)                                 # bent behind it
    # the crowd, a dark mass in the foreground, below the platform
    for x in range(-4, 256, 8):
        h = (x * 7) % 7
        p.ellipse((x, hz - 4 + h, x + 8, hz + 4 + h), 0.0)
    p.grain(3)
    return p

if __name__ == "__main__":
    for name, fn in (("house", house), ("window", window), ("grave", grave), ("court", court),
                     ("dock", dock), ("isobel_in", isobel_in), ("pillory", pillory)):
        scr = fn().to_scr()
        open(os.path.join(HERE, name + ".scr"), "wb").write(scr)
        scr_preview(scr, os.path.join(HERE, name + ".png"))
        print(name + ".scr written")
