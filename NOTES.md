# 1711 (working title): project notes, v0.7

A ZX Spectrum 128K game. You are the clerk to Mayor Ellis of Carrickfergus,
taking sworn statements at Braehead House, Islandmagee, in March 1711, as a
young woman names her neighbours as witches. You read, compare and record.
The horror is the process: what gets written down, and what doesn't.

Based on the trial documents edited by Andrew Sneddon and Shannon Devlin
(w1711.org, CC BY 4.0). Real places and dates; every person renamed. The
w1711 graphic novel (CC BY-NC-ND) was read for research only: nothing from
it is used.

## What v0.7 has

v0.7: the banks and the boot stub (see Memory plan). Nothing on screen
changes: every test screen is the same, pixel for pixel. The code below
C000h goes from 14.2 KB to 6.2 KB, with 18 KB free there for Nights Two
and Three and the trial.

## What v0.5 has

v0.5: the scripts (title, prologue, credits) are packed with ZX0 in
chunks, like the night's text (see The script engine), and the candle
(below). Otherwise as v0.4:


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
- **The candle** (v0.5): one a night (`candle` in the night data, 1-16;
  Night One 16). C burns 1; Y on a finding burns 2 more (never below 0);
  the parade and reading cost nothing. Drawn in the top right corner
  (column 31, pixel rows 0-23) on the hub, the reader and the compare
  screen: a dish, a pixel of wax a unit, a 5-pixel flame (its cell bright
  yellow). When a compare uses the last of it the compare screen says "The
  candle has burnt down to nothing."; after that C says the candle is out
  (reading by the fire goes on). The night card says "You have one candle
  for the night."; the hub's help says C burns candle and writing burns
  more. "page 1 of 2" moved to column 22 to leave the corner free.
  Night One: all four findings written cost 12, leaving 4 compares that
  find nothing (nightcheck.py prints this).
