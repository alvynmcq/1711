#!/usr/bin/env python3
"""The title, the prologue and the credits.

The prologue is adapted from THE ISLANDMAGEE WITCHES (1822), in Andrew
Sneddon and Shannon Devlin (eds), 'Documents from the Trial of the
"Islandmagee Witches" at Carrickfergus Assizes, County Antrim, Ireland,
1711' (w1711.org, CC BY 4.0). The events, dates and much of the dialogue
follow that account; every person's name has been changed. The clerk only
arrives on 3 March, so the prologue is told as hearsay: what the household
says or swears, never as fact:

  Ann Haltridge -> Agnes Wylie     Knowehead House -> Braehead House
  Margaret Spear -> Meg Lowry      Mary Dunbar -> Isobel Halliday
  Robert Sinclair -> Mr Gordon     Edward Clements -> Mayor Ellis
"""
from script import BLK, YEL, BYEL, WHT, BWHT, RED, BRED, CYN

VERSION = "v0.5 slice"

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
    ("story", YEL, "So the household tells it. Agnes Wylie, the old minister's "
                   "widow, sat at her son's kitchen fire, and small stones struck "
                   "her back and shoulders. She said there was no one there to "
                   "throw them."),
    ("wait",),
    ("story", YEL, "At night, she said, something pulled the blankets from her "
                   "bed and walked across her as she lay. The servant, Meg "
                   "Lowry, says that when a candle was lit there was nothing to "
                   "be seen, and when it went out it began again."),
    ("wait",),
    ("pic", "window"),
    ("story", WHT, "11 December. Meg says a boy came in at dusk and sat by the "
                   "old woman at the fire: an old black bonnet, a torn blanket "
                   "trailing behind him. He kept his face covered and would not "
                   "speak."),
    ("story", YEL, "She says he danced about the kitchen, and then was gone."),
    ("wait",),
    ("story", WHT, "February 1711. The old woman's book of sermons went missing. "
                   "Meg swears that next day the boy broke a pane of the kitchen "
                   "window and pushed his arm through, holding the book open, "
                   "and that these were the words:"),
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
    ("story", WHT, "Then, Meg says, she saw him out at the gable end, digging "
                   "with a sword."),
    ("say", "MEG", "What are you doing?"),
    ("say", "BOY", "Making a grave."),
    ("say", "MEG", "For whom?"),
    ("say", "BOY", "For a corpse which will come out of this house very "
                   "soon."),
    ("wait",),
    ("cls", YEL),
    ("story", YEL, "The household says that for eight days the bedclothes were "
                   "lifted from the old woman's bed and laid out in the shape of "
                   "a corpse, and never while anyone was in the room."),
    ("story", YEL, "Mr Gordon the minister sat up with two of his elders, "
                   "praying. At midnight, they say, Agnes cried out that "
                   "something had been stuck into her back like a knife."),
    ("story", BWHT, "On the 22nd of February 1711, at noon, she died."),
    ("wait",),
    ("story", YEL, "On the 27th her niece Isobel Halliday came to Braehead: "
                   "eighteen, well bred, a stranger to Islandmagee."),
    ("story", YEL, "That night, the house says, an apron that had been locked "
                   "away was found on the parlour floor, knotted tight, and "
                   "Isobel untied the knots."),
    ("story", YEL, "Soon after, they say, she fell on the stairs, crying out "
                   "that a knife was in her thigh."),
    ("wait",),
    ("story", YEL, "Within days she had named her tormentors, women she said "
                   "she had never seen. They were sent for, one by one."),
    ("story", YEL, "On the 3rd of March, Mayor Ellis of Carrickfergus rides out "
                   "to take sworn statements."),
    ("story", BWHT, "He brings his clerk. You."),
    ("wait",),
    ("story", YEL, "You saw none of what came before. You have only what the "
                   "household says. Now they will swear to it, and you will "
                   "write it down."),
    ("wait",),
    ("text", 9, 9, BYEL, "N I G H T    O N E"),
    ("text", 11, 10, WHT, "3rd March 1711"),
    ("text", 15, 2, YEL, "Mayor Ellis sits in the parlour. One by"),
    ("text", 16, 2, YEL, "one they come in and swear, and you"),
    ("text", 17, 2, YEL, "write down what they say."),
    ("text", 19, 2, BWHT, "You have one candle for the night."),
    ("wait",),
    ("night",),
    ("cls", WHT),
    ("story", YEL, "Night One ends. Mayor Ellis takes the book with him to "
                   "Carrickfergus. This build goes no further: the next nights "
                   "are still to come."),
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
    ("text", 12, 1, YEL, "Dates and order compressed: some lines"),
    ("text", 13, 1, YEL, "were sworn later, or come from accounts"),
    ("text", 14, 1, YEL, "of the trial."),
    ("text", 16, 1, WHT, "The people in this game are fictional."),
    ("text", 17, 1, WHT, "Nine real people were convicted of"),
    ("text", 18, 1, WHT, "witchcraft at Carrickfergus in 1711."),
    ("text", 19, 1, WHT, "Their story: w1711.org"),
    ("text", 21, 1, WHT, "ZX0: Einar Saukas."),
    ("wait",),
    ("jump", "title"),
]

SCRIPTS = [("title", TITLE), ("prologue_start", PROLOGUE), ("credits_start", CREDITS)]
PICS = ["house", "window", "grave"]
