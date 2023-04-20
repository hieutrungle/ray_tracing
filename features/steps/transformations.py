import os
import sys
import math

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
package_path = os.path.abspath(os.path.join(package_path, ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.tuples as tuples
from ray_tracing.utils.constants import *
import ray_tracing.utils.utils as utils
from behave import given, when, then
