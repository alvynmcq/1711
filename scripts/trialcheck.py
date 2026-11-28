#!/usr/bin/env python3
"""Check the trial (data/trial.py) and print what Lyle can do with it.

  python3 scripts/trialcheck.py            the record, the witnesses, the paths
  python3 scripts/trialcheck.py --paths    the paths only

Prints the court record, each witness's lines with their presses, the
facts that contradict them (HOLD, SIR!) and the ones with their own
rebuke, then plays each path in "paths" through the whole day by the
engine's rules (src/trial.asm) and prints where the day went, the bench's
patience, what was written and the verdict. The rules, as the engine has
them:
  hear     a line heard for the first time costs "line" minutes
  press    "press" minutes, once a line; a line it draws out is shown
           next and heard at once ("line" minutes more)
  present  a contradiction: "hold" minutes, a note (once), and the
           witness's own bench cost (the Mayor's 3); anything else:
           "wrong" minutes and the witness's wrong cost (silenced at 0)
  a witness stands down when the path is done, when "box" minutes have
  gone since they were called, or at two (the jury retires); a scene
  costs its minutes; a witness or scene not reached by two is not heard
The verdict: the spectral evidence is discredited if a "thirty" note and
at least verdict["spectral"] spectral notes are written; then each
accused whose score (a note on all 1, a note on her 2) reaches
verdict["acquit"] is acquitted. Otherwise all are convicted.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trial  # noqa: E402  (scripts/trial.py)


def hhmm(m):
    return "%d:%02d" % divmod(m, 60)


class Day:
    def __init__(self, T):
        self.T, self.C = T, T["cost"]
        self.t = 0
        self.pat = T["bench"]["start"]
        self.silenced = False
        self.notes, self.log = [], []
        self.end = T["jury"] - T["start"]

    def spend(self, m):
        self.t += m
        if self.t >= self.end or self.t - self.t0 >= self.w["box"]:
            self.over = True

    def witness(self, w, path):
        self.w, self.t0, self.over = w, self.t, False
        self.lines = {ln["id"]: ln for ln in w["lines"]}
        self.order = [ln["id"] for ln in w["lines"]]
        self.shown = [lid for lid in self.order if not self.lines[lid].get("hidden")]
        self.heard, self.pressed, self.raised = set(), set(), set()
        self.hear(self.shown[0])                         # the first line, at once
        if path is None:
            path = [("hearall",)]
        for act in path:
            if self.over:
                self.log.append("    (the bell: %s, %s cut short)" % (hhmm(self.T["start"] + self.t), w["id"]))
                break
            self.do(act)
        self.log.append("  %s: %s to %s, %d minutes" % (w["id"], hhmm(self.T["start"] + self.t0),
                                                        hhmm(self.T["start"] + self.t), self.t - self.t0))

    def hear(self, lid):
        if lid not in self.heard:
            self.heard.add(lid)
            self.spend(self.C["line"])

    def do(self, act):
        kind = act[0]
        if kind == "hearall":
            for lid in list(self.order):
                if lid in self.shown and not self.over:
                    self.hear(lid)
            return
        if kind == "pressall":
            for lid in list(self.order):
                if lid in self.shown and not self.over:
                    self.do(("hear", lid))
                    self.do(("press", lid))
            return
        lid = act[1]
        ln = self.lines[lid]
        if lid not in self.shown:
            raise SystemExit("path: %s's line %s isn't shown yet" % (self.w["id"], lid))
        if kind == "hear":
            self.hear(lid)
            return
        if self.silenced:
            return
        self.hear(lid)
        if kind == "press":
            if lid in self.pressed:
                return
            self.pressed.add(lid)
            self.spend(self.C["press"])
            p = ln.get("press")
            if p:
                q, a, add, nid = p
                if add:
                    self.shown.append(add)
                    self.hear(add)
                if nid:
                    self.write(nid)
        elif kind == "present":
            fid = act[2]
            if fid in ln.get("holds", {}):
                nid = ln["holds"][fid][3]
                if nid in self.notes:
                    return
                self.write(nid)
                self.pat = max(0, self.pat - self.w["hold"])
                self.log.append("    HOLD, SIR! %s at %s, the bench at %d" % (fid, lid, self.pat))
                self.check_silence()
                self.spend(self.C["hold"])
            else:
                self.pat = max(0, self.pat - self.w["wrong"])
                self.log.append("    wrong: %s at %s, the bench at %d" % (fid, lid, self.pat))
                self.check_silence()
                self.spend(self.C["wrong"])

    def check_silence(self):
        if self.pat == 0 and not self.silenced:
            self.silenced = True
            self.log.append("    silenced at %s" % hhmm(self.T["start"] + self.t))

    def write(self, nid):
        if nid not in self.notes:
            self.notes.append(nid)


def verdict(T, notes):
    V, N = T["verdict"], T["notes"]
    spec = sum(1 for n in notes if N[n]["spectral"])
    thirty = any(N[n]["thirty"] for n in notes)
    disc = thirty and spec >= V["spectral"]
    out = []
    for aid, name in T["accused"]:
        score = sum(1 if N[n]["bears"] == "all" else (2 if aid in N[n]["bears"].split() else 0)
                    for n in notes)
        out.append((name, score, disc and score >= V["acquit"]))
    return spec, thirty, disc, out


def play(T, path):
    d = Day(T)
    W = {w["id"]: w for w in T["witnesses"]}
    for o in T["order"]:
        if d.t >= d.end:
            d.log.append("  %s: not heard (two o'clock)" % o)
            continue
        if o in T["scenes"]:
            d.t += T["scenes"][o]["cost"]
            d.log.append("  %s brought in: %d minutes" % (o, T["scenes"][o]["cost"]))
            continue
        d.witness(W[o], path.get(o))
    return d


def main():
    T = trial.load()
    nids = trial.check(T)
    st = T["start"]
    if "--paths" not in sys.argv:
        print("THE COURT RECORD")
        for i, (fid, fact, who, when) in enumerate(T["record"]):
            print("  %2d %-12s %-37s %s, %s" % (i + 1, fid, fact, who, when))
        for w in T["witnesses"]:
            print("\n%s (%d lines, %d hidden; box %d, bench %d a HOLD, %d wrong)" % (
                w["name"], len(w["lines"]), sum(1 for ln in w["lines"] if ln.get("hidden")),
                w["box"], w["hold"], w["wrong"]))
            for ln in w["lines"]:
                print("  %s%s: %s" % (ln["id"], " (drawn out)" if ln.get("hidden") else "",
                                      " / ".join(trial.wrap(ln["say"]))))
                if "press" in ln:
                    q, a, add, nid = ln["press"]
                    extra = []
                    if add:
                        extra.append("draws out %s" % add)
                    if nid:
                        extra.append("note %s%s" % (nid, " (spectral)" if T["notes"][nid]["spectral"] else ""))
                    print("      press: %s%s" % (q, " [%s]" % ", ".join(extra) if extra else ""))
                else:
                    print("      press: nothing more")
                for fid, h in ln.get("holds", {}).items():
                    print("      HOLD, SIR! with %s -> %s" % (fid, h[3]))
                for fid in ln.get("wrong", {}):
                    print("      its own rebuke: %s" % fid)
        print("\nNotes there are to write: %d (%d spectral, %d the thirty)" % (
            len(nids), sum(1 for n in nids if T["notes"][n]["spectral"]),
            sum(1 for n in nids if T["notes"][n]["thirty"])))
        C, B = T["cost"], T["bench"]
        print("Costs: line %d, press %d, hold %d, wrong %d; the day runs %s-%s (%d minutes)"
              % (C["line"], C["press"], C["hold"], C["wrong"], hhmm(st), hhmm(T["jury"]),
                 T["jury"] - st))
    for name, path in T["paths"].items():
        d = play(T, path)
        spec, thirty, disc, out = verdict(T, d.notes)
        print("\n== %s: ends %s, the bench at %d%s, %d notes (%d spectral%s)" % (
            name, hhmm(st + d.t), d.pat, ", silenced" if d.silenced else "",
            len(d.notes), spec, ", the thirty" if thirty else ""))
        for ln in d.log:
            print(ln)
        print("  spectral evidence %s" % ("DISCREDITED" if disc else "stands"))
        print("  " + ", ".join("%s %d %s" % (n, s, "acquitted" if a else "guilty") for n, s, a in out))


if __name__ == "__main__":
    try:
        main()
    except trial.TrialError as e:
        sys.exit("trialcheck: " + str(e))
