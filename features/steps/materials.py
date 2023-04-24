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
import ray_tracing.elements.material as material
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


# Define a material
@given("material {name} ← material()")
def step_impl(context, name):
    setattr(context, name, material.Material())


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
