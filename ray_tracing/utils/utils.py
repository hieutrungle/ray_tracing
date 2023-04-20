def matrix_text2list(table_headings, table_rows):
    """
    Converts a string of text to a list.
    """
    matrix_list = []
    matrix_list.append([float(element) for element in table_headings])
    for row in table_rows:
        matrix_list.append([float(element) for element in row])
    return matrix_list
