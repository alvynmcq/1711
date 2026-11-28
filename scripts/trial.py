#!/usr/bin/env python3
"""Compile data/trial.py (v1.0: the day).

Works out what the Z80 would find awkward: every text is wrapped to 40
characters (column 1 on) as a block (db rows, then each row's string, 0),
the time of day in words for every five minutes, and the tables below.

Writes
  src/trialc.inc     the day's common tables, assembled with the code
                     below C000h (main.asm includes it): the record, the
                     notes, the bench, the clock, the order, the scenes,
                     the accused and the verdict
  src/trialw_ID.inc  a witness: its header and lines, assembled into a
                     bank with its portrait (build.py chooses the bank and
                     writes the witness table, witab, to banks.inc)
  src/witnesses.txt  the witness ids, in the order of witab

  wh_ID      the header, WH_SIZE bytes, copied to `wh` (trial.asm) when the
             witness is called:
               dw name, lines; db lines, portrait; dw falter;
               dw opening, after_hold, asked, raised (one row each);
               dw stand_down, bell, press_none's question and answer,
               called (blocks); db box (minutes), bench cost of a HOLD,
               bench cost of a wrong fact
  lines      9 bytes a line: dw say, db flags (1: hidden until pressed),
             dw press (0 none), dw holds (0 none), dw wrong (0 none)
  press      dw question, dw answer, db line drawn out (0FFh none),
             db note (0FFh none), db 0
  holds      db n, then n x (db fact, dw question, dw answer, dw Ormsby,
             db note)
  wrong      db n, then n x (db fact, dw what Ormsby says)
  tr_facts   TR_NF x (dw fact, dw "Sworn by ...")
  tr_notes   TR_NN x dw (Lyle's notes, as blocks)
  tr_ntag    TR_NN x (db the accused it bears on, a bit each; db flags:
             1 spectral, 2 the thirty, 4 character)
  tr_order   TR_NORD x (db 0 a witness / 1 a scene, db which)
  tr_scenes  per scene: db picture (pictab), db minutes, db pages, then a
             dw block per page
  tr_time    a dw per five minutes from TR_START (words, one row)

Run as a script it writes the files; trialcheck.py imports it.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

WIDTH = 40          # characters a row, from column 1
FACTW = 36          # a fact on the record screen, after the mark and number
MAXROWS = 4         # rows 17-20
PAGEROWS = 8        # a scene's page, rows 15-22 under its picture
WH_SIZE = 29


class TrialError(Exception):
    pass


def load():
    # by path: data/trial.py and this file share a module name
    import importlib.util
    spec = importlib.util.spec_from_file_location("trial_data", os.path.join(ROOT, "data", "trial.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.TRIAL


def wrap(s, width=WIDTH):
    out, line = [], ""
    for w in s.split():
        if len(w) > width:
            raise TrialError("word too long: %r" % w)
        if len(line) + len(w) + (1 if line else 0) > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w) if line else w
    if line:
        out.append(line)
    return out


def paras(ps):
    """paragraphs as one block's rows, a blank row between"""
    rows = []
    for p in ps:
        if rows:
            rows.append("")
        rows += wrap(p)
    return rows


HOURS = ["twelve", "one", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "eleven"]
MINS = ["%s o'clock", "five past %s", "ten past %s", "a quarter past %s",
        "twenty past %s", "twenty-five past %s", "half past %s", "twenty-five to %s",
        "twenty to %s", "a quarter to %s", "ten to %s", "five to %s"]


def time_words(minute):
    """minute from midnight -> 'A quarter past six' (to the five minutes below)"""
    h, m = divmod(minute, 60)
    i = m // 5
    hr = HOURS[(h + (1 if i > 6 else 0)) % 12]
    s = MINS[i] % hr
    return s[0].upper() + s[1:]


def rows_ok(s, n, what):
    if len(wrap(s)) > n:
        raise TrialError("%s: more than %d rows: %r" % (what, n, s))


def one_row(s, what):
    if len(s) > WIDTH:
        raise TrialError("%s is %d characters: %r" % (what, len(s), s))


