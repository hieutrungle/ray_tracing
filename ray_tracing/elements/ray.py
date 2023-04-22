"""
This module contains the Ray class.
"""

import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import numpy as np
import math
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.matrix as matrix
import ray_tracing.utils.utils as utils


class Ray:
    """
    This class represents a ray in 3D space.
    """

    def __init__(self, origin: tuples.Point, direction: tuples.Vector):
        """
        Constructor for the Ray class.

        :param origin: The origin of the ray.
        :param direction: The direction of the ray.
        """
        if not origin.is_point():
            raise ValueError("Origin is not a point.")
        if not direction.is_vector():
            raise ValueError("direction is not a vector.")
        self.origin = origin
        self.direction = direction

    def position(self, t: float) -> tuples.Point:
        """
        Returns the position of the ray at time t.

        :param t: The time at which to calculate the position.
        :return: The position of the ray at time t.
        """
        # new_point = self.origin + self.direction * t
        return self.origin + self.direction * t

    def transform(self, trans: matrix.Matrix):
        """
        Transforms the ray by the given matrix.

        :param matrix: The matrix to transform the ray by.
        :type matrix: matrix.Matrix
        :return: The transformed ray.
        :rtype: Ray
        """
        return Ray(trans * self.origin, trans * self.direction)

    def __eq__(self, other):
        """
        Compares two rays for equality.

        :param other: The other ray to compare to.
        :type other: Ray
        :return: True if the rays are equal, false otherwise.
        :rtype: bool
        """
        return self.origin == other.origin and self.direction == other.direction

    def __repr__(self):
        """
        Returns a string representation of the ray.

        :return: A string representation of the ray.
        :rtype: str
        """
        return f"Ray(origin={self.origin}, direction={self.direction})"

    def __str__(self):
        """
        Returns a string representation of the ray.

        :return: A string representation of the ray.
        :rtype: str
        """
        return f"Ray(origin={self.origin}, direction={self.direction})"

    def local_intersect(self, ray):
        """
        Intersects the sphere with the given ray.
        """
        