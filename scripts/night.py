#!/usr/bin/env python3
"""Compile a night (data/nightN.py) into src/night.inc for the engine's
night screens: the hub, the statement reader, compare, the clerk's book.

  python3 scripts/night.py 1

Everything the Z80 would find awkward is worked out here: clauses are
wrapped to the screen, statements are cut into pages, and every pair of
lines that means something when compared (a contradiction, or a line
sworn word for word the same by two people) is listed with its finding.
The engine only looks a pair up in that table.

Layout of src/night.inc (all labels used by src/main.asm):

  HUBROW EQU r          row of the first statement on the hub
  NIGHT_NF EQU n        number of findings
  NIGHT_CANDLE EQU n    the night's candle: a compare burns 1, writing 2 more
  night_hub             textlist: the hub screen
  night_book            textlist: the book's heading
  night_people          textlist: the book's page of names
  night_nst: db n       statements, then night_st: dw st_0, st_1, ...
  st_k: dw who, sworn   then db clauses, pages; dw clause table;
                        then per page db first clause, clause count
  clause: db lines, then each line as a 0-terminated string
  night_pairs: db n     then n x (db s0, c0, s1, c1, finding),
                        (s0, c0) < (s1, c1)
  night_find            dw seen, book for each finding (both clause-
                        format blocks: db lines, strings)
  txt_nobear            block shown when a pair means nothing
  par_...               the parade (see compile_parade)
"""
import importlib.util
import itertools
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from script import MARGIN, wrap, BYEL, WHT, BWHT, YEL, CYN  # noqa: E402
from font import FONTW  # noqa: E402  (script.py put art/ on the path)

WIDTH = (256 - 8 - MARGIN) // FONTW   # characters per line from column 1 (40)
PAGE0, PAGEROWS = 3, 17               # statement text: rows 3-19
CLAUSE_MAX = 4                        # compare screen: lines per clause
RESULT_MAX = 4                        # compare screen: lines of a finding (rows 14-17)
HUBROW = 6
NUMBERS = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"]
NOBEAR = "These two lines do not bear on one another."


