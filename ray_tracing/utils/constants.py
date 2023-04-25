import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import ray_tracing.elements.tuples as tuples

EPSILON = 1e-6
OBJECT_COUNT = 0
BLACK = tuples.Color(0.0, 0.0, 0.0)
WHITE = tuples.Color(1.0, 1.0, 1.0)
ORIGIN = tuples.Point(0.0, 0.0, 0.0)
