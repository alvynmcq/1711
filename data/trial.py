"""The trial, 31st March 1711, Carrickfergus (stage 3, v0.9 slice).

DRAFT CONTENT. Adapted from the depositions and accounts in Sneddon &
Devlin (eds), w1711.org, CC BY 4.0, every name changed (NOTES.md has the
list). The court record is what was sworn in March (Night One's data in
v0.8); the testimony has drifted since, towards the Mayor's version.

The slice is one witness: Margaret Lowry, from six until seven.

Text rules (scripts/trial.py checks them):
  record facts   36 characters (the record screen: mark, number, fact)
  testimony      up to 4 rows of 40 (rows 17-20)
  answers        up to 4 rows; a HOLD's question up to 2 rows (19-20)
  remarks        one row (row 23); manner lines one row (row 21)
Never "witch" of the accused; humour at the bench and the Mayor only.
"""

TRIAL = {
    "date": "31st March 1711",
    "start": 6 * 60,            # the court sits at six (minutes from midnight)
    "jury": 14 * 60,            # at two the jury retires
    "slice_end": 7 * 60,        # the slice: Lowry has the first hour

    # what things cost, in minutes (the checker prints paths against them)
    "cost": {"line": 3,         # a testimony line heard for the first time
             "press": 6,        # SPACE on a line
             "hold": 8,         # a fact that contradicts it: HOLD, SIR!
             "wrong": 10},      # a fact that doesn't bear (and the bench -2)

    # the bench's patience (Justice Ormsby): 0-12, from 12
    "bench": {
        "start": 12,
        "wrong": -2,
        # by band: 10-12, 6-9, 3-5, 1-2 (row 21)
        "manner": ["Justice Ormsby writes steadily.",
                   "Justice Ormsby looks at the clock.",
                   "Justice Ormsby has stopped writing.",
                   "Justice Ormsby is looking at you."],
        # a presentation that doesn't bear, in turn (typed, rows 17-20)
        "rebukes": ["Ormsby: 'That does not bear upon it, brother.'",
                    "Ormsby: 'The record says what it says, brother. So does "
                    "she. We are not here to hear you read.'",
                    "Ormsby: 'We have a great many witnesses, brother, and one "
                    "dinner.'",
                    "Ormsby: 'Brother Lyle, the jury can count. They have "
                    "counted your papers twice.'"],
        "silenced": "Ormsby: 'Brother Lyle, you have said enough. The witness "
                    "will go on, and you will listen.'",
        "silent_row": "You may not speak again today.",
        "silent_key": "Ormsby: 'Brother.'",
        "opening": "Ormsby: 'Go on, Mrs Lowry.'",
        "asked": "Ormsby: 'She has answered that.'",
        "raised": "Ormsby: 'You have had that from her.'",
        "after_hold": "Ormsby: 'Go on, Mrs Lowry.'",
        "after_wrong": "Ormsby turns back to the witness.",
        "after_press": "Ormsby: 'Go on.'",
        "stand_down": "Ormsby: 'You may stand down, Mrs Lowry.'",
        "bell": "Ormsby: 'Seven o'clock. That is long enough in the box, "
                "Mrs Lowry. Stand down.'",
    },

    # what Lyle asks of a line with nothing more in it, and what he hears
    "press_none": ("Go on, Mrs Lowry. What more?", "'It is as I said, my lord.'"),

    # -------------------------------------------------------------
    # The court record: what was sworn in March. (id, fact, who, when)
    # -------------------------------------------------------------
    "record": [
        ("knots5", "The apron: tied with five knots.", "Margaret Lowry", "3rd March"),
        ("lowry_found", "Lowry found the apron herself.", "Margaret Lowry", "3rd March"),
        ("only_isobel", "Only Miss Halliday would loose them.", "Margaret Lowry", "3rd March"),
        ("knots9", "Nine knots; Miss Halliday found it.", "Margaret Wylie", "3rd March"),
        ("never_seen", "She had never seen them before.", "William Dickey", "3rd March"),
        ("fit_sight", "A fit as soon as she saw them.", "William Dickey", "3rd March"),
        ("wilson", "Wilson's words are Dickey's, exact.", "John Wilson", "3rd March"),
        ("thirty", "Thirty women brought in: no fit.", "Hugh Gilmour", "5th March"),
        ("moore", "None knew Janet Moore was coming.", "Hugh Gilmour", "5th March"),
        ("gordon", "Mr Gordon sent for Janet Moore.", "Robert Gordon", "3rd March"),
    ],

    # -------------------------------------------------------------
    # The witnesses. Each line: id, what is said; "hidden" lines appear
    # only when a press draws them out (after the pressed line).
    #   press: (Lyle's question, the answer, line it draws out or None,
    #           note for Lyle's notes or None, spectral)
    #   holds: {fact: (Lyle's question, the answer, Ormsby, the note)}
    #   wrong: {fact: what Ormsby says instead of the next rebuke}
    # -------------------------------------------------------------
    "witnesses": [{
        "id": "lowry",
        "name": "MARGARET LOWRY, servant",
        "portrait": "lowry",
        "lines": [
            {"id": "mantua",
             "say": "'On the night of the 27th of February, my lord, the mistress's "
                    "new mantua was taken from the trunk and strewn about the house.'",
             "press": ("Who saw it done, Mrs Lowry?",
                       "'None saw it done, my lord. We found the things in the "
                       "morning, all about.'", None, None, False)},
            {"id": "apron",
             "say": "'Two days after, an apron was found on the parlour floor, that "
                    "had lain two days locked in a room.'",
             "press": ("Found by whom?",
                       "'By Miss Halliday, my lord. She was the first that found "
                       "it.'", "found", None, False)},
            {"id": "found", "hidden": True,
             "say": "'Miss Halliday found the apron, my lord, and called me to it.'",
             "holds": {"lowry_found": (
                 "In March you swore you found it yourself. Today Miss Halliday "
                 "found it?",
                 "'Did I, my lord? I carried it to the parlour. Miss Halliday says "
                 "she found it first, and she would know.'",
                 "Ormsby: 'Whoever found it, brother, it was found. That is the "
                 "matter.'",
                 "In March she found the apron herself. Today Miss Halliday did.")}},
            {"id": "knots",
             "say": "'It was rolled up close, my lord, and tied hard with nine "
                    "strange knots.'",
             "press": ("Did you count them yourself?",
                       "'I did, my lord. Nine. I have told it so many times.'",
                       None, None, False),
             "holds": {"knots5": (
                 "On the 3rd of March you swore five knots. How came you to swear "
                 "nine?",
                 "'I... it was a great confusion, my lord. I have heard it told so "
                 "often, it is nine now.'",
                 "Ormsby: 'A servant's count, brother. The apron was knotted, and "
                 "that is the matter.'",
                 "In March she swore five knots. Today she swears nine.")},
             "wrong": {"knots9": "Ormsby: 'Mrs Wylie swore nine, brother. They "
                                 "agree. You have helped the Crown.'"}},
            {"id": "loosed",
             "say": "'And Miss Halliday loosed every knot of it, without the least "
                    "fear.'",
             "press": ("Why would none of you loose them?",
                       "'We durst not, my lord. It was not a thing of this world.'",
                       None, None, False),
             "wrong": {"only_isobel": "Ormsby: 'That is what she swears, brother. "
                                      "It agrees with her.'"}},
            {"id": "cap",
             "say": "'Inside it was a flannel cap of the late Mrs Wylie's.'"},
            {"id": "boyd",
             "say": "'That night Miss Halliday cried out that Janet Boyd stood at "
                    "the bed's foot, and she pointed at her.'",
             "press": ("Did you see Janet Boyd there, Mrs Lowry?",
                       "'No, my lord. None saw her but Miss Halliday. But she "
                       "pointed, my lord, as if she were there.'",
                       None, "None saw Janet Boyd at the bed but Miss Halliday.",
                       True)},
        ],
    }],

    # nightcheck-style paths for trialcheck.py: what each does, in order.
    # ("hear", line) ("press", line) ("present", line, fact)
    "paths": {
        "the slice's best": [
            ("hear", "mantua"), ("hear", "apron"), ("press", "apron"),
            ("hear", "found"), ("present", "found", "lowry_found"),
            ("hear", "knots"), ("present", "knots", "knots5"),
            ("hear", "loosed"), ("hear", "cap"), ("hear", "boyd"),
            ("press", "boyd")],
        "press everything": [
            ("hear", "mantua"), ("press", "mantua"), ("hear", "apron"),
            ("press", "apron"), ("hear", "found"), ("hear", "knots"),
            ("press", "knots"), ("present", "knots", "knots5"),
            ("hear", "loosed"), ("press", "loosed"), ("hear", "cap"),
            ("press", "cap"), ("hear", "boyd"), ("press", "boyd"),
            ("present", "found", "lowry_found")],
        "the wrong fact": [
            ("hear", "mantua"), ("hear", "apron"), ("hear", "knots"),
            ("present", "knots", "knots9"), ("present", "knots", "knots5"),
            ("hear", "loosed"), ("present", "loosed", "only_isobel"),
            ("present", "loosed", "lowry_found"), ("present", "loosed", "thirty"),
            ("present", "loosed", "moore"), ("present", "loosed", "gordon"),
            ("present", "loosed", "wilson")],
        "listen only": [
            ("hear", "mantua"), ("hear", "apron"), ("hear", "knots"),
            ("hear", "loosed"), ("hear", "cap"), ("hear", "boyd")],
    },
}
