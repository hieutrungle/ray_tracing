"""
This module contains the World class
"""
from __future__ import annotations
import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

from typing import List, Union
import numpy as np
import math
from ray_tracing.utils.constants import *
import ray_tracing.elements.tuples as tuples
import ray_tracing.elements.matrix as matrix
import ray_tracing.elements.rays as rays
import ray_tracing.elements.lights as lights
import ray_tracing.elements.materials as materials
import ray_tracing.elements.shape as shape
import typing
import ray_tracing.operations.intersection as intersection


class World:
    """
    This class represents the world in which the scene is rendered
    """

    def __init__(self):
        self.objects = []
        self.lights = []

    def __eq__(self, other):
        return self.objects == other.objects and self.lights == other.lights

    def __str__(self):
        return "World(objects={}, lights={})".format(self.objects, self.lights)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.objects, self.lights))

    def __copy__(self):
        return World(self.objects, self.lights)

    def __deepcopy__(self, memo):
        return World(self.objects, self.lights)

    def __getstate__(self):
        return (self.objects, self.lights)

    def __setstate__(self, state):
        self.objects, self.lights = state

    def __len__(self):
        return len(self.objects) + len(self.lights)

    def __iter__(self):
        return iter(self.objects + self.lights)

    def __getitem__(self, key):
        return (
            self.objects[key]
            if key < len(self.objects)
            else self.lights[key - len(self.objects)]
        )

    def __setitem__(self, key, value):
        if key < len(self.objects):
            self.objects[key] = value
        else:
            self.lights[key - len(self.objects)] = value

    def __delitem__(self, key):
        if key < len(self.objects):
            del self.objects[key]
        else:
            del self.lights[key - len(self.objects)]

    def __contains__(self, item):
        return item in self.objects or item in self.lights

    def __add__(self, other):
        return World(self.objects + other.objects, self.lights + other.lights)

    def __iadd__(self, other):
        self.objects += other.objects
        self.lights += other.lights
        return self

    def num_objects(self):
        """
        Returns the number of objects in the world
        """
        return len(self.objects)

    def num_lights(self):
        """
        Returns the number of lights in the world
        """
        return len(self.lights)

    def add_object(self, obj: Union[shape.Shape, List[shape.Shape]]):
        """
        Adds an object to the world
        """
        if isinstance(obj, shape.Shape):
            self.objects.append(obj)
        elif isinstance(obj, list):
            self.objects += obj
        else:
            raise TypeError("Invalid type for object")

    def add_light(self, light: Union[lights.Light, List[lights.Light]]):
        """
        Adds a light to the world
        """
        if isinstance(light, lights.Light):
            self.lights.append(light)
        elif isinstance(light, list):
            self.lights += light
        else:
            raise TypeError("Invalid type for light")

    def replace_lights(self, new_lights: Union[List[lights.Light], lights.Light]):
        """
        Replaces the lights in the world
        """
        if isinstance(new_lights, lights.Light):
            self.lights = [new_lights]
        elif isinstance(new_lights, list):
            self.lights = new_lights
        else:
            raise TypeError("Invalid type for lights")

    def replace_objects(self, new_objects: Union[List[shape.Shape], shape.Shape]):
        """
        Replaces the objects in the world
        """
        if isinstance(new_objects, shape.Shape):
            self.objects = [new_objects]
        elif isinstance(new_objects, list):
            self.objects = new_objects
        else:
            raise TypeError("Invalid type for objects")

    def intersect_world(self, ray: rays.Ray) -> intersection.Intersections:
        """
        Intersects the world with a ray
        """
        intersections = intersection.Intersections()
        for obj in self.objects:
            intersections += obj.intersect(ray)
        return intersections

    def shade_hit(
        self, comps: intersection.IntersectionComputations, remaining: int = 5
    ):
        """
        Shades a hit with the world
        """
        surface = BLACK
        for light in self.lights:
            in_shadow = self.is_shadowed(comps.over_point)
            surface += light.lighting(
                comps.get_object().material,
                comps.get_point(),
                comps.get_eye_vector(),
                comps.get_normal_vector(),
                in_shadow,
            )
        # reflected = self.reflected_color(comps, remaining)
        # refracted = self.refracted_color(comps, remaining)
        # material = comps.object.material
        # if material.reflective > 0 and material.transparency > 0:
        #     reflectance = comps.schlick()
        #     return surface + reflected * reflectance + refracted * (1 - reflectance)
        # else:
        #     return surface + reflected + refracted
        return surface

    def color_at(self, ray: rays.Ray, remaining: int = 5):
        """
        Returns the color at a ray
        """
        intersections = self.intersect_world(ray)
        hit = intersections.get_first_hit()
        if hit is None:
            return BLACK
        else:
            comps = hit.prepare_computations(ray)
            return self.shade_hit(comps, remaining)

    def is_shadowed(self, point: tuples.Point):
        """
        Checks if a point is shadowed
        """
        # checking for the first light only
        v = self.lights[0].position - point
        distance = v.magnitude()
        direction = v.normalize()
        r = rays.Ray(point, direction)
        intersections = self.intersect_world(r)
        if (
            intersections is not None
            and intersections.get_first_hit() is not None
            and intersections.get_first_hit().get_t() < distance
        ):
            return True
        else:
            return False

    def reflected_color(
        self, comps: intersection.IntersectionComputations, remaining: int = 5
    ):
        """
        Returns the reflected color
        """
        if comps.object.material.reflective == 0 or remaining == 0:
            return BLACK
        else:
            reflect_ray = rays.Ray(comps.over_point, comps.reflectv)
            color = self.color_at(reflect_ray, remaining - 1)
            return color * comps.object.material.reflective

    def refracted_color(self, comps, remaining=5):
        """
        Returns the refracted color
        """
        if comps.object.material.transparency == 0 or remaining == 0:
            return BLACK
        else:
            n_ratio = comps.n1 / comps.n2
            cos_i = np.dot(comps.eyev, comps.normalv)
            sin2_t = n_ratio**2 * (1 - cos_i**2)
            if sin2_t > 1:
                return BLACK
            cos_t = math.sqrt(1 - sin2_t)
            direction = comps.normalv * (n_ratio * cos_i - cos_t) - comps.eyev * n_ratio
            refract_ray = rays.Ray(comps.under_point, direction)
            return (
                self.color_at(refract_ray, remaining - 1)
                * comps.object.material.transparency
            )

    def render(self, camera):
        """
        Renders the world
        """
        image = camera.render(self)
        return image

    def contains_object(self, obj: shape.Shape):
        """
        Checks if the world contains an object
        """
        return obj in self.objects

    def contains_light(self, light: lights.Light):
        """
        Checks if the world contains a light
        """
        return light in self.lights


class DefaultWorld(World):
    """
    A default world
    """

    def __init__(self):
        super().__init__()
        self.objects = [
            shape.Sphere(
                material=materials.Material(
                    color=tuples.Color(0.8, 1.0, 0.6),
                    diffuse=0.7,
                    specular=0.2,
                )
            ),
            shape.Sphere(
                transform=matrix.ScalingMatrix(0.5, 0.5, 0.5),
            ),
        ]
        self.lights = [
            lights.PointLight(
                position=tuples.Point(-10, 10, -10),
                intensity=tuples.Color(1, 1, 1),
            )
        ]
