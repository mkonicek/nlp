from typing import List, Optional

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


def find_word(text: str, words: List[Word]) -> Optional[Word]:
    try:
        return next(w for w in words if text == w.text)
    except StopIteration:
        return None