def load(n):
    path = os.path.join(ROOT, "data", "night%d.py" % n)
    spec = importlib.util.spec_from_file_location("night", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.NIGHT


def asm_str(s):
    assert all(32 <= ord(c) < 128 for c in s), s
    assert '"' not in s, "no double quotes in game text: %r" % s
    return '        db "%s",0' % s


def spaced(word):
    return " ".join(word)              # "ONE" -> "O N E", like the card


def clauses_of(night):
    """[(statement index, [(text, claim, value), ...])], copies resolved."""
    by_id = {st["id"]: st for st in night["statements"]}
    out = []
    for st in night["statements"]:
        src = by_id[st["copy_of"]] if "copy_of" in st else st
        lines = [ln if isinstance(ln, tuple) else (ln, None, None) for ln in src["lines"]]
        out.append(lines)
    return out


def findings_of(night):
    """Every meaningful pair: {(s0, c0, s1, c1): key}, and the keys in order."""
    sts = night["statements"]
    cl = clauses_of(night)
    every = [(s, c) for s in range(len(sts)) for c in range(len(cl[s]))]
    pairs, keys = {}, []
    for (s0, c0), (s1, c1) in itertools.combinations(every, 2):
        t0, k0, v0 = cl[s0][c0]
        t1, k1, v1 = cl[s1][c1]
        key = None
        if s0 != s1 and t0 == t1:
            copy = sts[s1] if sts[s1].get("copy_of") == sts[s0]["id"] else sts[s0]
            key = "copy:" + copy["id"]
        elif k0 and k0 == k1 and v0 != v1:
            key = k0
        if key:
            pairs[(s0, c0, s1, c1)] = key
            if key not in keys:
                keys.append(key)
    return pairs, keys


def paginate(lines):
    pages, first, rows = [], 0, 0
    for i, (text, _, _) in enumerate(lines):
        n = len(wrap(text, WIDTH))
        assert n <= PAGEROWS
        assert i - first < 16, "pg_row holds 16 lines a page"
        if rows + n > PAGEROWS:
            pages.append((first, i - first))
            first, rows = i, 0
        rows += n
    pages.append((first, len(lines) - first))
    return pages


def block(label, text, maxlines):
    w = wrap(text, WIDTH)
    assert len(w) <= maxlines, "%s: %d lines, at most %d: %r" % (label, len(w), maxlines, text)
    return ["%s:" % label, "        db %d" % len(w)] + [asm_str(x) for x in w]


def textrec(row, col, attr, s):
    assert col * 8 + MARGIN + len(s) * FONTW <= 256, "too wide: %r" % s
    return ["        db %d,%d,%d" % (row, col, attr), asm_str(s)]


def compile_parade(night):
    """The parade: the arranging screen, the scene's pieces, and for each
    of the 2^choices arrangements which "seen" and "record" lines apply.

      par_screen      textlist: title, intro, choice headings, keys
      par_port        db the accused's portrait (art/portraits.py order),
                      0FFh if there is none; drawn at rows 6-17, cols 22-31
      par_opt         dw menu string, per choice, per option (2 each)
      par_scene       dw scene block, the same order
      par_always      block: the fit, every time
      par_spoken      block: what the accused says, every time
      par_seen, par_rec   dw blocks
      par_fit         block: what the Mayor gives the clerk to write
      par_combo       per arrangement (bit i = option of choice i):
                      db seen mask, record mask
    """
    p = night.get("parade")
    assert p, "every night has a parade for now (night.asm expects one)"
    who = night["people"][p["accused"]].split(",")[0]
    names = list(p["choices"])
    assert len(names) <= 3, "three choices fit the arranging screen"
    for k in names:
        assert len(p["choices"][k][1]) == 2, "a choice has two options (1-3 toggle them)"
    seen, rec = p.get("seen", []), p["record"]
    assert len(seen) <= 8 and len(rec) <= 8
    from portraits import PORTRAITS
    ports = [nm for nm, _ in PORTRAITS]
    port = ports.index(p["accused"]) if p["accused"] in ports else 0xFF
    out = ["PAR_NC  EQU %d" % len(names), "par_port: db %d" % port, "par_screen:"]
    out += textrec(0, 1, BYEL, who + " is sent for")
    intro = wrap(p["intro"], WIDTH)
    assert len(intro) <= 4
    for i, ln in enumerate(intro):
        out += textrec(2 + i, 1, YEL, ln)
    for i, k in enumerate(names):
        out += textrec(7 + 4 * i, 1, BYEL, "%d  %s" % (i + 1, p["choices"][k][0]))
    out += textrec(22, 1, CYN, "1 2 3  change      SPACE  send for her")
    out += textrec(23, 1, CYN, "X  not yet")
    out.append("        db 0FFh")
    out.append("par_brought:")
    out += textrec(0, 1, BYEL, who + " is brought")
    out.append("        db 0FFh")
    out.append("msg_brought:")
    out += textrec(20, 1, YEL, who + " has been brought already.")
    out.append("        db 0FFh")
    out.append("par_opt: dw " + ",".join("po_%d_%d" % (i, j) for i in range(len(names)) for j in (0, 1)))
    out.append("par_scene: dw " + ",".join("ps_%d_%d" % (i, j) for i in range(len(names)) for j in (0, 1)))
    for i, k in enumerate(names):
        for j, (_, menu, scene) in enumerate(p["choices"][k][1]):
            assert 2 * 8 + MARGIN + len(menu) * FONTW <= 256, menu
            out += ["po_%d_%d:" % (i, j), asm_str(menu)]
            out += block("ps_%d_%d" % (i, j), scene, 3)
    out += block("par_always", p["always"], 4)
    out += block("par_spoken", p["spoken"], 3)
    out.append("par_seen: dw " + ",".join("pn_%d" % i for i in range(len(seen))) if seen else "par_seen:")
    for i, (_, t) in enumerate(seen):
        out += block("pn_%d" % i, t, 3)
    out.append("par_rec: dw " + ",".join("pr_%d" % i for i in range(len(rec))))
    for i, (_, t) in enumerate(rec):
        out += block("pr_%d" % i, t, 2)
    out += block("par_fit", p["fit"], 3)
    out.append("par_combo:")
    for combo in range(1 << len(names)):
        pick = {k: p["choices"][k][1][(combo >> i) & 1][0] for i, k in enumerate(names)}
        hits = lambda lst: [i for i, (cond, _) in enumerate(lst)
                            if all(pick[k] == v for k, v in cond.items())]
        sm, rm = hits(seen), hits(rec)
        # the scene: a line per choice, a blank, the fit, a blank, what was seen
        rows = 2 + sum(len(wrap(p["choices"][k][1][(combo >> i) & 1][2], WIDTH))
                       for i, k in enumerate(names))
        rows += 1 + len(wrap(p["always"], WIDTH)) + 1
        rows += len(wrap(p["spoken"], WIDTH)) + 1
        rows += sum(len(wrap(seen[i][1], WIDTH)) + 1 for i in sm)
        assert rows <= 22, "parade scene %d runs to row %d" % (combo, rows)
        # the record screen: the fit from row 3, a blank, a heading, the lines
        rows = 3 + len(wrap(p["fit"], WIDTH)) + 2 + sum(len(wrap(rec[i][1], WIDTH)) + 1 for i in rm)
        assert rows <= 21, "parade record %d runs to row %d" % (combo, rows)
        out.append("        db %d,%d   ; %s" % (sum(1 << i for i in sm), sum(1 << i for i in rm),
                                                " ".join(pick.values())))
    return out


def compile_night(n):
    night = load(n)
    sts = night["statements"]
    assert len(sts) <= 9, "keys 1-9 pick a statement"
    cl = clauses_of(night)
    pairs, keys = findings_of(night)
    texts = night.get("findings", {})
    missing = [k for k in keys if k not in texts]
    assert not missing, "findings with no text in night%d.py: %s" % (n, ", ".join(missing))
    unused = [k for k in texts if k not in keys]
    assert not unused, "text for findings that never happen: %s" % ", ".join(unused)
    assert len(pairs) < 256 and 1 <= len(keys) <= 16   # night_fflag holds 16

    out = ["; generated by scripts/night.py from data/night%d.py" % n,
           "HUBROW  EQU %d" % HUBROW, "NIGHT_NF EQU %d" % len(keys),
           "NIGHT_CANDLE EQU %d" % night["candle"]]
    assert 1 <= night["candle"] <= 16, "a candle is 1-16 units (16 pixels of wax)"

    # the hub
    out.append("night_hub:")
    out += textrec(1, 1, BYEL, "N I G H T    " + spaced(NUMBERS[n - 1]))
    out += textrec(2, 1, WHT, night["date"] + ", " + night["place"].split(",")[0])
    out += textrec(4, 1, YEL, "The statements sworn this day:")
    for i, st in enumerate(sts):
        out += textrec(HUBROW + i, 1, WHT, "%d  %s" % (i + 1, st["who"]))
    r = HUBROW + len(sts) + 1
    out += textrec(r, 1, WHT, "B  The clerk's book")
    p = night.get("parade")
    if p:
        out += textrec(r + 1, 1, WHT, "K  " + night["people"][p["accused"]].split(",")[0]
                       + " is sent for")
    out += textrec(r + 2, 1, WHT, "X  End the night")
    out += textrec(r + 4, 1, YEL, "In a statement, M marks a line. Mark two")
    out += textrec(r + 5, 1, YEL, "and C sets them side by side. That burns")
    out += textrec(r + 6, 1, YEL, "candle, and writing it out burns more.")
    assert r + 6 < 20
    out.append("        db 0FFh")

    # the book's heading and its page of names
    out.append("night_book:")
    out += textrec(0, 1, BYEL, "The Clerk's Book")
    out += textrec(1, 1, WHT, night["place"].split(",")[0] + ", " + night["date"])
    out.append("        db 0FFh")
    out.append("night_people:")
    out += textrec(0, 1, BYEL, "Names taken down this night")
    row = 2
    for who in night["people"].values():
        # "Name, of Place, accused. An ordinary detail." -> the name in white,
        # the detail under it, indented, in yellow
        head, _, detail = who.partition(". ")
        if not detail:
            head = who
        ws = [(1 if k == 0 else 2, WHT, ln)
              for k, ln in enumerate(wrap(head + ("." if detail else ""), WIDTH))]
        ws += [(2, YEL, ln) for ln in wrap(detail, WIDTH - 2)]
        for col, attr, ln in ws:
            assert row <= 21, "too many names for one page"
            out += textrec(row, col, attr, ln)
            row += 1
    out.append("        db 0FFh")

    # statements
    out.append("night_nst: db %d" % len(sts))
    out.append("night_st: dw " + ",".join("st_%d" % i for i in range(len(sts))))
    by_id = {st["id"]: i for i, st in enumerate(sts)}
    for i, st in enumerate(sts):
        own = by_id[st["copy_of"]] if "copy_of" in st else i
        pages = paginate(cl[i])
        out.append("st_%d:   ; %s" % (i, st["id"]))
        out.append("        dw st_%d_who,st_%d_sw" % (i, i))
        out.append("        db %d,%d" % (len(cl[i]), len(pages)))
        out.append("        dw cltab_%d" % own)     # a copy shares the words exactly
        out.append("        db " + ",".join("%d,%d" % pg for pg in pages))
        assert len(st["who"]) <= WIDTH
        out += ["st_%d_who:" % i, asm_str(st["who"])]
        out += ["st_%d_sw:" % i, asm_str("Sworn " + st["sworn"] + " 1711")]
        if own == i:
            out.append("cltab_%d: dw " % i + ",".join("cl_%d_%d" % (i, c) for c in range(len(cl[i]))))
            for c, (text, _, _) in enumerate(cl[i]):
                out += block("cl_%d_%d" % (i, c), text, CLAUSE_MAX)

    # findings
    out.append("night_pairs: db %d" % len(pairs))
    for (s0, c0, s1, c1), key in pairs.items():
        out.append("        db %d,%d,%d,%d,%d   ; %s" % (s0, c0, s1, c1, keys.index(key), key))
    out.append("night_find:")
    for f in range(len(keys)):
        out.append("        dw f%d_seen,f%d_book" % (f, f))
    book_rows = 0
    for f, key in enumerate(keys):
        seen, book = texts[key]
        out += block("f%d_seen" % f, seen, RESULT_MAX)
        out += block("f%d_book" % f, book, 3)
        book_rows += len(wrap(book, WIDTH)) + 1
    assert book_rows <= 19, "the book would run off its page"   # rows 3-21
    out += block("txt_nobear", NOBEAR, RESULT_MAX)
    out += compile_parade(night)

    open(os.path.join(ROOT, "src", "night.inc"), "w").write("\n".join(out) + "\n")
    return night, pairs, keys


if __name__ == "__main__":
    night, pairs, keys = compile_night(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    print("night.inc: %d statements, %d findings from %d pairs" %
          (len(night["statements"]), len(keys), len(pairs)))
