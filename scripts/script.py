#!/usr/bin/env python3
"""Compile the game's scripted pages (title, prologue, credits) into
src/script.inc, and pack the pictures into src/pics.inc.

A script is a list of steps run by the engine's `run` (src/main.asm):

  ("cls", attr)                    clear the screen to one colour
  ("pic", name)                    unpack art/<name>.scr (ZX0) to the screen
  ("text", row, col, attr, s)      print s at once (own font, 6 px a char)
  ("type", row, col, attr, s)      print s a letter at a time (SPACE: rest at once)
  ("say", who, s)                  a line of dialogue in the text area:
                                   speaker label + wrapped, typed text
  ("story", attr, s)               a paragraph in the text area, wrapped + typed
  ("wait",)                        "SPACE" prompt, wait, then clear the text area
  ("pause", frames)
  ("border", n)
  ("clear",)                       clear the text area (rows TEXT0-23)
  ("choice", [(key, label)...])    wait for one of the keys; jump to that label
  ("label", name) / ("jump", name)
  ("night",)                       the night's screens (src/night.asm, data from
                                   scripts/night.py) until the clerk presses X
  ("end",)                         return to the caller

Each script is a chunk, packed with ZX0 and unpacked by the engine into
the script buffer (the same place as the night's text: a script never runs
while a night is unpacked). A ("night",) step ends its chunk: the steps
after it become a new chunk, which the engine loads when the night is over.
A jump or a choice to a label in another chunk becomes LOAD n, so such a
label must be the first thing in its chunk. Pictures go by number (pictab).

say/story keep a cursor in the text area and wrap at the right edge; a
"wait" clears the area and puts the cursor back at the top. The compiler
checks that nothing runs off the bottom.
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "art"))
from font import FONTW  # noqa: E402
from zx0 import compress  # noqa: E402

# opcodes (must match src/main.asm)
OP = dict(end=0, cls=1, pic=2, text=3, type=4, wait=5, pause=6, border=7,
          clrrows=8, jump=9, choice=10, night=11, load=12)

BLK, YEL, BYEL, WHT, BWHT, RED, BRED, CYN = 0x00, 0x06, 0x46, 0x07, 0x47, 0x02, 0x42, 0x05
TEXT0 = 15                        # first text row under a picture
MARGIN = 4                        # the engine's left margin in pixels
COLS = (256 - 2 * MARGIN) // FONTW  # characters per line from column 0 (41)
SPEAKERS = {"MEG": BWHT, "BOY": BRED}


def wrap(s, width):
    out, line = [], ""
    for word in s.split():
        if line and len(line) + 1 + len(word) > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word) if line else word
    if line:
        out.append(line)
    return out


class Compiler:
    def __init__(self, where=None, pics=()):
        self.out = []             # assembler lines of the chunk being compiled
        self.chunks = []          # (name, lines)
        self.where = where or {}  # label -> (chunk number, first in its chunk)
        self.found = {}
        self.pics = list(pics)
        self.stubs = {}
        self.row = TEXT0
        self.text0 = TEXT0
        self.empty = True

    def begin(self, name):
        if self.chunks or self.out:
            self.finish()
        self.cur = name
        self.out = ["%s:" % name]
        self.stubs = {}
        self.empty = True
        self.label(name)

    def finish(self):
        for name, n in self.stubs.items():           # far choices: LOAD stubs
            self.out.append("%s:" % name)
            self.out.append("        db %d,%d" % (OP["load"], n))
        self.chunks.append((self.cur, self.out))
        self.out = []

    def label(self, name):
        self.found[name] = (len(self.chunks), self.empty)

    def far(self, name):
        """None if name is in this chunk, else its chunk number."""
        n, first = self.where[name]
        if n == len(self.chunks):
            return None
        assert first, "%s is in another chunk but not at its start" % name
        return n

    def db(self, *vals):
        self.empty = False
        self.out.append("        db " + ",".join(str(v) for v in vals))

    def string(self, s):
        self.empty = False
        assert all(32 <= ord(c) < 128 for c in s), s
        self.out.append('        db "%s",0' % s.replace('"', "'"))

    def lines(self, op, attr, lines, indent=0):
        for ln in lines:
            assert self.row <= 22, "text runs off the screen: %r" % ln   # row 23 is the prompt
            self.db(OP[op], self.row, indent, attr)
            self.string(ln)
            self.row += 1

    def step(self, st):
        k = st[0]
        if k == "label":
            self.label(st[1])
            self.out.append("%s:" % st[1])
        elif k == "end":
            self.db(OP["end"])
        elif k == "night":
            self.db(OP["night"], len(self.chunks) + 1)
            self.begin(self.cur + "_after")
        elif k == "cls":
            self.db(OP["cls"], st[1])
            self.text0 = self.row = 1
        elif k == "pic":
            self.db(OP["pic"], self.pics.index(st[1]))
            self.text0 = self.row = TEXT0
        elif k in ("text", "type"):
            _, row, col, attr, s = st
            assert col * 8 + MARGIN + len(s) * FONTW <= 256, "too wide: %r" % s
            self.db(OP[k], row, col, attr)
            self.string(s)
        elif k == "story":
            self.lines("type", st[1], wrap(st[2], COLS))
            self.row += 1
        elif k == "say":
            who, s = st[1], st[2]
            body = wrap(s, COLS - 5)                   # 5 chars for "MEG: "
            assert self.row <= 22
            self.db(OP["text"], self.row, 0, SPEAKERS[who])
            self.string(who + ":")
            # the speech itself starts 30 px in: at col 3 plus FONTW*1 ~ "MEG: "
            for ln in body:
                assert self.row <= 22, "text runs off the screen: %r" % ln
                self.db(OP["type"], self.row, 4, YEL if who == "MEG" else BRED)
                self.string(ln)
                self.row += 1
        elif k == "wait":
            self.db(OP["wait"], self.text0)
            self.row = self.text0
        elif k == "clear":
            self.db(OP["clrrows"], self.text0, 24 - self.text0)
            self.row = self.text0
        elif k == "pause":
            self.db(OP["pause"], st[1])
        elif k == "border":
            self.db(OP["border"], st[1])
        elif k == "jump":
            n = self.far(st[1])
            if n is None:
                self.db(OP["jump"])
                self.out.append("        dw %s" % st[1])
            else:
                self.db(OP["load"], n)
        elif k == "choice":
            self.db(OP["choice"], len(st[1]))
            for key, label in st[1]:
                n = self.far(label)
                if n is not None:
                    label = "go_%s_%d" % (self.cur, n)
                    self.stubs[label] = n
                self.out.append("        db %d" % ord(key))
                self.out.append("        dw %s" % label)
        else:
            raise ValueError(k)


def compile_all(scripts, pics, where=None):
    c = Compiler(where, pics)
    for name, steps in scripts:
        c.begin(name)
        for st in steps:
            c.step(st)
    c.finish()
    return c


def build(scripts, pics):
    # two passes: the first finds which chunk each label is in
    probe = Compiler(None, pics)
    probe.far = lambda name: None                 # pass 1: no LOADs yet
    for name, steps in scripts:
        probe.begin(name)
        for st in steps:
            probe.step(st)
    probe.finish()
    c = compile_all(scripts, pics, probe.found)
    src = os.path.join(ROOT, "src")
    names = []
    for n, (name, lines) in enumerate(c.chunks):
        open(os.path.join(src, "chunk%d.inc" % n), "w").write(
            "; generated by scripts/script.py: chunk %d (%s)\n" % (n, name) +
            "\n".join(lines) + "\n")
        names.append(name)
    open(os.path.join(src, "chunks.txt"), "w").write("\n".join(names) + "\n")
    lines, total = ["; generated by scripts/script.py: pictures, ZX0"], 0
    lines.append("pictab: dw " + ",".join("pic_%s" % p for p in pics))
    for name in pics:
        data = open(os.path.join(ROOT, "art", name + ".scr"), "rb").read()
        assert len(data) == 6912
        comp = compress(data)
        total += len(comp)
        lines.append("pic_%s:   ; %d bytes" % (name, len(comp)))
        for k in range(0, len(comp), 24):
            lines.append("        db " + ",".join(str(b) for b in comp[k:k + 24]))
    open(os.path.join(ROOT, "src", "pics.inc"), "w").write("\n".join(lines) + "\n")
    print("%d script chunks + pics.inc written (pictures %d bytes packed)"
          % (len(names), total))


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from story import SCRIPTS, PICS
    build(SCRIPTS, PICS)
