import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.shape as shape
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.light as light
import ray_tracing.elements.ray as ray
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# Define a point light
@given("light {intensity} ← color({r}, {g}, {b})")
def step_impl(context, intensity, r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    setattr(context, intensity, tuples.Color(r, g, b))


@given("light {position} ← point({x}, {y}, {z})")
def step_impl(context, position, x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    setattr(context, position, tuples.Point(x, y, z))


@when("light {name} ← point_light({position}, {intensity})")
def step_impl(context, name, position, intensity):
    light_position = getattr(context, position)
    light_intensity = getattr(context, intensity)
    setattr(context, name, light.PointLight(light_position, light_intensity))


@then("light {name}.{attribute} = {attribute}")
def step_impl(context, name, attribute):
    light = getattr(context, name)
    light_attribute = getattr(light, attribute)
    print(f"light: {light}")
    print(f"light atributte: {light_attribute}")
    print(f"given context atributte: {getattr(context, attribute)}")
    assert light_attribute == getattr(context, attribute)
