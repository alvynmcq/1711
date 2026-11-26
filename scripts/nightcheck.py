#!/usr/bin/env python3
"""Check a night's data (data/nightN.py) and show what the clerk can find.

  python3 scripts/nightcheck.py 1

Checks the shape of the data and that every line fits the screen once
wrapped, then lists the contradictions (same claim, different values),
the copied statements, the parade's combinations, and the size of the
text, so we can see how much a night costs in memory before writing
any engine code for it.
"""
import importlib.util
import itertools
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from script import COLS, wrap  # noqa: E402


def load(n):
    path = os.path.join(ROOT, "data", "night%d.py" % n)
    spec = importlib.util.spec_from_file_location("night", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.NIGHT


def lines_of(st, by_id):
    if "copy_of" in st:
        return by_id[st["copy_of"]]["lines"]
    return st["lines"]


def main(n):
    night = load(n)
    by_id = {st["id"]: st for st in night["statements"]}
    assert len(by_id) == len(night["statements"]), "duplicate statement id"
    claims, text_bytes, rows = {}, 0, {}
    for st in night["statements"]:
        if "copy_of" in st:
            assert st["copy_of"] in by_id, st["id"]
        r = 0
        for ln in lines_of(st, by_id):
            if isinstance(ln, tuple):
                text, key, val = ln
                claims.setdefault(key, []).append((st["id"], val))
            else:
                text = ln
            assert all(32 <= ord(c) < 128 for c in text), text
            w = wrap(text, COLS)
            r += len(w)
            if "copy_of" not in st:
                text_bytes += len(text) + 1
        rows[st["id"]] = r

    print("Night %d, %s, %s" % (night["n"], night["date"], night["place"]))
    print("\nStatements (screen rows once wrapped):")
    for st in night["statements"]:
        tag = "  (copy of %s)" % st["copy_of"] if "copy_of" in st else ""
        print("  %-8s %-40s %2d rows%s" % (st["id"], st["who"], rows[st["id"]], tag))

    print("\nContradictions the clerk can flag:")
    found = 0
    for key, vals in sorted(claims.items()):
        for (a, va), (b, vb) in itertools.combinations(vals, 2):
            if va != vb:
                print("  %-16s %s says %s, %s says %s" % (key, a, va, b, vb))
                found += 1
    if not found:
        print("  (none)")
    print("\nClaims made once only (no conflict yet):",
          ", ".join(sorted(k for k, v in claims.items() if len(v) == 1)))

    from night import findings_of
    pairs, keys = findings_of(night)
    texts = night.get("findings", {})
    print("\nFindings (what C finds when two lines are compared):")
    for key in keys:
        n = sum(1 for k in pairs.values() if k == key)
        print("  %-16s %d pair%s%s" % (key, n, "" if n == 1 else "s",
                                       "" if key in texts else "   ** NO TEXT in findings **"))
        if key in texts:
            text_bytes += sum(len(t) + 1 for t in texts[key])

    p = night.get("parade")
    if p:
        assert p["accused"] in night["people"], p["accused"]
        names = list(p["choices"])
        print("\nParade (%s): %d ways to arrange it" % (
            p["accused"], len(list(itertools.product(*p["choices"].values())))))
        for combo in itertools.product(*[[o[0] for o in p["choices"][k]] for k in names]):
            pick = dict(zip(names, combo))
            rec = [r for cond, r in p["record"] if all(pick[k] == v for k, v in cond.items())]
            print("  %-28s -> %s" % (" ".join(combo), " / ".join(rec) or "(nothing extra)"))
        text_bytes += len(p["intro"]) + len(p["always"]) + sum(len(r) + 1 for _, r in p["record"])
        text_bytes += sum(len(o[1]) + 1 for opts in p["choices"].values() for o in opts)

    text_bytes += sum(len(v) + 1 for v in night["people"].values())
    print("\nText this night: %d bytes uncompressed (a 16K bank holds about %d nights like it)"
          % (text_bytes, 16384 // max(1, text_bytes)))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
