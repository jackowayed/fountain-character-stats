#!/usr/bin/env python3

import collections
import os
import re
import sys

Character = collections.namedtuple("Character", ["lines", "words"])

# State machine
COULD_SEE_CHARACTER = 1
JUST_SAW_CHARACTER = 2
IN_DIALOGUE = 3
CANT_SEE_CHARACTER = 4


DEBUG = os.getenv("DEBUG")
ORDER_OF_APPEARANCE = os.getenv("ORDER_OF_APPEARANCE")

def is_character_name(line):
    if line and line[0] == "@":
        return True
    # Once you strip whitespace, a character is:
    # 1 or more ALLCAPS words, optionally followed by
    # a parenthetical that can have basically whatever in it.
    # TODO support the parentheticals (\([\w\./-']+\))?
    return re.search(r"^[A-Z\d]+( [A-Z\d]+)*$", line)

def is_dialogue_line(line):
    return line.strip() or len(line) > 2

def count_words(line):
    return len(line.split())

def debug_print(*args):
    if DEBUG:
        print(*args)


def parse(filename):
    characters = collections.defaultdict(lambda: Character(0, 0))
    state = COULD_SEE_CHARACTER
    current_character = None
    characters_in_order = []
    with open(filename) as f:
        for line in f:
            cleaned = line.strip()
            if state == COULD_SEE_CHARACTER:
                if is_character_name(cleaned):
                    current_character = cleaned[1:] if cleaned[0] == "@" else cleaned
                    current_character = current_character.upper()
                    state = JUST_SAW_CHARACTER
                    characters_in_order.append(current_character)
            elif state == JUST_SAW_CHARACTER:
                if is_dialogue_line(line):
                    c = characters[current_character]
                    characters[current_character] = Character(c.lines + 1, c.words + count_words(cleaned))
                    state = IN_DIALOGUE
                    debug_print("<<<START", current_character)
                elif not cleaned:
                    # The line is blank, so the next line could be a character name
                    state = COULD_SEE_CHARACTER
                else:
                    # The line isn't blank, so the next line can't be a character name
                    state = CANT_SEE_CHARACTER
            elif state == IN_DIALOGUE:
                if is_dialogue_line(line):
                    c = characters[current_character]
                    characters[current_character] = Character(c.lines, c.words + count_words(cleaned))
                else:
                    assert not cleaned
                    state = COULD_SEE_CHARACTER
                    debug_print(">>>END", current_character)
            elif state == CANT_SEE_CHARACTER:
                if not cleaned:
                    state = COULD_SEE_CHARACTER
            debug_print(cleaned)
    if ORDER_OF_APPEARANCE:
        return characters_in_order
    return characters


if __name__ == '__main__':
    if ORDER_OF_APPEARANCE:
        s = set()
        for c in parse(sys.argv[1]):
            if c not in s:
                s.add(c)
                print(c)
        exit()
    for charname, stats in sorted(iter(parse(sys.argv[1]).items()), key=lambda kv: kv[1].words, reverse=True):
        print("%s\t%s\t%s" % (charname, stats.words, stats.lines))
                    
