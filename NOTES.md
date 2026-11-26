# 1711 (working title): project notes, v0.2 slice

A ZX Spectrum 128K game. You are the clerk to Mayor Ellis of Carrickfergus,
taking sworn statements at Braehead House, Islandmagee, in March 1711, as a
young woman names her neighbours as witches. You read, compare and record.
The horror is the process: what gets written down, and what doesn't.

Based on the trial documents edited by Andrew Sneddon and Shannon Devlin
(w1711.org, CC BY 4.0). Real places and dates; every person renamed. The
w1711 graphic novel (CC BY-NC-ND) was read for research only: nothing from
it is used.

## What v0.2 has

Title, the prologue (Sept 1710 to 3 March 1711: the haunting, the boy at
the window, the grave, Agnes Wylie's death, Isobel's arrival, the apron),
the Night One card, Night One's statements (below), a "not in this build
yet" card for the parade, credits with the CC BY attribution. 48K machines
get a "needs a 128K" message.

### Night One's statements (v0.2)

- **Hub**: the six statements (keys 1-6), B the clerk's book, K the parade
  (not built yet: says so), X ends the night. A red mark beside a statement
  means a line in it is marked.
- **Statement reader**: who and when sworn, the statement a clause at a
  time (rows 3-19, "page 1 of 2" when it runs over). Q/A move a line (and
  over the page edge), O/P turn the page, M marks or unmarks the line (a red
  mark in the margin; two marks at most, across any statements), C compares
  the two marked lines, B the book, X back to the hub.
- **Compare**: both lines with who swore them, then what the clerk finds:
  a contradiction, a statement sworn word for word the same as another, or
  "These two lines do not bear on one another." For a finding, Y writes it
  in the book (typed out, with the quill tick) and N leaves it out ("Mayor
  Ellis does not ask what you found."). Either way the marks are used up.
  A finding already written says so.
- **The clerk's book**: what was written down, nothing else (what was found
  and left out is kept, flag 1, for the indictment later), then a page of
  the names taken down this night.
- Every screen is drawn hidden and shown at once (`veil`/`unveil`: text
  colours go to a 768-byte copy while drawing), about 20 frames a page.

## Build

Python 3 with Pillow, `pasmo`, a C compiler (`cc`, builds tools/zx0 once).

    python3 build.py            # -> 1711.tap
    python3 scripts/nightcheck.py 1

build.py runs art/font.py, art/prologue_art.py and scripts/script.py, then
assembles src/main.asm. Tape: BASIC loader (CLEAR 24575), loading screen
(the house), code at 6000h.

## Files

| File | What it is |
|---|---|
| src/main.asm | The engine: 128K check, script interpreter, text, keys |
| src/dzx0_standard.asm | ZX0 decoder (Einar Saukas, BSD 3-Clause, tools/zx0/LICENSE) |
| scripts/story.py | Title, prologue and credits as scripts; the name list |
| scripts/script.py | Compiles scripts to src/script.inc, packs pictures to src/pics.inc |
| art/render.py | Picture renderer: greyscale + ink hints -> Spectrum screen |
| art/prologue_art.py | The three prologue pictures (house, window, grave) |
| art/font.py, art/zx0.py | From Night Porter: the 6-pixel font, the ZX0 wrapper |
| src/night.asm | The night's screens: hub, statement reader, compare, book |
| scripts/night.py | Compiles data/nightN.py to src/night.inc |
| data/night1.py | Night One in the night format (draft content) |
| scripts/nightcheck.py | Checks a night and lists what the clerk can find |
| tools/simtest.py | From Night Porter: headless test runner (SkoolKit) |

## The script engine

