"""
This module contains the Camera class
"""
from __future__ import annotations
import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import math
from ray_tracing.utils.constants import *
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.rays as rays
import ray_tracing.elements.canvas as canvas


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
        self.half_width = 0
        self.half_height = 0
        self._calculate_half_width_and_height()
        self.pixel_size = self._calculate_pixel_size()

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

    def _calculate_pixel_size(self):
        """
        Calculates the pixel size of the camera
        """
        return (self.half_width * 2) / self.hsize

    def ray_for_pixel(self, px: int, py: int):
        """
        Returns the ray for a given pixel
        """
        # the offset from the edge of the canvas to the pixel's center
        x_offset = (px + 0.5) * self.pixel_size
        y_offset = (py + 0.5) * self.pixel_size

        # the untransformed coordinates of the pixel in world space.
        # (remember that the camera looks toward -z, so +x is to the *left*.)
        world_x = self.half_width - x_offset
        world_y = self.half_height - y_offset

        # using the camera matrix, transform the canvas point and the origin,
        # and then compute the ray's direction vector.
        # (remember that the canvas is at z=-1)
        pixel = self.transform.inverse() * tuples.Point(world_x, world_y, -1)
        origin = self.transform.inverse() * tuples.Point(0, 0, 0)
        direction = (pixel - origin).normalize()
        return rays.Ray(origin, direction)

    def render(self, world):
        """
        Renders the world from the camera's perspective
        """
        image = canvas.Canvas(self.hsize, self.vsize)
        for y in range(self.vsize):
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray)
                image.write_pixel(x, y, color)
        return image
