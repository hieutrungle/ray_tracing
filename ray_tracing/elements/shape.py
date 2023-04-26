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
import ray_tracing.elements.materials as materials
import ray_tracing.elements.rays as rays
import ray_tracing.operations.intersection as intersection
import ray_tracing.utils.utils as utils


class Shape:
    """
    This class represents a shape in 3D space.
    """

    def __init__(
        self, transform=matrix.IdentityMatrix(4), material=materials.Material(), id=None
    ):
        """
        Constructor for the Shape class.
        """
        self.transform = transform
        self.material = material
        if id is None:
            self.id = utils.generate_uuid()
        else:
            self.id = id

    def __str__(self):
        """
        Returns a string representation of the shape.
        """
        return (
            f"Shape(id={self.id}, transform={self.transform}, material={self.material})"
        )

    def __repr__(self):
        """
        Returns a string representation of the shape.
        """
        return (
            f"Shape(id={self.id}, transform={self.transform}, material={self.material})"
        )

    def __eq__(self, other):
        """
        Checks if two shapes are equal.
        """
        return self.transform == other.transform and self.material == other.material

    def set_transform(self, transform):
        """
        Sets the transform of the shape.
        """
        self.transform = transform

    def get_transform(self):
        """
        Returns the transform of the shape.
        """
        return self.transform

    def set_material(self, material):
        """
        Sets the material of the shape.
        """
        self.material = material

    def get_material(self):
        """
        Returns the material of the shape.
        """
        return self.material

    def translate(self, x, y, z):
        """
        Translates the shape by the given values.
        """
        self.transform = matrix.translation(x, y, z) * self.transform

    def scale(self, x: float, y, z):
        """
        Scales the shape by the given values.
        """
        self.transform = matrix.scaling(x, y, z) * self.transform

    def rotate_x(self, r):
        """
        Rotates the shape around the x-axis by the given value.
        """
        self.transform = matrix.rotation_x(r) * self.transform

    def rotate_y(self, r):
        """
        Rotates the shape around the y-axis by the given value.
        """
        self.transform = matrix.rotation_y(r) * self.transform

    def rotate_z(self, r):
        """
        Rotates the shape around the z-axis by the given value.
        """
        self.transform = matrix.rotation_z(r) * self.transform

    def rotate(self, angle_x=0, angle_y=0, angle_z=0, order="xyz"):
        """
        Rotates the shape around the given axes by the given values.
        """
        self.transform = (
            matrix.rotation(angle_x, angle_y, angle_z, order) * self.transform
        )

    def shear(self, xy, xz, yx, yz, zx, zy):
        """
        Shears the shape by the given values.
        """
        self.transform = matrix.shearing(xy, xz, yx, yz, zx, zy) * self.transform

    def local_intersect(self, ray: rays.Ray):
        """
        Intersects the shape with the given ray.
        """
        raise NotImplementedError("local_intersect not implemented.")

    def local_normal_at(self, point: tuples.Point):
        """
        Returns the normal of the shape at the given point.
        """
        raise NotImplementedError("local_normal_at not implemented.")

    def intersect(self, ray: rays.Ray):
        """
        Intersects the shape with the given ray.
        """
        ray = ray.transform(self.transform.inverse())
        return self.local_intersect(ray)

    def normal_at(self, point: tuples.Point) -> tuples.Vector:
        """
        Returns the normal of the shape at the given point.
        """
        local_point = self.world_to_object(point)
        local_normal = self.local_normal_at(local_point)
        world_normal = self.normal_to_world(local_normal)
        return world_normal

    def world_to_object(self, point: tuples.Point):
        """
        Transforms the given point from world space to object space.
        """
        return self.transform.inverse() * point

    def normal_to_world(self, normal: tuples.Vector):
        """
        Transforms the given normal from object space to world space.
        """
        object_normal = self.transform.inverse().transpose()
        object_normal = object_normal * normal
        object_normal = object_normal.to_vector()
        return object_normal.normalize()


class Sphere(Shape):
    """
    This class represents a sphere in 3D space.
    """

    def __init__(
        self,
        radius: float = 1.0,
        transform=matrix.IdentityMatrix(4),
        material=materials.Material(),
        id=None,
    ):
        """
        Constructor for the Sphere class.
        """
        super().__init__(id=id, transform=transform, material=material)
        self.radius = radius

    def __repr__(self):
        return f"Sphere(id={self.id}, radius={self.radius}, transform=\n{self.transform}, material={self.material})"

    def local_intersect(self, ray: rays.Ray):
        """
        Intersects the sphere with the given ray.
        """
        sphere_to_ray = ray.origin - tuples.Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return intersection.Intersections()

        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        intersection_1 = intersection.Intersection(t1, self)
        intersection_2 = intersection.Intersection(t2, self)
        intersections = intersection.Intersections(intersection_1, intersection_2)
        return intersections

    def local_normal_at(self, point: tuples.Point):
        """
        Returns the normal of the sphere at the given point.
        """
        return point - tuples.Point(0, 0, 0)
