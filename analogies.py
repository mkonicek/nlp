from typing import List, Tuple

from load import load_words
from vectors import Vector, add, sub, cosine_similarity_normalized
from word import Word, find_word

WORDS_FILE_NAME = 'data/words.vec'


def related_words(base_vector: Vector, words: List[Word]) -> List[Tuple[float, Word]]:
    words_with_distance = [(cosine_similarity_normalized(
        base_vector, w.vector), w) for w in words]
    # We want cosine similarity to be as large as possible (close to 1)
    sorted_by_distance = sorted(
        words_with_distance, key=lambda t: t[0], reverse=True)
    return sorted_by_distance


def closest_analogies(
    left2: str, left1: str, right2: str, words: List[Word]
) -> List[Tuple[float, Word]]:
    word_left1 = find_word(left1, words)
    if not word_left1:
        print(f"Unknown word: {left1}")
        return []

    word_left2 = find_word(left2, words)
    if not word_left2:
        print(f"Unknown word: {left2}")
        return []

    word_right2 = find_word(right2, words)
    if not word_right2:
        print(f"Unknown word: {right2}")
        return []

    vector = add(sub(word_left1.vector, word_left2.vector), word_right2.vector)
    closest_list = related_words(vector, words)[:10]

    def is_redundant(word: str) -> bool:
        # Sometimes the two left vectors are so close the answer is e.g.
        # "shirt-clothing is like phone-phones". Skip 'phones' and get the next
        # suggestion, which might be more interesting.
        word_lower = word.lower()
        return (
            left1.lower() in word_lower or
            left2.lower() in word_lower or
            right2.lower() in word_lower)
    closest_filtered = [(dist, w)
                        for (dist, w) in closest_list if not is_redundant(w.text)]
    return closest_filtered


def print_analogy(left2: str, left1: str, right2: str, words: List[Word]) -> None:
    analogies = closest_analogies(left2, left1, right2, words)
    if (len(analogies) == 0):
        print(f"{left2}-{left1} is like {right2}-?")
    else:
        (_, w) = analogies[0]
        # alternatives = ', '.join(
        #    [f"{w.text} ({dist:.2f})" for (dist, w) in analogies])
        print(f"{left2}-{left1} is like {right2}-{w.text}")


words = load_words(WORDS_FILE_NAME)
print("")

while True:
    left2 = input("Type a word: ")
    left1 = input("Type a word: ")
    right2 = input("Type a word: ")
    print_analogy(left2, left1, right2, words)
    print("")
