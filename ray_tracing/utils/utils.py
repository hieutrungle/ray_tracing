import math
from .constants import *


def equal(a, b):
    if abs(a - b) < EPSILON:
        return True
    else:
        return False


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


def matrix_text2list(table_headings, table_rows):
    """
    Converts a string of text to a list.
    """
    matrix_list = []
    matrix_list.append([float(element) for element in table_headings])
    for row in table_rows:
        matrix_list.append([float(element) for element in row])
    return matrix_list
