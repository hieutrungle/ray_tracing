import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

from .constants import *
import ray_tracing.elements.tuples as tuples


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


def generate_uuid():
    """
    Generates a unique id.
    """
    global OBJECT_COUNT
    OBJECT_COUNT += 1
    return OBJECT_COUNT


def context_table_to_list(context):
    """
    Converts a context table to a list.
    """
    given_list = []
    given_list.append([element for element in context.table.headings])
    for row in context.table.rows:
        given_list.append([element for element in row])
    return given_list


def list_to_material(given_list):
    """
    Converts a list to a material.
    """
    import ray_tracing.elements.materials as materials

    material_properties = {}

    for row in given_list:
        if row[0].lower().find("material") != -1:
            if row[0].lower().find("color") != -1:
                color = row[1].strip("() ").split(",")
                material_properties["color"] = tuples.Color(
                    float(color[0]), float(color[1]), float(color[2])
                )
            elif row[0].lower().find("ambient") != -1:
                material_properties["ambient"] = float(row[1])
            elif row[0].lower().find("diffuse") != -1:
                material_properties["diffuse"] = float(row[1])
            elif row[0].lower().find("specular") != -1:
                material_properties["specular"] = float(row[1])
            elif row[0].lower().find("shininess") != -1:
                material_properties["shininess"] = float(row[1])
    if material_properties == {}:
        material = materials.Material()
    else:
        material = materials.Material(**material_properties)
    return material


def list_to_transform(given_list):
    """
    Converts a list to a transform.
    """
    import ray_tracing.elements.matrix as matrix

    transform = matrix.IdentityMatrix()
    for row in given_list:
        if row[0].lower().find("transform") != -1:
            [operation, values] = row[1].strip(")").split("(")
            values = values.split(",")
            if operation.lower().find("scaling") != -1:
                transform = transform.scale(
                    float(values[0]), float(values[1]), float(values[2])
                )
            elif operation.lower().find("translation") != -1:
                transform = transform.translate(
                    float(values[0]), float(values[1]), float(values[2])
                )
            elif operation.lower().find("rotation_x") != -1:
                transform = transform.rotate_x(float(values[0]))
            elif operation.lower().find("rotation_y") != -1:
                transform = transform.rotate_y(float(values[0]))
            elif operation.lower().find("rotation_z") != -1:
                transform = transform.rotate_z(float(values[0]))
            elif operation.lower().find("shearing") != -1:
                operation = matrix.ShearingMatrix(
                    float(values[0]),
                    float(values[1]),
                    float(values[2]),
                    float(values[3]),
                    float(values[4]),
                    float(values[5]),
                )
                transform = operation * transform

    return transform


def str_to_bool(is_shadowed: str) -> bool:
    if is_shadowed.lower().find("true") != -1:
        is_shadowed = True
    elif is_shadowed.lower().find("false") != -1:
        is_shadowed = False
    else:
        raise ValueError("is_shadowed must be true or false")
    return is_shadowed
