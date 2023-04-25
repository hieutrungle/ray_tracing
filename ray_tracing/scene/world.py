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
import ray_tracing.elements.materials as materials
import ray_tracing.elements.shape as shape
import ray_tracing.operations.intersection as intersection
import ray_tracing.utils.utils as utils


class World:
    """
    This class represents the world in which the scene is rendered
    """

    def __init__(self):
        self.objects = []
        self.lights = []

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

    def add_object(self, obj):
        """
        Adds an object to the world
        """
        self.objects.append(obj)

    def add_light(self, light):
        """
        Adds a light to the world
        """
        self.lights.append(light)

    def intersect_world(self, ray):
        """
        Intersects the world with a ray
        """
        intersections = intersection.Intersections()
        for obj in self.objects:
            intersections += obj.intersect(ray)
        return intersections

    def shade_hit(self, comps, remaining=5):
        """
        Shades a hit with the world
        """
        shadowed = self.is_shadowed(comps.over_point)
        surface = comps.object.material.lighting(
            comps.object,
            self.lights,
            comps.over_point,
            comps.eyev,
            comps.normalv,
            shadowed,
        )
        reflected = self.reflected_color(comps, remaining)
        refracted = self.refracted_color(comps, remaining)
        material = comps.object.material
        if material.reflective > 0 and material.transparency > 0:
            reflectance = comps.schlick()
            return surface + reflected * reflectance + refracted * (1 - reflectance)
        else:
            return surface + reflected + refracted

    def color_at(self, ray, remaining=5):
        """
        Returns the color at a ray
        """
        intersections = self.intersect_world(ray)
        hit = intersection.hit(intersections)
        if hit is None:
            return BLACK
        else:
            comps = hit.prepare_computations(ray)
            return self.shade_hit(comps, remaining)

    def is_shadowed(self, point):
        """
        Checks if a point is shadowed
        """
        v = self.lights[0].position - point
        distance = np.linalg.norm(v)
        direction = v / distance
        r = rays.Ray(point, direction)
        intersections = self.intersect_world(r)
        hit = intersection.hit(intersections)
        if hit is not None and hit.t < distance:
            return True
        else:
            return False

    def reflected_color(self, comps, remaining=5):
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

    def contains_object(self, obj):
        """
        Checks if the world contains an object
        """
        return obj in self.objects

    def contains_light(self, light):
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
