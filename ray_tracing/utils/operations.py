import math
from .constants import *


def equal(a, b):
    if abs(a - b) < EPSILON:
        return True
    else:
        return False


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)
