"""
Functions that roam around but have no home.
"""

import math


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def vector2_lerp(x1: float, y1: float, x2: float, y2: float, t: float) -> tuple[float, float]:
    x: float = (1 - t) * x1 + t * x2
    y: float = (1 - t) * y1 + t * y2
    return (x, y)


def sine(x: float) -> float:
    return math.sin(x)