- **The index of names** (v0.4): each accused has an ordinary detail
  (invented, not from the records: flax and eggs, mending nets, a daughter
  who walked to the minister's), the name in white, the detail indented in
  yellow.
- Every screen is drawn hidden and shown at once (`veil`/`unveil`: text
  colours go to a 768-byte copy while drawing), about 20 frames a page.
- Register rules (v0.4): `strat` and `unveil` keep BC; `drawclause` keeps C
  and returns B as the row below the block. Callers no longer push BC
  around them.

### Portraits (v0.6, under way)

- Decided (26 Nov): portraits are 10 x 12 characters (80 x 96 pixels), on
  the Night One card (Isobel above "NIGHT ONE", the clerk's first sight
  of her: the prologue is hearsay) and on the parade's arranging screen
  (the accused, columns 22-31; Kate first, a new face each night). Not
  on the statement reader (its 40-column text would halve) and not yet on
  the index of names (a page per person, later, with banks).
- art/portraits.py draws them: shapes at 4x in greyscale with ink hints,
  scaled down and quantised to five clean dither patterns (0, 1/4, 1/2,
  3/4, 1), no grain, then the eyes, nose and mouth set a pixel at a time
  so the scaling doesn't smear them. Written out as a block: 96 pixel rows
  of 10 bytes, then 12 rows of 10 colours (1080 bytes), packed by
  script.py into pics.inc (`porttab`).
- PORTRAIT n row col (opcode 13; ("portrait", name, row, col) in a script):
  `portrait` (A, B row, C col) unpacks to PSCR, blacks out the block's
  colours, copies the pixels, then the colours, so it appears at once;
  colours go through `attrbase`, so it works on a veiled night screen.
- Isobel: candle low on the left, a linen coif lost in shadow on the right
  (never a ring: no halo), red bodice, white neckerchief; she looks at the
  clerk, mouth level, tired. Not a monster, not a saint. 367 bytes packed.
  The Night One card's text moved down 4 rows (title row 13).

### From the first play-test (v0.6)

- The tester marked the two knot lines but may not have seen "Two lines
  marked. C compares them." (row 20, the same yellow as the statement).
  Now it is bright white, and `ckeys` makes "C  compare" in the key help
  flash bright white while two lines are marked and there is candle left
  (plain again when the candle is out, so it never invites a compare that
  can't happen). Called after the page's key help is drawn and after M.
- The parade option "No further than the house door" is now "Only to the
  house door", leaving columns 22-31 clear for Kate's portrait.

## Build

Python 3 with Pillow, `pasmo`, a C compiler (`cc`, builds tools/zx0 once).

    python3 build.py            # -> 1711.tap
    python3 scripts/nightcheck.py 1

    python3 tools/keytest.py    # headless key-script tests (SkoolKit)

build.py runs art/font.py, art/prologue_art.py, art/portraits.py,
scripts/script.py and scripts/night.py, then builds the bank images, each
assembled at C000h (v0.7):

- bank 1: the script buffer SBUF (C000h, as long as the largest chunk; not
  on the tape), then the script chunks packed with ZX0, the prologue
  pictures and the portraits shown from scripts (Isobel). LOAD pages bank
  1 in and unpacks the chunk to SBUF, in the same bank; the script runs
  from there.
- bank 3: Night One's text and tables (night.inc) at C000h, read in place:
  `night` pages bank 3 in for the whole night (no unpacking, no buffer),
  then the portraits shown during the night (Kate, next).

Which bank a portrait goes in is PORT_BANK in build.py. Then it writes
src/banks.inc (chunktab, pictab, porttab as `db bank, dw address`, and the
stub's load table B_tab) and src/nightsym.inc (the night's labels, NBUF =
C000h), and assembles src/main.asm. build.py stops if the code reaches
C000h or a bank runs into PSCR or the IM2 table, and prints what's free.

Tape: BASIC loader (CLEAR 24575), loading screen (the house), code at
6000h, then a headerless block per bank (bank 1, bank 3), each packed with
ZX0 when that saves room (bank 1's contents are packed already, so it goes
raw; bank 3 goes packed, 2942 bytes for 6452).

## Files

| File | What it is |
|---|---|
| src/main.asm | The engine: 128K check, paging (`page`, `farent`), IM2 handler, script interpreter, text, keys |
| src/boot.asm | The boot stub (v0.7): loads the banks, writes the IM2 table into each; sits in abuf |
| src/dzx0_standard.asm | ZX0 decoder (Einar Saukas, BSD 3-Clause, tools/zx0/LICENSE) |
| scripts/story.py | Title, prologue and credits as scripts; the name list |
| scripts/script.py | Compiles scripts to chunks (src/chunkN.inc), packs pictures to src/pics.inc |
| art/render.py | Picture renderer: greyscale + ink hints -> Spectrum screen |
| art/prologue_art.py | The three prologue pictures (house, window, grave) |
| art/portraits.py | Portraits, 10 x 12 characters (Isobel) |
| art/font.py, art/zx0.py | From Night Porter: the 6-pixel font, the ZX0 wrapper |
| src/night.asm | The night's screens: hub, statement reader, compare, book |
| scripts/night.py | Compiles data/nightN.py to src/night.inc |
| data/night1.py | Night One in the night format (draft content) |
| scripts/nightcheck.py | Checks a night and lists what the clerk can find |
| tools/simtest.py | From Night Porter: headless test runner (SkoolKit) |
| tools/keytest.py | Runs tools/tests/*.keys, compares with tools/ref/*.png (snapshot at `game`, after boot) |

## The script engine

Scripts are byte code run by `run` in main.asm: an opcode, then its
arguments. Opcodes: END, CLS attr, PIC n (picture n from `pictab`, a ZX0
full screen, hidden while it unpacks; by number since v0.5), TEXT row col attr "..", TYPE (the same, a letter every 2
frames with a faint tick; SPACE shows the rest of the page), WAIT row
(flashing SPACE prompt, then clears the text area from that row), PAUSE n,
BORDER n, CLRROWS row n, JUMP addr, CHOICE n {key, addr}, NIGHT n (the
night's screens in night.asm, until the clerk presses X, then LOAD n),
LOAD n (v0.5: unpack chunk n to SBUF and run it from its start),
PORTRAIT n row col (v0.6).

Chunks (v0.5): each script in story.py is a chunk, packed with ZX0. A
("night",) step ends its chunk, and the steps after it become the next
chunk ("prologue_start_after": the end card), because the night's text is
unpacked over the script buffer. script.py turns a jump to another chunk
into LOAD n and a choice into a two-byte LOAD stub, so a label another
chunk goes to must be the first thing in its chunk (the compiler checks).
v0.5 chunks: title 189 bytes, prologue 3042, end card 155, credits 602;
3988 bytes in all, 2455 packed. Unpacking the prologue takes a few
frames, so the SPACE that begins no longer also skips page 1's typing.
Later the chunks move to banks with the nights (LOAD will page one in). In story.py,
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
- **candle** (v0.5): the night's candle in units, 1-16 (see above).

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

v0.7 (decided 26 Nov): Night Porter's way, the boot stub, the ROM loader
and the IM2 table in each bank.

| Where | What |
|---|---|
| 5B00h-5BFFh | The stack, once IM2 is on (BASIC's done with) |
| 6000h-7821h | The code: engine, night screens, ZX0 decoder, font, tables, variables, abuf (6178 bytes) |
| 7822h-BFFFh | Free: 18398 bytes, for Nights Two and Three's screens and the trial |
| C000h, bank 0 | Nothing yet but the IM2 table (the AY player, later) |
| bank 1 | SBUF C000h-CC0Ch, chunks, pictures, Isobel; ends E06Eh, 5970 free under PSCR |
| bank 3 | Night One C000h-D933h; 9417 free (Kate goes here, with PSCR) |
| banks 4, 6, 7 | Night Two, Night Three, the trial (each with its portraits); free now |
| F7C0h-FBF7h | PSCR, the portrait scratch, in any bank that holds a portrait |
| FDFDh-FF00h | The IM2 jump (JP isr) and table, in banks 0, 1, 3, 4, 6, 7 |

- Startup: `start` checks for a 128K (else "needs a 128K"), pages bank 0,
  calls `B_boot`. The stub is assembled inside abuf (the veil buffer:
  768 bytes of zeros on the tape anyway, first used in the night), so it
  costs nothing. For each block in B_tab it pages the bank, loads it with
  the ROM's LD-BYTES entered at 056Bh (so BREAK comes back to us), and if
  packed (loaded high, just under FDFDh) unpacks it in place to its
  address. Then the IM2 table into banks 0, 1, 3, 4, 6, 7, bank 0 back in.
  A tape error or BREAK: "Tape loading error. Rewind a little and load
  again." and stop. Then `booted`: I = FEh, IM 2, the stack to 5B00h.
- `page` (A = bank) writes `curbank` before the OUT, so an interrupt that
  pages (the music) can always put the right bank back. `isr` only counts
  `frames` for now. `farent` reads a (bank, address) table entry.
- PIC and PORTRAIT page the picture's bank in, draw, and put back the
  bank that was in, so a script (bank 1) or a night (bank 3) can show a
  picture from any bank. A portrait unpacks to PSCR in its own bank.
- Each night's finding flags (16 bytes) and parade record stay below
  C000h, so they outlive the night's bank being paged out (for the trial).
- When Night Two comes: night.inc needs a short header at C000h (the
  NIGHT_ constants, the tables' addresses) so night.asm reads them from
  the paged night rather than from nightsym.inc; `night` takes a bank.

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

1. Done in v0.5: the scripts are ZX0 chunks (LOAD, pictures by number);
   1.5 KB saved.
2. Decided (26 Nov): the clerk's book feeds Justice Lyle's doubts at the
   trial (the real Justice Upton argued for acquittal and was outvoted),
   and one candle a night is the cost: comparing burns a little, writing a
   finding out burns more, so leaving one out keeps light for comparing.
   Why: comparing was free (Night One: 30 lines, 435 pairs, 9 that mean
   anything) and Y was always the best answer. The verdict never changes
   (they are convicted, as in 1711); what changes is what Lyle can say and
   what the record shows was there to be seen. Stage 1, the candle, done
   in v0.5;
   stage 2, the trial and Lyle's argument, once there are banks (keep each
   night's finding flags, about 16 bytes a night, after its buffer goes).
3. Portraits (Isobel first), hand-checked for the "human, not monstrous"
   rule: the accused's scars are never the scary part. Isobel on the
   Night One card done (v0.6); next Kate Rankin on the parade's
   arranging screen (cols 22-31, rows 6-17; the long option is shortened).
   Decided (26 Nov, from play-testing): the clerk is never told how many
   findings there are, or that he has found them all. Not knowing what he
   missed is the clerk's position; the book is the only record.
   Stage 2 decided (26 Nov), keeping it a game: the verdict is fixed, so
   the player's choices must be felt during play, with a cost, and the
   payoff must differ between playthroughs.
   - Three nights, then the trial (scope: a finishable 128K game).
   - The Mayor's patience, a second pressure beside the candle: writing
     findings that hurt his case wears it down; at nothing he takes the
     pen and a deputy writes the rest of the nights (a thinner record at
     the trial). Write everything and be dismissed, or keep quiet and stay.
     Never shown as a number (the wife's rule: the clerk isn't told);
     shown through the Mayor's manner. Tuning to be play-tested.
   - The trial is played: Carrickfergus, 31 March 1711. The court sits
     from six till two (MacSkimin: six in the morning till two in the
     afternoon), and that is the trial's clock, as the candle is the
     night's. The clerk is called with his book; Lyle (Upton) can raise
     only what was written; each point costs court time; Ormsby
     (Macartney) answers each with the reasoning of the day. The jury
     convicts. What changes is how close Lyle comes and what the record
     holds.
   - After the verdict: the sentence (a year's imprisonment and four times
     in the pillory, where the crowd pelted them), then the end.
   - The reveal: the game says roughly how much was missed without saying
     what (a line by proportion, in period voice: most of what was there to
     be seen is in the record / much is not / almost none of it), never a
     count or the findings themselves. Draft lines to be shown first.
   Build order: banks; the patience in Night One; Nights Two and Three
   (with portraits); the trial; the end.
4. Banks and the boot stub: done in v0.7. AY music (a slow theme, a
   church-bell tone) still to do: the player goes in bank 0, called from
   `isr`, which pages it in and puts `curbank` back.

## Testing

v0.7: keytest's snapshot is taken at `game` (after the stub has loaded the
banks and IM2 is on), not at 6000h; every reference screen is unchanged.
Checked by hand: a tape with bank 3's block corrupted stops at "Tape
loading error."; a 48K still stops at "needs a 128K".

v0.6: apron.keys also shoots frame 1400, just after the second mark (the
bright message, "C  compare" lit); the candle test shows it plain once the
candle is out; the parade's arranging screen has the shorter option.

v0.5: candle.keys compares two lines of Dickey's statement 16 times
(nothing found), shows the 16th burning the last of it, then C refused
("The candle is out"), then the hub with the dish alone. The prologue
test needs one more SPACE (the press that begins no
longer skips page 1's typing; every page is the same screen as before,
one press later). New test credits.keys (C on the title, the credits,
back to the title); parade.keys goes on from the end card to the credits
and the title, so every chunk and LOAD is run.

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
