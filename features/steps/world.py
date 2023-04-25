import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.shape as shape
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.rays as rays
import ray_tracing.elements.materials as materials
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
import ray_tracing.scene.world as world
from behave import given, when, then


# definition
@given("world {w} ← world()")
def step_impl(context, w):
    setattr(context, w, world.World())


@then("world {w} contains no objects")
def step_impl(context, w):
    assert getattr(context, w).num_objects() == 0


@then("world {w} has no light source")
def step_impl(context, w):
    assert getattr(context, w).num_lights() == 0


# default world
@when("world {w} ← default_world()")
def step_impl(context, w):
    setattr(context, w, world.DefaultWorld())


@then("world {w}.light = {light}")
def step_impl(context, w, light):
    w = getattr(context, w)
    light = getattr(context, light)
    assert w.lights[0] == light


@then("world {w} contains {obj}")
def step_impl(context, w, obj):
    w = getattr(context, w)
    obj = getattr(context, obj)
    assert w.contains_object(obj)
