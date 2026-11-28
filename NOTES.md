# 1711 (working title): project notes, v0.8

A ZX Spectrum 128K game. You are the clerk to Mayor Ellis of Carrickfergus,
taking sworn statements at Braehead House, Islandmagee, in March 1711, as a
young woman names her neighbours as witches. You read, compare and record.
The horror is the process: what gets written down, and what doesn't.

Based on the trial documents edited by Andrew Sneddon and Shannon Devlin
(w1711.org, CC BY 4.0). Real places and dates; every person renamed. The
w1711 graphic novel (CC BY-NC-ND) was read for research only: nothing from
it is used.

**Stage 3 (decided 27 Nov) replaces this: the game is now the trial.** You
play Justice Lyle, in court, for one day. See "Stage 3: the courtroom",
next. Everything from "What v0.8 has" down describes v0.8 and earlier.

## Stage 3: the courtroom (decided 27 Nov)

### What v0.8 had, and why it changed

v0.8 was the clerk's desk, Night One: witnesses came to the table one at
a time, you set a line against a statement in the book (SPACE compares,
a candle unit each), stamped what you'd found (ENTER), and the Mayor's
patience fell as you wrote down things that hurt his case. A play of
Night One was too confusing. Hunting for two lines that clash across 30
lines and six statements has no immediacy: you're looking for matching
text, not hearing anything. And the three nights still had to come before
the part that matters, the trial.

So the trial becomes the whole game. The contradictions in the night
data, and the witnesses' answers, are kept: they become the court record
and the testimony.

### The day

- One day, one room: Carrickfergus, 31 March 1711. The court sits at six
  in the morning; at two the jury retires, whatever has or hasn't been
  raised (MacSkimin: six till two).
- You are Justice Lyle (Upton), the one judge who argued for acquittal.
  The accused had no counsel (felony, 1711); judges questioned the
  witnesses. Said once, plainly, at the start.
- No investigation. You start with the court record: about ten one-line
  facts, each with who swore it and when (as on 3 March). "The apron: five
  knots. Margaret Lowry, 3rd March." You choose from a short list, never
  search text (The Vera Cruz Affair's evidence menus, Ace Attorney's court
  record: structure only, no names, art or catchphrases).
- Witnesses testify a line at a time. Their stories have drifted since
  March towards the Mayor's version (Lowry now swears nine knots, and that
  Miss Halliday found the apron). They aren't villains: they have heard
  the story told until it is what they remember.

### Keys and the moment

