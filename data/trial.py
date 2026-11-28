"""The trial, 31st March 1711, Carrickfergus (stage 3, v1.0: the day).

DRAFT CONTENT. Adapted from the depositions and accounts in Sneddon &
Devlin (eds), w1711.org, CC BY 4.0, every name changed (NOTES.md has the
list). The court record is what was sworn in March; the testimony has
drifted since, towards the Mayor's version. The court sits from six till
two (MacSkimin); the girl was dumb throughout and had no fit (Tisdall);
the accused were churchgoers, and one judge told the jury they could not
convict on the girl's visions alone (Tisdall, Upton's charge).

Text rules (scripts/trial.py checks them):
  record facts   36 characters (the record screen: mark, number, fact)
  testimony      up to 4 rows of 40 (rows 17-20)
  answers        up to 4 rows; a HOLD's question up to 2 rows (19-20)
  notes          up to 3 rows
  remarks        one row (row 23); manner lines one row (row 21)
Never "witch", anywhere: the accused are "the accused", or named.
Humour at the bench and the Mayor only.

Notes (what Lyle has written) carry what they bear on, for the verdict:
  bears     "all", or the accused they bear on (ids in "accused")
  spectral  what only Isobel saw, heard or felt (none else did)
  thirty    the thirty women brought before her, and she not disturbed
  character the accused come to worship and took the sacrament
"""


def note(text, bears="all", spectral=False, thirty=False, character=False):
    return {"text": text, "bears": bears, "spectral": spectral, "thirty": thirty,
            "character": character}


