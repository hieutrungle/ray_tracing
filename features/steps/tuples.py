import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.tuples as tuples
from ray_tracing.utils.constants import *
import ray_tracing.utils.operations as operations
from behave import given, when, then


# tuples
@given("a ← tuple({x}, {y}, {z}, {w})")
def step_impl(context, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    context.a = tuples.Tuple(x, y, z, w)


@then("a.{name} = {value}")
def step_impl(context, name, value):
    tuple_value = getattr(context.a, name)
    assert (tuple_value - float(value)) < EPSILON


@then("a is a point")
def step_impl(context):
    assert context.a.is_point()


@then("a is not a point")
def step_impl(context):
    assert not context.a.is_point()


@then("a is a vector")
def step_impl(context):
    assert not context.a.is_point()


@then("a is not a vector")
def step_impl(context):
    assert context.a.is_point()


# point
@given("p ← point({x}, {y}, {z})")
def step_impl(context, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    context.p = tuples.Tuple(x, y, z, 1)


@then("p = tuple({x}, {y}, {z}, 1)")
def step_impl(context, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    assert context.p == tuples.Point(x, y, z)


# vector
@given("v ← vector({x}, {y}, {z})")
def step_impl(context, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    context.v = tuples.Tuple(x, y, z, 0)


@then("v = tuple({x}, {y}, {z}, 0)")
def step_impl(context, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    assert context.v == tuples.Vector(x, y, z)


# adding tuples
@given("a{num} ← tuple({x}, {y}, {z}, {w})")
def step_impl(context, num, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    setattr(context, "a" + num, tuples.Tuple(x, y, z, w))


@then("a{num1} + a{num2} = tuple({x}, {y}, {z}, {w})")
def step_impl(context, num1, num2, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    assert getattr(context, "a" + num1) + getattr(context, "a" + num2) == tuples.Tuple(
        x, y, z, w
    )


# define points and vectors
@given("p{num1} ← point({x1}, {y1}, {z1})")
def step_impl(context, num1, x1, y1, z1):
    x1 = float(x1)
    y1 = float(y1)
    z1 = float(z1)
    setattr(context, "p" + num1, tuples.Point(x1, y1, z1))


@given("v{num1} ← vector({x1}, {y1}, {z1})")
def step_impl(context, num1, x1, y1, z1):
    x1 = float(x1)
    y1 = float(y1)
    z1 = float(z1)
    setattr(context, "v" + num1, tuples.Vector(x1, y1, z1))


# subtracting points
@then("p{num1} - p{num2} = vector({x}, {y}, {z})")
def step_impl(context, num1, num2, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    assert getattr(context, "p" + num1) - getattr(context, "p" + num2) == tuples.Vector(
        x, y, z
    )


# subtracting vector from a point
@then("p - v = point({x}, {y}, {z})")
def step_impl(context, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    assert getattr(context, "p") - getattr(context, "v") == tuples.Point(x, y, z)


# subtracting two vectors
@then("v{num1} - v{num2} = vector({x}, {y}, {z})")
def step_impl(context, num1, num2, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    assert getattr(context, "v" + num1) - getattr(context, "v" + num2) == tuples.Vector(
        x, y, z
    )


# negate a tuple
@then("-a = tuple({x}, {y}, {z}, {w})")
def step_impl(context, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    assert -getattr(context, "a") == tuples.Tuple(x, y, z, w)


# multiply a tuple by a scalar
@then("a * {scalar} = tuple({x}, {y}, {z}, {w})")
def step_impl(context, scalar, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    scalar = float(scalar)
    assert getattr(context, "a") * scalar == tuples.Tuple(x, y, z, w)


# magnitude
@then("magnitude(v) = {magnitude}")
def step_impl(context, magnitude):
    magnitude = float(magnitude)
    assert operations.equal((getattr(context, "v")).magnitude(), magnitude)


# normalize
@then("normalize(v) = vector({x}, {y}, {z})")
def step_impl(context, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    assert getattr(context, "v").normalize() == tuples.Vector(x, y, z)


@when("norm ← normalize(v)")
def step_impl(context):
    context.norm = getattr(context, "v").normalize()


@then("magnitude(norm) = 1")
def step_impl(context):
    assert operations.equal((context.norm).magnitude(), 1)


# dot product
@then("dot(v{num1}, v{num2}) = {dot_product}")
def step_impl(context, num1, num2, dot_product):
    dot_product = float(dot_product)
    assert operations.equal(
        getattr(context, "v" + num1).dot(getattr(context, "v" + num2)),
        dot_product,
    )


# cross product
@then("cross(v{num1}, v{num2}) = vector({x}, {y}, {z})")
def step_impl(context, num1, num2, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    assert getattr(context, "v" + num1).cross(
        getattr(context, "v" + num2)
    ) == tuples.Vector(x, y, z)
