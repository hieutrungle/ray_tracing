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

# import ray_tracing.elements.shape as shapeobject
import ray_tracing.elements.tuples as tuples
import ray_tracing.utils.utils as utils
from typing import List


class Intersection:
    """
    This class represents an intersection between a ray and a shape_object.
    """

    def __init__(self, t: float, shape_object):
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

    def hit(self):
        """
        Returns the first intersection with a positive t value.
        """
        if self.any():
            self.sort()
            for i in self.intersections:
                if i.t > 0:
                    return i
        return None

    def add(self, intersection: Intersection):
        """
        Adds the given intersection to the collection.
        """
        self.intersections.append(intersection)
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
