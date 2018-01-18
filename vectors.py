import math
from typing import Iterator, List

Vector = List[float]

class Word:
    def __init__(self, word: str, vector: Vector) -> None:
        self.word = word
        self.vector = vector

    def __repr__(self) -> str:
        vector_preview = ', '.join(map(str, self.vector[:2]))
        return f"{self.word} [{vector_preview}, ...]"

def vector_len(v: Vector) -> float:
    return math.sqrt(sum([x*x for x in v]))

def dot_product(v1: Vector, v2: Vector) -> float:
    assert len(v1) == len(v2)
    return sum([x*y for (x,y) in zip(v1, v2)])

def cosine_similarity(v1: Vector, v2: Vector) -> float:
    """Returns the cosine of the angle between the two vectors."""
    return dot_product(v1, v2) / (vector_len(v1) * vector_len(v2))

def load_words(file_name: str) -> List[Word]:
    return [
        Word('cat', [-0.3, 1.12, 3.1]),
        Word('dog', [0.3, -0.6, -0.4])
    ]

print(vector_len([3, 4]))

print(dot_product([2, 3], [-1, 7]))

print(load_words('words-short.vec'))
