# 1711 (working title): project notes, v0.4 slice

A ZX Spectrum 128K game. You are the clerk to Mayor Ellis of Carrickfergus,
taking sworn statements at Braehead House, Islandmagee, in March 1711, as a
young woman names her neighbours as witches. You read, compare and record.
The horror is the process: what gets written down, and what doesn't.

Based on the trial documents edited by Andrew Sneddon and Shannon Devlin
(w1711.org, CC BY 4.0). Real places and dates; every person renamed. The
w1711 graphic novel (CC BY-NC-ND) was read for research only: nothing from
it is used.

## What v0.4 has

Title, the prologue (Sept 1710 to 3 March 1711: the haunting, the boy at
the window, the grave, Agnes Wylie's death, Isobel's arrival, the apron),
told as hearsay (v0.4): the clerk arrives on 3 March, so everything before
is what the household says or swears ("Meg says", "they say"), closing on
"You saw none of what came before. You have only what the household says."
the Night One card, Night One's statements and Kate Rankin's parade
(below), an end card, credits with the CC BY attribution. 48K machines
get a "needs a 128K" message.

### Night One's statements (v0.2)

- **Hub**: the six statements (keys 1-6), B the clerk's book, K the parade
  (once a night; after that it says she has been brought), X ends the night
  after "End the night? Y/N" (v0.4). A red mark beside a statement
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
- **The parade** (v0.3): the arranging screen shows the intro and three
  choices, each with two options (1-3 toggle; the chosen one bright with
  a red mark). SPACE sends for her, X backs out. The scene is typed: a
  sentence per choice, the fit (always, bright), then anything the clerk
  notices ("seen"). Then the record: the fit is written whatever happens,
  because the Mayor gives the words; each other line that applies is
  shown and the clerk presses Y (bright, marked, written) or N (plain
  white with a dash in the margin, left out; v0.3's dim blue was
  unreadable). After the fit the scene types Kate's own plain words
  ("spoken", v0.4). The book shows the fit under "In Mayor Ellis's words:"
  in bright white (v0.4), then the lines written, after the findings, and
  runs on to another page when it is full.
