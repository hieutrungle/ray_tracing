"""
This module contains the ShapeObject class.
"""
from __future__ import annotations
import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

from ray_tracing.utils.constants import *
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.rays as rays
from typing import List
import typing

if typing.TYPE_CHECKING:
    import ray_tracing.elements.shapes as shapes


class IntersectionComputations:
    """
    Computation properties for an intersection.
    """

    def __init__(
        self,
        t: float,
        shape,
        point: tuples.Point,
        eye_vector: tuples.Vector,
        normal_vector: tuples.Vector,
        inside: bool = False,
    ):
        """
        Constructor for the IntersectionComputations class.
        """
        self.t = t
        self.shape = shape
        self.point = point
        self.over_point = point + normal_vector * EPSILON
        self.eye_vector = eye_vector
        self.normal_vector = normal_vector
        self.inside = inside

    def get_t(self):
        """
        Returns the t-value of the intersection.
        """
        return self.t

    def get_object(self):
        """
        Returns the object that was intersected.
        """
        return self.shape

    def get_point(self):
        """
        Returns the point of intersection.
        """
        return self.point

    def get_eye_vector(self):
        """
        Returns the eye vector.
        """
        return self.eye_vector

    def get_normal_vector(self):
        """
        Returns the normal vector.
        """
        return self.normal_vector

    def is_inside(self):
        """
        Returns whether the intersection is inside the object.
        """
        return self.inside


class Intersection:
    """
    This class represents an intersection between a ray and a shape.
    """

    def __init__(self, t: float, shape: shapes.Shape):
        """
        Constructor for the Intersection class.
        """
        self.t = t
        self.shape = shape

    def get_object(self):
        """
        Returns the object that was intersected.
        """
        return self.shape

    def get_t(self):
        """
        Returns the t-value of the intersection.
        """
        return self.t

    def __repr__(self):
        """
        Returns a string representation of the intersection.
        """
        return f"Intersection(t={self.t}, shape={self.shape})"

    def __eq__(self, other: "Intersection"):
        """
        Checks if the intersection is equal to the other.
        """
        return self.t == other.t and self.shape == other.shape

    def prepare_computations(self, ray: rays.Ray):
        """
        Prepares the computations for the intersection.
        """
        point = ray.position(self.t)
        eye_vector = -ray.direction
        normal_vector = self.shape.normal_at(point)
        if normal_vector.dot(eye_vector) < 0:
            inside = True
            normal_vector = -normal_vector
        else:
            inside = False
        return IntersectionComputations(
            self.t,
            self.shape,
            point,
            eye_vector,
            normal_vector,
            inside,
        )


class Intersections:
    """
    This class represents a collection of intersections.
    """

    def __init__(self, *intersections: List[Intersection]):
        """
        Constructor for the Intersections class.
        """
        self.intersections = list(intersections)
        self.first_hit = self.hit()

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

    def __add__(self, other):
        """
        Returns the union of the two collections.
        """
        return Intersections(*self.intersections, *other.intersections)

    def hit(self):
        """
        Returns the first intersection with a positive t value.
        """
        if self.any():
            self.sort()
            for intersection in self.intersections:
                if intersection.t > 0:
                    return intersection
        return None

    def get_first_hit(self):
        """
        Returns the first intersection with a positive t value.
        """
        if self.any():
            return self.first_hit
        return None

    def add(self, intersection: Intersection):
        """
        Adds the given intersection to the collection.
        """
        self.intersections.append(intersection)
        self.hit()

    def add_all(self, *intersections: List[Intersection]):
        """
        Adds the given intersections to the collection.
        """
        self.intersections.extend(intersections)
        self.hit()

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
        self.hit()

    def remove(self, intersection: Intersection):
        """
        Removes the given intersection from the collection.
        """
        self.intersections.remove(intersection)

    def remove_all(self):
        """
        Removes all intersections from the collection.
        """
        self.intersections = []

    def contains(self, intersection: Intersection):
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
