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
             "That when they came into the room she fell into a violent fit, and said "
             "that as soon as she saw them she was stung to the heart.",
             "That a great many other women were present when she challenged them.",
             "That she never saw them in her lifetime before her trouble.",
         ]},
        {"id": "wilson", "who": "John Wilson, of Islandmagee", "sworn": "3rd March",
         "copy_of": "dickey"},      # the same words exactly: the engine shows the copy

        {"id": "gilmour", "who": "Hugh Gilmour, of Islandmagee", "sworn": "3rd March",
         "lines": [
             "Saith that on the 28th of February he was in the house and saw Miss "
             "Halliday fall into fits as if she had been dead.",
             "That in one fit she said 'So and so', and after told them a woman came "
             "to the bedside and asked her, 'Molly Halliday, how do you do?'",
             "That she gave the marks of one Janet Boyd, whom she had never seen.",
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
             "That when Janet Moore came to the door she cried out her name, and three "
             "strong men could scarcely hold her in the bed.",
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
                ("door",  "No further than the house door",
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
        "record": [   # (conditions, what the clerk may write)
            ({"warn": "tell"}, "She was told beforehand who was coming."),
            ({"warn": "quiet", "where": "door"}, "Kate was unseen by her, at the house door only."),
            ({"warn": "quiet", "where": "door"},
             "Her name was spoken in the hall before Kate reached the door."),
            ({"crowd": "among", "where": "room"}, "She singled Kate out from among six women."),
            ({"crowd": "among", "where": "room"},
             "Kate was the youngest of the six, and like her mother."),
            ({"crowd": "alone", "where": "room"}, "Kate was brought to her alone."),
        ],
    },

    # -------------------------------------------------------------
    # What the clerk sees when two marked lines are compared, and what
    # goes in the book if he writes it down. Keyed by claim name for a
    # contradiction, or "copy:<id>" for a statement sworn word for word
    # the same as another. scripts/night.py refuses a finding with no
    # text here. Plain statements of what was sworn: the clerk does not
    # say who is lying, and nothing here says the accused did anything.
    # -------------------------------------------------------------
    "findings": {
        "apron_knots": (
            "Margaret Lowry saith five knots. Margaret Wylie saith nine. "
            "It is the one apron.",
            "Of the apron: Margaret Lowry saith it was tied with five knots, "
            "Margaret Wylie saith nine."),
        "moore_expected": (
            "Hugh Gilmour saith none in the house knew Janet Moore was coming. "
            "Mr Gordon saith he sent for her himself, and went down before her.",
            "Mr Gordon himself sent for Janet Moore, and sat with Miss Halliday "
            "before she came. Gilmour saith none knew."),
        "apron_found_by": (
            "Margaret Lowry saith she found the apron herself. Margaret Wylie "
            "saith Miss Halliday was the first who found it.",
            "Of the apron: Margaret Lowry saith she found it; Margaret Wylie "
            "saith Miss Halliday found it first."),
        "copy:wilson": (
            "Line for line, John Wilson swears the same words as William Dickey.",
            "John Wilson's statement agreeth with William Dickey's, word for word."),
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