- **The index of names** (v0.4): each accused has an ordinary detail
  (invented, not from the records: flax and eggs, mending nets, a daughter
  who walked to the minister's), the name in white, the detail indented in
  yellow.
- Every screen is drawn hidden and shown at once (`veil`/`unveil`: text
  colours go to a 768-byte copy while drawing), about 20 frames a page.
- Register rules (v0.4): `strat` and `unveil` keep BC; `drawclause` keeps C
  and returns B as the row below the block. Callers no longer push BC
  around them.

## Build

Python 3 with Pillow, `pasmo`, a C compiler (`cc`, builds tools/zx0 once).

    python3 build.py            # -> 1711.tap
    python3 scripts/nightcheck.py 1

    python3 tools/keytest.py    # headless key-script tests (SkoolKit)

build.py runs art/font.py, art/prologue_art.py, scripts/script.py and
scripts/night.py, assembles src/night.inc on its own at NBUF (as high
under C000h as it fits; A600h for Night One), packs it with ZX0 into
src/night.zx0 and writes its labels to src/nightsym.inc, then assembles
src/main.asm. `night` unpacks it to NBUF at the start of each night.
Tape: BASIC loader (CLEAR 24575), loading screen (the house), code at 6000h.

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
| tools/keytest.py | Runs tools/tests/*.keys, compares with tools/ref/*.png |

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
  different values are a contradiction the clerk can flag. A claim must
  appear in at least two statements (a copy counts as its original):
  nightcheck.py warns about one that doesn't. Otherwise make it plain text.
- **dates**: every Night One statement shows "Sworn 3rd March". The real
  sources are listed in data/night1.py (Gilmour's is from 5 March; Lowry's,
  Margaret Wylie's and Gordon's come from Tisdall's account and the 1822
  narrative), and the credits say "Dates and order compressed". A statement
  with `copy_of` repeats another word for word, as two of the real
  depositions do ("agreeth with the above, word for word"); the game
  should let the clerk notice that.
- **parade** (format changed in v0.3: each choice is (heading, options),
  each option (name, menu text, scene sentence); "fit" is the line the
  Mayor gives; "seen" lines are what the clerk notices, which keep an
  ordinary explanation in view; night.py works out, for each of the 2^n
  arrangements, which seen and record lines apply, and checks the scene
  and record screens fit): the accused, an intro, and choices the clerk makes about how
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
can be arranged and the text size. Night One (v0.4): 4.9 KB of text, 3
contradictions (the apron's five or nine knots; who found the apron, Lowry
or Miss Halliday; whether the house knew Janet Moore was coming), 1 copied
statement, 8 parade arrangements. The parade also has "spoken": what the
accused says, typed after the fit every time.

## Memory plan

The code stays below C000h. v0.4: code 6000h-9962h (14.3 KB), then 3.2 KB
free, then the night buffer A600h-BFFFh: Night One's text and tables, 6.4
KB unpacked, kept in the code as 2.9 KB of ZX0 (was 6.4 KB unpacked in the
code at v0.3). The buffer moves to a bank with the boot stub. Nights' text and pictures go
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

1. Pack the prologue's script with ZX0 too (3.0 KB -> about 1.8 KB). Not
   done in v0.4: the scripts jump between title, prologue and credits and
   point at the pictures by address, so they need a "load script" opcode
   and pictures by number first. The night's text is packed (v0.4).
2. To discuss before building: what the clerk's book is for. Ideas: it
   feeds Justice Lyle's doubts at the trial (the real Justice Upton argued
   for acquittal and was outvoted); a candle that burns down with each
   compare, so comparing has a cost and the clerk can't try every pair.
3. Portraits (Isobel first), hand-checked for the "human, not monstrous"
   rule: the accused's scars are never the scary part.
4. Banks and the boot stub; AY music (a slow theme, a church-bell tone).

## Testing

v0.4: committed tests. `python3 tools/keytest.py` loads 1711.tap with
tap2sna (128K ROM loader, to 6000h), runs each tools/tests/*.keys through
tools/simtest.py and compares the screens with tools/ref/*.png pixel for
pixel; any change fails, and the new screen goes to tools/out/ (--sheet
writes a contact sheet, --update rewrites the references once a change is
right). Tests: prologue (every page, title to hub), apron (Lowry line 2
against Margaret Wylie line 2, the new who-found-it finding, written in,
the book and the names page), parade (tell/among/room, Kate's words, N Y
Y, the book with the Mayor's words, X then N, X then Y, the end card).

v0.3: the parade, from the hub: tell/among/room (scene, three lines,
N then Y), quiet/among/door (both door lines written, the book), a whole
night with all three findings and three parade lines written (the book
runs on to a second page), K a second time, X to the end card. Two bugs
found and fixed this way: the SPACE that sends for her was still held and
skipped the typed scene (now `release` first), and text drawing clobbers
B (push/pop around `strat`, and around `unveil`, whose LDIR zeroes BC).

v0.2: as below, plus three key scripts from the hub (tools/simtest.py,
keys every 40 frames): the apron (Lowry line 3 against Margaret Wylie line
1, written in, then the book and the names); Dickey against Wilson (the
copy, left out), Gilmour against Gordon (Janet Moore, written in), paging,
Q over the page edge, C with no marks, a third mark, a pair with no
bearing, the book holding only the Moore entry, X to the end card; K on
the hub, unmarking, and comparing a pair already in the book. Screens in
docs/v02_screens.png and docs/v03_parade.png.

v0.1: SkoolKit tap2sna (real ROM loader, 48K and 128K) + tools/simtest.py:
the 48K message; on 128K title -> whole prologue (13 SPACE presses) ->
Night One card -> credits -> title; C from the title for credits. Not yet
tested in FuseX or on real hardware.
