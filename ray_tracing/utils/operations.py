import math
from .constants import *

def equal(a, b):
    if abs(a - b) < EPSILON:
        return True
    else:
        return False