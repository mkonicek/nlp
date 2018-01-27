from typing import List
from vectors import Vector

class Word:
    """A single word (one line of the input file)"""

    def __init__(self, text: str, vector: Vector, frequency: int) -> None:
        self.text = text
        self.vector = vector
        self.frequency = frequency

    def __repr__(self) -> str:
        vector_preview = ', '.join(map(str, self.vector[:2]))
        return f"{self.text} [{vector_preview}, ...]"
