import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import math
import ray_tracing
from ray_tracing.elements.tuples import Point, Vector, Color
from ray_tracing.elements.canvas import Canvas
from ray_tracing.elements.shape import Sphere
from ray_tracing.elements.rays import Ray
from ray_tracing.elements.lights import PointLight
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements as elements


def main():
    can_width = 200
    canvas = Canvas(can_width, can_width)
    white = Color(1, 1, 1)
    canvas.set_background(white)

    # sphere
    sphere = Sphere()
    sphere.material.color = Color(1, 0.2, 1)
    sphere.set_transform(matrix.ScalingMatrix(0.5, 1, 1))
    sphere.set_transform(
        matrix.ShearingMatrix(1, 0, 0, 0, 0, 0) * matrix.ScalingMatrix(0.5, 1, 1)
    )

    # light
    light_position = Point(-10, 10, -10)
    light_color = Color(1, 1, 1)
    light = PointLight(light_position, light_color)

    # ray
    ray_origin = Point(0, 0, -6)

    # wall
    wall_z = 10
    wall_size = 8

    # pixel_size
    pixel_size = wall_size / can_width

    red = Color(1, 0, 0)

    for y in range(can_width):
        world_y = wall_size / 2 - pixel_size * y
        for x in range(can_width):
            world_x = -wall_size / 2 + pixel_size * x
            position = Point(world_x, world_y, wall_z)
            ray = Ray(ray_origin, (position - ray_origin).normalize())
            xs = sphere.intersect(ray)
            if xs.hit():
                intersec_point = ray.position(xs.get_first_hit().t)
                intersect_object = xs.get_first_hit().shape
                normal = intersect_object.normal_at(intersec_point)
                eye = -ray.direction
                color = intersect_object.material.lighting(
                    light, intersec_point, eye, normal
                )
                canvas.write_pixel(x, y, color)

    canvas.save_to_file("./sphere_3d.ppm")


if __name__ == "__main__":
    main()
