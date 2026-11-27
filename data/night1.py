"""Night One, 3rd March 1711: Braehead House, Islandmagee.

DRAFT CONTENT in the night format (see NOTES.md). Adapted from the
depositions and the 1822 narrative in Sneddon & Devlin (eds), w1711.org,
CC BY 4.0, with every name changed (see scripts/story.py for the list):

  dickey   <- William Fenton's examination, 3 March
  wilson   <- John Willson, "agreeth with the above, word for word"
  gilmour  <- Hugh Donaldson's examination, 5 March
  lowry    <- the narrative (the apron, five knots)
  wylie_m  <- Tisdall's account of the trial (the apron, nine knots)
  gordon   <- the narrative (Janet Carson sent for by the minister)

Every statement is shown as sworn on 3 March: the credits say that dates
and order are compressed (Gilmour's is really from 5 March; Lowry's,
Margaret Wylie's and Gordon's come from accounts, not that night's
depositions). Claims appear only where two statements really give them.
"""

NIGHT = {
    "n": 1,
    "date": "3rd March 1711",
    "place": "Braehead House, Islandmagee",
    # one candle for the night (v0.5): each compare burns 1, writing a
    # finding out burns 2 more; at most 16 (it is drawn a pixel a unit)
    "candle": 16,

    # stage 2: the witnesses come to the table in this order, one closed
    # case each (statement ids); the parade comes last
    "order": ["dickey", "wilson", "gilmour", "lowry", "wylie_m", "gordon"],

    # -------------------------------------------------------------
    # Statements. A line is plain text, or (text, claim, value).
    # Two claims with the same name and different values are a
    # contradiction the clerk can find and flag. Identical statements
    # are noticed by the engine as "agreeth word for word".
    # -------------------------------------------------------------
    "statements": [
        {"id": "dickey", "who": "William Dickey, of Islandmagee", "sworn": "3rd March",
         "lines": [
             "Saith that for some time past the house of Hugh Wylie hath been haunted "
             "with evil spirits, as he is credibly informed.",
             "That Isobel Halliday, being now in the said house, is tormented both day "
             "and night by witches.",
             "That by the description she gave of them, they sent for Janet Boyd and "
             "Bessie Shaw on Friday last.",
             ("That when they came into the room she fell into a violent fit, and said "
              "that as soon as she saw them she was stung to the heart.", "fit_on_sight", "yes"),
             "That a great many other women were present when she challenged them.",
             ("That she never saw them in her lifetime before her trouble.",
              "never_seen", "yes"),
         ]},
        {"id": "wilson", "who": "John Wilson, of Islandmagee", "sworn": "3rd March",
         "copy_of": "dickey"},      # the same words exactly: the engine shows the copy

        {"id": "gilmour", "who": "Hugh Gilmour, of Islandmagee", "sworn": "3rd March",
         "lines": [
             "Saith that on the 28th of February he was in the house and saw Miss "
             "Halliday fall into fits as if she had been dead.",
             "That in one fit she said 'So and so', and after told them a woman came "
             "to the bedside and asked her, 'Molly Halliday, how do you do?'",
             ("That she gave the marks of one Janet Boyd, whom she had never seen.",
              "never_seen", "yes"),
             "That she heard her tormentors name one another: Janet Moore, Katty, "
             "Janet Kerr, and one McAlexander.",
             ("That Janet Moore was sent for about the first instant, and no one in "
              "the house knew of her coming.", "moore_expected", "no"),
             "That about thirty other women were brought into the room severally, "
             "and she was not disturbed in the least.",
         ]},
        {"id": "lowry", "who": "Margaret Lowry, servant", "sworn": "3rd March",
         "lines": [
             "Saith that on the night of the 27th of February a new mantua and head "
             "clothes were taken from a trunk and scattered through the house.",
             ("That she found on the parlour floor an apron that had lain two days "
              "in a locked room.", "apron_found_by", "lowry"),
             ("That it was rolled close and tied hard with five strange knots.",
              "apron_knots", "5"),
             "That none would loose the knots until Miss Halliday offered to.",
             "That inside was a flannel cap of the late Mrs Wylie's.",
         ]},
        {"id": "wylie_m", "who": "Margaret Wylie, sister of Hugh Wylie", "sworn": "3rd March",
         "lines": [
             ("Saith that an apron missing some time was brought back, tied with nine "
              "knots.", "apron_knots", "9"),
             ("That Miss Halliday was the first who found it, and untied all the knots "
              "without the least fear.", "apron_found_by", "isobel"),
             "That in the evening she was seized with violent fits, and cried out that "
             "a knife was run through her thigh.",
         ]},
        {"id": "gordon", "who": "Mr Robert Gordon, minister", "sworn": "3rd March",
         "lines": [
             "Saith that on the 1st of March Janet Moore's daughter came to him, "
             "much troubled that her mother was named for a witch.",
             ("That he desired Janet Moore to step down to the house as a neighbour, "
              "and went down himself before her.", "moore_expected", "yes"),
             "That whilst he sat talking with Miss Halliday, before Janet Moore was "
             "seen, she said a great terror and heat came upon her.",
             ("That when Janet Moore came to the door she cried out her name, and three "
              "strong men could scarcely hold her in the bed.", "fit_on_sight", "yes"),
         ]},
    ],

    # -------------------------------------------------------------
    # The parade: the clerk arranges how the accused is brought.
    # Each choice is (heading, options); every combination is allowed.
    # An option is (name, menu text, the sentence the scene uses).
    # The fit always happens (that is what was sworn), and "fit" is
    # always written: the Mayor gives the clerk those words. What changes
    # is what else the clerk saw, and what he can honestly add ("record",
    # each one Y or N). "seen" lines are what the clerk notices in the
    # house; they keep an ordinary explanation in view, so the parade
    # never reads as Isobel knowing anything she could not have known.
    # -------------------------------------------------------------
    "parade": {
        "accused": "kate",
        "intro": "Isobel has heard her tormentors call one of them Katty. Mayor Ellis "
                 "sends for Kate Rankin, Janet Boyd's daughter. You are to arrange it.",
        "choices": {
            "warn":  ("Before she comes", [
                ("tell",  "Tell Isobel who is coming",
                          "Isobel is told that Kate Rankin, Janet Boyd's daughter, is coming."),
                ("quiet", "Tell no one in the house",
                          "You tell no one in the house who is sent for.")]),
            "crowd": ("How she comes", [
                ("alone", "Bring Kate alone",
                          "Kate comes alone."),
                ("among", "Bring her among six women",
                          "Kate comes among six women of the island.")]),
            "where": ("How far", [
                ("room",  "Into the room",
                          "You have her brought into the room where Isobel lies."),
                ("door",  "Only to the house door",
                          "You have her kept at the house door.")]),
        },
        "always": "As soon as Kate comes to the house, Isobel's pains seize her, with a great "
                  "sweat. Three people cannot hold her. 'That is one of them.'",
        "seen": [   # (conditions, what the clerk notices)
            ({"warn": "quiet", "where": "door"},
             "Before Kate reaches the door her name is spoken in the hall. The house "
             "is full of neighbours, and voices carry."),
            ({"crowd": "among", "where": "room"},
             "Kate is the youngest of the six, and the only one with her mother's face."),
        ],
        # what Kate herself says, after the fit, every time
        "spoken": "Kate, when they let her go: 'I left my wheel to come. May I go "
                  "home to my mother now?'",
        "fit": "Kate Rankin was brought, and Isobel fell into fits and said, "
               "'That is one of them.'",
        "record": [   # (conditions, what the clerk may write, Mayor's patience)
            ({"warn": "tell"}, "She was told beforehand who was coming.", -2),
            ({"warn": "quiet", "where": "door"}, "Kate was unseen by her, at the house door only.",
             -1),
            ({"warn": "quiet", "where": "door"},
             "Her name was spoken in the hall before Kate reached the door.", -2),
            ({"crowd": "among", "where": "room"}, "She singled Kate out from among six women.",
             +2),
            ({"crowd": "among", "where": "room"},
             "Kate was the youngest of the six, and like her mother.", -2),
            ({"crowd": "alone", "where": "room"}, "Kate was brought to her alone.", 0),
        ],
    },

    # -------------------------------------------------------------
    # The findings (stage 2, the desk). Keyed by claim name (two
    # statements giving the claim different values: THEY DIFFER; the
    # same value: THEY AGREE) or "copy:<id>" (a statement sworn word for
    # word the same as another: WORD FOR WORD). A finding belongs to the
    # case of the later of its two statements, and goes "in hand" when
    # the clerk compares the pair. At the stamp each one is toggled
    # between its ways of writing it and "Let it lie" (always last,
    # nothing written, no cost).
    #
    #   label    the stamp list's heading for it (one line)
    #   write    [(menu, book text, patience, slip or None, answer or None)]
    #            menu: the option (the stamp list puts them side by side)
    #            book: what goes in the clerk's book
    #            patience: what it does to Mayor Ellis's patience
    #            slip: what he says (None: one from "mayor" by the cost)
    #            answer: a question put: what the witness at the table
    #                    answers, typed, and written in the book after it
    #
    # Plain statements of what was sworn: the clerk does not say who is
    # lying, and nothing here says the accused did anything. The answers
    # smooth the gap over; none of them says who was right.
    # -------------------------------------------------------------
    "findings": {
        "copy:wilson": {
            "label": "John Wilson's words are Dickey's",
            "write": [
                ("Corroborates", "John Wilson corroborates William Dickey.",
                 +1, "'Two witnesses. The law is satisfied.'", None),
                ("Word for word", "John Wilson's statement is William Dickey's, "
                 "word for word.",
                 -2, "'Two honest men may swear alike, sir.'",
                 "'I swear to what William swore. It is true, so it is the same.'"),
            ]},
        "never_seen": {
            "label": "Never seen before her trouble",
            "write": [
                ("Note it", "Hugh Gilmour agreeth with William Dickey: she had never "
                 "seen them before her trouble.", +1, None, None),
            ]},
        "apron_knots": {
            "label": "The apron: five knots or nine",
            "write": [
                ("Put the question", "Of the apron: Margaret Lowry saith it was tied "
                 "with five knots, Margaret Wylie saith nine.",
                 -1, "'Five or nine, it was knotted. Write on.'",
                 "'Nine, sir. Meg was frighted and miscounted.'"),
            ]},
        "apron_found_by": {
            "label": "The apron: who found it",
            "write": [
                ("Put the question", "Of the apron: Margaret Lowry saith she found it; "
                 "Margaret Wylie saith Miss Halliday found it first.",
                 -2, None,
                 "'Miss Halliday found it. Meg only brought it to the parlour.'"),
            ]},
        "moore_expected": {
            "label": "Was Janet Moore expected?",
            "write": [
                ("Put the question", "Mr Gordon himself sent for Janet Moore, and sat "
                 "with Miss Halliday before she came. Gilmour saith none knew.",
                 -3, "'Mr Gordon is a minister of the Gospel.'",
                 "'I sent for her as a neighbour. I said nothing of it to the girl.'"),
            ]},
        "fit_on_sight": {
            "label": "Fits at the sight of them",
            "write": [
                ("Note it", "Mr Gordon agreeth with William Dickey: she fell into "
                 "fits at the sight of them.", +1, None, None),
            ]},
    },

    # -------------------------------------------------------------
    # Mayor Ellis (stage 2). His patience is one hidden byte, 0-12;
    # Night One starts at 12. Never shown as a number: only by his manner
    # (a line at the top of the desk, by band) and what he says after
    # each stamp (a slip). Gains from the desk (agreements, the copy as
    # corroboration) count at most GAIN_MAX a night; the parade's don't.
    # -------------------------------------------------------------
    "orders": "'Take down what is sworn. Where two swear alike, note it: "
              "the law wants two.'",
    "mayor": {
        # by patience: 10-12, 6-9, 3-5, 1-2 (one line each, beside the candle)
        "manner": ["The Mayor warms his hands at the fire.",
                   "The Mayor reads over your shoulder.",
                   "The Mayor stands at your elbow.",
                   "The Mayor has his hand on the book."],
        # after a stamp, by what it did to his patience, when the costliest
        # item has no slip of its own (one line each; taken in turn)
        "slips": {
            "gain":   ["He helps himself to Hugh Wylie's brandy.",
                       "'There. That is the way of it.'",
                       "'Neatly put. I may tell the Bishop.'"],
            "none":   ["'Good. Call the next.'",
                       "Mayor Ellis nods, and calls the next."],
            "small":  ["He drums his fingers on the table.",
                       "'Write on, sir.'"],
            "middle": ["'Must you?'",
                       "'Ink is dear, and so is my evening.'"],
            "large":  ["'Thrice Mayor, sir, and never a question.'",
                       "He says nothing at all."],
        },
        # above the slip, when a cost leaves him at 5 or less
        "cold": ["He does not look at you.",
                 "'I begin to wonder whose clerk you are.'"],
        # the ledger, by band (10-12, 6-9, 3-5, 1-2)
        "goodnight": ["'A good night's work. Sleep well, sir.'",
                      "'Goodnight. Fewer questions tomorrow.'",
                      "He takes the book from you without a word.",
                      "'Tomorrow you write what is sworn, sir, or Mr Agnew will.'"],
        # at 0 (Agnew is an invented deputy)
        "dismiss": "'Give me the pen. Mr Agnew will write. You may sit by the "
                   "fire and warm your scruples.'",
        "bare": -2,           # the book holds only the fit at the night's end
    },
    # the ledger ends with the next night's order
    "next_orders": "'Tomorrow the girl's sight is evidence. Where she saw a "
                   "shape, write that the woman appeared to her.'",

    # -------------------------------------------------------------
    # nightcheck.py's three paths: what each writes. desk: finding ->
    # option (0 the first way of writing it; None let it lie; not listed:
    # never compared). parade: the arrangement and which record lines are
    # written ("all", or a list of their texts' first words).
    # -------------------------------------------------------------
    "paths": {
        "everything": {
            "desk": {"copy:wilson": 1, "never_seen": 0, "apron_knots": 0,
                     "apron_found_by": 0, "moore_expected": 0, "fit_on_sight": 0},
            "parade": ("quiet", "among", "room"), "lines": "all"},
        "collaborator": {
            "desk": {"copy:wilson": 0, "never_seen": 0, "fit_on_sight": 0},
            "parade": ("quiet", "among", "room"), "lines": ["She singled"]},
        "balanced": {
            "desk": {"copy:wilson": 0, "never_seen": 0, "fit_on_sight": 0,
                     "moore_expected": 0, "apron_found_by": 0, "apron_knots": None},
            "parade": ("quiet", "among", "room"), "lines": "all"},
    },

    # people named this night, for the clerk's index (game names)
    "people": {
        "isobel": "Isobel Halliday, 18, of Castlereagh, the afflicted",
        # each accused gets an ordinary detail (invented, not from the records)
        "boyd":   "Janet Boyd, of Islandmagee, accused. Spins flax, and sells eggs at "
                  "Carrickfergus on market days.",
        "shaw":   "Bessie Shaw, of Islandmagee, accused. William Shaw's wife; she mends "
                  "nets with him in the winter.",
        "moore":  "Janet Moore, of Islandmagee, accused. Her daughter walked to the "
                  "minister's for her.",
        "kate":   "Kate Rankin, daughter of Janet Boyd. Brought from her spinning wheel.",
        "kerr":   "Janet Kerr, of Ballycarry: named. Sends her butter to Larne.",
        "mcalexander": "McAlexander: named, never sent for. No one gives a first name.",
    },
}
