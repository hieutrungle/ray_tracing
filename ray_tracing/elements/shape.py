"""
This module contains the Shape class.
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
import ray_tracing.utils.utils as utils


class Shape:
    """
    This class represents a shape in 3D space.
    """

    def __init__(self, id=OBJECT_COUNT, transform=matrix.IdentityMatrix(4)):
        """
        Constructor for the Shape class.
        """
        self.transform = transform
        self.id = id

    def local_intersect(self, ray):
        """
        Intersects the shape with the given ray.
        """
        raise NotImplementedError("local_intersect not implemented.")

    def local_normal_at(self, point):
        """
        Returns the normal of the shape at the given point.
        """
        raise NotImplementedError("local_normal_at not implemented.")

    def intersect(self, ray):
        """
        Intersects the shape with the given ray.
        """
        ray = ray.transform(self.transform.inverse())
        return self.local_intersect(ray)

    def normal_at(self, point):
        """
        Returns the normal of the shape at the given point.
        """
        local_point = self.world_to_object(point)
        local_normal = self.local_normal_at(local_point)
        world_normal = self.normal_to_world(local_normal)
        return world_normal

    def world_to_object(self, point):
        """
        Transforms the given point from world space to object space.
        """
        return self.transform.inverse() * point

    def normal_to_world(self, normal):
        """
        Transforms the given normal from object space to world space.
        """
        object_normal = self.transform.inverse().transpose() * normal
        object_normal.w = 0
        return object_normal.normalize()


class Sphere(Shape):
    """
    This class represents a sphere in 3D space.
    """

    def __init__(self, radius=1, id=OBJECT_COUNT, transform=matrix.IdentityMatrix(4)):
        """
        Constructor for the Sphere class.
        """
        super().__init__(id=id, transform=transform)
        self.radius = radius

    def local_intersect(self, ray):
        """
        Intersects the sphere with the given ray.
        """
        sphere_to_ray = ray.origin - tuples.Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return []

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return [t1, t2]

    def local_normal_at(self, point):
        """
        Returns the normal of the sphere at the given point.
        """
        return point - tuples.Point(0, 0, 0)
