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
import ray_tracing.elements.lights as lights
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


# intersect world
@given("world {w} ← default_world()")
def step_impl(context, w):
    setattr(context, w, world.DefaultWorld())


@when("world {xs} ← intersect_world({w}, {r})")
def step_impl(context, xs, w, r):
    w = getattr(context, w)
    r = getattr(context, r)
    setattr(context, xs, w.intersect_world(r))


# shading intersection
@given("world {shape} ← the first object in {w}")
def step_impl(context, shape, w):
    w = getattr(context, w)
    setattr(context, shape, w.objects[0])


@given("world {shape} ← the second object in {w}")
def step_impl(context, shape, w):
    w = getattr(context, w)
    setattr(context, shape, w.objects[1])


@given("world {w}.light ← point_light(point({x}, {y}, {z}), color({r}, {g}, {b}))")
def step_impl(context, w, x, y, z, r, g, b):
    x = float(x)
    y = float(y)
    z = float(z)
    r = float(r)
    g = float(g)
    b = float(b)
    w = getattr(context, w)
    new_light = lights.PointLight(tuples.Point(x, y, z), tuples.Color(r, g, b))
    w.replace_lights(new_light)


@when("world {c} ← shade_hit({w}, {comps})")
def step_impl(context, c, w, comps):
    w = getattr(context, w)
    comps = getattr(context, comps)
    setattr(context, c, w.shade_hit(comps))


# color at world intersection
@when("world {c} ← color_at({w}, {r})")
def step_impl(context, c, w, r):
    w = getattr(context, w)
    r = getattr(context, r)
    print(w.color_at(r))
    setattr(context, c, w.color_at(r))


@given("world {obj}.material.ambient ← 1")
def step_impl(context, obj):
    obj = getattr(context, obj)
    obj.get_material().ambient = 1


@then("world {c} = {obj}.material.color")
def step_impl(context, c, obj):
    c = getattr(context, c)
    obj = getattr(context, obj)
    assert c == obj.get_material().color


# shadows
@then("world is_shadowed({w}, {p}) is {is_shadowed}")
def step_impl(context, w, p, is_shadowed):
    w = getattr(context, w)
    p = getattr(context, p)
    is_shadowed = utils.str_to_bool(is_shadowed)
    assert w.is_shadowed(p) == is_shadowed


# render shadows
@given("world {shape} is added to {w}")
def step_impl(context, shape, w):
    wor = getattr(context, w)
    shape = getattr(context, shape)
    wor.add_object(shape)
    setattr(context, w, wor)
