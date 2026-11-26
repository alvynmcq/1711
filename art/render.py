"""Picture renderer for 1711: draw with PIL in greyscale plus an ink-hint
layer, then turn it into a Spectrum screen (6912 bytes).

lum  : 'L' image, 0-255 brightness
hint : 'L' image, 0 = default ink; otherwise ink (1-7) + 8 if BRIGHT
Ordered (Bayer 8x8) dithering, black paper everywhere. Each 8x8 cell takes
the most common hinted ink in it (or the picture's default ink); BRIGHT if
the hint says so or the cell is mostly light.

Look: candle yellow and red on black, white for paper and moonlight.
"""
from PIL import Image, ImageDraw

W, H = 256, 192
K, BLUE, RED, MAG, GREEN, CYAN, YELLOW, WHITE = range(8)
BR = 8

BAYER8 = [[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
          [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
          [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
          [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]


class Pic:
    def __init__(self, rows=(0, 24), ink=WHITE, seed=1711):
        import random
        self.lum = Image.new("L", (W, H), 0)
        self.hint = Image.new("L", (W, H), 0)
        self.L = ImageDraw.Draw(self.lum)
        self.C = ImageDraw.Draw(self.hint)
        self.rows, self.ink = rows, ink
        self.rng = random.Random(seed)

    def poly(self, pts, v, ink=None):
        self.L.polygon(pts, fill=int(v * 255))
        if ink is not None:
            self.C.polygon(pts, fill=ink)

    def rect(self, x0, y0, x1, y1, v, ink=None):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], v, ink)

    def ellipse(self, box, v, ink=None):
        self.L.ellipse(box, fill=int(v * 255))
        if ink is not None:
            self.C.ellipse(box, fill=ink)

    def line(self, pts, v, width=1, ink=None):
        self.L.line(pts, fill=int(v * 255), width=width)
        if ink is not None:
            self.C.line(pts, fill=ink, width=width)

    def glow(self, cx, cy, r, v, ink=None, squash=1.0):
        """Soft light added round a point (candle, lit window)."""
        px = self.lum.load()
        hp = self.hint.load()
        for y in range(max(0, int(cy - r * squash)), min(H, int(cy + r * squash) + 1)):
            for x in range(max(0, int(cx - r)), min(W, int(cx + r) + 1)):
                d = ((x - cx) ** 2 + ((y - cy) / squash) ** 2) ** 0.5 / r
                if d < 1:
                    add = v * (1 - d) ** 2 * 255
                    px[x, y] = min(255, int(px[x, y] + add))
                    if ink is not None and d < 0.8 and hp[x, y] == 0:
                        hp[x, y] = ink

    def grain(self, amount=10):
        px = self.lum.load()
        for y in range(H):
            for x in range(W):
                v = px[x, y]
                if 8 < v < 247:
                    px[x, y] = max(0, min(255, v + self.rng.randint(-amount, amount)))

    def to_scr(self):
        scr = bytearray(6912)
        lum, hint = self.lum.load(), self.hint.load()
        r0, r1 = self.rows
        for cy in range(r0, r1):
            for cx in range(32):
                counts, light = {}, 0
                for y in range(cy * 8, cy * 8 + 8):
                    for x in range(cx * 8, cx * 8 + 8):
                        h = hint[x, y]
                        if h:
                            counts[h] = counts.get(h, 0) + 1
                        if lum[x, y] > 170:
                            light += 1
                h = max(counts, key=counts.get) if counts else self.ink
                ink, bright = h & 7, 1 if (h & BR or light >= 24) else 0
                scr[6144 + cy * 32 + cx] = (bright << 6) | ink
                for y in range(cy * 8, cy * 8 + 8):
                    for x in range(cx * 8, cx * 8 + 8):
                        if lum[x, y] * 64 > (BAYER8[y % 8][x % 8] + 0.5) * 255:
                            a = ((y & 0xC0) << 5) | ((y & 7) << 8) | ((y & 0x38) << 2) | (x >> 3)
                            scr[a] |= 0x80 >> (x & 7)
        return bytes(scr)


def scr_preview(scr, path, scale=2):
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        for x in range(W):
            a = ((y & 0xC0) << 5) | ((y & 7) << 8) | ((y & 0x38) << 2) | (x >> 3)
            on = scr[a] & (0x80 >> (x & 7))
            at = scr[6144 + (y // 8) * 32 + x // 8]
            c = at & 7 if on else (at >> 3) & 7
            lv = 255 if at & 64 else 215
            px[x, y] = ((lv if c & 2 else 0), (lv if c & 4 else 0), (lv if c & 1 else 0))
    im.resize((W * scale, H * scale), Image.NEAREST).save(path)
