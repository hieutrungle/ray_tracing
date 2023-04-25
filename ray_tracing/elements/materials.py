"""
This module contains the Material class
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
import ray_tracing.elements.lights as lights
import ray_tracing.operations.intersection as intersection
import ray_tracing.utils.utils as utils


class Material:
    """
    This class represents a material.
    """

    def __init__(
        self,
        color: tuples.Color = WHITE,
        ambient: float = 0.1,
        diffuse: float = 0.9,
        specular: float = 0.9,
        shininess: float = 200.0,
    ):
        """
        Constructor for the Material class.
        """
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def __repr__(self):
        """
        Returns a string representation of the material.
        """
        return f"Material(color={self.color}, ambient={self.ambient}, diffuse={self.diffuse}, specular={self.specular}, shininess={self.shininess})"

    def __eq__(self, other):
        """
        Checks if the material is equal to the other.
        """
        return (
            self.color == other.color
            and self.ambient == other.ambient
            and self.diffuse == other.diffuse
            and self.specular == other.specular
            and self.shininess == other.shininess
        )

    def lighting(
        self,
        light: lights.Light,
        point: tuples.Point,
        eye_vector: tuples.Vector,
        normal_vector: tuples.Vector,
        in_shadow=False,
    ):
        """
        Calculates the lighting at the given point.
        """
        if isinstance(light, lights.Light):
            color = self.color
            ambient = color * self.ambient
            if in_shadow:
                return ambient
            else:
                light_vector = (light.position - point).normalize()
                light_dot_normal = light_vector.dot(normal_vector)
                if light_dot_normal < 0:
                    diffuse = BLACK
                    specular = BLACK
                else:
                    diffuse = color * self.diffuse * light_dot_normal
                    reflect_vector = (-light_vector).reflect(normal_vector)
                    reflect_dot_eye = reflect_vector.dot(eye_vector)
                    if reflect_dot_eye <= 0:
                        specular = BLACK
                    else:
                        factor = reflect_dot_eye**self.shininess
                        specular = light.intensity * self.specular * factor
                return ambient + diffuse + specular
        else:
            raise TypeError("The light must be a Light object.")

    # def lighting(
    #     self,
    #     light: Light,
    #     point: tuples.Point,
    #     eye_vector: tuples.Vector,
    #     normal_vector: tuples.Vector,
    #     in_shadow=False,
    # ):
    #     """
    #     Calculates the lighting at the given point.
    #     """
    #     if isinstance(light, Light):
    #         color = self.color
    #         ambient = color * self.ambient
