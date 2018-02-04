from typing import List

import math

Vector = List[float]

def l2_len(v: Vector) -> float:
    return math.sqrt(sum([x*x for x in v]))

def dot(v1: Vector, v2: Vector) -> float:
    assert len(v1) == len(v2)
    return sum([x*y for (x,y) in zip(v1, v2)])

def add(v1: Vector, v2: Vector) -> Vector:
    assert len(v1) == len(v2)
    return [x + y for (x,y) in zip(v1, v2)]

def sub(v1: Vector, v2: Vector) -> Vector:
    assert len(v1) == len(v2)
    return [x - y for (x,y) in zip(v1, v2)]

def normalize(v: Vector) -> Vector:
    l = l2_len(v)
    return [x / l for x in v]

def cosine_similarity_normalized(v1: Vector, v2: Vector) -> float:
    """
    Returns the cosine of the angle between the two vectors.
    Each of the vectors must have length (L2-norm) equal to 1.
    Results range from -1 (very different) to 1 (very similar).
    """
    return dot(v1, v2)
