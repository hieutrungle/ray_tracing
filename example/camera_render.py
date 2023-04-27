import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import math
import ray_tracing.elements.tuples as tuples
import ray_tracing.scene.camera as camera
import ray_tracing.scene.world as world
import ray_tracing.elements.shapes as shapes
import ray_tracing.elements.lights as lights
import ray_tracing.elements.materials as materials
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements as elements


def main():
    floor = shapes.Sphere()
    floor.transform = matrix.ScalingMatrix(10, 0.01, 10)
    floor.material = materials.Material(color=tuples.Color(1, 0.9, 0.9), specular=0)

    left_wall = shapes.Sphere()
    left_wall.transform = (
        matrix.TranslationMatrix(0, 0, 5)
        * matrix.RotationYMatrix(-math.pi / 4)
        * matrix.RotationXMatrix(math.pi / 2)
        * matrix.ScalingMatrix(10, 0.01, 10)
    )
    left_wall.material = floor.material

    right_wall = shapes.Sphere()
    right_wall.transform = (
        matrix.TranslationMatrix(0, 0, 5)
        * matrix.RotationYMatrix(math.pi / 4)
        * matrix.RotationXMatrix(math.pi / 2)
        * matrix.ScalingMatrix(10, 0.01, 10)
    )
    right_wall.material = floor.material

    middle = shapes.Sphere()
    middle.transform = matrix.TranslationMatrix(-0.5, 1, 0.5)
    middle.material = materials.Material(
        color=tuples.Color(0.1, 1, 0.5), diffuse=0.7, specular=0.3
    )

    right = shapes.Sphere()
    right.transform = matrix.TranslationMatrix(1.5, 0.5, -0.5) * matrix.ScalingMatrix(
        0.5, 0.5, 0.5
    )
    right.material = materials.Material(
        color=tuples.Color(0.5, 1, 0.1), diffuse=0.7, specular=0.3
    )

    left = shapes.Sphere()
    left.transform = matrix.TranslationMatrix(-1.5, 0.33, -0.75) * matrix.ScalingMatrix(
        0.33, 0.33, 0.33
    )
    left.material = materials.Material(
        color=tuples.Color(1, 0.8, 0.1), diffuse=0.7, specular=0.3
    )

    w = world.World()
    w.add_object([floor, left_wall, right_wall, middle, right, left])
    w.add_light(
        [lights.PointLight(tuples.Point(-10, 10, -10), tuples.Color(0.2, 0.1, 0.32))]
    )
    w.add_light(
        [lights.PointLight(tuples.Point(10, 10, -10), tuples.Color(0.5, 0.5, 0.5))]
    )

    cam = camera.Camera(200, 100, math.pi / 3)
    from_point = tuples.Point(0, 1.5, -5)
    to_point = tuples.Point(0, 1, 0)
    up_vector = tuples.Vector(0.4, 0.5, 0.1)
    cam.transform = camera.view_transform(from_point, to_point, up_vector)

    image = cam.render(w)
    image.save_to_file("./camera_render.ppm")


if __name__ == "__main__":
    main()