def all_texts(T):
    """every string the game shows from the trial, for the word check"""
    out = []

    def walk(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            for k, v in x.items():
                if k not in ("paths", "id", "portrait", "pic", "bears"):
                    walk(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                walk(v)
    walk(T)
    return out


def check(T):
    """The rules the screens need. Returns the note ids in order."""
    for s in all_texts(T):
        if "witch" in s.lower():
            raise TrialError("'witch' in %r: the accused are never called that" % s)
    for fid, fact, who, when in T["record"]:
        if len(fact) > FACTW:
            raise TrialError("fact %s is %d characters (at most %d): %r" % (fid, len(fact), FACTW, fact))
        if len("Sworn by %s, %s." % (who, when)) > WIDTH - 4:
            raise TrialError("fact %s: who and when too long" % fid)
    if len(T["record"]) > 20:
        raise TrialError("at most twenty facts (two pages)")
    ids = [f[0] for f in T["record"]]
    acc = [a for a, _ in T["accused"]]
    if len(acc) > 8:
        raise TrialError("at most eight accused (a bit each)")
    B = T["bench"]
    for s in B["manner"] + [B["silent_row"], B["silent_key"], B["after_wrong"], B["after_press"]]:
        one_row(s, "bench line")
    for s in B["rebukes"] + [B["silenced"], B["jury_bell"]]:
        rows_ok(s, MAXROWS, "bench")
    nids = list(T["notes"])
    for nid, n in T["notes"].items():
        rows_ok(n["text"], MAXROWS - 1, "note " + nid)
        if n["bears"] != "all":
            for a in n["bears"].split():
                if a not in acc:
                    raise TrialError("note %s bears on %s: no such accused" % (nid, a))
    used = set()
    wids = [w["id"] for w in T["witnesses"]]
    for o in T["order"]:
        if o not in wids and o not in T["scenes"]:
            raise TrialError("order: %s is neither a witness nor a scene" % o)
    for sid, sc in T["scenes"].items():
        for p in sc["pages"]:
            if len(paras(p)) > PAGEROWS:
                raise TrialError("scene %s: a page is more than %d rows" % (sid, PAGEROWS))
    for w in T["witnesses"]:
        if len(w["name"]) > 33:
            raise TrialError("name too long (the hour marks): %r" % w["name"])
        for k in ("opening", "after_hold", "asked", "raised"):
            one_row(w[k], "%s %s" % (w["id"], k))
        for k in ("stand_down", "bell", "called"):
            rows_ok(w[k], MAXROWS, "%s %s" % (w["id"], k))
        if sum(len(wrap(s)) for s in w["press_none"]) > MAXROWS:
            raise TrialError("%s: press_none too long" % w["id"])
        if len(w["lines"]) > 16:
            raise TrialError("%s: at most 16 lines" % w["id"])
        lids = [ln["id"] for ln in w["lines"]]
        for ln in w["lines"]:
            where = "%s %s" % (w["id"], ln["id"])
            rows_ok(ln["say"], MAXROWS, where)
            if "press" in ln:
                q, a, add, nid = ln["press"]
                if add is not None:
                    if add not in lids:
                        raise TrialError("press on %s draws out %s: no such line" % (where, add))
                    j = lids.index(add)
                    if j != lids.index(ln["id"]) + 1 or not w["lines"][j].get("hidden"):
                        raise TrialError("a drawn-out line must be hidden and come next: %s" % add)
                if len(wrap(q)) + len(wrap(a)) > MAXROWS:
                    raise TrialError("press on %s: question and answer more than %d rows"
                                     % (where, MAXROWS))
                if nid is not None:
                    if nid not in nids:
                        raise TrialError("press on %s: no note %s" % (where, nid))
                    used.add(nid)
            for fid, (q, a, o, nid) in ln.get("holds", {}).items():
                if fid not in ids:
                    raise TrialError("hold on %s: no fact %s" % (where, fid))
                if nid not in nids:
                    raise TrialError("hold on %s: no note %s" % (where, nid))
                used.add(nid)
                if len(wrap(q)) > 2:
                    raise TrialError("hold on %s: the question is more than 2 rows: %r" % (where, q))
                for s in (a, o):
                    rows_ok(s, MAXROWS, "hold on " + where)
            for fid, s in ln.get("wrong", {}).items():
                if fid not in ids or fid in ln.get("holds", {}):
                    raise TrialError("wrong on %s: %s" % (where, fid))
                rows_ok(s, MAXROWS, "wrong on " + where)
    for nid in nids:
        if nid not in used:
            raise TrialError("note %s is never written" % nid)
    if len(nids) > 32:
        raise TrialError("at most 32 notes")
    V = T["verdict"]
    for k in ("no_more", "two", "lyle_open", "lyle_none", "lyle_spectral", "lyle_weak",
              "lyle_church", "ormsby_shaken", "jury", "all_guilty", "some", "none"):
        rows_ok(V[k], PAGEROWS - 2, "verdict " + k)
    for s in V["ormsby"]:
        rows_ok(s, PAGEROWS - 2, "ormsby's charge")
    return nids


class Asm:
    def __init__(self, prefix):
        self.out = []
        self.strings = {}
        self.n = 0
        self.prefix = prefix

    def label(self):
        self.n += 1
        return "%s_%d" % (self.prefix, self.n)

    def str1(self, s):
        """a one-row string: label"""
        key = ("s", s)
        if key not in self.strings:
            lb = self.label()
            self.strings[key] = lb
            self.out.append("%s: db %s,0" % (lb, asmstr(s)))
        return self.strings[key]

    def rows(self, rows):
        key = ("b", tuple(rows))
        if key not in self.strings:
            lb = self.label()
            self.strings[key] = lb
            self.out.append("%s: db %d" % (lb, len(rows)))
            for r in rows:
                self.out.append("        db %s,0" % asmstr(r) if r else "        db 0")
        return self.strings[key]

    def block(self, s):
        """wrapped rows: label of db rows, strings"""
        return self.rows(wrap(s))


def asmstr(s):
    for ch in s:
        if not (32 <= ord(ch) < 127):
            raise TrialError("character %r can't be drawn" % ch)
    parts, cur = [], ""
    for ch in s:
        if ch == '"':
            if cur:
                parts.append('"%s"' % cur)
                cur = ""
            parts.append("34")
        else:
            cur += ch
    if cur:
        parts.append('"%s"' % cur)
    return ",".join(parts)


def portrait_index(name):
    sys.path.insert(0, os.path.join(ROOT, "art"))
    from portraits import PORTRAITS
    return [p[0] for p in PORTRAITS].index(name)


def pic_index(name):
    sys.path.insert(0, HERE)
    from story import PICS
    return PICS.index(name)


def compile_witness(T, w, nids):
    ids = [f[0] for f in T["record"]]
    lids = [ln["id"] for ln in w["lines"]]
    a = Asm("tw_" + w["id"])
    hdr = "wh_%s" % w["id"]
    lines = "tw_%s_lines" % w["id"]
    q, ans = w["press_none"]
    body = ["; generated by scripts/trial.py from data/trial.py: do not edit",
            "%s:" % hdr,
            "        dw %s,%s" % (a.str1(w["name"]), lines),
            "        db %d,%d" % (len(w["lines"]), portrait_index(w["portrait"])),
            "        dw falter_%s" % w["portrait"],
            "        dw %s,%s,%s,%s" % (a.str1(w["opening"]), a.str1(w["after_hold"]),
                                        a.str1(w["asked"]), a.str1(w["raised"])),
            "        dw %s,%s,%s,%s,%s" % (a.block(w["stand_down"]), a.block(w["bell"]),
                                           a.block(q), a.block(ans), a.block(w["called"])),
            "        db %d,%d,%d" % (w["box"], w["hold"], w["wrong"])]
    recs = []
    body.append("%s:" % lines)
    for ln in w["lines"]:
        say = a.block(ln["say"])
        pr = ho = wr = "0"
        if "press" in ln:
            pq, pa, add, nid = ln["press"]
            pr = a.label()
            recs.append("%s: dw %s,%s" % (pr, a.block(pq), a.block(pa)))
            recs.append("        db %d,%d,0" % (0xFF if add is None else lids.index(add),
                                               0xFF if nid is None else nids.index(nid)))
        if ln.get("holds"):
            ho = a.label()
            recs.append("%s: db %d" % (ho, len(ln["holds"])))
            for fid, (hq, ha, ho_, nid) in ln["holds"].items():
                recs.append("        db %d" % ids.index(fid))
                recs.append("        dw %s,%s,%s" % (a.block(hq), a.block(ha), a.block(ho_)))
                recs.append("        db %d" % nids.index(nid))
        if ln.get("wrong"):
            wr = a.label()
            recs.append("%s: db %d" % (wr, len(ln["wrong"])))
            for fid, s in ln["wrong"].items():
                recs.append("        db %d" % ids.index(fid))
                recs.append("        dw %s" % a.block(s))
        body.append("        dw %s" % say)
        body.append("        db %d" % (1 if ln.get("hidden") else 0))
        body.append("        dw %s,%s,%s" % (pr, ho, wr))
    return "\n".join(body + recs + a.out) + "\n"


def compile_common(T, nids):
    a = Asm("trs")
    C, B, V = T["cost"], T["bench"], T["verdict"]
    acc = [x for x, _ in T["accused"]]
    wids = [w["id"] for w in T["witnesses"]]
    sids = list(T["scenes"])
    head = ["; generated by scripts/trial.py from data/trial.py: do not edit",
            "TR_NF   EQU %d" % len(T["record"]),
            "TR_NN   EQU %d" % len(nids),
            "TR_NACC EQU %d" % len(acc),
            "TR_NORD EQU %d" % len(T["order"]),
            "TR_START EQU %d" % T["start"],
            "TR_DAY  EQU %d" % (T["jury"] - T["start"]),
            "TR_CLINE EQU %d" % C["line"], "TR_CPRESS EQU %d" % C["press"],
            "TR_CHOLD EQU %d" % C["hold"], "TR_CWRONG EQU %d" % C["wrong"],
            "TR_PAT0 EQU %d" % B["start"],
            "TR_NREB EQU %d" % len(B["rebukes"]),
            "TR_SPECN EQU %d" % V["spectral"],
            "TR_ACQ  EQU %d" % V["acquit"],
            "WH_SIZE EQU %d" % WH_SIZE]
    body = ["tr_facts:"]
    for fid, fact, who, when in T["record"]:
        body.append("        dw %s,%s" % (a.str1(fact), a.str1("Sworn by %s, %s." % (who, when))))
    body.append("tr_notes:")
    for nid in nids:
        body.append("        dw %s" % a.block(T["notes"][nid]["text"]))
    body.append("tr_ntag:")
    for nid in nids:
        n = T["notes"][nid]
        mask = 0xFF if n["bears"] == "all" else sum(1 << acc.index(x) for x in n["bears"].split())
        flags = (1 if n["spectral"] else 0) | (2 if n["thirty"] else 0) | (4 if n["character"] else 0)
        body.append("        db %d,%d" % (mask, flags))
    body.append("tr_manner:")
    body.append("        dw " + ",".join(a.str1(s) for s in B["manner"]))
    body.append("tr_rebukes:")
    body.append("        dw " + ",".join(a.block(s) for s in B["rebukes"]))
    for k in ("silent_row", "silent_key", "after_wrong", "after_press"):
        body.append("tr_%s: dw %s" % (k, a.str1(B[k])))
    for k in ("silenced", "jury_bell"):
        body.append("tr_%s: dw %s" % (k, a.block(B[k])))
    body.append("tr_order:")
    for o in T["order"]:
        body.append("        db %d,%d" % ((0, wids.index(o)) if o in wids else (1, sids.index(o))))
    body.append("tr_scenes:")
    body.append("        dw " + ",".join("trsc_%s" % s for s in sids))
    for s in sids:
        sc = T["scenes"][s]
        body.append("trsc_%s: db %d,%d,%d" % (s, pic_index(sc["pic"]), sc["cost"], len(sc["pages"])))
        body.append("        dw " + ",".join(a.rows(paras(p)) for p in sc["pages"]))
    body.append("tr_acc:")
    body.append("        dw " + ",".join(a.str1(n) for _, n in T["accused"]))
    for k in ("no_more", "two", "lyle_open", "lyle_none", "lyle_spectral", "lyle_weak",
              "lyle_church", "ormsby_shaken", "jury", "all_guilty", "some", "none"):
        body.append("tv_%s: dw %s" % (k, a.block(V[k])))
    for k in ("lyle_head", "ormsby_head", "verdict_head", "guilty", "not_guilty"):
        body.append("tv_%s: dw %s" % (k, a.str1(V[k])))
    body.append("tv_ormsby: db %d" % len(V["ormsby"]))
    body.append("        dw " + ",".join(a.block(s) for s in V["ormsby"]))
    body.append("tr_time:")
    times = list(range(T["start"], T["jury"] + 1, 5))
    for k in range(0, len(times), 8):
        body.append("        dw " + ",".join(a.str1(time_words(m)) for m in times[k:k + 8]))
    return "\n".join(head + body + a.out) + "\n"


def main():
    T = load()
    nids = check(T)
    src = os.path.join(ROOT, "src")
    open(os.path.join(src, "trialc.inc"), "w").write(compile_common(T, nids))
    for w in T["witnesses"]:
        open(os.path.join(src, "trialw_%s.inc" % w["id"]), "w").write(compile_witness(T, w, nids))
    open(os.path.join(src, "witnesses.txt"), "w").write(
        "\n".join("%s %s" % (w["id"], w["portrait"]) for w in T["witnesses"]) + "\n")
    print("trial: %d witnesses, %d facts, %d notes" % (len(T["witnesses"]), len(T["record"]), len(nids)))


if __name__ == "__main__":
    try:
        main()
    except TrialError as e:
        sys.exit("trial.py: " + str(e))
