from typing import List, Tuple

from load import load_words
from vectors import Vector, cosine_similarity_normalized
from word import Word, find_word

WORDS_FILE_NAME = 'data/words.vec'


def related_words(base_vector: Vector, words: List[Word]) -> List[Tuple[float, Word]]:
    words_with_distance = [(cosine_similarity_normalized(
        base_vector, w.vector), w) for w in words]
    # We want cosine similarity to be as large as possible (close to 1)
    sorted_by_distance = sorted(
        words_with_distance, key=lambda t: t[0], reverse=True)
    return sorted_by_distance


def print_related_words(words: List[Word], text: str) -> None:
    base_word = find_word(text, words)
    if not base_word:
        print(f"Unknown word: {text}")
        return
    related_words_list = related_words(base_word.vector, words)
    sorted_by_distance = [
        word.text for (_, word) in
        related_words_list
        if word.text.lower() != base_word.text.lower()
    ]
    print(', '.join(sorted_by_distance[:10]))


words = load_words(WORDS_FILE_NAME)
print("")

while True:
    text = input("Words related to: ")
    print_related_words(words, text)
    print("")
