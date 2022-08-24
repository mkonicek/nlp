# Load the input file and do some cleanup.

from typing import List, Set

import re
from vectors import normalize
from word import Word


def load_words(file_path: str) -> List[Word]:
    print(f"Loading {file_path}...")

    def parse_line(line: str, frequency: int) -> Word:
        tokens = line.split()
        word = tokens[0]
        vector = normalize([float(x) for x in tokens[1:]])
        return Word(word, vector, frequency)

    words = []
    # Words are sorted from the most common to the least common ones
    frequency = 1
    with open(file_path) as f:
        for line in f:
            w = parse_line(line, frequency)
            words.append(w)
            frequency += 1

    words = [w for w in words if len(w.vector) == 300]
    print(f"Loaded {len(words)} words.")

    words = remove_stop_words(words)
    print(f"Removed stop words, {len(words)} remain.")

    words = remove_duplicates(words)
    print(f"Removed duplicates, {len(words)} remain.")

    return words


# We want to ignore these characters,
# so that e.g. "U.S.", "U.S", "US_" and "US" are the same word.
IGNORE_CHAR_REGEX = re.compile("[\W_]")


def remove_duplicates(words: List[Word]) -> List[Word]:
    seen_words: Set[str] = set()
    unique_words: List[Word] = []
    for w in words:
        canonical = IGNORE_CHAR_REGEX.sub("", w.text)
        if not canonical in seen_words:
            seen_words.add(canonical)
            # Keep the original ordering
            unique_words.append(w)
    return unique_words


# Has to start and end with an alphanumeric character
VALID_WORD_REGEX = re.compile("^[^\W_].*[^\W_]$")


def remove_stop_words(words: List[Word]) -> List[Word]:
    return [w for w in words if (
        len(w.text) > 1 and VALID_WORD_REGEX.match(w.text))]
