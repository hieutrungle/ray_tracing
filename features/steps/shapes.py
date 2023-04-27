import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.shapes as shapes
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
from ray_tracing.utils.constants import *
from behave import given, when, then


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
