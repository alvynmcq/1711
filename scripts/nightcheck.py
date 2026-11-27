#!/usr/bin/env python3
"""Check a night's data (data/nightN.py) and show what the clerk can find.

  python3 scripts/nightcheck.py 1

Checks the shape of the data and that every line fits the screen once
wrapped (scripts/night.py checks the rest as it compiles), then prints:

- the statements in case order (the order the witnesses come to the table)
  and the items that can be found at each case: what goes in hand when the
  clerk compares a line of the witness at the table with a line of an
  earlier statement (THEY DIFFER, THEY AGREE, WORD FOR WORD), with the
  ways it can be written and what each does to Mayor Ellis's patience;
- any claim made in one statement only (it can never be compared);
- every way the parade can be arranged, with its record lines' patience;
- three paths through the night (the night's "paths": everything, the
  collaborator, balanced): the patience after each case and at the end of
  the night, and the candle each needs at the least (one compare an item
  found, two units an item written);
- the size of the text.
"""
import itertools
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from script import wrap  # noqa: E402
from night import (load, findings_of, case_of, check_findings, WIDTH,  # noqa: E402
                   PAT0, PATMAX, GAIN_MAX, BANDS)

WORD = {"differ": "THEY DIFFER", "agree": "THEY AGREE", "copy": "WORD FOR WORD"}


def lines_of(st, by_id):
    if "copy_of" in st:
        return by_id[st["copy_of"]]["lines"]
    return st["lines"]


def band(p):
    for i, lo in enumerate(BANDS):
        if p >= lo:
            return i
    return len(BANDS)


def walk(night, path, cases, kinds, verbose):
    """Patience and candle along a path; prints the patience case by case."""
    sts, f = night["statements"], night["findings"]
    pat, gains, cdl, steps = PAT0, 0, 0, []
    out = None
    for s in range(len(sts)):
        here = [k for k in path["desk"] if cases[k] == s]
        d = 0
        for k in here:
            cdl += 1                              # the compare that finds it
            opt = path["desk"][k]
            if opt is None:
                continue
            cdl += 2                              # writing it
            p = f[k]["write"][opt][2]
            if p > 0:
                p = min(p, GAIN_MAX - gains)
                gains += p
            d += p
        pat = max(0, min(PATMAX, pat + d))
        steps.append("%s %+d -> %d" % (sts[s]["id"], d, pat))
        if pat == 0 and out is None:
            out = sts[s]["id"]
    p = night["parade"]
    names = list(p["choices"])
    pick = dict(zip(names, path["parade"]))
    rec = [(t, v) for cond, t, v in p["record"] if all(pick[k] == x for k, x in cond.items())]
    if path["lines"] != "all":
        rec = [(t, v) for t, v in rec if any(t.startswith(w) for w in path["lines"])]
    d = sum(v for _, v in rec)
    written = sum(1 for k in path["desk"] if path["desk"][k] is not None) + len(rec)
    if not written:
        d += night["mayor"]["bare"]
    pat = max(0, min(PATMAX, pat + d))
    steps.append("parade %+d -> %d" % (d, pat))
    if pat == 0 and out is None:
        out = "the parade"
    return pat, cdl, steps, out


