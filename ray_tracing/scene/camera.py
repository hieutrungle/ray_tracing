"""
This module contains the Camera class
"""

import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import math
from ray_tracing.utils.constants import *
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.matrix as matrix

# import ray_tracing.elements.rays as rays
# import ray_tracing.elements.lights as lights
# import ray_tracing.elements.materials as materials
# import ray_tracing.elements.shape as shape
# import ray_tracing.operations.intersection as intersection
# import ray_tracing.utils.utils as utils


def view_transform(
    from_point: tuples.Point, to_point: tuples.Point, up_vector: tuples.Vector
):
    """
    Returns the view transformation matrix
    """
    forward = (to_point - from_point).normalize()
    up_normalized = up_vector.normalize()
    left = forward.cross(up_normalized)
    true_up = left.cross(forward)
    orientation = matrix.Matrix(
        [
            [left.x(), left.y(), left.z(), 0],
            [true_up.x(), true_up.y(), true_up.z(), 0],
            [-forward.x(), -forward.y(), -forward.z(), 0],
            [0, 0, 0, 1],
        ]
    )
    return orientation * matrix.TranslationMatrix(
        -from_point.x(), -from_point.y(), -from_point.z()
    )


class Camera:
    """
    This class represents a camera in 3D space
    """

    def __init__(
        self,
        hsize: int,
        vsize: int,
        field_of_view: float,
        transform: matrix.Matrix = matrix.IdentityMatrix(4),
    ):
        """
        Constructor for the Camera class
        """
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view
        self.transform = transform
        self.pixel_size = self._calculate_pixel_size()
        self.half_width = 0
        self.half_height = 0
        self._calculate_half_width_and_height()

    def __str__(self):
        """
        Returns a string representation of the camera
        """
        return f"Camera(hsize={self.hsize}, vsize={self.vsize}, field_of_view={self.field_of_view}, transform={self.transform})"

    def __repr__(self):
        """
        Returns a string representation of the camera
        """
        return f"Camera(hsize={self.hsize}, vsize={self.vsize}, field_of_view={self.field_of_view}, transform={self.transform})"

    def __eq__(self, other):
        """
        Checks if two cameras are equal
        """
        return (
            self.hsize == other.hsize
            and self.vsize == other.vsize
            and self.field_of_view == other.field_of_view
            and self.transform == other.transform
        )

    def _calculate_pixel_size(self):
        """
        Calculates the size of a pixel
        """
        half_view = math.tan(self.field_of_view / 2)
        aspect = self.hsize / self.vsize
        if aspect >= 1:
            half_width = half_view
            half_height = half_view / aspect
        else:
            half_width = half_view * aspect
            half_height = half_view
        return (half_width * 2) / self.hsize

    def _calculate_half_width_and_height(self):
        """
        Calculates the half width and height of the camera
        """
        half_view = math.tan(self.field_of_view / 2)
        aspect = self.hsize / self.vsize
        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view
