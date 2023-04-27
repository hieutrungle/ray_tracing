import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.shape as shape
import ray_tracing.operations.intersection as intersection
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.rays as rays
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# intersection encapsulation
@when("intersection {interx} ← intersection({t}, {s})")
def step_impl(context, interx, t, s):
    t = float(t)
    s = getattr(context, s)
    setattr(context, interx, intersection.Intersection(t, s))


@then("intersection {interx}.t = {value}")
def step_impl(context, interx, value):
    interx = getattr(context, interx)
    attribute = interx.get_t()
    value = float(value)
    assert attribute == value


@then("intersection {interx}.shape = {given_object}")
def step_impl(context, interx, given_object):
    interx = getattr(context, interx)
    attribute = interx.get_object()
    given_object = getattr(context, given_object)
    assert attribute == given_object


# intersections
@given("intersection {interx} ← intersection({t}, {s})")
def step_impl(context, interx, t, s):
    t = float(t)
    s = getattr(context, s)
    setattr(context, interx, intersection.Intersection(t, s))


@given("intersections {xs} ← 2 intersections({i1}, {i2})")
def step_impl(context, xs, i1, i2):
    i1 = getattr(context, i1)
    i2 = getattr(context, i2)
    setattr(context, xs, intersection.Intersections(i1, i2))


@given("intersections {xs} ← 4 intersections({i1}, {i2}, {i3}, {i4})")
def step_impl(context, xs, i1, i2, i3, i4):
    i1 = getattr(context, i1)
    i2 = getattr(context, i2)
    i3 = getattr(context, i3)
    i4 = getattr(context, i4)
    setattr(context, xs, intersection.Intersections(i1, i2, i3, i4))


@when("intersections {xs} ← 2 intersections({i1}, {i2})")
def step_impl(context, xs, i1, i2):
    i1 = getattr(context, i1)
    i2 = getattr(context, i2)
    setattr(context, xs, intersection.Intersections(i1, i2))


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


# hit
@when("intersection {interx} ← hit({xs})")
def step_impl(context, interx, xs):
    xs = getattr(context, xs)
    setattr(context, interx, xs.hit())


@then("intersection {interx} = {given_intersection}")
def step_impl(context, interx, given_intersection):
    interx = getattr(context, interx)
    given_intersection = getattr(context, given_intersection)
    assert interx == given_intersection


@then("intersection {interx} is Nothing")
def step_impl(context, interx):
    interx = getattr(context, interx)
    assert interx is None


# prepare computations
@when("computation {comp} ← prepare_computations({interx}, {ray})")
def step_impl(context, comp, interx, ray):
    interx = getattr(context, interx)
    ray = getattr(context, ray)
    setattr(context, comp, interx.prepare_computations(ray))


@then("computation {comp}.t = {interx}.t")
def step_impl(context, comp, interx):
    comp = getattr(context, comp)
    interx = getattr(context, interx)
    assert comp.t == interx.t


@then("computation {comp}.object = {interx}.object")
def step_impl(context, comp, interx):
    comp = getattr(context, comp)
    interx = getattr(context, interx)
    assert comp.get_object() == interx.get_object()


@then("computation {comp}.point = point({x}, {y}, {z})")
def step_impl(context, comp, x, y, z):
    comp = getattr(context, comp)
    x = float(x)
    y = float(y)
    z = float(z)
    assert comp.get_point() == tuples.Point(x, y, z)


@then("computation {comp}.eyev = vector({x}, {y}, {z})")
def step_impl(context, comp, x, y, z):
    comp = getattr(context, comp)
    x = float(x)
    y = float(y)
    z = float(z)
    assert comp.get_eye_vector() == tuples.Vector(x, y, z)


@then("computation {comp}.normalv = vector({x}, {y}, {z})")
def step_impl(context, comp, x, y, z):
    comp = getattr(context, comp)
    x = float(x)
    y = float(y)
    z = float(z)
    assert comp.get_normal_vector() == tuples.Vector(x, y, z)


@then("computation {comp}.inside = {inside}")
def step_impl(context, comp, inside):
    comp = getattr(context, comp)
    if inside.lower() == "true":
        inside = True
    else:
        inside = False
    assert comp.is_inside() == inside


# over point intersection
@then("computation {comp}.over_point.z < -EPSILON/2")
def step_impl(context, comp):
    comp = getattr(context, comp)
    assert comp.over_point.z() < -EPSILON / 2


@then("computation {comp}.point.z > {comp}.over_point.z")
def step_impl(context, comp):
    comp = getattr(context, comp)
    assert comp.point.z() > comp.over_point.z()
