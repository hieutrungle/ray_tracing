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
from behave import given, when, then


# Define a material
@given("material {name} ← material()")
def step_impl(context, name):
    setattr(context, name, materials.Material())


@then("material {name}.color = color({r}, {g}, {b})")
def step_impl(context, name, r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    material = getattr(context, name)
    assert material.color == tuples.Color(r, g, b)


@then("material {name}.ambient = {value}")
def step_impl(context, name, value):
    material = getattr(context, name)
    assert material.ambient == float(value)


@then("material {name}.diffuse = {value}")
def step_impl(context, name, value):
    material = getattr(context, name)
    assert material.diffuse == float(value)


@then("material {name}.specular = {value}")
def step_impl(context, name, value):
    material = getattr(context, name)
    assert material.specular == float(value)


@then("material {name}.shininess = {value}")
def step_impl(context, name, value):
    material = getattr(context, name)
    assert material.shininess == float(value)


# assign values to the material
@given("material {m}.ambient ← {value}")
def step_impl(context, m, value):
    material = getattr(context, m)
    material.ambient = float(value)


@then("material {m} = material()")
def step_impl(context, m):
    material = getattr(context, m)
    assert material == materials.Material()
