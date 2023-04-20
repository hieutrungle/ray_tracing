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
    if name == "x":
        tuple_value = context.a.tuple[0]
    elif name == "y":
        tuple_value = context.a.tuple[1]
    elif name == "z":
        tuple_value = context.a.tuple[2]
    elif name == "w":
        tuple_value = context.a.tuple[3]
    # tuple_value = getattr(context.a, name)
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
@given("{name} ← tuple({x}, {y}, {z}, {w})")
def step_impl(context, name, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    setattr(context, name, tuples.Tuple(x, y, z, w))


@then("a{num1} + a{num2} = tuple({x}, {y}, {z}, {w})")
def step_impl(context, num1, num2, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    new_tuple = getattr(context, "a" + num1) + getattr(context, "a" + num2)
    assert new_tuple == tuples.Tuple(x, y, z, w)


# define points and vectors
@given("{name} ← point({x}, {y}, {z})")
def step_impl(context, name, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    setattr(context, name, tuples.Point(x, y, z))


@given("{name} ← vector({x}, {y}, {z})")
def step_impl(context, name, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    setattr(context, name, tuples.Vector(x, y, z))


# subtracting points
@then("p{num1} - p{num2} = vector({x}, {y}, {z})")
def step_impl(context, num1, num2, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    results = getattr(context, "p" + num1) - getattr(context, "p" + num2)
    assert results == tuples.Vector(x, y, z)


# subtracting vector from a point
@then("p - v = point({x}, {y}, {z})")
def step_impl(context, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    results = getattr(context, "p") - getattr(context, "v")
    assert results == tuples.Point(x, y, z)


# subtracting two vectors
@then("v{num1} - v{num2} = vector({x}, {y}, {z})")
def step_impl(context, num1, num2, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    results = getattr(context, "v" + num1) - getattr(context, "v" + num2)
    assert results == tuples.Vector(x, y, z)


# negate a tuple
@then("-a = tuple({x}, {y}, {z}, {w})")
def step_impl(context, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    results = -getattr(context, "a")
    assert results == tuples.Tuple(x, y, z, w)


# multiply a tuple by a scalar
@then("a * {scalar} = tuple({x}, {y}, {z}, {w})")
def step_impl(context, scalar, x, y, z, w):
    x = float(x)
    y = float(y)
    z = float(z)
    w = float(w)
    scalar = float(scalar)
    results = getattr(context, "a") * scalar
    assert results == tuples.Tuple(x, y, z, w)


# magnitude
@then("magnitude(v) = {magnitude}")
def step_impl(context, magnitude):
    magnitude = float(magnitude)
    results = getattr(context, "v").magnitude()
    assert operations.equal(results, magnitude)


# normalize
@then("normalize(v) = vector({x}, {y}, {z})")
def step_impl(context, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    results = getattr(context, "v").normalize()
    assert results == tuples.Vector(x, y, z)


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
    results = getattr(context, "v" + num1).dot(getattr(context, "v" + num2))
    assert operations.equal(results, dot_product)


# cross product
@then("cross(v{num1}, v{num2}) = vector({x}, {y}, {z})")
def step_impl(context, num1, num2, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    new_vector = getattr(context, "v" + num1).cross(getattr(context, "v" + num2))
    assert new_vector == tuples.Vector(x, y, z)


# color
@given("c ← color({r}, {g}, {b})")
def step_impl(context, r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    context.c = tuples.Color(r, g, b)


@given("c{num} ← color({x}, {y}, {z})")
def step_impl(context, num, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    setattr(context, "c" + num, tuples.Color(x, y, z))


# Representing color
@then("c.{name} = {value}")
def step_impl(context, name, value):
    if name == "r":
        tuple_value = context.c.tuple[0]
    elif name == "g":
        tuple_value = context.c.tuple[1]
    elif name == "b":
        tuple_value = context.c.tuple[2]
    elif name == "a":
        tuple_value = context.c.tuple[3]
    assert (tuple_value - float(value)) < EPSILON


# Adding colors
@then("c{num1} + c{num2} = color({r}, {g}, {b})")
def step_impl(context, num1, num2, r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    results = getattr(context, "c" + num1) + getattr(context, "c" + num2)
    assert results == tuples.Color(r, g, b)


# Subtracting colors
@then("c{num1} - c{num2} = color({r}, {g}, {b})")
def step_impl(context, num1, num2, r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    results = getattr(context, "c" + num1) - getattr(context, "c" + num2)
    assert results == tuples.Color(r, g, b)


# Multiplying a color by a scalar
@then("c * {scalar} = color({r}, {g}, {b})")
def step_impl(context, scalar, r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    scalar = float(scalar)
    results = getattr(context, "c") * scalar
    assert results == tuples.Color(r, g, b)


# Multiplying colors
@then("c{num1} * c{num2} = color({r}, {g}, {b})")
def step_impl(context, num1, num2, r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    results = getattr(context, "c" + num1).hadamard_product(
        getattr(context, "c" + num2)
    )
    assert results == tuples.Color(r, g, b)
