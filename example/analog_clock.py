import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import math
import ray_tracing
from ray_tracing.elements.tuples import Point, Vector, Color
from ray_tracing.elements.canvas import Canvas
from ray_tracing.elements import matrix


def main():
    can_width = 900
    canvas = Canvas(can_width, can_width)
    canter_point = Point(can_width / 2, can_width / 2, 0)
    radius = 3 / 8 * can_width
    red = Color(0.7, 0.3, 0.5)
    start_pos = Point(0, 1, 0)
    rotation = matrix.RotationZMatrix(math.pi / 6)
    scaling = matrix.ScalingMatrix(radius, radius, 1)
    translation = matrix.TranslationMatrix(canter_point.x(), canter_point.y(), 0)
    for i in range(12):
        rotation = matrix.RotationZMatrix(i * math.pi / 6)
        pos = translation * scaling * rotation * start_pos
        for j in [-2, -1, 0, 1, 2]:
            for k in [-2, -1, 0, 1, 2]:
                canvas.write_pixel(int(pos.x() + j), int(pos.y() + k), red)

    canvas.save_to_file("./analog_clock.ppm")


if __name__ == "__main__":
    main()
