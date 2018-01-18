import math

from itertools import groupby
from operator import itemgetter
from typing import Any, Iterable, List

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
    return [word.word for (dist, word) in sorted_by_distance[:n]]

def print_most_similar(words: List[Word], index: int) -> None:
    base_word = words[index]
    print(f"Most similar words to {base_word.word}:")
    print(n_most_similar(base_word, words, 10))

def load_words(file_path: str) -> List[Word]:
    def parse_line(line: str, frequency: int) -> Word:
        tokens = line.split()
        word = tokens[0]
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

    print(f"Loaded {len(words)} vectors")
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

# "Unit tests"
assert vector_len([3, 4]) == 5
assert dot_product([2, 3], [-1, 7]) == 19

# Preview of loaded data
words = load_words('words.vec')
num_dimensions = most_common_dimension(words)
print(f"Using {num_dimensions}-dimensional vectors")
words = [w for w in words if len(w.vector) == num_dimensions and len(w.word) > 1]
words = remove_case_duplicates(words)
print("Preview:")
print(words[:5])

print_most_similar(words, 1000)
print_most_similar(words, 1200)
print_most_similar(words, 1230)
print_most_similar(words, 2500)
print_most_similar(words, 3100)
print_most_similar(words, 3200)
print_most_similar(words, 3300)
print_most_similar(words, 3400)
