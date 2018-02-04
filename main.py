from typing import Any, Iterable, List, Optional, Set, Tuple

from load import load_words
import math
import time
import vectors as v
from vectors import Vector
from word import Word

# Timing for most_similar (100k words):
# Original version: 7.3s per call
# Normalized vectors: 3.4s per call
# Numpy: 0.27s per call (12x speedup), 300MB memory total

def most_similar(base_vector: Vector, words: List[Word]) -> List[Tuple[float, Word]]:
    start = time.time()
    """Finds n words with smallest cosine similarity to a given word"""
    words_with_distance = [(v.cosine_similarity_normalized(base_vector, w.vector), w) for w in words]
    # We want cosine similarity to be as large as possible (close to 1)
    sorted_by_distance = sorted(words_with_distance, key=lambda t: t[0], reverse=True)
    print(f"Elapsed {time.time() - start} s")
    return sorted_by_distance

def print_most_similar(words: List[Word], text: str) -> None:
    base_word = find_word(text, words)
    if not base_word:
        print(f"Uknown word: {text}")
        return
    print(f"Words related to {base_word.text}:")
    sorted_by_distance = [
        word.text for (dist, word) in
            most_similar(base_word.vector, words)
            if word.text.lower() != base_word.text.lower()
        ]
    print(', '.join(sorted_by_distance[:10]))

def read_word() -> str:
    return input("Type a word: ")

def find_word(text: str, words: List[Word]) -> Optional[Word]:
    try:
       return next(w for w in words if text == w.text)
    except StopIteration:
       return None

def closest_analogies(
    left2: str, left1: str, right2: str, words: List[Word]
) -> List[Tuple[float, Word]]:
    word_left1 = find_word(left1, words)
    word_left2 = find_word(left2, words)
    word_right2 = find_word(right2, words)
    if (not word_left1) or (not word_left2) or (not word_right2):
        return []
    vector = v.add(
        v.sub(word_left1.vector, word_left2.vector),
        word_right2.vector)
    closest = most_similar(vector, words)[:10]
    def is_redundant(word: str) -> bool:
        """
        Sometimes the two left vectors are so close the answer is e.g.
        "shirt-clothing is like phone-phones". Skip 'phones' and get the next
        suggestion, which might be more interesting.
        """
        word_lower = word.lower()
        return (
            left1.lower() in word_lower or
            left2.lower() in word_lower or
            right2.lower() in word_lower)
    closest_filtered = [(dist, w) for (dist, w) in closest if not is_redundant(w.text)]
    return closest_filtered

def print_analogy(left2: str, left1: str, right2: str, words: List[Word]) -> None:
    analogies = closest_analogies(left2, left1, right2, words)
    if (len(analogies) == 0):
        print(f"{left2}-{left1} is like {right2}-?")
    else:
        (dist, w) = analogies[0]
        #alternatives = ', '.join([f"{w.text} ({dist})" for (dist, w) in analogies])
        print(f"{left2}-{left1} is like {right2}-{w.text}")

words = load_words('data/words.vec')

print_most_similar(words, words[190].text)
print_most_similar(words, words[230].text)
print_most_similar(words, words[330].text)
print_most_similar(words, words[430].text)

print("")

print_analogy('man', 'him' , 'woman', words)
# You'll need to download the pretrained word vectors to complete the analogies
# below:
# https://fasttext.cc/docs/en/english-vectors.html
print_analogy('quick', 'quickest' , 'far', words)
print_analogy('sushi', 'rice', 'pizza', words)
print_analogy('Paris', 'France', 'Rome', words)
print_analogy('dog', 'mammal', 'eagle', words)
print_analogy('German', 'BMW' , 'American', words)
print_analogy('German', 'Opel', 'American', words)

# Analogies (interactive)
while False:
    left2 = find_word(read_word(), words)
    if not left2:
        print("Sorry, I don't know that word.")
        continue
    left1 = find_word(read_word(), words)
    if not left1:
        print("Sorry, I don't know that word.")
        continue
    right2 = find_word(read_word(), words)
    if not right2:
        print("Sorry, I don't know that word.")
        continue
    print_analogy(left2, left1, right2, words)

# Related words (interactive)
while False:
    text = read_word()
    w = find_word(text, words)
    if not w:
        print("Sorry, I don't know that word.")
    else:
        print_most_similar(w)
