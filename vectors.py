import math

from itertools import groupby
from operator import itemgetter
import re
from typing import Any, Iterable, List, Set

Vector = List[float]

class Word:
    def __init__(self, word: str, vector: Vector, frequency: int) -> None:
        self.word = word
        self.vector = vector
        self.frequency = frequency

    def __repr__(self) -> str:
        vector_preview = ', '.join(map(str, self.vector[:2]))
        return f"{self.word} [{vector_preview}, ...]"

def vector_len(v: Vector) -> float:
    return math.sqrt(sum([x*x for x in v]))

def dot_product(v1: Vector, v2: Vector) -> float:
    assert len(v1) == len(v2)
    return sum([x*y for (x,y) in zip(v1, v2)])

def cosine_similarity(v1: Vector, v2: Vector) -> float:
    """
    Returns the cosine of the angle between the two vectors.
    Results range from -1 (totally different) to 1 (very similar).
    """
    return dot_product(v1, v2) / float(vector_len(v1) * vector_len(v2))

def n_most_similar(base_word: Word, words: List[Word], n: int) -> List[Word]:
    """Finds n words with smallest cosine similarity to a given word"""
    distances = [(cosine_similarity(base_word.vector, w.vector), w) for w in words]
    # We want cosine similarity to be as large as possible (close to 1)
    sorted_by_distance = sorted(distances, key=itemgetter(0), reverse=True)
    return [word for (dist, word) in sorted_by_distance[:n]]

def print_most_similar(words: List[Word], index: int) -> None:
    base_word = words[index]
    print("")
    print(f"Words related to {base_word.word}:")
    print(', '.join([word.word for word in n_most_similar(base_word, words, 12)]))

def load_words(file_path: str) -> List[Word]:
    def parse_line(line: str, frequency: int) -> Word:
        tokens = line.split()
        word = tokens[0].lower()
        vector = [float(x) for x in tokens[1:]]
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
    most_common = sorted(dimensions, key=itemgetter(1), reverse=True)[0]
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
        canonical = ignore_char_regex.sub("", w.word)
        if not canonical in seen_words:
            seen_words.add(canonical)
            # Keep the original ordering
            unique_words.append(w)
    return unique_words

def remove_stop_words(words: List[Word]) -> List[Word]:
    return [w for w in words if (
        len(w.word) > 1 and is_valid_word.match(w.word))]

# "Unit tests"
assert vector_len([3, 4]) == 5
assert dot_product([2, 3], [-1, 7]) == 19
assert [w.word for w in remove_stop_words([
    Word('a', [], 1),
    Word('ab', [], 1),
    Word('-ab', [], 1),
    Word('ab_', [], 1),
    Word('a.', [], 1),
    Word('.a', [], 1),
    Word('ab', [], 1),
])] == ['ab', 'ab']
assert [w.word for w in remove_duplicates([
    Word('a.b', [], 1),
    Word('-a-b', [], 1),
    Word('ab_+', [], 1),
    Word('.abc...', [], 1),
])] == ['a.b', '.abc...']

# Preview of loaded data
file_path = 'words.vec'
print(f"Loading {file_path}...")
words = load_words(file_path)
print(f"Loaded {len(words)} words.")

num_dimensions = most_common_dimension(words)
words = [w for w in words if len(w.vector) == num_dimensions]
print(f"Using {num_dimensions}-dimensional vectors, {len(words)} remain.")

words = remove_stop_words(words)
print(f"Removed stop words, {len(words)} remain.")

words = remove_duplicates(words)
print(f"Removed duplicates, {len(words)} remain.")

print_most_similar(words, 50)
print_most_similar(words, 120)
print_most_similar(words, 1120)
print_most_similar(words, 4220)
print_most_similar(words, 5620)