def main(n):
    night = load(n)
    sts = night["statements"]
    by_id = {st["id"]: st for st in sts}
    claims, text_bytes, rows = {}, 0, {}
    for st in sts:
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
            r += len(wrap(text, WIDTH))
            if "copy_of" not in st:
                text_bytes += len(text) + 1
        rows[st["id"]] = r

    pairs, keys, kinds = findings_of(night)
    check_findings(night, keys)
    cases = case_of(pairs)
    f = night["findings"]

    print("Night %d, %s, %s" % (night["n"], night["date"], night["place"]))
    print("\nThe cases, in the order they come to the table (rows once wrapped):")
    for s, st in enumerate(sts):
        tag = "  (copy of %s)" % st["copy_of"] if "copy_of" in st else ""
        here = [k for k in keys if cases[k] == s]
        print("\n  %d %-8s %-38s %2d rows%s   %d item%s" % (
            s + 1, st["id"], st["who"], rows[st["id"]], tag, len(here), "" if len(here) == 1 else "s"))
        assert len(here) <= 3, "at most three items in hand at a case (1-3 toggle them)"
        for k in here:
            np = sum(1 for v in pairs.values() if v == k)
            print("      %-14s %-16s %d pair%s: %s" % (WORD[kinds[k]], k, np, "" if np == 1 else "s",
                                                     f[k]["label"]))
            for menu, book, pat, slip, answer in f[k]["write"]:
                print("          %-17s %+d%s" % (menu, pat, "   (a question)" if answer else ""))
            print("          %-17s +0" % "Let it lie")
            text_bytes += len(f[k]["label"]) + 1
            text_bytes += sum(len(w[0]) + len(w[1]) + len(w[3] or "") + len(w[4] or "") + 4
                              for w in f[k]["write"])

    once = sorted(k for k, v in claims.items()
                  if len({by_id[s].get("copy_of", s) for s, _ in v}) == 1)
    for k in once:
        print("\nWARNING: claim %r appears in one statement only (%s): give it a "
              "second statement or make it a plain line" % (k, claims[k][0][0]))

    p = night["parade"]
    assert p["accused"] in night["people"], p["accused"]
    names = list(p["choices"])
    opts = [[o[0] for o in p["choices"][k][1]] for k in names]
    print("\nThe parade (%s), last: %d ways to arrange it" % (
        p["accused"], len(list(itertools.product(*opts)))))
    for combo in itertools.product(*opts):
        pick = dict(zip(names, combo))
        rec = ["%s (%+d)" % (r, v) for cond, r, v in p["record"]
               if all(pick[k] == x for k, x in cond.items())]
        print("  %-18s -> %s" % (" ".join(combo), " / ".join(rec) or "(the fit only)"))
    text_bytes += len(p["intro"]) + len(p["always"]) + len(p["fit"]) + 1
    text_bytes += len(p.get("spoken", "")) + 1
    text_bytes += sum(len(r[1]) + 1 for r in p["record"] + p.get("seen", []))
    text_bytes += sum(len(o[1]) + len(o[2]) + 2 for _, os_ in p["choices"].values() for o in os_)

    print("\nMayor Ellis's patience: starts at %d (at most %d); desk gains at most +%d a night;"
          " a bare book %+d" % (PAT0, PATMAX, GAIN_MAX, night["mayor"]["bare"]))
    print("Bands (the manner line): %s" % ", ".join(
        "%d-%d" % (lo, hi) for lo, hi in zip(BANDS, [PATMAX] + [b - 1 for b in BANDS[:-1]])))
    for name, path in night["paths"].items():
        for k in path["desk"]:
            assert k in f, "path %s: no finding %s" % (name, k)
        pat, cdl, steps, out = walk(night, path, cases, kinds, True)
        print("\n  %-13s ends at %2d (%s)%s; candle at least %d of %d" % (
            name, pat, night["mayor"]["manner"][band(pat)] if pat else "dismissed",
            ", dismissed at " + out if out else "", cdl, night["candle"]))
        print("      " + "; ".join(steps))

    m = night["mayor"]
    text_bytes += sum(len(t) + 1 for t in m["manner"] + m["cold"] + m["goodnight"])
    text_bytes += sum(len(t) + 1 for v in m["slips"].values() for t in v)
    text_bytes += len(m["dismiss"]) + len(night["orders"]) + len(night["next_orders"]) + 3
    text_bytes += sum(len(v) + 1 for v in night["people"].values())
    every = sum(1 + 2 for k in keys)
    print("\nCandle: %d. A compare burns 1, writing an item 2 more: finding and writing all"
          " %d items costs %d at the least, leaving %d for compares that find nothing."
          % (night["candle"], len(keys), every, night["candle"] - every))
    print("\nText this night: %d bytes uncompressed" % text_bytes)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
