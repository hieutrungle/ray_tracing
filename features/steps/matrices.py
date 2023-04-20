import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# matrix representation
@given("the following {num1}x{num2} matrix {matrix_name}")
def step_impl(context, num1, num2, matrix_name):
    given_list = utils.matrix_text2list(context.table.headings, context.table.rows)
    m = matrix.Matrix(given_list)
    setattr(context, matrix_name, m)


@then("{matrix_name}[{row},{column}] = {value}")
def step_impl(context, matrix_name, row, column, value):
    m = getattr(context, matrix_name)
    print(f"m[{row},{column}] = {m[int(row), int(column)]}")
    print(f"value = {value}")
    assert m[int(row), int(column)] == float(value)


# matrix comparison
@given("the following matrix {name}")
def step_impl(context, name):
    given_list = utils.matrix_text2list(context.table.headings, context.table.rows)
    m = matrix.Matrix(given_list)
    setattr(context, name, m)


@then("matrix {name1} == {name2}")
def step_impl(context, name1, name2):
    assert getattr(context, name1) == getattr(context, name2)


@then("matrix {name1} != {name2}")
def step_impl(context, name1, name2):
    assert getattr(context, name1) != getattr(context, name2)


# matrix multiplication
@then("matrix {name1} * matrix {name2} =")
def step_impl(context, name1, name2):
    given_list = utils.matrix_text2list(context.table.headings, context.table.rows)
    m = matrix.Matrix(given_list)
    assert getattr(context, name1) * getattr(context, name2) == m


# matrix * tuple
@then("matrix {name1} * tuple {name2} = tuple({x}, {y}, {z}, {w})")
def step_impl(context, name1, name2, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    t = tuples.Tuple(x, y, z, w)
    results = getattr(context, name1) * getattr(context, name2)
    assert results == t


# multiplication with identity matrix
@then("matrix {name1} * identity_matrix = matrix {name1}")
def step_impl(context, name1):
    m = getattr(context, name1)
    identity_matrix = matrix.IdentityMatrix(m.shape[0])
    m = m * identity_matrix
    assert m == getattr(context, name1)


@then("identity_matrix * tuple {name1} = tuple {name1}")
def step_impl(context, name1):
    t = getattr(context, name1)
    identity_matrix = matrix.IdentityMatrix(4)
    t = identity_matrix * t
    assert t == getattr(context, name1)


# transpose of matrix
@then("transpose({name}) is the following matrix")
def step_impl(context, name):
    given_list = utils.matrix_text2list(context.table.headings, context.table.rows)
    m = matrix.Matrix(given_list)
    assert getattr(context, name).transpose() == m


# transpose of identity matrix
@given("{name} ← transpose(identity_matrix)")
def step_impl(context, name):
    m = matrix.IdentityMatrix(4)
    setattr(context, name, m.transpose())


@then("{name} = identity_matrix")
def step_impl(context, name):
    m = matrix.IdentityMatrix(4)
    assert getattr(context, name) == m


# determinant of 2x2 matrix
@then("determinant({name}) = {value}")
def step_impl(context, name, value):
    assert getattr(context, name).determinant() == float(value)


# submatrix of matrix
@then("submatrix({name}, {row}, {column}) is the following {num1}x{num2} matrix")
def step_impl(context, name, row, column, num1, num2):
    given_list = utils.matrix_text2list(context.table.headings, context.table.rows)
    m = matrix.Matrix(given_list)
    assert getattr(context, name).submatrix(int(row), int(column)) == m


# minor of matrix
@given("{name} ← submatrix({name1}, {row}, {column})")
def step_impl(context, name, name1, row, column):
    m = getattr(context, name1).submatrix(int(row), int(column))
    setattr(context, name, m)


@then("minor({name}, {row}, {column}) = {value}")
def step_impl(context, name, row, column, value):
    assert getattr(context, name).minor(int(row), int(column)) == float(value)


# cofactor of matrix
@then("cofactor({name}, {row}, {column}) = {value}")
def step_impl(context, name, row, column, value):
    assert getattr(context, name).cofactor(int(row), int(column)) == float(value)


# is invertible
@then("{name} is invertible")
def step_impl(context, name):
    assert getattr(context, name).is_invertible() == True


@then("{name} is not invertible")
def step_impl(context, name):
    assert getattr(context, name).is_invertible() == False


# inverse of matrix
@given("matrix {name1} ← inverse({name2})")
def step_impl(context, name1, name2):
    if name2 == "identity_matrix":
        setattr(context, name1, matrix.IdentityMatrix(4).inverse())
    else:
        m = getattr(context, name2).inverse().round_matrix(5)
        setattr(context, name1, m)


@then("matrix {name} is the following 4x4 matrix")
def step_impl(context, name):
    given_list = utils.matrix_text2list(context.table.headings, context.table.rows)
    m = matrix.Matrix(given_list)
    assert getattr(context, name) == m


@then("inverse({name}) is the following 4x4 matrix")
def step_impl(context, name):
    given_list = utils.matrix_text2list(context.table.headings, context.table.rows)
    m = matrix.Matrix(given_list)
    results = getattr(context, name).inverse().round_matrix(5)
    print(results)
    assert results == m


# C ← A * B -> C * inverse(B) = A
@given("matrix {name1} ← matrix {name2} * matrix {name3}")
def step_impl(context, name1, name2, name3):
    m = getattr(context, name2) * getattr(context, name3)
    setattr(context, name1, m)


@then("matrix {name1} * matrix inverse({name2}) = matrix {name3}")
def step_impl(context, name1, name2, name3):
    m = getattr(context, name1) * getattr(context, name2).inverse()
    assert m.round_matrix(5) == getattr(context, name3).round_matrix(5)


# inverse identity matrix
@when("matrix {name1} ← matrix {name2} * matrix inverse({name2})")
def step_impl(context, name1, name2):
    m = getattr(context, name2) * getattr(context, name2).inverse()
    setattr(context, name1, m)


# Inverse of transpose and transpose of inverse
@when("matrix {name1} ← transpose(inverse({name2}))")
def step_impl(context, name1, name2):
    m = getattr(context, name2).inverse().transpose().round_matrix(5)
    setattr(context, name1, m)


@when("matrix {name1} ← inverse(transpose({name2}))")
def step_impl(context, name1, name2):
    m = getattr(context, name2).transpose().inverse().round_matrix(5)
    setattr(context, name1, m)
