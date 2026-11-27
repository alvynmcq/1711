#!/usr/bin/env python3
"""Compile a night (data/nightN.py) into src/night.inc for the engine's
night screens (src/night.asm): the orders card, the desk, the parade, the
ledger, the clerk's book.

  python3 scripts/night.py 1

Everything the Z80 would find awkward is worked out here: clauses are
wrapped to the screen, statements are cut into pages of the desk's halves,
and every pair of lines in two statements that means something (THEY
DIFFER, THEY AGREE, WORD FOR WORD) is listed with its finding, so the
engine only looks a pair up in a table (the desk's compare must land
within 2 frames).

Layout of src/night.inc (all labels used by src/night.asm):

  NIGHT_N, NIGHT_NF, NIGHT_NST, NIGHT_CANDLE, PAT0, PATMAX, GAIN_MAX,
  BARE (what a bare book costs), CDL_Q, CDL_H (a quarter, a half of the
  candle, for the ledger)
  night_orders          textlist: the orders card
  night_book, night_ledger, night_people   textlists: headings, names
  night_nst: db n       statements in case order, then night_st: dw st_0, ...
  st_k: dw who, sworn, short name, clause table; db clauses, pages;
        then per page db first clause, clause count
  clause: db lines, then each line as a 0-terminated string
  night_pairs: db n     then n x (db s0, c0, s1, c1, finding), s0 < s1
                        (s1 is the case at the table, s0 a statement in the book)
  night_find: dw fr_0, ...   one record a finding:
        db kind (0 differ, 1 agree, 2 copy), ways to write it (1-2)
        dw label
        db the column of each option (the ways, then Let it lie; 3 bytes)
        per way: dw menu, book block, answer block (0: none), slip (0: by cost)
                 db patience (signed)
  night_fcase: db the case each finding is found at
  man_tab: dw 4 manner lines; slip_tab: dw 5 lists (gain, none, small,
  middle, large), each db n, dw strings; cold_tab: db n, dw strings;
  good_tab: dw 4 blocks; txt_dismiss, txt_next: blocks
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

WIDTH = 39                  # characters a line from column 1, clear of column 31
                            # (the candle, rows 0-3); v0.7 was 40
HALFROWS = 8                # the desk's halves: rows 3-10 and 12-19
CANDLE_MAX = 25             # 32 pixel rows: the dish, the wax, a 5-pixel flame
KIND = {"differ": 0, "agree": 1, "copy": 2}
LETLIE = "Let it lie"
# Mayor Ellis's patience (stage 2): a byte, 0-12; Night One starts at 12,
# +2 overnight; desk gains at most GAIN_MAX a night; the manner line's
# bands start at BANDS (10-12, 6-9, 3-5, 1-2); at 0 he takes the pen
PAT0, PATMAX, GAIN_MAX, BANDS = 12, 12, 3, (10, 6, 3, 1)


def load(n):
    """The night's data, its statements put in case order ("order")."""
    path = os.path.join(ROOT, "data", "night%d.py" % n)
    spec = importlib.util.spec_from_file_location("night", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    night = mod.NIGHT
    by_id = {st["id"]: st for st in night["statements"]}
    order = night.get("order", list(by_id))
    assert sorted(order) == sorted(by_id), "order must list every statement once"
    night["statements"] = [by_id[i] for i in order]
    return night


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


KINDS = ("differ", "agree", "copy")    # THEY DIFFER, THEY AGREE, WORD FOR WORD


def kind_of(key):
    return "copy" if key.startswith("copy:") else None


def findings_of(night):
    """Every pair of lines in two different statements that means something:
    {(s0, c0, s1, c1): key} with s0 < s1 (s1 is the case it is found at),
    the keys in order, and {key: kind}. A copied line is WORD FOR WORD; the
    same claim with another value THEY DIFFER, with the same value THEY
    AGREE. A claim may not both agree and differ (one key, one kind)."""
    sts = night["statements"]
    cl = clauses_of(night)
    every = [(s, c) for s in range(len(sts)) for c in range(len(cl[s]))]
    pairs, keys, kinds = {}, [], {}
    for (s0, c0), (s1, c1) in itertools.combinations(every, 2):
        if s0 == s1:
            continue
        t0, k0, v0 = cl[s0][c0]
        t1, k1, v1 = cl[s1][c1]
        key = kind = None
        if t0 == t1:
            copy = sts[s1] if sts[s1].get("copy_of") == sts[s0]["id"] else sts[s0]
            key, kind = "copy:" + copy["id"], "copy"
        elif k0 and k0 == k1:
            key, kind = k0, ("differ" if v0 != v1 else "agree")
        if key:
            assert kinds.get(key, kind) == kind, "claim %s both agrees and differs" % key
            kinds[key] = kind
            pairs[(s0, c0, s1, c1)] = key
            if key not in keys:
                keys.append(key)
    return pairs, keys, kinds


def case_of(pairs):
    """{key: the case (statement index) it is found at}; each key at one only."""
    out = {}
    for (s0, c0, s1, c1), key in pairs.items():
        assert out.get(key, s1) == s1, "finding %s can be found at two cases" % key
        out[key] = s1
    return out


def check_findings(night, keys):
    texts = night.get("findings", {})
    missing = [k for k in keys if k not in texts]
    assert not missing, "findings with no text: %s" % ", ".join(missing)
    unused = [k for k in texts if k not in keys]
    assert not unused, "text for findings that never happen: %s" % ", ".join(unused)
    for k, f in texts.items():
        assert 1 <= len(f["write"]) <= 2, "%s: one or two ways to write it" % k
        for menu, book, pat, slip, answer in f["write"]:
            assert -12 <= pat <= 12 and book


def paginate(lines):
    pages, first, rows = [], 0, 0
    for i, (text, _, _) in enumerate(lines):
        n = len(wrap(text, WIDTH))
        assert n <= HALFROWS
        if rows + n > HALFROWS:
            pages.append((first, i - first))
            first, rows = i, 0
        rows += n
    pages.append((first, len(lines) - first))
    return pages


def block(label, text, maxlines):
    w = wrap(text, WIDTH)
    assert len(w) <= maxlines, "%s: %d lines, at most %d: %r" % (label, len(w), maxlines, text)
    return ["%s:" % label, "        db %d" % len(w)] + [asm_str(x) for x in w]


def fits(col, s, right=248):
    """True if s drawn from column col ends left of pixel `right` (column 31
    is the candle's in rows 0-3; keep every line clear of it)."""
    return col * 8 + MARGIN + len(s) * FONTW <= right


def cells(s):
    return (MARGIN + len(s) * FONTW + 7) // 8


def textrec(row, col, attr, s):
    assert fits(col, s, 256), "too wide: %r" % s
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
    out.append("        db 0FFh")
    out.append("par_brought:")
    out += textrec(0, 1, BYEL, who + " is brought")
    out.append("        db 0FFh")
    out.append("par_mayor:")             # dismissed: he arranges it himself
    out += textrec(0, 1, BYEL, who + " is brought")
    out += textrec(1, 1, WHT, "Mayor Ellis arranges it himself.")
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
    for i, (_, t, _) in enumerate(rec):
        out += block("pr_%d" % i, t, 2)
    out.append("par_pat: db " + ",".join(str(v & 255) for _, _, v in rec))
    out += block("par_fit", p["fit"], 3)
    out.append("par_combo:")
    for combo in range(1 << len(names)):
        pick = {k: p["choices"][k][1][(combo >> i) & 1][0] for i, k in enumerate(names)}
        hits = lambda lst: [i for i, (cond, *_) in enumerate(lst)
                            if all(pick[k] == v for k, v in cond.items())]
        sm, rm = hits(seen), hits(rec)
        # the scene: a line per choice, a blank, the fit, a blank, what was seen
        rows = 3 + sum(len(wrap(p["choices"][k][1][(combo >> i) & 1][2], WIDTH))
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


def one(label, s, col=1, right=248):
    """A one-line string that must fit from column col, clear of column 31
    (right=256 for a line drawn below the candle's rows)."""
    assert fits(col, s, right), "%s: too long for one line: %r" % (label, s)
    return ["%s:" % label, asm_str(s)]


def compile_night(n):
    night = load(n)
    sts = night["statements"]
    assert len(sts) <= 9, "keys 1-9 turn the book to a statement"
    cl = clauses_of(night)
    pairs, keys, kinds = findings_of(night)
    check_findings(night, keys)
    cases = case_of(pairs)
    f = night["findings"]
    assert len(pairs) < 256 and 1 <= len(keys) <= 9   # night_fflag holds 16; the ledger counts 0-9
    for s in range(len(sts)):
        assert sum(1 for k in keys if cases[k] == s) <= 3, "three items in hand at most"
    assert 1 <= night["candle"] <= CANDLE_MAX, "a candle is 1-%d units" % CANDLE_MAX
    m = night["mayor"]

    out = ["; generated by scripts/night.py from data/night%d.py" % n,
           "NIGHT_N EQU %d" % n, "NIGHT_NF EQU %d" % len(keys), "NIGHT_NST EQU %d" % len(sts),
           "NIGHT_CANDLE EQU %d" % night["candle"],
           "CDL_Q EQU %d" % (night["candle"] // 4), "CDL_H EQU %d" % (night["candle"] // 2),
           "PAT0 EQU %d" % PAT0, "PATMAX EQU %d" % PATMAX, "GAIN_MAX EQU %d" % GAIN_MAX,
           "BARE EQU %d" % -m["bare"]]
    assert m["bare"] <= 0

    # the orders card, before the first witness
    out.append("night_orders:")
    out += textrec(1, 1, BYEL, "Mayor Ellis gives his orders:")
    row = 3
    for ln in wrap(night["orders"], WIDTH):
        out += textrec(row, 1, BWHT, ln)
        row += 1
    row += 1
    how = ("One by one the witnesses come to your table. Q and A choose a line "
           "of what is sworn; P and L, a line in the book, and 1-6 turn the book "
           "to an earlier statement. SPACE sets the two side by side, and burns "
           "candle. ENTER stamps the statement into the book, with what you have "
           "in hand, and the witness goes. No one is called back.")
    for ln in wrap(how, WIDTH):
        out += textrec(row, 1, YEL, ln)
        row += 1
    assert row <= 22
    out.append("        db 0FFh")

    # headings: the ledger, the book, the names
    place = night["place"].split(",")[0]
    out.append("night_ledger:")
    out += textrec(0, 1, BYEL, "The Ledger")
    out += textrec(1, 1, WHT, night["date"] + ", " + place)
    out.append("        db 0FFh")
    out.append("night_book:")
    out += textrec(0, 1, BYEL, "The Clerk's Book")
    out += textrec(1, 1, WHT, place + ", " + night["date"])
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

    # statements, in case order
    out.append("night_nst: db %d" % len(sts))
    out.append("night_st: dw " + ",".join("st_%d" % i for i in range(len(sts))))
    by_id = {st["id"]: i for i, st in enumerate(sts)}
    for i, st in enumerate(sts):
        own = by_id[st["copy_of"]] if "copy_of" in st else i
        pages = paginate(cl[i])
        short = st["who"].split(",")[0]
        out.append("st_%d:   ; %s" % (i, st["id"]))
        out.append("        dw st_%d_who,st_%d_sw,st_%d_sh,cltab_%d" % (i, i, i, own))  # a copy shares the words
        out.append("        db %d,%d" % (len(cl[i]), len(pages)))
        out.append("        db " + ",".join("%d,%d" % pg for pg in pages))
        out += one("st_%d_who" % i, st["who"])
        out += one("st_%d_sw" % i, "Sworn " + st["sworn"] + " 1711")
        assert fits(11, short), short       # row 11: "The book: 5  " then the name
        assert len(short) <= 20, short      # the book: "name" then "Entered as sworn." at column 17
        out += ["st_%d_sh:" % i, asm_str(short)]
        if own == i:
            out.append("cltab_%d: dw " % i + ",".join("cl_%d_%d" % (i, c) for c in range(len(cl[i]))))
            for c, (text, _, _) in enumerate(cl[i]):
                out += block("cl_%d_%d" % (i, c), text, HALFROWS)

    # the pairs, and the findings
    out.append("night_pairs: db %d" % len(pairs))
    for (s0, c0, s1, c1), key in pairs.items():
        out.append("        db %d,%d,%d,%d,%d   ; %s" % (s0, c0, s1, c1, keys.index(key), key))
    out.append("night_find: dw " + ",".join("fr_%d" % i for i in range(len(keys))))
    for i, key in enumerate(keys):
        fd = f[key]
        ways = fd["write"]
        assert fits(8, fd["label"]), "label too long for 'In hand: ': %r" % fd["label"]
        cols, c = [], 2                         # the options side by side from column 2
        for menu in [w[0] for w in ways] + [LETLIE]:
            cols.append(c)
            c += cells(menu)
        assert c <= 31, "%s: the options don't fit one line" % key
        out.append("fr_%d:   ; %s, found at case %d" % (i, key, cases[key] + 1))
        out.append("        db %d,%d" % (KIND[kinds[key]], len(ways)))
        out.append("        dw fl_%d" % i)
        out.append("        db " + ",".join(str(x) for x in (cols + [0, 0, 0])[:3]))
        for j, (menu, book, pat, slip, answer) in enumerate(ways):
            out.append("        dw fm_%d_%d,fb_%d_%d,%s,%s" % (
                i, j, i, j, "fa_%d_%d" % (i, j) if answer else "0", "fs_%d_%d" % (i, j) if slip else "0"))
            out.append("        db %d" % (pat & 255))
        out += ["fl_%d:" % i, asm_str(fd["label"])]
        for j, (menu, book, pat, slip, answer) in enumerate(ways):
            out += ["fm_%d_%d:" % (i, j), asm_str(menu)]
            out += block("fb_%d_%d" % (i, j), book, 3)
            if answer:
                out += block("fa_%d_%d" % (i, j), answer, 2)    # the stamp screen: two a case
            if slip:
                out += one("fs_%d_%d" % (i, j), slip, right=256)
    out.append("night_fcase: db " + ",".join(str(cases[k]) for k in keys))
    # the book must fit: every finding written, with its answer
    book_rows = sum(len(wrap(max((w[1] for w in f[k]["write"]), key=len), WIDTH)) + 3 for k in keys)
    assert book_rows <= 19 * 3, "the book runs past three pages"

    # Mayor Ellis
    assert len(m["manner"]) == 4
    out.append("man_tab: dw " + ",".join("mn_%d" % i for i in range(4)))
    for i, t in enumerate(m["manner"]):
        out += one("mn_%d" % i, t)
    bands = ["gain", "none", "small", "middle", "large"]
    out.append("slip_tab: dw " + ",".join("sl_%s" % b for b in bands))
    for b in bands:
        lst = m["slips"][b]
        assert 1 <= len(lst) <= 8
        out.append("sl_%s: db %d" % (b, len(lst)))
        out.append("        dw " + ",".join("sl_%s_%d" % (b, i) for i in range(len(lst))))
        for i, t in enumerate(lst):
            out += one("sl_%s_%d" % (b, i), t, right=256)
    out.append("cold_tab: db %d" % len(m["cold"]))
    out.append("        dw " + ",".join("cd_%d" % i for i in range(len(m["cold"]))))
    for i, t in enumerate(m["cold"]):
        out += one("cd_%d" % i, t, right=256)
    assert len(m["goodnight"]) == 4
    out.append("good_tab: dw " + ",".join("gn_%d" % i for i in range(4)))
    for i, t in enumerate(m["goodnight"]):
        out += block("gn_%d" % i, t, 2)
    out += block("txt_dismiss", m["dismiss"], 3)
    out += block("txt_next", night["next_orders"], 4)
    out += compile_parade(night)

    open(os.path.join(ROOT, "src", "night.inc"), "w").write("\n".join(out) + "\n")
    return night, pairs, keys


if __name__ == "__main__":
    night, pairs, keys = compile_night(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    print("night.inc: %d statements, %d findings from %d pairs" %
          (len(night["statements"]), len(keys), len(pairs)))
