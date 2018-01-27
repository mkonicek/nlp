"""
Load the input file (see https://fasttext.cc/docs/en/english-vectors.html)
and do some cleanup.
"""

from typing import Iterable, List, Set

from itertools import groupby
from operator import itemgetter
import re
import vectors as v
from word import Word

def load_words(file_path: str) -> List[Word]:
    """Load and cleanup the data."""
    print(f"Loading {file_path}...")
    words = load_words_raw(file_path)
    print(f"Loaded {len(words)} words.")

    #num_dimensions = most_common_dimension(words)
    words = [w for w in words if len(w.vector) == 300]
    #print(f"Using {num_dimensions}-dimensional vectors, {len(words)} remain.")

    words = remove_stop_words(words)
    print(f"Removed stop words, {len(words)} remain.")

    words = remove_duplicates(words)
    print(f"Removed duplicates, {len(words)} remain.")

    return words

def load_words_raw(file_path: str) -> List[Word]:
    """Load the file as-is, without doing any validation or cleanup."""
    def parse_line(line: str, frequency: int) -> Word:
        tokens = line.split()
        word = tokens[0]
        vector = v.normalize([float(x) for x in tokens[1:]])
        return Word(word, vector, frequency)

    words = []
    # Words are sorted from the most common to the least common ones
    frequency = 1
    with open(file_path) as f:
        for line in f:
            w = parse_line(line, frequency)
            words.append(w)
            frequency += 1
    return words

def iter_len(iter: Iterable[complex]) -> int:
    return sum(1 for _ in iter)

def most_common_dimension(words: List[Word]) -> int:
    """
    There is a line in the input file which is missing a word
    (search -0.0739, -0.135, 0.0584).
    """
    lengths = sorted([len(word.vector) for word in words])
    dimensions = [(k, iter_len(v)) for k, v in groupby(lengths)]
    print("Dimensions:")
    for (dim, num_vectors) in dimensions:
        print(f"{num_vectors} {dim}-dimensional vectors")
    most_common = sorted(dimensions, key=lambda t: t[1], reverse=True)[0]
    return most_common[0]

# We want to ignore these characters,
# so that e.g. "U.S.", "U.S", "US_" and "US" are the same word.
ignore_char_regex = re.compile("[\W_]")

# Has to start and end with an alphanumeric character
is_valid_word = re.compile("^[^\W_].*[^\W_]$")

def remove_duplicates(words: List[Word]) -> List[Word]:
    seen_words: Set[str] = set()
    unique_words: List[Word] = []
    for w in words:
        canonical = ignore_char_regex.sub("", w.text)
        if not canonical in seen_words:
            seen_words.add(canonical)
            # Keep the original ordering
            unique_words.append(w)
    return unique_words

def remove_stop_words(words: List[Word]) -> List[Word]:
    return [w for w in words if (
        len(w.text) > 1 and is_valid_word.match(w.text))]

# Run "smoke tests" on import
assert [w.text for w in remove_stop_words([
    Word('a', [], 1),
    Word('ab', [], 1),
    Word('-ab', [], 1),
    Word('ab_', [], 1),
    Word('a.', [], 1),
    Word('.a', [], 1),
    Word('ab', [], 1),
])] == ['ab', 'ab']
assert [w.text for w in remove_duplicates([
    Word('a.b', [], 1),
    Word('-a-b', [], 1),
    Word('ab_+', [], 1),
    Word('.abc...', [], 1),
])] == ['a.b', '.abc...']
