#!/usr/bin/env python3
"""The title, the prologue and the credits.

The prologue is adapted from THE ISLANDMAGEE WITCHES (1822), in Andrew
Sneddon and Shannon Devlin (eds), 'Documents from the Trial of the
"Islandmagee Witches" at Carrickfergus Assizes, County Antrim, Ireland,
1711' (w1711.org, CC BY 4.0). The events, dates and much of the dialogue
follow that account; every person's name has been changed:

  Ann Haltridge -> Agnes Wylie     Knowehead House -> Braehead House
  Margaret Spear -> Meg Lowry      Mary Dunbar -> Isobel Halliday
  Robert Sinclair -> Mr Gordon     Edward Clements -> Mayor Ellis
"""
from script import BLK, YEL, BYEL, WHT, BWHT, RED, BRED, CYN

VERSION = "v0.2 slice"

TITLE = [
    ("cls", WHT),
    ("border", 0),
    ("text", 4, 12, BYEL, "1  7  1  1"),
    ("text", 7, 6, WHT, "Islandmagee, County Antrim"),
    ("text", 9, 3, YEL, "Being a true account of strange"),
    ("text", 10, 3, YEL, "events, as taken down by the clerk."),
    ("text", 16, 7, BWHT, "SPACE  Begin"),
    ("text", 17, 7, WHT, "C      Credits"),
    ("text", 22, 1, WHT, VERSION),
    ("choice", [(" ", "prologue"), ("C", "credits")]),
]

PROLOGUE = [
    ("label", "prologue"),
    ("pic", "house"),
    ("story", WHT, "Islandmagee, County Antrim. September 1710."),
    ("story", YEL, "Agnes Wylie, the old minister's widow, sits at her son's "
                   "kitchen fire. Small stones strike her back and shoulders. "
                   "There is no one there to throw them."),
    ("wait",),
    ("story", YEL, "At night something pulls the blankets from her bed, and she "
                   "feels it walk across her as she lies. The doors are shut. "
                   "When the girl lights a candle there is nothing. When the "
                   "candle goes out, it begins again."),
    ("wait",),
    ("pic", "window"),
    ("story", WHT, "11 December. At dusk a boy comes in and sits by her at the "
                   "fire: an old black bonnet, a torn blanket trailing behind "
                   "him. He keeps his face covered. He will not speak."),
    ("story", YEL, "He dances, leaping higher than a boy should, and is gone."),
    ("wait",),
    ("story", WHT, "February 1711. Her book of sermons goes missing. Next day "
                   "the boy breaks a pane of the kitchen window and pushes his "
                   "arm through, holding the book open."),
    ("wait",),
    ("say", "BOY", "Do you want a book?"),
    ("say", "MEG", "No."),
    ("say", "BOY", "How came you to lie? For this is the book the old "
                   "gentlewoman wanted yesterday."),
    ("say", "MEG", "Can you read it?"),
    ("say", "BOY", "Yes."),
    ("wait",),
    ("say", "MEG", "Who taught you?"),
    ("say", "BOY", "The Devil taught me."),
    ("say", "MEG", "The Lord bless me from thee! Thou hast got ill lear."),
    ("say", "BOY", "Aye, bless yourself twenty times, but that shall not "
                   "save you."),
    ("wait",),
    ("pic", "grave"),
    ("story", WHT, "Through the broken window Meg sees him at the gable end, "
                   "digging with a sword."),
    ("say", "MEG", "What are you doing?"),
    ("say", "BOY", "Making a grave."),
    ("say", "MEG", "For whom?"),
    ("say", "BOY", "For a corpse which will come out of this house very "
                   "soon."),
    ("wait",),
    ("cls", YEL),
    ("story", YEL, "For eight days the bedclothes are lifted from the old "
                   "woman's bed and laid out in the shape of a corpse. "
                   "Never while anyone is in the room."),
    ("story", YEL, "Mr Gordon the minister sits up with two of his elders, "
                   "praying. At midnight Agnes cries out. Something has been "
                   "stuck into her back like a knife."),
    ("story", BWHT, "On the 22nd of February 1711, at noon, she dies."),
    ("wait",),
    ("story", YEL, "On the 27th her niece Isobel Halliday comes to Braehead: "
                   "eighteen, well bred, a stranger to Islandmagee."),
    ("story", YEL, "That night an apron that was locked away two days before "
                   "is found on the parlour floor, knotted tight. Nobody will "
                   "touch it. Isobel unties the knots."),
    ("story", YEL, "Next morning, on the stairs, she falls, crying out that a "
                   "knife is in her thigh."),
    ("wait",),
    ("story", YEL, "Within days she has named her tormentors, women she says "
                   "she has never seen. They are sent for, one by one."),
    ("story", YEL, "On the 3rd of March, Mayor Ellis of Carrickfergus rides out "
                   "to take sworn statements."),
    ("story", BWHT, "He brings his clerk. You."),
    ("wait",),
    ("text", 9, 9, BYEL, "N I G H T    O N E"),
    ("text", 11, 10, WHT, "3rd March 1711"),
    ("text", 15, 2, YEL, "Mayor Ellis sits in the parlour. One by"),
    ("text", 16, 2, YEL, "one they come in and swear, and you"),
    ("text", 17, 2, YEL, "write down what they say."),
    ("wait",),
    ("night",),
    ("cls", WHT),
    ("story", YEL, "The rest of Night One is not in this build yet. Next: "
                   "Kate Rankin is sent for, and you are to arrange how she "
                   "is brought before Isobel."),
    ("wait",),
    ("jump", "credits"),
]

CREDITS = [
    ("label", "credits"),
    ("cls", WHT),
    ("text", 1, 1, BYEL, "1711   " + VERSION),
    ("text", 3, 1, WHT, "Idea, design and direction: alvynmcq"),
    ("text", 4, 1, WHT, "Code, art and text made with AI"),
    ("text", 5, 1, WHT, "assistance (Claude)."),
    ("text", 7, 1, YEL, "Adapted from 'Documents from the Trial"),
    ("text", 8, 1, YEL, "of the Islandmagee Witches', 1711,"),
    ("text", 9, 1, YEL, "ed. Andrew Sneddon & Shannon Devlin,"),
    ("text", 10, 1, YEL, "w1711.org, licensed CC BY 4.0."),
    ("text", 11, 1, YEL, "Changes: names, wording, order."),
    ("text", 13, 1, WHT, "The people in this game are fictional."),
    ("text", 14, 1, WHT, "Nine real people were convicted of"),
    ("text", 15, 1, WHT, "witchcraft at Carrickfergus in 1711."),
    ("text", 16, 1, WHT, "Their story: w1711.org"),
    ("text", 18, 1, WHT, "ZX0: Einar Saukas."),
    ("wait",),
    ("jump", "title"),
]

SCRIPTS = [("title", TITLE), ("prologue_start", PROLOGUE), ("credits_start", CREDITS)]
PICS = ["house", "window", "grave"]