TRIAL = {
    "date": "31st March 1711",
    "start": 6 * 60,            # the court sits at six (minutes from midnight)
    "jury": 14 * 60,            # at two the jury retires

    # what things cost, in minutes (the checker prints paths against them)
    # (v1.0: v0.9's 3/6/8/10 were for an hour; over the day they left
    # hours to spare, so a third more, and 80 minutes in the box)
    "cost": {"line": 4,         # a testimony line heard for the first time
             "press": 8,        # SPACE on a line
             "hold": 10,        # a fact that contradicts it: HOLD, SIR!
             "wrong": 12},      # a fact that doesn't bear (and the bench)

    # the bench's patience (Justice Ormsby): 0-12, from 12, for the day
    "bench": {
        "start": 12,
        # by band: 10-12, 6-9, 3-5, 1-2 (row 21)
        "manner": ["Justice Ormsby writes steadily.",
                   "Justice Ormsby looks at the clock.",
                   "Justice Ormsby has stopped writing.",
                   "Justice Ormsby is looking at you."],
        # a presentation that doesn't bear, in turn (typed, rows 17-20)
        "rebukes": ["Ormsby: 'That does not bear upon it, brother.'",
                    "Ormsby: 'The record says what it says, brother. So does "
                    "the witness. We are not here to hear you read.'",
                    "Ormsby: 'We have a great many witnesses, brother, and one "
                    "dinner.'",
                    "Ormsby: 'Brother Lyle, the jury can count. They have "
                    "counted your papers twice.'"],
        "silenced": "Ormsby: 'Brother Lyle, you have said enough. The witnesses "
                    "will go on, and you will listen.'",
        "silent_row": "You may not speak again today.",
        "silent_key": "Ormsby: 'Brother.'",
        "after_wrong": "Ormsby turns back to the witness.",
        "after_press": "Ormsby: 'Go on.'",
        # two o'clock strikes while a witness is in the box
        "jury_bell": "Ormsby: 'Two o'clock. Stand down. The jury must retire, "
                     "brother, whatever is left unsaid.'",
    },

    # -------------------------------------------------------------
    # The accused, in the order the verdict reads them (game names;
    # NOTES.md has the real ones). Eight women.
    # -------------------------------------------------------------
    "accused": [("boyd", "Janet Boyd"), ("shaw", "Bessie Shaw"),
                ("rankin", "Kate Rankin"), ("moore", "Janet Moore"),
                ("kerr", "Janet Kerr"), ("erskine", "Janet Erskine"),
                ("patterson", "Jean Patterson"), ("ross", "Margaret Ross")],

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
        ("described", "She described them; others named.", "William Dickey", "3rd March"),
    ],

    # -------------------------------------------------------------
    # What Lyle can have written (by id). A press or a HOLD names one.
    # -------------------------------------------------------------
    "notes": {
        # Lowry
        "l_found": note("In March she found the apron herself. Today Miss Halliday did."),
        "l_knots": note("In March she swore five knots. Today she swears nine."),
        "l_boyd": note("None saw Janet Boyd at the bed but Miss Halliday.",
                       bears="boyd", spectral=True),
        # Margaret Wylie
        "w_knots": note("Mrs Wylie swears nine knots; Margaret Lowry swore five."),
        "w_talk": note("Janet Boyd was talked of in the kitchen before Miss "
                       "Halliday named her.", bears="boyd shaw"),
        "w_knife": note("No wound was found where she cried a knife was in her "
                        "thigh.", spectral=True),
        "w_tongue": note("None saw Jean Patterson or Janet Kerr at her; only Miss "
                         "Halliday.", bears="patterson kerr", spectral=True),
        # William Dickey
        "d_told": note("Dickey saw nothing at Braehead himself. He was told.",),
        "d_named": note("In March she described them, and others put the names "
                        "to it.", bears="boyd shaw"),
        "d_together": note("Boyd and Shaw were brought in together, and the "
                           "others stood back from them.", bears="boyd shaw"),
        # John Wilson
        "j_copy": note("Wilson set his mark to Dickey's words. He was there for "
                       "some of it.", bears="boyd shaw"),
        "j_yard": note("Wilson was in the yard when they came in. He heard; he "
                       "did not see.", bears="boyd shaw"),
        # Hugh Gilmour
        "g_names": note("None heard the names spoken but Miss Halliday. She told "
                        "them after.", bears="moore rankin kerr", spectral=True),
        "g_moore": note("Mr Gordon sent for Janet Moore and sat with Miss Halliday "
                        "first. Gilmour swore none knew.", bears="moore"),
        "g_thirty": note("Thirty women were brought before her, and she was not "
                         "disturbed by one.", thirty=True),
        # Robert Gordon
        "r_sent": note("Mr Gordon sent for Janet Moore himself, and went before "
                       "her to the house.", bears="moore"),
        "r_told": note("Mr Gordon may have told Miss Halliday a neighbour was "
                       "coming.", bears="moore"),
        "r_church": note("Most of the accused come to worship, and took the "
                         "sacrament at Christmas.", character=True),
        # Mayor Ellis
        "e_clerk": note("The Mayor gave his clerk the words of the depositions."),
        "e_thirty": note("The Mayor's thirty: she was not disturbed by one, as "
                         "Gilmour swore.", thirty=True),
        "e_erskine": note("Half Carrickfergus knew Janet Erskine was sent out to "
                          "Braehead.", bears="erskine"),
        "e_ross": note("The Mayor spoke of Margaret Ross in the house before she "
                       "was described.", bears="ross"),
        "e_named": note("Dickey swore the house put the names to her "
                        "descriptions. The Mayor swears not.", bears="boyd shaw"),
    },

    # -------------------------------------------------------------
    # The day, in order: the witnesses (by id) and the scenes.
    # -------------------------------------------------------------
    "order": ["lowry", "wylie", "dickey", "wilson", "gilmour", "gordon",
              "isobel", "ellis"],

    # Isobel brought in, once: unable to speak, never questioned (Tisdall:
    # struck dumb the day before, no fit while the trial lasted).
    "scenes": {
        "isobel": {
            "pic": "isobel_in",
            "cost": 10,
            "pages": [
                ["The court sends for the afflicted. Isobel Halliday is brought "
                 "in between two women of the house.",
                 "She has not spoken since yesterday."],
                ["She looks about the court as if she does not know where she "
                 "is. Ormsby asks if she can answer. She cannot.",
                 "She sinks against the woman beside her and her eyes close."],
                ["She is carried out. No one asks her anything. She is eighteen."],
            ],
        },
    },

    # -------------------------------------------------------------
    # The witnesses. Each line: id, what is said; "hidden" lines appear
    # only when a press draws them out (after the pressed line).
    #   press: (Lyle's question, the answer, line it draws out or None,
    #           note id or None)
    #   holds: {fact: (Lyle's question, the answer, Ormsby, note id)}
    #   wrong: {fact: what Ormsby says instead of the next rebuke}
    # box: the most minutes in the box; hold/wrong: what a presentation
    # costs the bench (the Mayor's cost more).
    # -------------------------------------------------------------
    "witnesses": [{
        "id": "lowry",
        "name": "MARGARET LOWRY, servant",
        "who": "Margaret Lowry",
        "called": "The court calls Margaret Lowry, servant at Braehead House. "
                  "She takes the oath.",
        "portrait": "lowry",
        "box": 80, "hold": 0, "wrong": 2,
        "opening": "Ormsby: 'Go on, Mrs Lowry.'",
        "after_hold": "Ormsby: 'Go on, Mrs Lowry.'",
        "asked": "Ormsby: 'She has answered that.'",
        "raised": "Ormsby: 'You have had that from her.'",
        "stand_down": "Ormsby: 'You may stand down, Mrs Lowry.'",
        "bell": "Ormsby: 'That is long enough in the box, Mrs Lowry. Stand "
                "down.'",
        "press_none": ("Go on, Mrs Lowry. What more?", "'It is as I said, my lord.'"),
        "lines": [
            {"id": "mantua",
             "say": "'On the night of the 27th of February, my lord, the mistress's "
                    "new mantua was taken from the trunk and strewn about the house.'",
             "press": ("Who saw it done, Mrs Lowry?",
                       "'None saw it done, my lord. We found the things in the "
                       "morning, all about.'", None, None)},
            {"id": "apron",
             "say": "'Two days after, an apron was found on the parlour floor, that "
                    "had lain two days locked in a room.'",
             "press": ("Found by whom?",
                       "'By Miss Halliday, my lord. She was the first that found "
                       "it.'", "found", None)},
            {"id": "found", "hidden": True,
             "say": "'Miss Halliday found the apron, my lord, and called me to it.'",
             "holds": {"lowry_found": (
                 "In March you swore you found it yourself. Today Miss Halliday "
                 "found it?",
                 "'Did I, my lord? I carried it to the parlour. Miss Halliday says "
                 "she found it first, and she would know.'",
                 "Ormsby: 'Whoever found it, brother, it was found. That is the "
                 "matter.'", "l_found")}},
            {"id": "knots",
             "say": "'It was rolled up close, my lord, and tied hard with nine "
                    "strange knots.'",
             "press": ("Did you count them yourself?",
                       "'I did, my lord. Nine. I have told it so many times.'",
                       None, None),
             "holds": {"knots5": (
                 "On the 3rd of March you swore five knots. How came you to swear "
                 "nine?",
                 "'I... it was a great confusion, my lord. I have heard it told so "
                 "often, it is nine now.'",
                 "Ormsby: 'A servant's count, brother. The apron was knotted, and "
                 "that is the matter.'", "l_knots")},
             "wrong": {"knots9": "Ormsby: 'Mrs Wylie swore nine, brother. They "
                                 "agree. You have helped the Crown.'"}},
            {"id": "loosed",
             "say": "'And Miss Halliday loosed every knot of it, without the least "
                    "fear.'",
             "press": ("Why would none of you loose them?",
                       "'We durst not, my lord. It was not a thing of this world.'",
                       None, None),
             "wrong": {"only_isobel": "Ormsby: 'That is what she swears, brother. "
                                      "It agrees with her.'"}},
            {"id": "cap",
             "say": "'Inside it was a flannel cap of the late Mrs Wylie's.'"},
            {"id": "boyd",
             "say": "'That night Miss Halliday cried out that Janet Boyd stood at "
                    "the bed's foot, and she pointed at her.'",
             "press": ("Did you see Janet Boyd there, Mrs Lowry?",
                       "'No, my lord. None saw her but Miss Halliday. But she "
                       "pointed, my lord, as if she were there.'", None, "l_boyd")},
        ],
    }, {
        "id": "wylie",
        "name": "MARGARET WYLIE, of Braehead",
        "who": "Margaret Wylie",
        "called": "The court calls Margaret Wylie, sister of Hugh Wylie, of "
                  "Braehead House. She takes the oath.",
        "portrait": "wylie",
        "box": 80, "hold": 0, "wrong": 2,
        "opening": "Ormsby: 'Go on, Mrs Wylie.'",
        "after_hold": "Ormsby: 'Go on, Mrs Wylie.'",
        "asked": "Ormsby: 'She has answered that.'",
        "raised": "Ormsby: 'You have had that from her.'",
        "stand_down": "Ormsby: 'You may stand down, Mrs Wylie.'",
        "bell": "Ormsby: 'That is long enough, Mrs Wylie. You may stand down.'",
        "press_none": ("Go on, Mrs Wylie. What more?", "'Only what I have said, my "
                                                      "lord.'"),
        "lines": [
            {"id": "apron",
             "say": "'My late mother's apron went missing in February, my lord, and "
                    "was brought back to the parlour, knotted.'"},
            {"id": "knots",
             "say": "'Nine knots, my lord, as I swore, and Miss Halliday was the "
                    "first that found it.'",
             "holds": {"knots5": (
                 "Margaret Lowry swore five knots in March. Which of you counted?",
                 "'Meg was frighted, my lord. She miscounted. It was nine; "
                 "everyone says nine now.'",
                 "Ormsby: 'One woman counted badly and one well, brother. It is "
                 "an apron, not a ledger.'", "w_knots")},
             "wrong": {"knots9": "Ormsby: 'She swore nine then and nine now, "
                                 "brother. That is called consistency.'"}},
            {"id": "named",
             "say": "'That night in her fit she named Janet Boyd, my lord, a "
                    "woman she had never seen in her life.'",
             "press": ("How came she by the name, Mrs Wylie?",
                       "'The women in her fit called each other by name, my lord. "
                       "And... there was talk in the house.'", "talk", None),
             "wrong": {"never_seen": "Ormsby: 'Mr Dickey says the same, brother. "
                                     "Thank you.'"}},
            {"id": "talk", "hidden": True,
             "say": "'Janet Boyd was spoken of in the kitchen that week, my lord. "
                    "The neighbours said she had a bad eye. Everyone says so.'",
             "press": ("Before Miss Halliday named her?",
                       "'Before, my lord. Well... it was all talked of. The girl "
                       "was in the next room.'", None, "w_talk")},
            {"id": "knife",
             "say": "'Next evening she fell on the stairs, crying out that a knife "
                    "was run through her thigh.'",
             "press": ("Was there a wound?",
                       "'No, my lord. Not a mark. That is how we knew it was no "
                       "natural knife.'", None, "w_knife")},
            {"id": "tongue",
             "say": "'In her fits she cried out on Jean Patterson, and on Janet "
                    "Kerr, that twisted her tongue back in her throat.'",
             "press": ("Did anyone see those women at her?",
                       "'None, my lord. Only she. But we saw her tongue drawn back; "
                       "that we all saw.'", None, "w_tongue")},
        ],
    }, {
        "id": "dickey",
        "name": "WILLIAM DICKEY, of Islandmagee",
        "who": "William Dickey",
        "called": "The court calls William Dickey, of Islandmagee, a farmer. He "
                  "takes the oath.",
        "portrait": "dickey",
        "box": 80, "hold": 0, "wrong": 2,
        "opening": "Ormsby: 'Go on, Mr Dickey.'",
        "after_hold": "Ormsby: 'Go on, Mr Dickey.'",
        "asked": "Ormsby: 'He has answered that.'",
        "raised": "Ormsby: 'You have had that from him.'",
        "stand_down": "Ormsby: 'You may stand down, Mr Dickey.'",
        "bell": "Ormsby: 'That is long enough, Mr Dickey. Stand down.'",
        "press_none": ("Go on, Mr Dickey. What more?", "'That is all of it, my "
                                                      "lord.'"),
        "lines": [
            {"id": "haunted",
             "say": "'For some time past the house of Hugh Wylie hath been haunted, "
                    "my lord, as all the island knows.'",
             "press": ("Did you see anything there yourself?",
                       "'No, my lord. I was credibly informed. Everyone was.'",
                       None, "d_told")},
            {"id": "named",
             "say": "'Miss Halliday named the women that tormented her, my lord, "
                    "and they sent for Janet Boyd and Bessie Shaw on the Friday.'",
             "holds": {"described": (
                 "In March she gave a description, and by it they sent. Today she "
                 "named them?",
                 "'It comes to the same, my lord. She told how they looked, and "
                 "we knew who she meant.'",
                 "Ormsby: 'A description, a name. The jury will not split that "
                 "hair, brother.'", "d_named")}},
            {"id": "room",
             "say": "'A great many women were in the room, and she challenged "
                    "those two only.'",
             "press": ("How were they brought in?",
                       "'Together, my lord, mother and daughter. The others stood "
                       "back from them.'", None, "d_together")},
            {"id": "fit",
             "say": "'As soon as she saw them she fell into a violent fit, and said "
                    "she was stung to the heart.'",
             "wrong": {"fit_sight": "Ormsby: 'He swore that in March, brother, "
                                    "and he swears it now.'"}},
            {"id": "never",
             "say": "'And she never saw them in her lifetime before her trouble, "
                    "my lord.'",
             "wrong": {"never_seen": "Ormsby: 'Mr Dickey agrees with Mr Dickey, "
                                     "brother.'"}},
        ],
    }, {
        "id": "wilson",
        "name": "JOHN WILSON, of Islandmagee",
        "who": "John Wilson",
        "called": "The court calls John Wilson, of Islandmagee, a neighbour of "
                  "William Dickey's. He takes the oath.",
        "portrait": "wilson",
        "box": 80, "hold": 0, "wrong": 2,
        "opening": "Ormsby: 'Go on, Mr Wilson.'",
        "after_hold": "Ormsby: 'Go on, Mr Wilson.'",
        "asked": "Ormsby: 'He has answered that.'",
        "raised": "Ormsby: 'You have had that from him.'",
        "stand_down": "Ormsby: 'You may stand down, Mr Wilson.'",
        "bell": "Ormsby: 'That is long enough, Mr Wilson. Stand down.'",
        "press_none": ("Go on, Mr Wilson. What more?", "'As William said, my lord.'"),
        "lines": [
            {"id": "haunted",
             "say": "'Saith that for some time past the house of Hugh Wylie hath been "
                    "haunted, as he is credibly informed.'",
             "holds": {"wilson": (
                 "Your March statement was Dickey's, word for word. Whose words "
                 "are these?",
                 "'I set my mark to what William swore, my lord. I was there on "
                 "the Friday. Some of it.'",
                 "Ormsby: 'Two men saw the same thing and said it the same way. "
                 "That is called corroboration, brother.'", "j_copy")}},
            {"id": "tormented",
             "say": "'Miss Halliday is tormented both day and night, my lord.'"},
            {"id": "friday",
             "say": "'On the Friday Janet Boyd and Bessie Shaw were sent for, and "
                    "she fell into a fit as soon as she saw them.'",
             "press": ("Were you in the room when they came in?",
                       "'I was not, my lord.'", "yard", None),
             "wrong": {"fit_sight": "Ormsby: 'Mr Dickey swore the same, brother. "
                                    "As we have heard.'"}},
            {"id": "yard", "hidden": True,
             "say": "'I was in the yard, my lord, seeing to William's horse. I heard "
                    "her cry out when they came.'",
             "press": ("Then you did not see her fall?",
                       "'No, my lord. But I heard it, and William saw it.'",
                       None, "j_yard")},
            {"id": "never",
             "say": "'She never saw them in her lifetime before, my lord.'",
             "wrong": {"never_seen": "Ormsby: 'They agree, brother. You keep "
                                     "showing us that they agree.'"}},
        ],
    }, {
        "id": "gilmour",
        "name": "HUGH GILMOUR, of Islandmagee",
        "who": "Hugh Gilmour",
        "called": "The court calls Hugh Gilmour, of Islandmagee, an elder of the "
                  "congregation. He takes the oath.",
        "portrait": "gilmour",
        "box": 80, "hold": 0, "wrong": 2,
        "opening": "Ormsby: 'Go on, Mr Gilmour.'",
        "after_hold": "Ormsby: 'Go on, Mr Gilmour.'",
        "asked": "Ormsby: 'He has answered that.'",
        "raised": "Ormsby: 'You have had that from him.'",
        "stand_down": "Ormsby: 'You may stand down, Mr Gilmour.'",
        "bell": "Ormsby: 'That is long enough, Mr Gilmour. Stand down.'",
        "press_none": ("Go on, Mr Gilmour. What more?", "'I have told it, my lord.'"),
        "lines": [
            {"id": "fits",
             "say": "'On the 28th of February, my lord, I saw Miss Halliday fall "
                    "into fits, as if she had been dead.'"},
            {"id": "names",
             "say": "'In her fits her tormentors named one another: Janet Moore, "
                    "Katty, and Janet Kerr.'",
             "press": ("Did you hear them name each other, Mr Gilmour?",
                       "'No, my lord. She told us after what they said. None heard "
                       "it but she.'", None, "g_names")},
            {"id": "moore",
             "say": "'Janet Moore was sent for about the first of March, and none in "
                    "the house knew of her coming.'",
             "holds": {"gordon": (
                 "Mr Gordon swore he sent for her, and sat with Miss Halliday "
                 "before she came.",
                 "'Did he, my lord? I... I did not know that. Then the minister "
                 "knew.'",
                 "Ormsby: 'A minister may visit a sick girl, brother.'",
                 "g_moore")},
             "wrong": {"moore": "Ormsby: 'He swore that in March, brother. He "
                                "agrees with himself.'"}},
            {"id": "thirty",
             "say": "'Thirty other women were brought in to her, my lord, and she "
                    "knew her tormentors from them all.'",
             "holds": {"thirty": (
                 "In March you swore thirty came in, and she was not disturbed "
                 "in the least.",
                 "'That is so, my lord. They were honest women, and she was not "
                 "troubled by them. She knew the difference.'",
                 "Ormsby: 'Just so. The honest did not trouble her. Go on.'",
                 "g_thirty")}},
            {"id": "marks",
             "say": "'She gave the marks of Janet Boyd, my lord, whom she had never "
                    "seen.'",
             "press": ("What marks?",
                       "'Her height, my lord, and her clothes. And a scar. I am "
                       "not sure now who said the scar.'", None, None),
             "wrong": {"never_seen": "Ormsby: 'Mr Dickey says the same, brother. "
                                     "They agree.'"}},
        ],
    }, {
        "id": "gordon",
        "name": "MR ROBERT GORDON, minister",
        "who": "Robert Gordon",
        "called": "The court calls Mr Robert Gordon, minister of the congregation "
                  "at Islandmagee. He takes the oath.",
        "portrait": "gordon",
        "box": 80, "hold": 0, "wrong": 2,
        "opening": "Ormsby: 'Go on, Mr Gordon.'",
        "after_hold": "Ormsby: 'Go on, Mr Gordon.'",
        "asked": "Ormsby: 'He has answered that.'",
        "raised": "Ormsby: 'You have had that from him.'",
        "stand_down": "Ormsby: 'Thank you, Mr Gordon. You may stand down.'",
        "bell": "Ormsby: 'That is long enough, Mr Gordon. Thank you.'",
        "press_none": ("Go on, Mr Gordon. What more?", "'I have said what I know, "
                                                      "my lord.'"),
        "lines": [
            {"id": "prayed",
             "say": "'I sat up with the family in their trouble, my lord, and prayed "
                    "with them, as was my duty.'"},
            {"id": "came",
             "say": "'On the 1st of March Janet Moore came down to the house. I was "
                    "there, sitting with Miss Halliday.'",
             "holds": {"gordon": (
                 "In March you swore you desired her to come, and went down "
                 "before her.",
                 "'I asked her to step down as a neighbour, my lord. Her daughter "
                 "was troubled. I meant it kindly.'",
                 "Ormsby: 'A minister's kindness, brother. Would you have him "
                 "unkind?'", "r_sent")},
             "wrong": {"moore": "Ormsby: 'Mr Gilmour says none knew she was "
                                "coming, brother. That helps the Crown.'"}},
            {"id": "heat",
             "say": "'Before Janet Moore was seen, the girl said a great terror and "
                    "heat came upon her.'",
             "press": ("Had you spoken of Janet Moore in her hearing?",
                       "'I may have said a neighbour was coming, my lord. I do "
                       "not remember.'", None, "r_told")},
            {"id": "door",
             "say": "'When Janet Moore came to the door she cried out her name, and "
                    "three strong men could scarcely hold her in the bed.'",
             "wrong": {"fit_sight": "Ormsby: 'A fit at the sight of her, brother. "
                                    "As Mr Dickey swore of the others.'"}},
            {"id": "flock",
             "say": "'The accused are of my congregation, my lord. I would not have "
                    "them wronged, nor the girl.'",
             "press": ("Do they come to worship, Mr Gordon?",
                       "'Most of them, my lord. Some took the sacrament at "
                       "Christmas. Janet Boyd prays with her family.'",
                       None, "r_church")},
        ],
    }, {
        "id": "ellis",
        "name": "MAYOR ELLIS, of Carrickfergus",
        "who": "Mayor Ellis",
        "called": "The court calls Thomas Ellis, Mayor of Carrickfergus, who took "
                  "the depositions. He takes the oath, and adds a few words of his own.",
        "portrait": "ellis",
        "box": 80, "hold": 3, "wrong": 3,
        "opening": "Ormsby: 'Mr Mayor.'",
        "after_hold": "Ormsby: 'Go on, Mr Mayor. Briefly.'",
        "asked": "Ormsby: 'He has answered, at length.'",
        "raised": "Ormsby: 'You have had that from him.'",
        "stand_down": "Ormsby: 'Thank you, Mr Mayor. You may stand down.'",
        "bell": "Ormsby: 'Thank you, Mr Mayor. That is ample.'",
        "press_none": ("Go on, Mr Mayor.", "'I could go on all day, my lord.'"),
        "lines": [
            {"id": "thrice",
             "say": "'I am thrice Mayor of Carrickfergus, my lord, and I took every "
                    "deposition myself, fairly.'",
             "press": ("Did you write them yourself, Mr Mayor?",
                       "'My clerk wrote, my lord. I gave him the words. That is, I "
                       "saw they were plainly put.'", None, "e_clerk")},
            {"id": "thirty",
             "say": "'We tried the girl fairly. Thirty women were brought before "
                    "her, and she picked out her tormentors from them all.'",
             "holds": {"thirty": (
                 "Gilmour swore thirty were brought in, and she was not "
                 "disturbed in the least.",
                 "'Not by the honest ones, my lord. That was the test. It worked "
                 "admirably. I devised it myself.'",
                 "Ormsby: 'The Mayor's tests always work, brother. He tells us "
                 "so himself.'", "e_thirty")}},
            {"id": "erskine",
             "say": "'Janet Erskine was sent out from Carrickfergus privately, my "
                    "lord, and the girl knew her at once.'",
             "press": ("Who knew she was sent?",
                       "'Only myself, my lord. And Mr Craig, and my officer, and "
                       "the officer's wife. And the carter.'", "carter", None)},
            {"id": "carter", "hidden": True,
             "say": "'The carter drove her out by Braehead and stopped at the gate "
                    "for his dinner. He is a great talker, my lord.'",
             "press": ("A great talker, at the gate of the house?",
                       "'He talks to his horse, my lord. Mostly to his horse.'",
                       None, "e_erskine")},
            {"id": "ross",
             "say": "'Margaret Ross she described so exactly that I knew her by it, "
                    "and had her taken.'",
             "press": ("Had you spoken of Margaret Ross in the house before?",
                       "'I may have mentioned her, my lord. She is well known. I "
                       "know everyone.'", None, "e_ross")},
            {"id": "named",
             "say": "'Every one of the accused was named by the girl herself, my "
                    "lord, and none was named to her. On my honour.'",
             "holds": {"described": (
                 "Mr Dickey swore she gave a description, and others put the "
                 "names to it.",
                 "'Mr Dickey is a farmer, my lord, not a lawyer. He swore what I "
                 "wrote... what he saw.'",
                 "Ormsby: 'Mr Mayor, you need not help us quite so much.'",
                 "e_named"),
                       "gordon": (
                 "Mr Gordon swore he sent for Janet Moore himself.",
                 "'The minister is a good man, my lord. He does what he is told.'",
                 "Ormsby: 'Brother, the Mayor has been very patient with you. "
                 "I have not.'", "r_sent")}},
        ],
    }],

    # -------------------------------------------------------------
    # The end of the day: Lyle's charge, Ormsby's, the jury, the verdict.
    # The spectral evidence is discredited when Lyle has the thirty and
    # at least "spectral" admissions written. Then each accused is
    # acquitted whose score reaches "acquit": a note that bears on all
    # counts 1, a note that bears on her counts 2. Otherwise all are
    # convicted, as they were.
    # -------------------------------------------------------------
    "verdict": {
        "spectral": 3,
        "acquit": 10,
        "no_more": "The Crown calls no more witnesses. Ormsby looks at the clock "
                   "with something like relief.",
        "two": "The bell strikes two. The court has sat since six. The jury must "
               "retire, whatever has or hasn't been said.",
        "lyle_head": "JUSTICE LYLE'S CHARGE",
        "lyle_open": "Gentlemen of the jury. I will tell you only what was sworn, "
                     "and what was written today.",
        "lyle_none": "Lyle rises. He has nothing written to set before them. He "
                     "says the accused have had no counsel, and sits down.",
        "lyle_spectral": "'You have heard what she saw, and that no one else saw "
                         "it. Thirty women stood before her and she was not "
                         "troubled. You cannot convict on visions.'",
        "lyle_weak": "'You cannot convict on what one girl saw.' He has not shown "
                     "them enough to make it more than an opinion.",
        "lyle_church": "'They come to worship. They took the sacrament. Would "
                       "such women be in league with the Devil?'",
        "ormsby_head": "JUSTICE ORMSBY'S CHARGE",
        "ormsby": ["'Gentlemen. You have heard the girl's afflictions sworn by "
                   "honest neighbours, and a minister of the Gospel.'",
                   "'My brother Lyle has been very busy with knots and dates. A "
                   "servant miscounts. A farmer forgets. That is not a defence.'",
                   "'The law allows you to convict upon this evidence. I think you "
                   "may. You will go out now.'"],
        "ormsby_shaken": "'My brother says she alone saw them. That is the nature "
                         "of such things, gentlemen. Weigh it as you think fit.'",
        "jury": "The jury goes out. It is back before the candles are trimmed.",
        "verdict_head": "THE VERDICT",
        "guilty": "GUILTY",
        "not_guilty": "NOT GUILTY",
        "all_guilty": "All eight are convicted. The jury took less time than "
                      "Margaret Lowry's knots.",
        "some": "Some are acquitted on Justice Lyle's charge. The rest are "
                "convicted, on the same evidence, by the same jury.",
        "none": "All eight are acquitted. Ormsby gathers his papers and does not "
                "look at you. The Mayor is already talking.",
    },

    # trialcheck.py's paths through the day: what each does, in order.
    # ("hear", witness, line) ("press", witness, line)
    # ("present", witness, line, fact) ("down", witness): let them go
    # A witness not named is heard line by line and let go.
    "paths": {
        "the best": {
            "lowry": [("hear", "mantua"), ("hear", "apron"), ("press", "apron"),
                      ("present", "found", "lowry_found"), ("hear", "knots"),
                      ("present", "knots", "knots5"), ("hear", "loosed"),
                      ("hear", "cap"), ("hear", "boyd"), ("press", "boyd")],
            "wylie": [("hear", "apron"), ("hear", "knots"), ("present", "knots", "knots5"),
                      ("hear", "named"), ("press", "named"), ("press", "talk"),
                      ("hear", "knife"), ("press", "knife"), ("hear", "tongue"),
                      ("press", "tongue")],
            "dickey": [("hear", "haunted"), ("press", "haunted"), ("hear", "named"),
                       ("present", "named", "described"), ("hear", "room"),
                       ("press", "room"), ("hear", "fit"), ("hear", "never")],
            "wilson": [("hear", "haunted"), ("present", "haunted", "wilson"),
                       ("hear", "tormented"), ("hear", "friday"), ("press", "friday"),
                       ("press", "yard"), ("hear", "never")],
            "gilmour": [("hear", "fits"), ("hear", "names"), ("press", "names"),
                        ("hear", "moore"), ("present", "moore", "gordon"),
                        ("hear", "thirty"), ("present", "thirty", "thirty"),
                        ("hear", "marks")],
            "gordon": [("hear", "prayed"), ("hear", "came"), ("present", "came", "gordon"),
                       ("hear", "heat"), ("press", "heat"), ("hear", "door"),
                       ("hear", "flock"), ("press", "flock")],
            "ellis": [("hear", "thrice"), ("press", "thrice"), ("hear", "thirty"),
                      ("present", "thirty", "thirty"), ("hear", "erskine"),
                      ("press", "erskine"), ("press", "carter"), ("hear", "ross"),
                      ("press", "ross"), ("hear", "named"),
                      ("present", "named", "described")],
        },
        "a careful first play": {   # presses everything, sees the obvious knots
            "lowry": [("hearall",), ("pressall",), ("present", "knots", "knots5")],
            "wylie": [("hearall",), ("pressall",)],
            "dickey": [("hearall",), ("pressall",), ("present", "never", "never_seen")],
            "wilson": [("hearall",), ("pressall",), ("present", "haunted", "wilson")],
            "gilmour": [("hearall",), ("pressall",), ("present", "thirty", "thirty")],
            "gordon": [("hearall",), ("pressall",)],
            "ellis": [("hearall",), ("pressall",)],
        },
        "listen only": {},
        "the Mayor pushed": {
            "lowry": [("hear", "mantua"), ("present", "mantua", "knots9"),
                      ("present", "mantua", "gordon")],
            "gilmour": [("hearall",), ("present", "thirty", "thirty")],
            "ellis": [("hear", "thrice"), ("hear", "thirty"),
                      ("present", "thirty", "thirty"), ("hear", "erskine"),
                      ("hear", "ross"), ("hear", "named"),
                      ("present", "named", "described"), ("present", "named", "gordon")],
        },
    },
}
