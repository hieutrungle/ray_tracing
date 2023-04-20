def matrix_from_list(table):
    """
    Converts a string of text to a matrix.
    """
    matrix = []
    for row in table:
        matrix.append([float(element) for element in row])
    return matrix
