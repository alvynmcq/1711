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
             ("That by the description she gave of them, they sent for Janet Boyd and "
              "Bessie Shaw on Friday last.", "boyd_shaw_test", "friday"),
             "That when they came into the room she fell into a violent fit, and said "
             "that as soon as she saw them she was stung to the heart.",
             ("That a great many other women were present when she challenged them.",
              "boyd_shaw_alone", "no"),
             ("That she never saw them in her lifetime before her trouble.",
              "boyd_shaw_known", "never"),
         ]},
        {"id": "wilson", "who": "John Wilson, of Islandmagee", "sworn": "3rd March",
         "copy_of": "dickey"},      # the same words exactly: the engine shows the copy

        {"id": "gilmour", "who": "Hugh Gilmour, of Islandmagee", "sworn": "3rd March",
         "lines": [
             "Saith that on the 28th of February he was in the house and saw Miss "
             "Halliday fall into fits as if she had been dead.",
             ("That in one fit she said 'So and so', and after told them a woman came "
              "to the bedside and asked her, 'Molly Halliday, how do you do?'",
              "first_words", "molly"),
             "That she gave the marks of one Janet Boyd, whom she had never seen.",
             ("That she heard her tormentors name one another: Janet Moore, Katty, "
              "Janet Kerr, and one McAlexander.", "names_heard", "moore_katty_kerr_mcalexander"),
             ("That Janet Moore was sent for about the first instant, and no one in "
              "the house knew of her coming.", "moore_expected", "no"),
             ("That about thirty other women were brought into the room severally, "
              "and she was not disturbed in the least.", "thirty_women", "untroubled"),
         ]},
        {"id": "lowry", "who": "Margaret Lowry, servant", "sworn": "3rd March",
         "lines": [
             "Saith that on the night of the 27th of February a new mantua and head "
             "clothes were taken from a trunk and scattered through the house.",
             ("That she found on the parlour floor an apron that had lain two days "
              "in a locked room.", "apron_where", "parlour"),
             ("That it was rolled close and tied hard with five strange knots.",
              "apron_knots", "5"),
             "That none would loose the knots until Miss Halliday offered to.",
             ("That inside was a flannel cap of the late Mrs Wylie's.", "apron_inside", "cap"),
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
    # Each choice is a list of options; every combination is allowed.
    # The record always shows the fit (that is what was sworn). What
    # changes is what the clerk can honestly write down.
    # -------------------------------------------------------------
    "parade": {
        "accused": "kate",
        "intro": "Isobel has heard her tormentors call one of them Katty. Mayor Ellis "
                 "sends for Kate Rankin, Janet Boyd's daughter. You are to arrange it.",
        "choices": {
            "warn":   [("tell", "Tell Isobel who is coming"), ("quiet", "Tell no one in the house")],
            "crowd":  [("alone", "Bring Kate alone"), ("among", "Bring her among six women")],
            "where":  [("room", "Into the room"), ("door", "No further than the house door")],
        },
        "always": "As soon as Kate enters the house, Isobel's pains seize her, with a great "
                  "sweat. Three people cannot hold her. 'That is one of them.'",
        "record": [   # (conditions, what the clerk may write)
            ({"warn": "tell"}, "She was told beforehand who was coming."),
            ({"warn": "quiet", "where": "door"}, "Kate was unseen by her, at the house door only."),
            ({"crowd": "among", "where": "room"}, "She singled Kate out from among six women."),
            ({"crowd": "alone", "where": "room"}, "Kate was brought to her alone."),
        ],
    },

    # people named this night, for the clerk's index (game names)
    "people": {
        "isobel": "Isobel Halliday, 18, of Castlereagh, the afflicted",
        "boyd":   "Janet Boyd, of Islandmagee, accused",
        "shaw":   "Bessie Shaw, of Islandmagee, accused",
        "moore":  "Janet Moore, of Islandmagee, accused",
        "kate":   "Kate Rankin, daughter of Janet Boyd",
        "kerr":   "Janet Kerr, of Ballycarry: named",
        "mcalexander": "McAlexander: named, never sent for",
    },
}
