import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.shapes as shapes
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# definition
@given("plane {p} ← plane()")
def step_impl(context, p):
    setattr(context, p, shapes.Plane())


@when("plane {n} ← local_normal_at({p}, point({x}, {y}, {z}))")
def step_impl(context, n, p, x, y, z):
    plane = getattr(context, p)
    point = tuples.Point(float(x), float(y), float(z))
    setattr(context, n, plane.local_normal_at(point))


# intersection
@when("plane {xs} ← local_intersect({p}, {r})")
def step_impl(context, xs, p, r):
    plane = getattr(context, p)
    ray = getattr(context, r)
    setattr(context, xs, plane.local_intersect(ray))


@then("plane {xs}.count = {length}")
def step_impl(context, xs, length):
    xs = getattr(context, xs)
    length = int(length)
    assert len(xs) == length


@then("plane {xs}[{index}].t = {value}")
def step_impl(context, xs, index, value):
    xs = getattr(context, xs)
    index = int(index)
    value = float(value)
    assert xs[index].t == value


@then("plane {xs}[{index}].object = {p}")
def step_impl(context, xs, index, p):
    xs = getattr(context, xs)
    index = int(index)
    p = getattr(context, p)
    assert xs[index].get_object() == p


@then("plane {xs} is empty")
def step_impl(context, xs):
    xs = getattr(context, xs)
    assert len(xs) == 0