- O / P: the previous / next line. Hearing a new line takes time.
- SPACE presses the line: a little time; may draw out more ("Who found
  it, Mrs Lowry?"), sometimes a new testimony line. Presses are fixed per
  line (keyword topics in the data), not free questions.
- ENTER opens the record over the portrait (the testimony line stays in
  view); Q / A choose a fact; ENTER presents it at this line; X backs out.
- Let it pass: just move on. You can't fight everything.
- A fact that contradicts the line: HOLD, SIR! The border flashes, the
  letters double height (bigstamp) in bright red, the AY bell; Lyle's
  question typed ("On the 3rd of March you swore five knots. How came you
  to swear nine?"); the portrait falters (a few cells swapped at once:
  eyes, mouth); the witness answers; Ormsby answers with the reasoning of
  the day ("A servant's count, brother. The apron was knotted, and that is
  the matter."); then "Let it be written: ..." into Lyle's notes.
- A fact that doesn't bear: "That does not bear upon it, brother." A
  rebuke, time, and the bench's patience.

### The clock

- 6:00 to 14:00 in 5-minute units (96, one byte). Eight marks top right,
  struck off on the hour with the AY bell; the time in words on row 1
  ("A quarter past seven").
- Costs (draft, for the checker to tune): a new line heard 5 min, a press
  10, a presentation that bears 15, one that doesn't 20 and the bench -2.
  Budget about an hour a witness, so a full cross-examination of one
  witness can't fit if every line is pressed.
- At two the jury retires: the witness in the box stops, Ormsby sums up,
  the verdict.

### The bench's patience (Ormsby)

- The stage-2 patience machinery, aimed at the bench: one hidden byte,
  0-12, from 12; shown only by Ormsby's manner line (bands 10-12, 6-9, 3-5,
  1-2) and his remarks after each presentation. Never a number.
- Costs: a wrong presentation -2 (a rebuke); presenting against the Mayor
  -3 even when it bears; a right one against anyone else 0. Pressing
  costs time only.
- At 0: "Brother Lyle, you have said enough." Silenced: SPACE and ENTER do
  nothing more; the testimony goes on and you can only listen.
- Humour aims at the Mayor and the bench, never the accused.

### The verdict

- The verdict can turn; the history doesn't. Acquittal is possible but
  hard: enough contradictions written into the record before the jury
  AND Isobel's spectral evidence discredited (visions and fits are not
  evidence, Upton's own argument). Not by proving the accused "good".
- Spectral evidence (decided 28 Nov): some testimony lines report
  what Isobel saw ("She cried out that Janet Boyd stood at the bed's
  foot"). Pressing such a line draws out that no one else saw it ("Did you
  see Janet Boyd there?" "No, my lord. None saw her but Miss Halliday.").
  Each admission goes into Lyle's notes; enough of them, with the fact
  that thirty women were brought in and she was not disturbed, discredit
  it in the summing-up.
- Partial outcomes: some acquitted, not all (the contradictions are
  per accused). Most first plays should fail.
- Whatever the verdict, the last screen says what really happened:
  convicted, a year's imprisonment and four times in the pillory; the
  game's people stand in for real ones (w1711.org).
- The accused are never called witches, in any ending: "the accused", or
  by name. Nothing suggests they really were.
- Isobel is brought in once, unable to speak (dumb throughout the trial,
  no fit while it lasted: MacSkimin), never questioned. A frightened young
  woman, not a villain.

### The cross-examination screen

| Rows | What |
|---|---|
| 0 | the witness (bright white); eight hour marks, columns 34-41 (candle yellow) |
| 1 | the time in words (yellow) |
| 2-15 | the portrait, 16 x 14 characters, columns 8-23 (centred) |
| 16 | a rule, "3 of 6" (the line) |
| 17-20 | the testimony line (white, 40 columns, up to 4 rows) |
| 21 | Ormsby's manner (yellow) |
| 22 | keys |
| 23 | Ormsby's last remark (the brief had keys on 22-23; changed 28 Nov) |

The record (ENTER) replaces rows 2-15: a heading, ten facts a row each
(one line, 36 characters after the mark and number; the chosen one bright white with a mark), and on
row 15 who swore the chosen one and when. So facts are written to fit
one row, and "Margaret Lowry, 3rd March" sits below rather than beside.

HOLD, SIR! goes on rows 17-18 (double height, bright red), Lyle's
question on 19-20; then the answers page through rows 17-20.

### Graphics

- Portraits 16 x 14 characters (128 x 112 pixels): art/portraits.py grows
  a size per portrait and a delta per face (the faltering cells: pixel
  bytes only, the attributes unchanged, so no clash when it swaps).
  2016 bytes raw each: PSCR (now F7C0h, 1080 bytes) has to move down to
  F5E0h-FDBFh in the trial's bank.
- Full-screen pictures: the courtroom from the gallery (three judges, the
  dock, candles at six in the morning); the accused together in the dock,
  ordinary people; Isobel brought in; the pillory at the end, distant and
  plain, never gory.
- Colour as the prologue: mostly black, candle yellow, white for paper
  and faces, red only for HOLD, SIR! and the verdict. No attribute clash
  in the faces.

### What carries over, what goes

- Keep: the text engine, the banks and memory plan, ZX0, the portrait
  tool, bigstamp's double-height letters, aysnd, the night data's
  contradictions and answers (now record facts and testimony),
  keytest/simtest with poke and the AY log, the prologue.
- Goes: the desk, the stamp, the candle, the nights. The prologue's
  ending is rewritten for Lyle (decided 28 Nov): no clerk, and the Night
  One card becomes a court card ("31st March 1711 / Carrickfergus")
  without Isobel's portrait, so her one appearance is in court.
- The mockup (docs/stage3_mockup.png, drawn at 256 x 192 with the game's
  font) showed a fact gets 36 characters after the mark and number.

### The court record (draft, from Night One's data)

1. The apron: five knots. Margaret Lowry, 3rd March.
2. Lowry found the apron on the parlour floor. Margaret Lowry.
3. None would loose the knots till Miss Halliday offered. Margaret Lowry.
4. The apron: nine knots, found by Miss Halliday. Margaret Wylie.
5. She never saw them before her trouble. William Dickey.
6. She fell into a fit as soon as she saw them. William Dickey.
7. Wilson's statement is Dickey's, word for word. John Wilson.
8. Thirty women brought in one by one: not disturbed. Hugh Gilmour.
9. None in the house knew Janet Moore was coming. Hugh Gilmour.
10. Mr Gordon sent for Janet Moore, and sat with her first. Robert Gordon.

### The slice: Margaret Lowry

Her testimony (draft), a line at a time, drifted from her March statement:
the mistress's things thrown about the house (27 Feb); an apron found on
the parlour floor that had lain in a locked room (press: "Miss Halliday
found it, and called me to it." a new line, against fact 2); rolled and
tied with nine strange knots (against fact 1); Miss Halliday loosed them
without fear (fact 3 agrees: a decoy); inside, the late Mrs Wylie's cap;
Miss Halliday cried that Janet Boyd stood at the bed's foot (press: none
saw her but Miss Halliday, a spectral admission). Then the slice ends on
Lyle's notes and the 1711 card.

Data in data/trial.py, compiled by scripts/trial.py; scripts/trialcheck.py
prints the record, each line's presses and the facts that contradict it,
and the time and patience of a few paths.

## What v0.8 has (stage 2, steps 1-5, Night One)

Stage 2's build order, steps 1-5, for Night One: the night format, the
desk (replacing the hub and the reader), the Mayor's patience, the
parade's costs and the candle, the tests. Title and credits say "v0.8
slice". Nights Two and Three, the trial and the end are still to come;
Night Three's test stays open.

Changes from the design (27 Nov), made on the screen:
- The desk's header is three rows, not two: row 0 the witness, row 1
  "Sworn 3rd March 1711", row 2 the manner line. So the halves are rows
  3-10 and 12-19, eight rows each (the design had 2-10 and 12-19).
- The manner lines say "The Mayor ..." ("Mayor Ellis is reading over
  your shoulder." doesn't fit one line beside the candle).
- The candle is column 31, rows 0-3 (32 pixel rows, at most 25 units), so
  all statement text wraps at 39, not 40.
- The slip after a stamp is on row 20 of the stamp screen (rows 21-23
  hold the candle message and the prompt), then on row 23 of the next
  desk until the next stamp. Slips are one line (40 characters): some
  drafts were shortened ("'Thrice Mayor, and never a question.'",
  "'Five or nine, it was knotted. Go on.'").
- The stamp: ENTERED. QUESTION PUT. if any question was put, else
  ENTERED AS SWORN (notes alone are "as sworn"). The stamp list's default
  for each item is its first way of writing it; "Let it lie" is a choice.
- ENTER with nothing in hand still opens the stamp list ("Nothing in
  hand. It goes into the book as sworn."): two ENTERs, as no one is
  called back.
- The parade has no "X not yet": it comes last, after the sixth witness.
- Gains capped at +3 a night are the desk's only (agreements and the copy
  as corroboration); the parade's "singled out" +2 is not capped, so the
  honest pair nets 0 as designed.
- The "none" slips don't say "call the next" (they follow the parade too).

### Night One's numbers (nightcheck.py)

everything ends at 6 (reads over your shoulder), candle 18 of 22;
collaborator ends at 12, candle 9; balanced (the Moore and who-found-it
questions, agreements noted, the copy as corroboration) ends at 8, candle
16. The lowest Night One can go is 1 (every cost and the worst parade),
so no one is dismissed on Night One. The design hoped "everything" would
end Night One cold (3-5); it ends at 6, one above. Left for play-testing.

### The night, in order (src/night.asm)

1. The orders card: the Mayor's order, and how the desk works.
2. The desk, a witness at a time, in `order` (below).
3. The parade, last (the arranging screen, the scene, the record).
4. The bare-book cost, if only the fit is written.
5. The ledger: statements entered, questions put, agreements noted,
   parade lines written, Mr Agnew's (if any, in bright cyan), the candle in
   words (burnt to the dish / a stub / half / more than half), the Mayor's
   goodnight by band (or the dismissal), his order for tomorrow.
6. The clerk's book: case by case what was written (the answers under
   their questions, in white), Mr Agnew's "Entered as sworn." lines in
   bright cyan, then the parade (the fit, in his colour if he wrote it),
   or "Nothing but what was sworn."; then the names page.

### The desk

| Rows | What |
|---|---|
| 0-2 | the witness (bright white), "Sworn ...", the Mayor's manner (cyan) |
| 3-10 | what this witness swore (yellow; Q / A move, over the edge turns the page) |
| 11 | a dashed rule, "The book: n  name" (1-9 turn it to an earlier statement) |
| 12-19 | that statement (cyan; P / L) |
| 20 | the result: "In hand: <label>" (bright when new), or why not |
| 21-22 | keys |
| 23 | the Mayor's last slip |
| col 31, rows 0-3 | the candle |

'^' and 'v' in column 0 of a half's first and last rows: there is a page
before or after. The chosen line in each half is bright white.

- Compare (SPACE): 1 candle; the pair is looked up in `night_pairs`
  (book statement and line, table statement and line), then a box drawn
  straight to the screen over row 11, cells 9-22: THEY DIFFER (white on
  red), THEY AGREE (black on white), WORD FOR WORD (black on yellow), NO
  BEARING (plain), and the AY thump. The box goes at the next key (row 11
  redrawn). Measured: the thump is written the frame after the key, the
  box before it (desk.keys shoots 2 frames after the key). A finding not
  in hand goes in hand (flag 1). No book (the first witness): "Nothing in
  the book to set it beside.", no candle. No candle: "The candle is out.
  You read by the fire."
- The stamp list (ENTER): rows 12-22, "1  label" and its ways side by side
  under it (columns from night.py), the chosen one bright white on red;
  1-3 cycle an item's ways ("Let it lie" last); X back to the desk (the
  choices kept); ENTER stamps.
- The stamp: each item written: flag 2 + its way, 2 candle (not below 0),
  its patience (gains capped). Rows 12-13: the stamp, letters twice as tall
  in a ruled box, bright red (Mr Agnew's bright cyan), and an AY stamp.
  The answers typed under it (rows 14-17). Then the patience is applied,
  the manner line redrawn, the slip (row 20): the item with the biggest
  cost speaks if it has a slip of its own (else the biggest gain), else
  the next slip of the band of the net change. A cost that leaves him at
  5 or less puts a cold line on row 19. A low AY note for a cost, a higher
  one for a gain. If this stamp burnt the candle out, row 21 says so.
- A redrawn half is drawn with its rows' colours black (a copy in abuf),
  then shown at once; the whole desk with `veil`, as before.

### The Mayor's patience

`pat` (0-12) and `dismissed` sit below C000h. Night One sets 12; later
nights add 2 (code in place, NIGHT_N > 1). Manner bands 10-12, 6-9, 3-5,
1-2. At 0 (after a stamp, or after the parade's record, or a bare book
at the end): "Mayor Ellis holds out his hand." and the dismissal; then
Mr Agnew stamps the remaining witnesses (each 48, 24, 12, 6, 6 frames:
about 3 seconds for four), the Mayor arranges the parade (the first
option of each choice: told, alone, into the room; no record screen; the
fit in Agnew's hand, `par_ag`). `agnew` is the first case he stamped.
Dismissal is permanent (later nights: by the fire, the pocket-book: not
built).

### Persistent state (below C000h, for the trial)

`pat`, `dismissed`, `night_fflag` (16: 0 not found, 1 found and let lie,
2 + the way written), `par_wr`, `par_ag`, `agnew`. One night's worth so
far: Night Two will need its own copies (about 20 bytes a night).

- Step 1, the night format (done): case order, agreements, stamp choices,
  patience on every finding and parade record line, the witnesses'
  answers, the Mayor's lines; nightcheck.py prints the items per case and
  three paths' patience. The v0.7 hub still ran on it (agreements left
  out; the compare screen showed the book wording).
- Step 2, the desk (done): replaces the hub and the reader (see The desk,
  below). The Mayor's patience went in with it (the stamp needs it), and
  is checked on its own in step 3. The hub tests (apron, candle, parade)
  are gone with the hub; desk.keys plays a whole night.
- Step 3, the Mayor's patience (done): the manner line, slips, cold lines,
  the ledger, the bare book, dismissal and Mr Agnew. Night One can't take
  him to 0 on its own numbers (the floor is 1: every cost, the worst
  parade), so the tests poke `pat` (keytest's new `poke` line): agnew.keys
  (dismissed at Wilson's stamp), patience.keys (cold lines, the low bands,
  dismissed after the parade), bare.keys (nothing written: the bare book
  shows in the goodnight). simtest.py now logs every AY write with its
  frame: the compare's thump is written the frame after the key.
- Step 4, the parade's costs and the candle (done): each parade record
  line carries its patience (told beforehand -2, unseen at the door -1,
  name spoken in the hall -2, singled out +2, like her mother -2, alone
  0); after the record the Mayor's slip, as after a stamp. The candle is
  22 (was 16): finding and writing all six items costs 18 at the least,
  leaving 4 for compares that find nothing, as v0.5 did. It is drawn in
  column 31, rows 0-3 now (at most 25 units), and statement text wraps at
  39 so it never touches it.

## What v0.7 has

v0.7: the banks and the boot stub (see Memory plan). Moving into banks
changed nothing on screen: every test screen stayed the same, pixel for
pixel. The code below C000h went from 14.2 KB to 6.2 KB, with 18 KB free
there for Nights Two and Three and the trial. Then Kate Rankin's portrait
on the parade's arranging screen (see Portraits).

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
- Kate Rankin (v0.7), on the parade's arranging screen, rows 6-17, columns
  22-31, drawn while the screen is veiled so she appears with it. Janet
  Boyd's daughter, fetched from her wheel: a plain linen kerchief, a grey
  woollen shawl, a glimpse of a brown-red bodice. The light comes cold from
  the right (the door), the other side from Isobel's candle, and the
  kerchief fades out on the dark side so it never rings her face. Rounder
  and younger; her eyes are down and aside, not on the clerk. Ordinary.
  278 bytes packed, in bank 3 with Night One.
- Which portrait a parade shows: night.py writes `par_port` (the
  accused's place in art/portraits.py's list, 0FFh for none) into the
  night data; night.asm draws it. A new night's accused only needs a
  portrait of the same name and a bank in PORT_BANK.

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
raw; bank 3 goes packed, 3222 bytes for 6731).

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
| src/night.asm | The night's screens (v0.8): orders card, the desk, stamp, parade, ledger, book |
| scripts/night.py | Compiles data/nightN.py to src/night.inc |
| data/night1.py | Night One in the night format (draft content) |
| scripts/nightcheck.py | Checks a night and lists what the clerk can find |
| tools/simtest.py | From Night Porter: headless test runner (SkoolKit) |
| tools/keytest.py | Runs tools/tests/*.keys, compares with tools/ref/*.png (snapshot at `game`, after boot); `poke` lines (v0.8) |

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

- **order** (v0.8): the statement ids in the order the witnesses come to
  the table, one closed case each; the parade comes last. night.py puts
  the statements in this order, so a statement's number is its case.
- **statements**: each has an id, who, when sworn, and lines. A line is
  text, or `(text, claim, value)`. Two statements giving the same claim
  different values: THEY DIFFER; the same value: THEY AGREE (v0.8,
  agreements: `never_seen`, Dickey and Gilmour; `fit_on_sight`, Dickey and
  Gordon). A claim never both agrees and differs (night.py checks). A
  claim must appear in at least two statements (a copy counts as its
  original): nightcheck.py warns about one that doesn't.
- **dates**: every Night One statement shows "Sworn 3rd March". The real
  sources are listed in data/night1.py (Gilmour's is from 5 March; Lowry's,
  Margaret Wylie's and Gordon's come from Tisdall's account and the 1822
  narrative), and the credits say "Dates and order compressed". A statement
  with `copy_of` repeats another word for word, as two of the real
  depositions do ("agreeth with the above, word for word"): WORD FOR WORD.
- **findings** (v0.8): keyed by claim, or "copy:<id>". A finding belongs to
  the case of the later of its two statements (night.py checks it can be
  found at one case only; at most three at a case, keys 1-3). Each has a
  `label` (the stamp list's heading) and `write`, one or two ways to write
  it: (menu, book text, patience, slip or None, answer or None). "Let it
  lie" is always added last (nothing written, no cost). An answer makes it
  a question put to the witness at the table: typed, and written in the
  book. Findings say what was sworn; they never say who lied, or that
  anyone was a witch; the answers smooth the gap over.
- **parade**: each choice is (heading, options), each option (name, menu
  text, scene sentence); "fit" is the line the Mayor gives; "seen" lines
  are what the clerk notices, which keep an ordinary explanation in view;
  "spoken" is what the accused says, typed after the fit every time.
  `record` (conditions, text, patience) lists what the clerk can honestly
  write for each arrangement; night.py works out, for each of the 2^n
  arrangements, which seen and record lines apply, and checks the screens
  fit.
- **orders** (v0.8): the Mayor's order for the night (a card before the
  first witness); **next_orders**: the next night's, at the end of the
  ledger.
- **mayor** (v0.8): manner lines by band, slips by cost ("gain", "none",
  "small" -1, "middle" -2, "large" -3 or worse), "cold" lines (above a
  slip when a cost leaves him at 5 or less), goodnight lines by band, the
  dismissal, the bare-book cost.
- **paths** (v0.8): nightcheck.py's three paths, what each writes.
- **people**: the clerk's index of names for the night.
- **candle** (v0.5): the night's candle in units (see The candle).

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
and the IM2 table in each bank. v0.8: the desk made the code 8739 bytes
(6000h-8222h; 15837 free below C000h); Night One's bank is 8101 bytes of
text and tables, Kate to E0BBh, 5893 free under PSCR (4151 bytes packed
on the tape). The AY sounds are direct register writes (`aysnd`, a few
bytes each), no player.

| Where | What |
|---|---|
| 5B00h-5BFFh | The stack, once IM2 is on (BASIC's done with) |
| 6000h-8222h | The code: engine, the desk and night screens, ZX0 decoder, font, tables, variables, abuf (8739 bytes, v0.8) |
| 8223h-BFFFh | Free: 15837 bytes, for Nights Two and Three's screens and the trial |
| C000h, bank 0 | Nothing yet but the IM2 table (the AY player, later) |
| bank 1 | SBUF C000h-CC0Ch, chunks, pictures, Isobel; ends E06Eh, 5970 free under PSCR |
| bank 3 | Night One C000h-DFA4h (v0.8), Kate to E0BBh; 5893 free under PSCR |
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
   Night One card done (v0.6); Kate Rankin on the parade's arranging
   screen done (v0.7).
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
   Build order: banks; the patience in Night One (done, v0.8); Nights Two and Three
   (with portraits); the trial; the end. The design for all of it was
   decided on 27 Nov: see "Stage 2 design" below.
4. Banks and the boot stub: done in v0.7. AY music (a slow theme, a
   church-bell tone) still to do: the player goes in bank 0, called from
   `isr`, which pages it in and puts `curbank` back.

## Testing

v0.8: the hub tests (apron, candle, parade) went with the hub. Seven
tests, every screen looked at before its reference was written:
- prologue: title to the Mayor's orders (16 SPACEs reach the desk now).
- credits: as before (the version reads v0.8 slice).
- desk: a whole Night One written honestly: Dickey as sworn, Wilson word
  for word (842: the box 2 frames after the key), Gilmour's agreement,
  Lowry as sworn, Margaret Wylie's two questions and answers, Gordon's
  question and agreement, the parade quiet / among / room with both lines,
  the ledger (patience 6, a stub of candle), the book's two pages, names.
- nav: Q/A and P/L over page edges, 1-9 (ignored past the case), SPACE
  with no book, a pair compared twice, the stamp list's 1 cycling and X.
- candle: 22 compares that find nothing (NO BEARING), the candle out, a
  compare refused, the stamp still works.
- patience (poke pat=7 before Margaret Wylie's stamp): the cold lines,
  the 3-5 and 1-2 manner lines, Gordon's own slip, dismissed after the
  parade, the ledger's goodnight the dismissal.
- agnew (poke pat=2 before Wilson's stamp): the dismissal, Mr Agnew's
  stamps, the Mayor's parade, the ledger and book in Agnew's colour.
- bare (poke pat=11): everything as sworn, ENTER then X at Lowry, the
  parade's lines left out: the bare book costs 2 (the goodnight drops a
  band), "Nothing but what was sworn."
keytest.py's `poke F LABEL=VALUE` sets a byte at a frame (labels from
main.sym); simtest.py logs every AY write with its frame (in its
_ay.txt).

v0.7: parade.keys' arranging screen (frame 1210) now has Kate's portrait
(reference updated after looking at it). keytest's snapshot is taken at `game` (after the stub has loaded the
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

## Stage 2 design (decided 27 Nov)

The worry was that the game isn't as immediate as Night Porter. The answer
is one loop in three stages: at night, compare, stamp, and the Mayor
reacts; in court, present, "Hold, sir!", and Ormsby answers. The pages
used in court are exactly what was stamped in at night. The full proposal
(with the reasoning and the risks) is the 1711 stage 2 design doc on
claude.ai. Everything below is accepted unless marked open.

### The night as a desk (replaces the hub and the reader)

- Witnesses come to the table in a fixed order, one closed case each:
  read, compare against the book, stamp, gone. No calling one back.
- The screen is split top and bottom (both keep 40-column text). Rows 0-1:
  the witness, "Sworn 3rd March", the Mayor's manner line, the candle.
  Rows 2-10: the statement before you (cursor Q/A). Row 11: a rule and
  "The book: <name>" (keys 1-6 pick an earlier statement). Rows 12-19: that
  statement (cursor P/L). Row 20: the result and what is in hand. Rows
  21-22: keys. Row 23: the Mayor's slip.
- Compare (SPACE) is instant: a boxed word over row 11, an AY thump, 1
  unit of candle. THEY DIFFER (red; goes in hand), THEY AGREE (white; in
  hand), WORD FOR WORD (the copy; in hand), NO BEARING (plain). It must
  land within 2 frames: a table lookup and a box drawn straight to the
  screen, never veiled.
- Stamp (ENTER): what is in hand is listed, toggled with 1-3 as on the
  parade screen. A difference: put the question / let it lie. An
  agreement: note it / let it lie. Then ENTERED AS SWORN or ENTERED.
  QUESTION PUT. in large letters. The witness answers each question in one
  typed line (into the book), then the Mayor's slip. Writing costs 2
  candle per item, as now. The question goes to the witness at the table
  (the later of the two statements).
- The copy can be written two ways: "John Wilson corroborates William
  Dickey." (the Mayor is pleased) or "John Wilson's statement is William
  Dickey's, word for word." (it costs), or let lie.
- Only witness answers, Lyle's questions and scenes type; the rest is shown
  at once.
- Night One's queue: Dickey (nothing to find: the Mayor's orders, a first
  stamp); Wilson (the copy); Gilmour (agrees with Dickey: never seen them,
  new claim `never_seen`); Lowry (clean); Margaret Wylie (differs from
  Lowry: the knots, who found the apron); Gordon (differs from Gilmour on
  Janet Moore; agrees with Dickey on the fit at first sight, new claim
  `fit_on_sight`); the parade, last. Draft answers: Wilson "I swear to
  what William swore. It is true, so it is the same."; Margaret Wylie
  "Nine, sir. Meg was frighted and miscounted." / "Miss Halliday found it.
  Meg only brought it to the parlour."; Gordon "I sent for her as a
  neighbour. I said nothing of it to the girl." The answers smooth the gap
  over; none says who was right.
- The night format grows: case order, agreements (same claim, same value;
  night.py lists agreeing pairs too), stamp choices, a `patience` value on
  every finding and record line, the witnesses' answers. nightcheck.py
  prints items per case and the patience of three paths (everything, the
  collaborator, balanced).
- The Mayor's orders, a card at the start of each night, grow:
  - Night One, two witnesses: "Take down what is sworn. Where two swear
    alike, note it: the law wants two."
  - Night Two, her sight is evidence (spectral evidence): a line where
    Isobel saw a shape is written "Janet Kerr appeared to her" (as
    ordered) or "She saith Janet Kerr appeared to her" (honest, a small
    cost each). The "she saith" pages let Lyle call it visionary
    imaginings, as Upton did.
  - Night Three, a test, arranged like the parade, with conditions the
    clerk chooses. OPEN: which test is in the Islandmagee record (a touch
    test, a search for marks, or another). Use only one the record has.
- The ledger, one screen at the end of each night, in the clerk's hand:
  what he entered, questions put, agreements noted, the candle, the
  Mayor's goodnight (by band), then the next night's order. It counts only
  what the clerk did, never what there was.
- Nights Two and Three: 6-8 items a night, with decoys (same topic, no
  bearing) and findings that share no word, so it is reading, not word
  matching.

### The Mayor's patience

- One hidden byte, 0-12. Night One starts at 12; +2 overnight (at most
  12). Shown by the manner line on the desk (10-12 "Mayor Ellis warms his
  hands at the fire."; 6-9 "...is reading over your shoulder."; 3-5
  "...stands at your elbow."; 1-2 "...has his hand on the book.") and the
  slip after every stamp (a low AY note for a cost, a brighter one for a
  gain).
- Night One costs (to be tuned by play-testing): an agreement noted +1
  each; Wilson as corroboration +1, as word for word -2; questions: the
  knots -1, who found the apron -2, Janet Moore -3. Parade: the fit 0;
  "singled Kate out from among six women" +2; "told beforehand" -2; "name
  spoken in the hall" -2; "youngest, and like her mother" -2; "unseen, at
  the house door only" -1; "brought to her alone" 0. A bare book at the
  end of the night (only the fit) -2. Gains from agreements at most +3 a
  night.
- So: writing everything honestly on Night One ends it cold, dismissed
  part way through Night Two; the collaborator stays at 12 and gives Lyle
  nothing; the balanced clerk keeps the two strongest pages. The honest
  parade pair ("singled out" and "like her mother") nets 0: buying
  patience means writing only the Crown's half.
- Slips (draft): gains "Two witnesses. The law is satisfied, and so am
  I." / "There. That is the way of it." (he helps himself to Hugh Wylie's
  brandy) / "Neatly put. I may mention you to the Bishop."; small "Five or
  nine, sir, it was knotted. Write on." / he drums his fingers; middling
  "Must you?" / "Two honest men may say the same thing, sir. It is called
  agreeing." / "Ink is dear, and so is my evening."; large "Mr Gordon is a
  minister of the Gospel." (nothing else) / "I have been Mayor of
  Carrickfergus three times and never once needed a question." Cold
  prefixes: he does not look at you / "I begin to wonder whose clerk you
  are." Humour is always at the Mayor and the bench, never the accused.
- At 0: "Give me the pen. Mr Agnew will write. You may sit by the fire and
  warm your scruples." (Agnew, an invented deputy.) The rest of the night
  is stamped ENTERED AS SWORN, faster and faster (under 5 seconds); if the
  parade is still to come, the Mayor arranges it (told, alone, into the
  room). Later nights: the clerk reads and compares by the fire (no
  candle) but cannot stamp; what he finds goes in his pocket-book, not the
  record. Agnew's pages are one line each, "Entered as sworn.", in another
  colour. Dismissal is permanent.

### The trial

- Carrickfergus, 31 March 1711, six till two. Isobel is brought in and
  cannot speak (she was dumb throughout the trial and had no fit while it
  lasted: MacSkimin); shown once in her portrait, never questioned. The
  household testify (Gordon, Lowry, Margaret Wylie, Gilmour, Dickey and
  Wilson, and the witnesses of Nights Two and Three), then Mayor Ellis on
  the parade: presenting a parade page against him costs his patience
  heavily.
- No defence counsel (felony, 1711): Lyle is the only voice they have. Say
  so once, plainly.
- Testimony has drifted towards the Mayor's version (Lowry now says nine
  knots, and that Miss Halliday found it); the book holds what was sworn
  in March. The witnesses aren't villains: they have heard the story told
  until it is what they remember.
- The clock: eight marks in the candle's corner, struck off by the hour
  with an AY church bell. Testimony takes fixed time; press 10 min; a page
  that bears 20 min; one that doesn't 30 min and the Mayor -1; a
  pocket-book page 40 min. At two the jury retires: the rest is heard in
  haste, nothing more presented. The Mayor's patience carries on; at 0 he
  has the clerk put out of court.
- Ormsby opens by reading out every agreement the clerk noted.
- Testimony a line at a time: the portrait right (columns 22-31), the line
  left; O/P between lines, SPACE presses (a further line, sometimes a new
  testimony line), ENTER opens the book (Q/A a page, ENTER passes it up).
- The moment: the border flashes red and white 6 frames, an AY bell
  (tone, decaying envelope), HOLD, SIR! double height in bright white,
  Lyle's question typed ("On the 3rd of March you swore five knots. How
  came you to swear nine?"), the portrait falters (a cell delta: eyes
  down, mouth changed), the witness answers ("I... it was a great
  confusion, my lord."), Ormsby answers with the reasoning of the day
  ("A servant's count, brother. The apron was knotted, and that is the
  matter."), Lyle: "Let it be written: ..." into Lyle's notes. A wrong
  page: "This does not bear upon it." Ormsby: "Brother Lyle, the clerk's
  papers are not Scripture." The copy in court: "Then they are
  consistent, brother."
- Lyle's summing-up starts from Upton's own points (sober, industrious,
  attended public worship, could say the Lord's Prayer: MacSkimin), then a
  sentence per point raised, in order; pocket-book points are spoken, not
  written into the record. Ormsby sums up (fixed); the jury convicts.
- The sentence is fixed: a year's imprisonment and four times in the
  pillory. It never varies with play (that would make their suffering the
  score). Optionally the clerk's own fate varies (kept on, or not employed
  again).
- The reveal: what was raised (Lyle's points), then one line by the
  proportion of everything there was that reached the court: "Most of what
  was there to be seen was put before the court. It is in the record. It
  changed nothing." / "Some ... More lay in the depositions, unread." /
  "Little of what was there to be seen reached the court." / "None of what
  was there to be seen reached the court. The record says what the house
  said."

### Cost and build order

Patience is a byte and its flags sit below C000h; slips and manner lines
about 1.5 KB of text per night bank; the desk about +1 KB of code; the AY
thump and bell are direct register writes (about 150 bytes, no player);
the trial in bank 7 (portraits about 300 bytes packed each, about 60 for a
faltering delta) with 3-4 KB of screen code below C000h. The hub tests
(apron, candle, parade) change on purpose: new key scripts for the desk.

1. The night format and nightcheck.py (above).
2. The desk: both halves, compare, the instant result, the stamp.
3. Patience: slips, the manner line, the ledger, dismissal and Agnew.
4. The parade's costs; retune the candle against the new minimum.
5. Tests and the tape. Then Nights Two and Three, the trial, the end.
