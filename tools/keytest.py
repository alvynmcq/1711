#!/usr/bin/env python3
"""Headless key-script tests: run 1711.tap with scripted keys and compare the
screens with the reference screenshots in tools/ref/.

  python3 tools/keytest.py              # run every test in tools/tests/
  python3 tools/keytest.py parade       # just tools/tests/parade.keys
  python3 tools/keytest.py --update     # (re)write the references
  python3 tools/keytest.py --sheet      # also write tools/out/NAME_sheet.png

Needs SkoolKit (pip install skoolkit) and Pillow. The tape is loaded with
tap2sna (the real ROM loader, 128K) up to `game` (v0.7: after the boot
stub has loaded the banks and turned IM2 on), then tools/simtest.py runs
it frame by frame. The simulation is exact, so a
screen that changes at all fails its test; look at tools/out/ to see why,
and --update once the new screen is right.

A test (tools/tests/NAME.keys) is lines of:
  frames N                     how many frames to run
  F KEY [KEY...]               hold these keys for 6 frames from frame F
  every F STEP COUNT KEY...    the same keys COUNT times, every STEP frames
  shot F [F...]                compare the screen at frame F
  # anything                   a comment
"""
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(TOOLS, "..")
TESTS, REF, OUT = (os.path.join(TOOLS, d) for d in ("tests", "ref", "out"))


def parse(path):
    events, shots, frames = [], [], 1000
    for ln in open(path):
        w = ln.split("#")[0].split()
        if not w:
            continue
        if w[0] == "frames":
            frames = int(w[1])
        elif w[0] == "shot":
            shots += [int(x) for x in w[1:]]
        elif w[0] == "every":
            f, step, count = int(w[1]), int(w[2]), int(w[3])
            events += [(f + k * step, w[4:]) for k in range(count)]
        else:
            events.append((int(w[0]), w[1:]))
    seen = {}
    for f, keys in events:
        assert f not in seen, "%s: two key events at frame %d" % (path, f)
        seen[f] = keys
    return sorted(events), sorted(set(shots)), frames


def game_address():
    for ln in open(os.path.join(ROOT, "src", "main.sym")):
        w = ln.split()
        if len(w) == 3 and w[0] == "game":
            return int(w[2].rstrip("Hh"), 16)
    raise SystemExit("no `game` in src/main.sym: build first")


def snapshot(tmp):
    snap = os.path.join(tmp, "s128.z80")
    subprocess.run(["tap2sna.py", "-c", "machine=128", "--start", str(game_address()),
                    os.path.join(ROOT, "1711.tap"), snap], check=True, stdout=subprocess.DEVNULL)
    return snap


def run(name, snap, tmp, update, sheet):
    events, shots, frames = parse(os.path.join(TESTS, name + ".keys"))
    prefix = os.path.join(tmp, name)
    args = [sys.executable, os.path.join(TOOLS, "simtest.py"), snap, prefix]
    # SkoolKit names letter keys in lower case: "A" in a test is "a"
    args += ["%d:%s" % (f, " ".join(x.lower() if len(x) == 1 else x for x in k))
             for f, k in events]
    args += ["--shots", ",".join(map(str, shots)), "--frames", str(frames)]
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
    bad = []
    for f in shots:
        got = "%s_%05d.png" % (prefix, f)
        ref = os.path.join(REF, "%s_%05d.png" % (name, f))
        if update:
            shutil.copy(got, ref)
            continue
        if not os.path.exists(ref):
            bad.append("%d (no reference)" % f)
            shutil.copy(got, os.path.join(OUT, os.path.basename(ref)))
            continue
        a, b = Image.open(got).convert("RGB"), Image.open(ref).convert("RGB")
        if ImageChops.difference(a, b).getbbox():
            bad.append(str(f))
            shutil.copy(got, os.path.join(OUT, os.path.basename(ref)))
    if sheet:
        ims = [Image.open("%s_%05d.png" % (prefix, f)) for f in shots]
        cols = 3
        sh = Image.new("RGB", (512 * cols, 384 * ((len(ims) + cols - 1) // cols)), (60, 60, 60))
        for i, im in enumerate(ims):
            sh.paste(im, (512 * (i % cols), 384 * (i // cols)))
        sh.save(os.path.join(OUT, name + "_sheet.png"))
    return bad


def main():
    args = sys.argv[1:]
    update, sheet = "--update" in args, "--sheet" in args
    names = [a for a in args if not a.startswith("--")] or sorted(
        f[:-5] for f in os.listdir(TESTS) if f.endswith(".keys"))
    os.makedirs(REF, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        snap = snapshot(tmp)
        for name in names:
            bad = run(name, snap, tmp, update, sheet)
            if update:
                print("%-12s references written" % name)
            elif bad:
                failed += 1
                print("%-12s FAIL at frame %s (new screens in tools/out/)" % (name, ", ".join(bad)))
            else:
                print("%-12s ok" % name)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
