#!/usr/bin/env python3
"""Build 1711.tap: BASIC loader -> loading screen -> game code (128K only).

Runs the art and script steps first:
  art/font.py          -> src/font.inc
  art/prologue_art.py  -> art/*.scr
  scripts/script.py    -> src/script.inc, src/pics.inc
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ORG = 0x6000

for script, cwd in (("font.py", "art"), ("prologue_art.py", "art"), ("script.py", "scripts")):
    subprocess.run([sys.executable, script], cwd=os.path.join(ROOT, cwd), check=True,
                   stdout=subprocess.DEVNULL)

os.chdir(os.path.join(ROOT, "src"))
subprocess.run(["pasmo", "--bin", "main.asm", "main.bin", "main.sym"], check=True)
code = open("main.bin", "rb").read()
end = ORG + len(code)
assert end <= 0xC000, "code must stay below C000h, where banks are paged (ends %04Xh)" % end

# loading screen: the house, rows 14-23 blank
screen = bytearray(open(os.path.join(ROOT, "art", "house.scr"), "rb").read())


def num(n):
    return str(n).encode() + bytes([0x0E, 0, 0, n & 255, n >> 8, 0])


BORDER, PAPER, INK, CLEAR, LOAD, SCREEN, POKE, CODE, RANDOMIZE, USR = \
    0xE7, 0xDA, 0xD9, 0xFD, 0xEF, 0xAA, 0xF4, 0xAF, 0xF9, 0xC0
line = (bytes([BORDER]) + num(0) + b":" + bytes([PAPER]) + num(0) + b":" +
        bytes([INK]) + num(7) + b":" + bytes([CLEAR]) + num(ORG - 1) + b":" +
        bytes([LOAD]) + b'""' + bytes([SCREEN]) + b":" +
        bytes([POKE]) + num(23739) + b"," + num(111) + b":" +
        bytes([LOAD]) + b'""' + bytes([CODE]) + b":" +
        bytes([RANDOMIZE, USR]) + num(ORG) + b"\r")
basic = bytes([0, 10]) + len(line).to_bytes(2, "little") + line


def block(flag, data):
    chk = flag
    for b in data:
        chk ^= b
    body = bytes([flag]) + data + bytes([chk])
    return len(body).to_bytes(2, "little") + body


def header(kind, name, length, p1, p2):
    return block(0, bytes([kind]) + name.ljust(10).encode() +
                 length.to_bytes(2, "little") + p1.to_bytes(2, "little") + p2.to_bytes(2, "little"))


tap = (header(0, "1711", len(basic), 10, len(basic)) + block(0xFF, basic) +
       header(3, "screen", 6912, 16384, 32768) + block(0xFF, bytes(screen)) +
       header(3, "1711", len(code), ORG, 32768) + block(0xFF, code))
open(os.path.join(ROOT, "1711.tap"), "wb").write(tap)
print("1711.tap: %d bytes; code %d bytes, %04Xh-%04Xh (%d free below C000h)"
      % (len(tap), len(code), ORG, end - 1, 0xC000 - end))
