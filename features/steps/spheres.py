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


# sphere intersection
@given("sphere {s} ← sphere()")
def step_impl(context, s):
    setattr(context, s, shape.Sphere())


@when("intersect {xs} ← intersect({s}, {r})")
def step_impl(context, xs, s, r):
    sphere = getattr(context, s)
    ray = getattr(context, r)
    setattr(context, xs, sphere.intersect(ray))


@then("intersect {xs}.count = {length}")
def step_impl(context, xs, length):
    xs = getattr(context, xs)
    length = int(length)
    assert len(xs) == length


@then("intersect {xs}[{index}].t = {value}")
def step_impl(context, xs, index, value):
    xs = getattr(context, xs)
    index = int(index)
    value = float(value)
    assert xs[index].t == value


@then("intersect {xs}[{index}].object = {s}")
def step_impl(context, xs, index, s):
    xs = getattr(context, xs)
    index = int(index)
    s = getattr(context, s)
    assert xs[index].shape_object == s


# transformation
@then("sphere {s}.transform = identity_matrix")
def step_impl(context, s):
    s = getattr(context, s)
    assert s.transform == matrix.IdentityMatrix(4)


@when("set_transform({s}, {m})")
def step_impl(context, s, m):
    s = getattr(context, s)
    m = getattr(context, m)
    s.set_transform(m)


@then("sphere {s}.transform = {m}")
def step_impl(context, s, m):
    s = getattr(context, s)
    m = getattr(context, m)
    assert s.transform == m


# normal
@when("normal {n} ← normal_at({s}, point({x}, {y}, {z}))")
def step_impl(context, n, s, x, y, z):
    s = getattr(context, s)
    x = float(x)
    y = float(y)
    z = float(z)
    setattr(context, n, s.normal_at(tuples.Point(x, y, z)))


@then("normal {n} = vector({x}, {y}, {z})")
def step_impl(context, n, x, y, z):
    n = getattr(context, n)
    x = float(x)
    y = float(y)
    z = float(z)
    n = n.round(5)
    assert n == tuples.Vector(x, y, z)


# normal has to be normalized
@then("normal {n} = normalize({n})")
def step_impl(context, n):
    n = getattr(context, n)
    assert n == n.normalize()


# normal on transformed sphere
@given("sphere {transform} ← scaling({x}, {y}, {z}) * rotation_z({angle_z})")
def step_impl(context, transform, x, y, z, angle_z):
    x = float(x)
    y = float(y)
    z = float(z)
    angle_z = float(angle_z)
    scaling_matrix = matrix.ScalingMatrix(x, y, z)
    rotation_matrix = matrix.RotationZMatrix(angle_z)
    setattr(context, transform, scaling_matrix * rotation_matrix)


@given("sphere {transform} ← translation({x}, {y}, {z})")
def step_impl(context, transform, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    setattr(context, transform, matrix.TranslationMatrix(x, y, z))


@given("sphere set_transform({s}, {transform})")
def step_impl(context, s, transform):
    s = getattr(context, s)
    transform = getattr(context, transform)
    s.set_transform(transform)
