import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.matrix as matrix

# import ray_tracing.elements.tuples as tuples
import ray_tracing.scene.camera as camera
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# definition
@given("camera {c} ← camera({hsize}, {vsize}, {field_of_view})")
def step_impl(context, c, hsize, vsize, field_of_view):
    hsize = int(hsize)
    vsize = int(vsize)
    field_of_view = float(field_of_view)
    setattr(context, c, camera.Camera(hsize, vsize, field_of_view))


@given("camera hsize ← {hsize}")
def step_impl(context, hsize):
    hsize = int(hsize)
    setattr(context, "hsize", hsize)


@given("camera vsize ← {vsize}")
def step_impl(context, vsize):
    vsize = int(vsize)
    setattr(context, "vsize", vsize)


@given("camera field_of_view ← {field_of_view}")
def step_impl(context, field_of_view):
    field_of_view = float(field_of_view)
    setattr(context, "field_of_view", field_of_view)


@when("camera {c} ← camera({hsize}, {vsize}, {field_of_view})")
def step_impl(context, c, hsize, vsize, field_of_view):
    hsize = int(getattr(context, hsize))
    vsize = int(getattr(context, vsize))
    field_of_view = float(getattr(context, field_of_view))
    setattr(context, c, camera.Camera(hsize, vsize, field_of_view))


@then("camera {c}.hsize = {hsize}")
def step_impl(context, c, hsize):
    hsize = int(hsize)
    assert getattr(context, c).hsize == hsize


@then("camera {c}.vsize = {vsize}")
def step_impl(context, c, vsize):
    vsize = int(vsize)
    assert getattr(context, c).vsize == vsize


@then("camera {c}.field_of_view = {field_of_view}")
def step_impl(context, c, field_of_view):
    field_of_view = float(field_of_view)
    assert getattr(context, c).field_of_view == field_of_view


@then("camera {c}.transform = identity_matrix")
def step_impl(context, c):
    assert getattr(context, c).transform == matrix.IdentityMatrix()


# pixel size of camera
@then("camera {c}.pixel_size = {pixel_size}")
def step_impl(context, c, pixel_size):
    pixel_size = float(pixel_size)
    results = getattr(context, c).pixel_size
    print(results)
    assert utils.equal(results, pixel_size)


# ray for pixel
@when("camera {r} ← ray_for_pixel({c}, {px}, {py})")
def step_impl(context, r, c, px, py):
    px = int(px)
    py = int(py)
    c = getattr(context, c)
    setattr(context, r, c.ray_for_pixel(px, py))


@when("camera {c}.transform ← rotation_y({radians}) * translation({x}, {y}, {z})")
def step_impl(context, c, radians, x, y, z):
    radians = float(radians)
    x = float(x)
    y = float(y)
    z = float(z)
    rotation = matrix.RotationYMatrix(radians)
    translation = matrix.TranslationMatrix(x, y, z)
    c = getattr(context, c)
    setattr(c, "transform", rotation * translation)


# render
@given("camera {c}.transform ← view_transform({from_point}, {to_point}, {up_vector})")
def step_impl(context, c, from_point, to_point, up_vector):
    from_point = getattr(context, from_point)
    to_point = getattr(context, to_point)
    up_vector = getattr(context, up_vector)
    results = camera.view_transform(from_point, to_point, up_vector)
    c = getattr(context, c)
    setattr(c, "transform", results)


@when("camera {image} ← render({c}, {w})")
def step_impl(context, image, c, w):
    c = getattr(context, c)
    w = getattr(context, w)
    setattr(context, image, c.render(w))
