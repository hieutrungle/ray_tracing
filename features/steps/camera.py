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
from behave import given, when, then


# definition
@given("camera {c} ← camera({hsize}, {vsize}, {field_of_view})")
def step_impl(context, c, hsize, vsize, field_of_view):
    hsize = int(hsize)
    vsize = int(vsize)
    field_of_view = float(field_of_view)
    setattr(context, c, camera.Camera(hsize, vsize, field_of_view))


@given("camera {attr} ← {value}")
def step_impl(context, attr, value):
    value = float(value)
    setattr(context, attr, value)


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
