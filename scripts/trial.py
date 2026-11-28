#!/usr/bin/env python3
"""Compile data/trial.py to src/trial.inc (stage 3, v0.9).

Works out what the Z80 would find awkward: every text is wrapped to 40
characters (column 1 on) as a block (db rows, then each row's string, 0),
the time of day in words for every five minutes, and the tables below.
The labels and EQUs end up in src/trialsym.inc (build.py), so
src/trial.asm reads everything from the bank in place.

  tr_lines   TR_NL x 9 bytes: dw say, db flags (1: hidden until pressed),
             dw press (0 none), dw holds (0 none), dw wrong (0 none)
  press      dw question, dw answer, db line drawn out (0FFh none),
             db note (0FFh none), db spectral
  holds      db n, then n x (db fact, dw question, dw answer, dw Ormsby,
             db note)
  wrong      db n, then n x (db fact, dw what Ormsby says)
  tr_facts   TR_NF x (dw fact, dw "Sworn by ...")
  tr_notes   TR_NN x dw (Lyle's notes, as blocks)
  tr_time    a dw per five minutes from TR_START (words, one row)

Run as a script it writes src/trial.inc; trialcheck.py imports it.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

WIDTH = 40          # characters a row, from column 1
FACTW = 36          # a fact on the record screen, after the mark and number
MAXROWS = 4         # rows 17-20


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


def check(T):
    """The rules the screens need. Returns the notes in order (texts)."""
    for fid, fact, who, when in T["record"]:
        if len(fact) > FACTW:
            raise TrialError("fact %s is %d characters (at most %d): %r" % (fid, len(fact), FACTW, fact))
        if len("Sworn by %s, %s." % (who, when)) > WIDTH - 4:
            raise TrialError("fact %s: who and when too long" % fid)
    if len(T["record"]) > 10:
        raise TrialError("at most ten facts (keys 1-0)")
    ids = [f[0] for f in T["record"]]
    B = T["bench"]
    for s in B["manner"] + [B["silent_row"]]:
        if len(s) > WIDTH:
            raise TrialError("manner line too long: %r" % s)
    for k in ("silent_key", "opening", "asked", "raised", "after_hold", "after_wrong",
              "after_press"):
        if len(B[k]) > WIDTH:
            raise TrialError("remark %s is %d characters: %r" % (k, len(B[k]), B[k]))
    for s in B["rebukes"] + [B["silenced"], B["stand_down"], B["bell"]]:
        if len(wrap(s)) > MAXROWS:
            raise TrialError("more than %d rows: %r" % (MAXROWS, s))
    notes = []
    for w in T["witnesses"]:
        if len(w["name"]) > 33:
            raise TrialError("name too long (the hour marks): %r" % w["name"])
        lids = [ln["id"] for ln in w["lines"]]
        for ln in w["lines"]:
            if len(wrap(ln["say"])) > MAXROWS:
                raise TrialError("line %s: more than %d rows" % (ln["id"], MAXROWS))
            if "press" in ln:
                q, a, add, note, spec = ln["press"]
                for s in (q, a):
                    if len(wrap(s)) > MAXROWS:
                        raise TrialError("press on %s: too long: %r" % (ln["id"], s))
                if add is not None:
                    if add not in lids:
                        raise TrialError("press on %s draws out %s: no such line" % (ln["id"], add))
                    j = lids.index(add)
                    if j != lids.index(ln["id"]) + 1 or not w["lines"][j].get("hidden"):
                        raise TrialError("a drawn-out line must be hidden and come next: %s" % add)
                if len(wrap(q)) + len(wrap(a)) > MAXROWS:
                    raise TrialError("press on %s: question and answer more than %d rows"
                                     % (ln["id"], MAXROWS))
                if note:
                    if len(wrap(note)) > MAXROWS - 1:
                        raise TrialError("note on %s: more than %d rows" % (ln["id"], MAXROWS - 1))
                    notes.append(note)
            for fid, (q, a, o, note) in ln.get("holds", {}).items():
                if len(wrap(note)) > MAXROWS - 1:
                    raise TrialError("hold note on %s: more than %d rows" % (ln["id"], MAXROWS - 1))
                if fid not in ids:
                    raise TrialError("hold on %s: no fact %s" % (ln["id"], fid))
                if len(wrap(q)) > 2:
                    raise TrialError("hold on %s: the question is more than 2 rows: %r" % (ln["id"], q))
                for s in (a, o, note):
                    if len(wrap(s)) > MAXROWS:
                        raise TrialError("hold on %s: too long: %r" % (ln["id"], s))
                notes.append(note)
            for fid, s in ln.get("wrong", {}).items():
                if fid not in ids or fid in ln.get("holds", {}):
                    raise TrialError("wrong on %s: %s" % (ln["id"], fid))
                if len(wrap(s)) > MAXROWS:
                    raise TrialError("wrong on %s: too long" % ln["id"])
            for s in (ln["say"],) + tuple(ln.get("press", ())[:2]):
                if "witch" in s.lower():
                    raise TrialError("'witch' in %s: the accused are never called that" % ln["id"])
    if len(notes) > 16:
        raise TrialError("at most 16 notes")
    if sum(len(wrap(s)) for s in T["press_none"]) > MAXROWS:
        raise TrialError("press_none too long")
    return notes


class Asm:
    def __init__(self):
        self.out = []
        self.strings = {}
        self.n = 0

    def label(self):
        self.n += 1
        return "trs_%d" % self.n

    def str1(self, s):
        """a one-row string: label"""
        key = ("s", s)
        if key not in self.strings:
            lb = self.label()
            self.strings[key] = lb
            self.out.append("%s: db %s,0" % (lb, asmstr(s)))
        return self.strings[key]

    def block(self, s):
        """wrapped rows: label of db rows, strings"""
        key = ("b", s)
        if key not in self.strings:
            lb = self.label()
            rows = wrap(s)
            self.strings[key] = lb
            self.out.append("%s: db %d" % (lb, len(rows)))
            for r in rows:
                self.out.append("        db %s,0" % asmstr(r))
        return self.strings[key]


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


def compile_trial(T):
    notes = check(T)
    a = Asm()
    ids = [f[0] for f in T["record"]]
    w = T["witnesses"][0]          # the slice: one witness
    lids = [ln["id"] for ln in w["lines"]]
    C, B = T["cost"], T["bench"]
    head = ["; generated by scripts/trial.py from data/trial.py: do not edit",
            "TR_NL   EQU %d" % len(w["lines"]),
            "TR_NF   EQU %d" % len(T["record"]),
            "TR_NN   EQU %d" % len(notes),
            "TR_START EQU %d" % T["start"],
            "TR_END  EQU %d" % (T["slice_end"] - T["start"]),
            "TR_CLINE EQU %d" % C["line"], "TR_CPRESS EQU %d" % C["press"],
            "TR_CHOLD EQU %d" % C["hold"], "TR_CWRONG EQU %d" % C["wrong"],
            "TR_PAT0 EQU %d" % B["start"], "TR_PWRONG EQU %d" % (-B["wrong"]),
            "TR_NREB EQU %d" % len(B["rebukes"])]
    body = []
    body.append("tr_name: db %s,0" % asmstr(w["name"]))
    recs = []                      # press, holds, wrong records after the table
    body.append("tr_lines:")
    for ln in w["lines"]:
        say = a.block(ln["say"])
        pr = ho = wr = "0"
        if "press" in ln:
            q, ans, add, note, spec = ln["press"]
            pr = a.label()
            recs.append("%s: dw %s,%s" % (pr, a.block(q), a.block(ans)))
            recs.append("        db %d,%d,%d" % (0xFF if add is None else lids.index(add),
                                                 0xFF if not note else notes.index(note),
                                                 1 if spec else 0))
        if ln.get("holds"):
            ho = a.label()
            recs.append("%s: db %d" % (ho, len(ln["holds"])))
            for fid, (q, ans, o, note) in ln["holds"].items():
                recs.append("        db %d" % ids.index(fid))
                recs.append("        dw %s,%s,%s" % (a.block(q), a.block(ans), a.block(o)))
                recs.append("        db %d" % notes.index(note))
        if ln.get("wrong"):
            wr = a.label()
            recs.append("%s: db %d" % (wr, len(ln["wrong"])))
            for fid, s in ln["wrong"].items():
                recs.append("        db %d" % ids.index(fid))
                recs.append("        dw %s" % a.block(s))
        body.append("        dw %s" % say)
        body.append("        db %d" % (1 if ln.get("hidden") else 0))
        body.append("        dw %s,%s,%s" % (pr, ho, wr))
    body += recs
    body.append("tr_facts:")
    for fid, fact, who, when in T["record"]:
        body.append("        dw %s,%s" % (a.str1(fact), a.str1("Sworn by %s, %s." % (who, when))))
    body.append("tr_notes:")
    for n in notes:
        body.append("        dw %s" % a.block(n))
    body.append("tr_manner:")
    body.append("        dw " + ",".join(a.str1(s) for s in B["manner"]))
    body.append("tr_rebukes:")
    body.append("        dw " + ",".join(a.block(s) for s in B["rebukes"]))
    for k in ("silent_row", "silent_key", "opening", "asked", "raised", "after_hold",
              "after_wrong", "after_press"):
        body.append("tr_%s: dw %s" % (k, a.str1(B[k])))
    for k in ("silenced", "stand_down", "bell"):
        body.append("tr_%s: dw %s" % (k, a.block(B[k])))
    q, ans = T["press_none"]
    body.append("tr_pnone: dw %s,%s" % (a.block(q), a.block(ans)))
    body.append("tr_time:")
    times = list(range(T["start"], T["jury"] + 1, 5))
    for k in range(0, len(times), 8):
        body.append("        dw " + ",".join(a.str1(time_words(m)) for m in times[k:k + 8]))
    return "\n".join(head + body + a.out) + "\n", notes


def main():
    T = load()
    text, notes = compile_trial(T)
    open(os.path.join(ROOT, "src", "trial.inc"), "w").write(text)
    print("trial.inc: %d lines, %d facts, %d notes" % (
        len(T["witnesses"][0]["lines"]), len(T["record"]), len(notes)))


if __name__ == "__main__":
    try:
        main()
    except TrialError as e:
        sys.exit("trial.py: " + str(e))
