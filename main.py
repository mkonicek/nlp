import math

from load import load_words
from word import Word, Vector
from operator import itemgetter
from typing import Any, Iterable, List, Set

def vector_len(v: Vector) -> float:
    return math.sqrt(sum([x*x for x in v]))

def dot_product(v1: Vector, v2: Vector) -> float:
    assert len(v1) == len(v2)
    return sum([x*y for (x,y) in zip(v1, v2)])

def cosine_similarity(v1: Vector, v2: Vector) -> float:
    """
    Returns the cosine of the angle between the two vectors.
    Results range from -1 (very different) to 1 (very similar).
    """
    return dot_product(v1, v2) / float(vector_len(v1) * vector_len(v2))

def n_most_similar(base_word: Word, words: List[Word], n: int) -> List[Word]:
    """Finds n words with smallest cosine similarity to a given word"""
    distances = [(cosine_similarity(base_word.vector, w.vector), w) for w in words if w.word != base_word.word]
    # We want cosine similarity to be as large as possible (close to 1)
    sorted_by_distance = sorted(distances, key=itemgetter(0), reverse=True)
    return [word for (dist, word) in sorted_by_distance[:n]]

def print_most_similar(base_word: Word) -> None:
    print(f"Words related to {base_word.word}:")
    print(', '.join([word.word for word in n_most_similar(base_word, words, 20)]))

def read_word() -> str:
    return input("Type a word: ")

def find_word(text: str, words: List[Word]) -> Word:
    matching_words = [w for w in words if text == w.word]
    if (len(matching_words) == 0):
        return None
    else:
        return matching_words[0]

# Smoke tests
assert vector_len([3, 4]) == 5
assert dot_product([2, 3], [-1, 7]) == 19

words = load_words('data/words.vec')

#print_most_similar(words[50])
#print_most_similar(words[120])
#print_most_similar(words[1120])
#print_most_similar(words[4220])
#print_most_similar(words[5620])

while True:
    text = read_word()
    w = find_word(text, words)
    if not w:
        print("Sorry, I don't know that word.")
    else:
        print_most_similar(w)
