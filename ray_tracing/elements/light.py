"""
This module contains the Light.
"""

import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import numpy as np
import math
from ray_tracing.utils.constants import *
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.ray as ray
import ray_tracing.operations.intersection as intersection
import ray_tracing.elements.material as material
import ray_tracing.utils.utils as utils


class Light:
    """
    This class represents a light.
    """

    def __init__(self, position: tuples.Point, intensity: tuples.Color):
        """
        Constructor for the Light class.
        """
        self.position = position
        self.intensity = intensity

    def __repr__(self):
        """
        Returns a string representation of the light.
        """
        return f"Light(position={self.position}, intensity={self.intensity})"

    def __eq__(self, other):
        """
        Checks if the light is equal to the other.
        """
        return self.position == other.position and self.intensity == other.intensity

    def lighting(
        self,
        shape_object,
        point: tuples.Point,
        eye_vector: tuples.Vector,
        normal_vector: tuples.Vector,
        in_shadow=False,
    ):
        """
        Calculates the lighting at the given point.
        """
        if isinstance(shape_object.material, material.Material):
            color = shape_object.material.color
            ambient = color * self.intensity
            if in_shadow:
                return ambient

            light_vector = (self.position - point).normalize()
            light_dot_normal = light_vector.dot(normal_vector)
            if light_dot_normal < 0:
                diffuse = BLACK
                specular = BLACK
            else:
                diffuse = color * self.intensity * light_dot_normal

                reflect_vector = (-light_vector).reflect(normal_vector)
                reflect_dot_eye = reflect_vector.dot(eye_vector)
                if reflect_dot_eye <= 0:
                    specular = BLACK
                else:
                    factor = math.pow(reflect_dot_eye, shape_object.material.shininess)
                    specular = self.intensity * shape_object.material.specular * factor

            return ambient + diffuse + specular
        else:
            return BLACK

    def is_shadowed(self, world, point: tuples.Point):
        """
        Checks if the point is in shadow.
        """
        v = self.position - point
        distance = v.magnitude()
        direction = v.normalize()

        r = ray.Ray(point, direction)
        intersections = world.intersect(r)
        hit = intersections.hit()
        if hit is not None and hit.t < distance:
            return True
        else:
            return False


class PointLight(Light):
    """
    This class represents a point light.
    """

    def __init__(
        self, position: tuples.Point = ORIGIN, intensity: tuples.Color = WHITE
    ):
        """
        Constructor for the PointLight class.
        """
        super().__init__(position, intensity)

    def __repr__(self):
        """
        Returns a string representation of the point light.
        """
        return f"PointLight(position={self.position}, intensity={self.intensity})"

    def __eq__(self, other):
        """
        Checks if the point light is equal to the other.
        """
        return super().__eq__(other)

    def lighting(
        self,
        shape_object,
        point: tuples.Point,
        eye_vector: tuples.Vector,
        normal_vector: tuples.Vector,
        in_shadow=False,
    ):
        """
        Calculates the lighting at the given point.
        """
        return super().lighting(
            shape_object, point, eye_vector, normal_vector, in_shadow
        )

    def is_shadowed(self, world, point: tuples.Point):
        """
        Checks if the point is in shadow.
        """
        return super().is_shadowed(world, point)
