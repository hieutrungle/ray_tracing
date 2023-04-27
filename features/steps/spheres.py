import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.shapes as shapes
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.rays as rays
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# sphere intersection
@given("sphere {s} ← sphere()")
def step_impl(context, s):
    setattr(context, s, shapes.Sphere())


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
    assert xs[index].get_object() == s


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


# material
@when("material {m} ← {sphere}.material")
def step_impl(context, m, sphere):
    sphere = getattr(context, sphere)
    setattr(context, m, sphere.material)


@when("sphere {s}.material ← {m}")
def step_impl(context, s, m):
    s = getattr(context, s)
    m = getattr(context, m)
    s.material = m


@then("sphere {s}.material = {m}")
def step_impl(context, s, m):
    s = getattr(context, s)
    m = getattr(context, m)
    assert s.material == m


# sphere with material
@given("sphere {s} ← sphere() with")
def step_impl(context, s):
    given_list = utils.context_table_to_list(context)
    material = utils.list_to_material(given_list)
    transform = utils.list_to_transform(given_list)
    # print(transform)
    # assert False
    setattr(context, s, shapes.Sphere(material=material, transform=transform))


# refactor
@given("shape {s} ← test_shape()")
def step_impl(context, s):
    setattr(context, s, shapes.Shape())


@given("shape {m} ← scaling({x}, {y}, {z}) * rotation_z({angle_z})")
def step_impl(context, m, x, y, z, angle_z):
    x = float(x)
    y = float(y)
    z = float(z)
    angle_z = float(angle_z)
    scaling_matrix = matrix.ScalingMatrix(x, y, z)
    rotation_matrix = matrix.RotationZMatrix(angle_z)
    setattr(context, m, scaling_matrix * rotation_matrix)


@then("shape {s}.transform = identity_matrix")
def step_impl(context, s):
    s = getattr(context, s)
    assert s.transform == matrix.IdentityMatrix(4)


@when("shape set_transform({shape}, scaling({x}, {y}, {z}))")
def step_impl(context, shape, x, y, z):
    shape = getattr(context, shape)
    shape.set_transform(matrix.ScalingMatrix(float(x), float(y), float(z)))


@when("shape set_transform({shape}, translation({x}, {y}, {z}))")
def step_impl(context, shape, x, y, z):
    shape = getattr(context, shape)
    shape.set_transform(matrix.TranslationMatrix(float(x), float(y), float(z)))


@then("shape {s}.transform = translation({x}, {y}, {z})")
def step_impl(context, s, x, y, z):
    shape = getattr(context, s)
    assert shape.transform == matrix.TranslationMatrix(float(x), float(y), float(z))


@when("shape set_transform({shape}, {m})")
def step_impl(context, shape, m):
    shape = getattr(context, shape)
    m = getattr(context, m)
    shape.set_transform(m)


@when("shape {m} ← {s}.material")
def step_impl(context, m, s):
    shape = getattr(context, s)
    setattr(context, m, shape.material)


@when("shape {s}.material ← {m}")
def step_impl(context, s, m):
    shape = getattr(context, s)
    material = getattr(context, m)
    shape.material = material


@then("shape {s}.material = {m}")
def step_impl(context, s, m):
    shape = getattr(context, s)
    material = getattr(context, m)
    assert shape.material == material


@then("shape {s}.saved_ray.origin = point({x}, {y}, {z})")
def step_impl(context, s, x, y, z):
    shape = getattr(context, s)
    assert shape.saved_ray.origin == tuples.Point(float(x), float(y), float(z))


@then("shape {s}.saved_ray.direction = vector({x}, {y}, {z})")
def step_impl(context, s, x, y, z):
    shape = getattr(context, s)
    assert shape.saved_ray.direction == tuples.Vector(float(x), float(y), float(z))
