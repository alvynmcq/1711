"""ZX0 packing for every compressed screen (v1.2; replaces the old lz.py).

compress() runs the vendored ZX0 compressor (tools/zx0, built with cc on
first use) and checks the result with decompress(), a Python copy of the
ZX0 v2 decoder that the game's unlz (dzx0_standard) implements.
"""
import glob
import os
import subprocess
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TOOL = os.path.join(ROOT, "tools", "zx0", "zx0")


def _tool():
    if not os.path.exists(TOOL):
        srcs = sorted(glob.glob(os.path.join(ROOT, "tools", "zx0", "src", "*.c")))
        subprocess.run(["cc", "-O2", "-o", TOOL] + srcs, check=True)
    return TOOL


def compress(data):
    data = bytes(data)
    with tempfile.TemporaryDirectory() as tmp:
        src, dst = os.path.join(tmp, "in.bin"), os.path.join(tmp, "out.zx0")
        open(src, "wb").write(data)
        subprocess.run([_tool(), "-f", src, dst], check=True, capture_output=True)
        comp = open(dst, "rb").read()
    assert decompress(comp) == data, "ZX0 round trip failed"
    return comp


def decompress(comp):
    """ZX0 v2 decoder (as tools/zx0 dzx0.c)."""
    out = bytearray()
    pos, mask, value, last, backtrack = 0, 0, 0, 0, False

    def byte():
        nonlocal pos, last
        last = comp[pos]
        pos += 1
        return last

    def bit():
        nonlocal mask, value, backtrack
        if backtrack:
            backtrack = False
            return last & 1
        mask >>= 1
        if not mask:
            mask, value = 128, byte()
        return 1 if value & mask else 0

    def elias(inverted=0):
        v = 1
        while not bit():
            v = v << 1 | (bit() ^ inverted)
        return v

    def copy(offset, length):
        assert 0 < offset <= len(out)
        for _ in range(length):
            out.append(out[-offset])

    offset = 1
    state = "literals"
    while True:
        if state == "literals":
            for _ in range(elias()):
                out.append(byte())
            if bit():
                state = "new"
                continue
            copy(offset, elias())
            if bit():
                state = "new"
            continue
        offset = elias(1)
        if offset == 256:
            assert pos == len(comp), "trailing data after the end marker"
            return bytes(out)
        offset = offset * 128 - (byte() >> 1)
        backtrack = True
        copy(offset, elias() + 1)
        state = "new" if bit() else "literals"
