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


# ray initialization
@when("ray {name} ← ray({origin}, {direction})")
def step_impl(context, name, origin, direction):
    ray_origin = getattr(context, origin)
    ray_direction = getattr(context, direction)
    setattr(context, name, ray.Ray(ray_origin, ray_direction))


@then("ray {name}.{attribute} = {attribute}")
def step_impl(context, name, attribute):
    ray = getattr(context, name)
    ray_attribute = getattr(ray, attribute)
    assert ray_attribute == getattr(context, attribute)


# position
@given("ray {name} ← ray(point({x1}, {y1}, {z1}), vector({x2}, {y2}, {z2}))")
def step_impl(context, name, x1, y1, z1, x2, y2, z2):
    x1 = float(x1)
    y1 = float(y1)
    z1 = float(z1)
    x2 = float(x2)
    y2 = float(y2)
    z2 = float(z2)
    setattr(context, name, ray.Ray(tuples.Point(x1, y1, z1), tuples.Vector(x2, y2, z2)))


@then("ray position({name}, {t}) = point({x}, {y}, {z})")
def step_impl(context, name, t, x, y, z):
    ray = getattr(context, name)
    t = float(t)
    x = float(x)
    y = float(y)
    z = float(z)
    assert ray.position(t) == tuples.Point(x, y, z)


# ray transformation
@when("ray {name2} ← transform({name1}, {m})")
def step_impl(context, name1, name2, m):
    ray = getattr(context, name1)
    matrix = getattr(context, m)
    setattr(context, name2, ray.transform(matrix))


@then("ray {name1}.origin = point({x1}, {y1}, {z1})")
def step_impl(context, name1, x1, y1, z1):
    ray = getattr(context, name1)
    x1 = float(x1)
    y1 = float(y1)
    z1 = float(z1)
    assert ray.origin == tuples.Point(x1, y1, z1)


@then("ray {name1}.direction = vector({x1}, {y1}, {z1})")
def step_impl(context, name1, x1, y1, z1):
    ray = getattr(context, name1)
    x1 = float(x1)
    y1 = float(y1)
    z1 = float(z1)
    assert ray.direction == tuples.Vector(x1, y1, z1)
