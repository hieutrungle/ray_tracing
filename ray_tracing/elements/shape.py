"""
This module contains the ShapeObject class.
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


class Intersection:
    """
    This class represents an intersection between a ray and a shape_object.
    """

    def __init__(self, t, shape_object):
        """
        Constructor for the Intersection class.
        """
        self.t = t
        self.shape_object = shape_object

    def __repr__(self):
        """
        Returns a string representation of the intersection.
        """
        return f"Intersection(t={self.t}, shape_object={self.shape_object})"

    def __eq__(self, other):
        """
        Checks if the intersection is equal to the other.
        """
        return self.t == other.t and self.shape_object == other.shape_object


class Intersections:
    """
    This class represents a collection of intersections.
    """

    def __init__(self, *intersections):
        """
        Constructor for the Intersections class.
        """
        self.intersections = list(intersections)

    def __repr__(self):
        """
        Returns a string representation of the intersections.
        """
        return f"Intersections({', '.join([str(i) for i in self.intersections])})"

    def __eq__(self, other):
        """
        Checks if the intersections are equal to the other.
        """
        return self.intersections == other.intersections

    def __getitem__(self, index):
        """
        Returns the intersection at the given index.
        """
        return self.intersections[index]

    def __len__(self):
        """
        Returns the number of intersections.
        """
        return len(self.intersections)

    def hit(self):
        """
        Returns the first intersection with a positive t value.
        """
        for i in self.intersections:
            if i.t > 0:
                return i
        return None

    def add(self, intersection):
        """
        Adds the given intersection to the collection.
        """
        self.intersections.append(intersection)

    def sort(self):
        """
        Sorts the intersections by t value.
        """
        self.intersections.sort(key=lambda i: i.t)

    def merge(self, other):
        """
        Merges the given intersections with this one.
        """
        self.intersections.extend(other.intersections)

    def remove(self, intersection):
        """
        Removes the given intersection from the collection.
        """
        self.intersections.remove(intersection)

    def remove_all(self):
        """
        Removes all intersections from the collection.
        """
        self.intersections = []

    def contains(self, intersection):
        """
        Checks if the collection contains the given intersection.
        """
        return intersection in self.intersections

    def count(self):
        """
        Returns the number of intersections in the collection.
        """
        return len(self.intersections)

    def all(self):
        """
        Returns all intersections in the collection.
        """
        return self.intersections

    def any(self):
        """
        Returns True if the collection contains any intersections.
        """
        return len(self.intersections) > 0

    def all_positive(self):
        """
        Returns True if all intersections have a positive t value.
        """
        for intersection in self.intersections:
            if intersection.t < 0:
                return False


class ShapeObject:
    """
    This class represents a shape in 3D space.
    """

    def __init__(self, transform=matrix.IdentityMatrix(4), id=None):
        """
        Constructor for the ShapeObject class.
        """
        self.transform = transform
        if id is None:
            self.id = utils.generate_uuid()
        else:
            self.id = id

    def translate(self, x, y, z):
        """
        Translates the shape by the given values.
        """
        self.transform = matrix.translation(x, y, z) * self.transform

    def scale(self, x, y, z):
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


class Sphere(ShapeObject):
    """
    This class represents a sphere in 3D space.
    """

    def __init__(self, radius=1, transform=matrix.IdentityMatrix(4), id=None):
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
        intersection_1 = Intersection(t1, self)
        intersection_2 = Intersection(t2, self)
        intersections = Intersections(intersection_1, intersection_2)
        return intersections

    def local_normal_at(self, point):
        """
        Returns the normal of the sphere at the given point.
        """
        return point - tuples.Point(0, 0, 0)
