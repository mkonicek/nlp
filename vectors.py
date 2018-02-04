from typing import List,Any

import math
import numpy as np

Vector = np.ndarray[float]

def l2_len(v: Vector) -> float:
    return math.sqrt(np.dot(v, v))

def dot(v1: Vector, v2: Vector) -> float:
    assert v1.shape == v2.shape
    return np.dot(v1, v2)

def add(v1: Vector, v2: Vector) -> Vector:
    assert v1.shape == v2.shape
    return np.add(v1, v2)

def sub(v1: Vector, v2: Vector) -> Vector:
    assert v1.shape == v2.shape
    return np.subtract(v1, v2)

def normalize(v: Vector) -> Vector:
    return v / l2_len(v)

def cosine_similarity_normalized(v1: Vector, v2: Vector) -> float:
    """
    Returns the cosine of the angle between the two vectors.
    Each of the vectors must have length (L2-norm) equal to 1.
    Results range from -1 (very different) to 1 (very similar).
    """
    return dot(v1, v2)
