import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.shape as shape
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.ray as ray
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# intersection encapsulation
@when("intersection {i} ← intersection({t}, {s})")
def step_impl(context, i, t, s):
    t = float(t)
    s = getattr(context, s)
    setattr(context, i, shape.Intersection(t, s))


@then("intersection {i}.t = {value}")
def step_impl(context, i, value):
    i = getattr(context, i)
    attribute = getattr(i, "t")
    value = float(value)
    assert attribute == value


@then("intersection {i}.shape_object = {given_object}")
def step_impl(context, i, given_object):
    i = getattr(context, i)
    attribute = getattr(i, "shape_object")
    given_object = getattr(context, given_object)
    assert attribute == given_object


# intersections
@given("intersection {i} ← intersection({t}, {s})")
def step_impl(context, i, t, s):
    t = float(t)
    s = getattr(context, s)
    setattr(context, i, shape.Intersection(t, s))


@when("intersections xs ← intersections({i1}, {i2})")
def step_impl(context, i1, i2):
    i1 = getattr(context, i1)
    i2 = getattr(context, i2)
    context.xs = shape.Intersections(i1, i2)


@then("intersections {xs}.count = {count}")
def step_impl(context, xs, count):
    xs = getattr(context, xs)
    count = int(count)
    assert len(xs) == count


@then("intersections {xs}[{index}].t = {t}")
def step_impl(context, xs, index, t):
    xs = getattr(context, xs)
    index = int(index)
    t = float(t)
    assert xs[index].t == t
