import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import numpy as np
import ray_tracing.elements.matrix as matrix
import ray_tracing.utils.utils as utils


