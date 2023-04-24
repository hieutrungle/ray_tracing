import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import math
import ray_tracing
from ray_tracing.elements.tuples import Point, Vector, Color
from ray_tracing.elements.canvas import Canvas
from ray_tracing.elements.shape import Sphere
from ray_tracing.elements.ray import Ray
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements as elements


def main():
    can_width = 100
    canvas = Canvas(can_width, can_width)
    white = Color(1, 1, 1)
    canvas.set_background(white)

    sphere_o = Sphere()
    # sphere_o.set_transform(matrix.ScalingMatrix(0.5, 1, 1))
    sphere_o.set_transform(
        matrix.ShearingMatrix(1, 0, 0, 0, 0, 0) * matrix.ScalingMatrix(0.5, 1, 1)
    )

    # ray
    ray_origin = Point(-1, 1, -6)

    # wall
    wall_z = 10
    wall_size = 10

    # pixel_size
    pixel_size = wall_size / can_width

    red = Color(1, 0, 0)

    for y in range(can_width):
        world_y = wall_size / 2 - pixel_size * y
        for x in range(can_width):
            world_x = -wall_size / 2 + pixel_size * x
            position = Point(world_x, world_y, wall_z)
            r = Ray(ray_origin, (position - ray_origin).normalize())
            xs = sphere_o.intersect(r)
            # print(f"xs: {xs}")
            if xs.hit():
                canvas.write_pixel(x, y, red)

    canvas.save_to_file("./sphere_shadow.ppm")


if __name__ == "__main__":
    main()