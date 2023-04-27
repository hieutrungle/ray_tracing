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
import ray_tracing.elements.rays as rays
import ray_tracing.operations.intersection as intersection
import ray_tracing.elements.materials as materials
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
        material,
        point: tuples.Point,
        eye_vector: tuples.Vector,
        normal_vector: tuples.Vector,
        in_shadow=False,
    ):
        """
        Calculates the lighting at the given point.
        """
        resulting_color = BLACK
        if isinstance(material, materials.Material):
            # combine the surface color with the light's color/intensity by hadamard multiplication
            effective_color = material.color * self.intensity
            # compute the ambient contribution
            ambient = effective_color * material.ambient

            if in_shadow:
                resulting_color = ambient
            else:
                # find the direction to the light source
                light_vector = (self.position - point).normalize()
                # light_dot_normal represents the cosine of the angle between the
                # light vector and the normal vector. A negative number means the
                # light is on the other side of the surface.
                light_dot_normal = light_vector.dot(normal_vector)
                if light_dot_normal < 0:
                    diffuse = BLACK
                    specular = BLACK
                else:
                    # compute the diffuse contribution
                    diffuse = effective_color * material.diffuse * light_dot_normal

                    # reflect_dot_eye represents the cosine of the angle between the
                    # reflection vector and the eye vector. A negative number means the
                    # light reflects away from the eye.
                    reflect_vector = (-light_vector).reflect(normal_vector)
                    reflect_dot_eye = reflect_vector.dot(eye_vector)
                    if reflect_dot_eye <= 0:
                        specular = BLACK
                    else:
                        # compute the specular contribution
                        factor = reflect_dot_eye**material.shininess
                        specular = self.intensity * material.specular * factor
                resulting_color = ambient + diffuse + specular

        return resulting_color


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
