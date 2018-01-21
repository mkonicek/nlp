from typing import List

Vector = List[float]

class Word:
    """A single word (one line of the input file)"""

    def __init__(self, word: str, vector: Vector, frequency: int) -> None:
        self.word = word
        self.vector = vector
        self.frequency = frequency

    def __repr__(self) -> str:
        vector_preview = ', '.join(map(str, self.vector[:2]))
        return f"{self.word} [{vector_preview}, ...]"
