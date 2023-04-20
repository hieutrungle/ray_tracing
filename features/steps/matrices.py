import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.canvas as canvas
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then


@given("the following 4x4 matrix M")
def step_impl(context):
    context.M = utils.matrix_from_list(context.table)


@then("M[{row},{column}] = {value}")
def step_impl(context, row, column, value):
    assert context.M[int(row)][int(column)] == float(value)
