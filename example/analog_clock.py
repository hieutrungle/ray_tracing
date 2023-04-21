import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import ray_tracing
from ray_tracing.elements.tuples import Point, Vector, Color
from ray_tracing.elements.canvas import Canvas
from ray_tracing.elements import matrix

def main():
    pass

if __name__=="__main__":
    main()