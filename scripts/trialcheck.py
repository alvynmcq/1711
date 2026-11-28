#!/usr/bin/env python3
"""Check the trial (data/trial.py) and print what Lyle can do with it.

  python3 scripts/trialcheck.py

Prints the court record, each testimony line with its press, the facts
that contradict it (HOLD, SIR!) and the ones with their own rebuke, then
plays each path in "paths" by the engine's rules (src/trial.asm) and
prints the time, the bench's patience and Lyle's notes at the end.
The rules, as the engine has them:
  hear     a line heard for the first time costs "line" minutes
  press    "press" minutes, once a line (again: "She has answered that.")
  present  a contradiction: "hold" minutes, a note (once); anything else:
           "wrong" minutes and the bench's "wrong" (silenced at 0)
  the bell at slice_end ends the examination
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trial  # noqa: E402  (scripts/trial.py)


def hhmm(m):
    return "%d:%02d" % divmod(m, 60)


class Court:
    def __init__(self, T):
        self.T, self.C, self.B = T, T["cost"], T["bench"]
        self.w = T["witnesses"][0]
        self.lines = {ln["id"]: ln for ln in self.w["lines"]}
        self.t = 0
        self.pat = self.B["start"]
        self.heard, self.pressed, self.raised = set(), set(), set()
        self.shown = {ln["id"] for ln in self.w["lines"] if not ln.get("hidden")}
        self.notes, self.spectral, self.log = [], 0, []
        self.silenced = self.over = False
        self.end = T["slice_end"] - T["start"]

    def spend(self, m):
        self.t += m
        if self.t >= self.end:
            self.over = True
            self.log.append("  the bell: seven o'clock, she stands down")

    def do(self, act):
        if self.over:
            self.log.append("  (too late: %s)" % " ".join(act))
            return
        kind, lid = act[0], act[1]
        ln = self.lines[lid]
        if lid not in self.shown:
            raise SystemExit("path: line %s isn't shown yet" % lid)
        if kind == "hear":
            if lid not in self.heard:
                self.heard.add(lid)
                self.spend(self.C["line"])
            return
        if self.silenced:
            self.log.append("  silenced: %s %s does nothing" % (kind, lid))
            return
        if kind == "press":
            if lid in self.pressed:
                return
            self.pressed.add(lid)
            p = ln.get("press")
            if p:
                q, a, add, note, spec = p
                if add:
                    self.shown.add(add)
                if note:
                    self.notes.append(note)
                    self.spectral += 1 if spec else 0
            self.spend(self.C["press"])
        elif kind == "present":
            fid = act[2]
            if fid in ln.get("holds", {}):
                if (lid, fid) in self.raised:
                    return
                self.raised.add((lid, fid))
                self.notes.append(ln["holds"][fid][3])
                self.log.append("  HOLD, SIR! %s at %s" % (fid, lid))
                self.spend(self.C["hold"])
            else:
                self.pat = max(0, self.pat + self.B["wrong"])
                self.log.append("  wrong: %s at %s, the bench at %d" % (fid, lid, self.pat))
                if self.pat == 0:
                    self.silenced = True
                    self.log.append("  silenced")
                self.spend(self.C["wrong"])


def main():
    T = trial.load()
    notes = trial.check(T)
    st = T["start"]
    print("THE COURT RECORD")
    for i, (fid, fact, who, when) in enumerate(T["record"]):
        print("  %d %-12s %-37s %s, %s" % ((i + 1) % 10, fid, fact, who, when))
    for w in T["witnesses"]:
        print("\n%s (%d lines, %d hidden)" % (w["name"], len(w["lines"]),
                                              sum(1 for ln in w["lines"] if ln.get("hidden"))))
        for ln in w["lines"]:
            print("  %s%s: %s" % (ln["id"], " (drawn out)" if ln.get("hidden") else "",
                                  " / ".join(trial.wrap(ln["say"]))))
            if "press" in ln:
                q, a, add, note, spec = ln["press"]
                extra = []
                if add:
                    extra.append("draws out %s" % add)
                if note:
                    extra.append("%snote" % ("spectral " if spec else ""))
                print("      press: %s%s" % (q, " [%s]" % ", ".join(extra) if extra else ""))
            else:
                print("      press: nothing more")
            for fid in ln.get("holds", {}):
                print("      HOLD, SIR! with %s" % fid)
            for fid in ln.get("wrong", {}):
                print("      its own rebuke: %s" % fid)
    print("\nLyle's notes there are to write: %d" % len(notes))
    C, B = T["cost"], T["bench"]
    print("\nCosts: line %d, press %d, hold %d, wrong %d (bench %d); the slice runs %s-%s"
          % (C["line"], C["press"], C["hold"], C["wrong"], B["wrong"], hhmm(st), hhmm(T["slice_end"])))
    for name, path in T["paths"].items():
        c = Court(T)
        for act in path:
            c.do(act)
        print("\n%s: ends %s, the bench at %d%s, %d notes (%d spectral)" % (
            name, hhmm(st + c.t), c.pat, ", silenced" if c.silenced else "",
            len(c.notes), c.spectral))
        for ln in c.log:
            print(ln)
    allp = sum(C["line"] for _ in T["witnesses"][0]["lines"]) + \
        C["press"] * len(T["witnesses"][0]["lines"])
    print("\nEvery line heard and pressed: %d minutes of %d" % (allp, T["slice_end"] - st))


if __name__ == "__main__":
    try:
        main()
    except trial.TrialError as e:
        sys.exit("trialcheck: " + str(e))
