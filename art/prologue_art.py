#!/usr/bin/env python3
"""The prologue pictures. Each fills character rows 0-13 (112 pixels);
the game prints the story text underneath.

  house  : Braehead House at night, one lit kitchen window
  window : the kitchen window from inside, a pane broken, the boy's arm
           through it holding the book open
  grave  : the gable end at dusk, the boy digging with a sword
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


if __name__ == "__main__":
    for name, fn in (("house", house), ("window", window), ("grave", grave)):
        scr = fn().to_scr()
        open(os.path.join(HERE, name + ".scr"), "wb").write(scr)
        scr_preview(scr, os.path.join(HERE, name + ".png"))
        print(name + ".scr written")
