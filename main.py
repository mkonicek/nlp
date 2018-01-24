import math

from load import load_words
from word import Word, Vector
from operator import itemgetter
from typing import Any, Iterable, List, Set, Tuple

def vector_len(v: Vector) -> float:
    return math.sqrt(sum([x*x for x in v]))

def dot_product(v1: Vector, v2: Vector) -> float:
    assert len(v1) == len(v2)
    return sum([x*y for (x,y) in zip(v1, v2)])

def add_vectors(v1: Vector, v2: Vector) -> Vector:
    assert len(v1) == len(v2)
    return [x + y for (x,y) in zip(v1, v2)]

def sub_vectors(v1: Vector, v2: Vector) -> Vector:
    assert len(v1) == len(v2)
    return [x - y for (x,y) in zip(v1, v2)]

def cosine_similarity(v1: Vector, v2: Vector) -> float:
    """
    Returns the cosine of the angle between the two vectors.
    Results range from -1 (very different) to 1 (very similar).
    """
    return dot_product(v1, v2) / float(vector_len(v1) * vector_len(v2))

def most_similar(base_vector: Vector, words: List[Word]) -> List[Tuple[float, Word]]:
    """Finds n words with smallest cosine similarity to a given word"""
    words_with_distance = [(cosine_similarity(base_vector, w.vector), w) for w in words]
    # We want cosine similarity to be as large as possible (close to 1)
    sorted_by_distance = sorted(words_with_distance, key=lambda t: t[0], reverse=True)
    return sorted_by_distance

def print_most_similar(words: List[Word], text: str) -> None:
    base_word = find_word(text, words)
    print(f"Words related to {base_word.word}:")
    sorted_by_distance = [
        word.word for (dist, word) in
            most_similar(base_word.vector, words)
            if word.word.lower() != base_word.word.lower()
        ]
    print(', '.join(sorted_by_distance[:10]))

def read_word() -> str:
    return input("Type a word: ")

def find_word(text: str, words: List[Word]) -> Word:
    return next(w for w in words if text == w.word)

def closest_analogies(left2: str, left1: str, right2: str, words: List[Word]) -> List[Tuple[float, Word]]:
    word_left1 = find_word(left1, words)
    word_left2 = find_word(left2, words)
    word_right2 = find_word(right2, words)
    vector = add_vectors(sub_vectors(word_left1.vector, word_left2.vector), word_right2.vector)
    closest = most_similar(vector, words)[:8]
    def is_redundant(word: str) -> bool:
        """
        Sometimes the two left vectors are so close the answer is e.g.
        "shirt-clothing is like phone-phones". Skip 'phones' and get the next
        suggestion, which might be more interesting.
        """
        word_lower = word.lower()
        return left1.lower() in word_lower or left2.lower() in word_lower or right2.lower() in word_lower
    closest_filtered = [(dist, w) for (dist, w) in closest if not is_redundant(w.word)]
    return closest_filtered

def print_analogy(left2: str, left1: str, right2: str, words: List[Word]) -> None:
    analogies = closest_analogies(left2, left1, right2, words)
    if (len(analogies) == 0):
        print(f"{left2}-{left1} is like {right2}-?")
    else:
        (dist, w) = analogies[0]
        print(f"{left2}-{left1} is like {right2}-{w.word}")

words = load_words('data/words.vec')

# print_most_similar(words, 'school')
# print_most_similar(words, 'apple')
# print_most_similar(words, 'spain')
# print_most_similar(words, words[150].word)
# print_most_similar(words, words[1150].word)
# print_most_similar(words, words[2150].word)
# print_most_similar(words, words[3150].word)
# print_most_similar(words, words[4150].word)

print_analogy('Paris', 'France', 'Rome', words)
print_analogy('shirt', 'clothing', 'bowl', words)  # Bad
print_analogy('shirt', 'clothing', 'phone', words)  # Bad
print_analogy('friend', 'smile', 'enemy', words)  # Bad
print_analogy('sushi', 'fish', 'haggis', words) # Bad
print_analogy('sushi', 'fish', 'pizza', words) # Bad
print_analogy('dog', 'mammal', 'eagle', words) # Bad
print_analogy('mouse', 'mammal', 'tuna', words) # Bad
print_analogy('book', 'reading' , 'tv', words)  # Bad
print_analogy('Frances', 'girl', 'Martin', words)
print_analogy('man', 'king', 'woman', words)
print_analogy('UK', 'London', 'Thailand', words)
print_analogy('English', 'Jaguar', 'German', words)
print_analogy('English', 'Vauxhall', 'German', words)
print_analogy('German', 'BMW' , 'American', words)
print_analogy('German', 'Opel', 'American', words)
print_analogy('BMW', 'German' , 'Chrysler', words)
print_analogy('Sushi', 'Japan' , 'Haggis', words)

while False:
    word1 = find_word(read_word(), words)
    if not word1:
        print("Sorry, I don't know that word.")
        continue
    word2 = find_word(read_word(), words)
    if not word2:
        print("Sorry, I don't know that word.")
        continue
    word3 = find_word(read_word(), words)
    if not word3:
        print("Sorry, I don't know that word.")
        continue
    vector = add_vectors(sub_vectors(word1.vector, word2.vector), word3.vector)
    print_analogy(word1, word2, word3, words)

while False:
    text = read_word()
    w = find_word(text, words)
    if not w:
        print("Sorry, I don't know that word.")
    else:
        print_most_similar(w)
