import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
import ray_tracing.scene.camera as camera
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# translation
@given("transformation {transform} ← translation({x}, {y}, {z})")
def step_impl(context, transform, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    translation_matrix = matrix.TranslationMatrix(x, y, z)
    setattr(context, transform, translation_matrix)


# scaling
@given("transformation {transform} ← scaling({x}, {y}, {z})")
def step_impl(context, transform, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    scaling_matrix = matrix.ScalingMatrix(x, y, z)
    setattr(context, transform, scaling_matrix)


# inverse
@given("transformation {inv} ← inverse({name})")
def step_impl(context, inv, name):
    inv_m = getattr(context, name).inverse()
    setattr(context, inv, inv_m)


# translation does not affect vectors
@then("transformation {transform} * {v} = {v}")
def step_impl(context, transform, v):
    results = getattr(context, transform) * getattr(context, v)
    assert results == getattr(context, v)


# transform a point
@then("transformation {transform} * {p} = point({x}, {y}, {z})")
def step_impl(context, transform, p, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    results = getattr(context, transform) * getattr(context, p)
    assert results == tuples.Point(x, y, z)


# transform a vector
@then("transformation {transform} * {v} = vector({x}, {y}, {z})")
def step_impl(context, transform, v, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    results = getattr(context, transform) * getattr(context, v)
    assert results == tuples.Vector(x, y, z)


# Rotate X
@given("transformation {transform} ← rotation_x({radians})")
def step_impl(context, transform, radians):
    radians = float(radians)
    rotation_matrix = matrix.RotationXMatrix(radians)
    setattr(context, transform, rotation_matrix)


# Rotate Y
@given("transformation {transform} ← rotation_y({radians})")
def step_impl(context, transform, radians):
    radians = float(radians)
    rotation_matrix = matrix.RotationYMatrix(radians)
    setattr(context, transform, rotation_matrix)


# Rotate Z
@given("transformation {transform} ← rotation_z({radians})")
def step_impl(context, transform, radians):
    radians = float(radians)
    rotation_matrix = matrix.RotationZMatrix(radians)
    setattr(context, transform, rotation_matrix)


# Shearing
@given("transformation {transform} ← shearing({xy}, {xz}, {yx}, {yz}, {zx}, {zy})")
def step_impl(context, transform, xy, xz, yx, yz, zx, zy):
    xy = float(xy)
    xz = float(xz)
    yx = float(yx)
    yz = float(yz)
    zx = float(zx)
    zy = float(zy)
    shearing_matrix = matrix.ShearingMatrix(xy, xz, yx, yz, zx, zy)
    setattr(context, transform, shearing_matrix)


# Chaining transformations
@when("point {point1} ← {transform1} * {point2}")
def step_impl(context, point1, transform1, point2):
    results = getattr(context, transform1) * getattr(context, point2)
    setattr(context, point1, results)


@then("point {point} = point({x}, {y}, {z})")
def step_impl(context, point, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    assert getattr(context, point) == tuples.Point(x, y, z)


@when("transformation {transform1} ← {transform4} * {transform3} * {transform2}")
def step_impl(context, transform1, transform2, transform3, transform4):
    results = (
        getattr(context, transform4)
        * getattr(context, transform3)
        * getattr(context, transform2)
    )
    setattr(context, transform1, results)


# View transformation matrix
@when(
    "transformation {transform} ← view_transform({from_point}, {to_point}, {up_vector})"
)
def step_impl(context, transform, from_point, to_point, up_vector):
    from_point = getattr(context, from_point)
    to_point = getattr(context, to_point)
    up_vector = getattr(context, up_vector)
    results = camera.view_transform(from_point, to_point, up_vector)
    setattr(context, transform, results)