Scripts are byte code run by `run` in main.asm: an opcode, then its
arguments. Opcodes: END, CLS attr, PIC addr (ZX0 full screen, hidden while
it unpacks), TEXT row col attr "..", TYPE (the same, a letter every 2
frames with a faint tick; SPACE shows the rest of the page), WAIT row
(flashing SPACE prompt, then clears the text area from that row), PAUSE n,
BORDER n, CLRROWS row n, JUMP addr, CHOICE n {key, addr}, NIGHT (the
night's screens in night.asm, until the clerk presses X). In story.py,
"story" and "say" wrap text and keep a cursor in the text area; the
compiler refuses any page that runs off the screen.

Pictures fill character rows 0-13; text goes in rows 15-22; row 23 is the
prompt. Colours: candle yellow and red on black, white for paper and
moonlight.

## The night format (data/nightN.py)

- **statements**: each has an id, who, when sworn, and lines. A line is
  text, or `(text, claim, value)`. Two statements giving the same claim
  different values are a contradiction the clerk can flag. A statement
  with `copy_of` repeats another word for word, as two of the real
  depositions do ("agreeth with the above, word for word"); the game
  should let the clerk notice that.
- **parade**: the accused, an intro, and choices the clerk makes about how
  she is brought (tell Isobel or not, alone or among others, into the room
  or only to the door). `always` is what happens whatever you choose (the
  fit, as sworn). `record` lists what the clerk can honestly write down
  for each arrangement. That record feeds the indictment at the end.
- **findings**: for every contradiction (by claim name) and every copied
  statement ("copy:<id>"), what the clerk sees when he compares the two
  lines, and what goes in the book if he writes it. night.py refuses a
  finding with no text, or text for a finding that can't happen. Findings
  say what was sworn; they never say who lied, or that anyone was a witch.
- **people**: the clerk's index of names for the night.

scripts/night.py works out everything the Z80 would find awkward: it wraps
each clause to 40 characters (column 1 on), cuts statements into pages of
17 rows, and lists every pair of lines that means something, as (statement,
line, statement, line, finding), so the engine only looks a pair up. A
copied statement shares the original's clause table, so the words really
are the same bytes.

nightcheck.py prints the contradictions, the copies, every way the parade
can be arranged and the text size. Night One: 3.2 KB of text, 2
contradictions (the apron's five or nine knots; whether the house knew
Janet Moore was coming), 1 copied statement, 8 parade arrangements.

## Memory plan

The code stays below C000h (9.6 KB free at v0.2; Night One's text,
about 4 KB with the findings, is in main memory for now and moves to a bank
with the boot stub). Nights' text and pictures go
in banks 1, 3, 4, 6 and 7, loaded from the tape like Night Porter's extras
(boot stub, ROM loader, IM2 table in each bank), and are paged in at C000h
when needed. About 3 KB of text a night uncompressed, so text is not the
constraint; pictures (portraits, about 2-4 KB each packed) are.

## Names (real -> game)

Mary Dunbar -> Isobel Halliday; Ann Haltridge -> Agnes Wylie; James
Haltridge -> Hugh Wylie; Margaret Spear -> Meg Lowry; Knowehead House ->
Braehead House; Janet Liston -> Janet Boyd; Catherine McCalmond -> Kate
Rankin; Elizabeth Sellor -> Bessie Shaw; William Sellor -> William Shaw;
Janet Carson -> Janet Moore; Janet Main -> Janet Kerr; Janet Latimer ->
Janet Erskine; Janet Millar -> Jean Patterson; Margaret Mitchell ->
Margaret Ross; "Mrs Ann" stays; Robert Sinclair -> Robert Gordon; Edward
Clements -> Mayor Thomas Ellis; Justice Upton -> Justice Lyle; Justice
MacCartney -> Justice Ormsby. Witnesses: Fenton -> William Dickey,
Willson -> John Wilson, Donaldson -> Hugh Gilmour.

## Next

1. The parade screen for Kate Rankin and its record (K on the hub).
2. Whether comparing costs anything (the Mayor's patience, candles), so
   the clerk can't simply try every pair.
3. Portraits (Isobel first), hand-checked for the "human, not monstrous"
   rule: the accused's scars are never the scary part.
4. Banks and the boot stub; AY music (a slow theme, a church-bell tone).

## Testing

v0.2: as below, plus three key scripts from the hub (tools/simtest.py,
keys every 40 frames): the apron (Lowry line 3 against Margaret Wylie line
1, written in, then the book and the names); Dickey against Wilson (the
copy, left out), Gilmour against Gordon (Janet Moore, written in), paging,
Q over the page edge, C with no marks, a third mark, a pair with no
bearing, the book holding only the Moore entry, X to the end card; K on
the hub, unmarking, and comparing a pair already in the book. Screens in
docs/v02_screens.png.

v0.1: SkoolKit tap2sna (real ROM loader, 48K and 128K) + tools/simtest.py:
the 48K message; on 128K title -> whole prologue (13 SPACE presses) ->
Night One card -> credits -> title; C from the title for credits. Not yet
tested in FuseX or on real hardware.
