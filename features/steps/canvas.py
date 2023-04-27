import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.canvas as canvas
from ray_tracing.utils.constants import *
from behave import given, when, then


# canvas
@given("can ← canvas({width}, {height})")
def step_impl(context, width, height):
    context.can = canvas.Canvas(int(width), int(height))


# representation
@then("can.{attribute} = {value}")
def step_impl(context, attribute, value):
    assert getattr(context.can, attribute) == int(value)


@then("every pixel of can is color({r}, {g}, {b})")
def step_impl(context, r, g, b):
    for row in context.can.pixels:
        for pixel in row:
            assert pixel == canvas.Color(float(r), float(g), float(b))


# writing pixels
@given("red ← color({r}, {g}, {b})")
def step_impl(context, r, g, b):
    context.red = canvas.Color(float(r), float(g), float(b))


@when("write_pixel(can, {x}, {y}, red)")
def step_impl(context, x, y):
    context.can.write_pixel(int(x), int(y), context.red)


@when("write_pixel(can, {x}, {y}, c{num})")
def step_impl(context, x, y, num):
    color = getattr(context, f"c{num}")
    context.can.write_pixel(int(x), int(y), color)


@when("ppm ← canvas_to_ppm(can)")
def step_impl(context):
    context.ppm = context.can.to_ppm()


# canvas to ppm
@then("pixel_at(can, {x}, {y}) = red")
def step_impl(context, x, y):
    assert context.can.pixel_at(int(x), int(y)) == context.red


@then("pixel_at({can}, {x}, {y}) = color({r}, {g}, {b})")
def step_impl(context, can, x, y, r, g, b):
    canvas_pixel = getattr(context, can).pixel_at(int(x), int(y))
    print(f"canvas_pixel: {canvas_pixel}")
    assert canvas_pixel == canvas.Color(float(r), float(g), float(b))


@then("lines {start}-{stop} of ppm are")
def step_impl(context, start, stop):
    start = int(start) - 1
    stop = int(stop) - 1
    ppm_lines = context.ppm.splitlines()
    for i, line in enumerate(context.text.splitlines()):
        assert ppm_lines[i + start] == line
        if i + start == stop:
            break


# splitting long lines
@when("every pixel of can is set to color({r}, {g}, {b})")
def step_impl(context, r, g, b):
    for i in range(context.can.width):
        for j in range(context.can.height):
            context.can.write_pixel(i, j, canvas.Color(float(r), float(g), float(b)))


# terminate with new line character
@then("ppm ends with a newline character")
def step_impl(context):
    assert context.ppm[-1] == "\n"
