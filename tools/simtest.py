#!/usr/bin/env python3
"""Run a Night Porter snapshot with scripted keys; save screens, log AY + beeper.

Needs SkoolKit (pip install skoolkit). Make a snapshot at the title screen first:
  tap2sna.py -c machine=128 --start <title address from porter.sym> porter.tap t128.z80
  (machine=48 for the 48K path)
Then e.g.:
  python3 tools/simtest.py t128.z80 out "100:SPACE" "300:SPACE" "500:SPACE" "800:9" --shots 850 --frames 1000
"frame:addr=val,..." pokes memory at that frame (e.g. to force an anomaly).

usage: tools/simtest.py SNAP OUTPREFIX "frame:keys" ... [--shots f1,f2,...] [--frames N]
keys: space-separated skoolkit key names held for 6 frames (e.g. 'SPACE', '1', 'r').
"""
import sys
from skoolkit import CSimulator
from skoolkit.snapshot import Snapshot
from skoolkit.simutils import from_snapshot
from skoolkit.pagingtracer import PagingTracer, Memory
from skoolkit.kbtracer import KEYS
from PIL import Image

snap, prefix = sys.argv[1], sys.argv[2]
events, shots, nframes, pokes = {}, set(), 500, {}
args = sys.argv[3:]
i = 0
while i < len(args):
    a = args[i]
    if a == '--shots':
        shots = {int(x) for x in args[i + 1].split(',')}
        i += 2
        continue
    if a == '--frames':
        nframes = int(args[i + 1])
        i += 2
        continue
    f, keys = a.split(':', 1)
    if '=' in keys:
        pokes.setdefault(int(f), []).extend(
            (int(k, 0), int(v, 0)) for k, v in (p.split('=') for p in keys.split(',')))
    else:
        events[int(f)] = keys.split()
    i += 1

s = Snapshot.get(snap)
sim = from_snapshot(CSimulator, s, config={'fast_djnz': False, 'fast_ldir': False})
mem = sim.memory
is128 = isinstance(mem, Memory)


class T(PagingTracer):
    def __init__(self):
        self.simulator = sim
        self.out7ffd = s.out7ffd
        self.outfffd = 0
        self.ay = [0] * 16
        self.border = 0
        self.outfe = 0
        self.keyboard = [0] * 8
        self.aylog = []
        self.beeps = 0

    def read_port(self, registers, port):
        if port & 0xC002 == 0xC000:
            return self.ay[self.outfffd % 16]
        if port % 2 == 0:
            h = (port // 256) ^ 0xFF
            v = 0
            for b in range(8):
                if h & (1 << b):
                    v |= self.keyboard[b]
            return (v ^ 0xFF) & 0xBF | 0x00
        if port & 0xFF == 0x1F:
            return 0
        return 0xFF

    def write_port(self, registers, port, value, offset):
        if port % 2 == 0 and (value ^ self.outfe) & 0x10:
            self.beeps += 1
        if port & 0xC002 == 0xC000:         # FFFDh: select an AY register
            self.outfffd = value
        elif port & 0xC002 == 0x8000:       # BFFDh: write it
            self.ay[self.outfffd % 16] = value
            self.aylog.append((state['n'], self.outfffd % 16, value))
        PagingTracer.write_port(self, registers, port, value, offset)


tr = T()
sim.set_tracer(tr)
held = []          # (until_frame, row, mask)
log = open(prefix + "_ay.txt", "w")
state = {'n': 0}


def keymask(name):
    port, bits = KEYS[name]
    row = [i for i in range(8) if not (port >> 8) & (1 << i)][0]
    return row, (~bits) & 0x1F


def save(scr, name):
    im = Image.new('RGB', (256, 192))
    px = im.load()
    for y in range(192):
        for x in range(256):
            addr = ((y & 0xC0) << 5) | ((y & 7) << 8) | ((y & 0x38) << 2) | (x >> 3)
            at = scr[6144 + (y // 8) * 32 + x // 8]
            on = scr[addr] & (0x80 >> (x & 7))
            c = at & 7 if on else (at >> 3) & 7
            lv = 255 if at & 64 else 205
            px[x, y] = ((lv if c & 2 else 0), (lv if c & 4 else 0), (lv if c & 1 else 0))
    im.resize((512, 384), Image.NEAREST).save(name)


def draw(scr, frame, border, keyboard):
    n = state['n']
    state['n'] = n + 1
    for k in range(8):
        keyboard[k] = 0
    held[:] = [h for h in held if h[0] > n]
    for addr, val in pokes.get(n, []):
        sim.memory[addr] = val
    if n in events:
        for name in events[n]:
            r, m = keymask(name)
            held.append((n + 6, r, m))
    for _, r, m in held:
        keyboard[r] |= m
    tr.keyboard = keyboard
    log.write("%5d pc=%04X sp=%04X 7ffd=%02X ay=%s beeps=%d\n" % (
        n, sim.registers[24], sim.registers[12], tr.out7ffd,
        " ".join("%02X" % v for v in tr.ay[:14]), tr.beeps))
    tr.beeps = 0
    for f, r, v in tr.aylog:            # every AY write, with its frame
        log.write("      ay %5d R%d=%02X\n" % (f, r, v))
    tr.aylog = []
    if n in shots:
        save(bytes(scr), "%s_%05d.png" % (prefix, n))
    return n < nframes


regs = sim.registers
sim.trace(regs[24], -1, 0, 0, True, draw, None, tr.keyboard, None, None)
print("ran", state['n'], "frames; PC=%04X" % regs[24])
