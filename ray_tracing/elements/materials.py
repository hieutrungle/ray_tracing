"""
This module contains the Material class
"""
from __future__ import annotations
import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

from ray_tracing.utils.constants import *
import ray_tracing.elements.tuples as tuples
import typing

if typing.TYPE_CHECKING:
    import ray_tracing.elements.lights as lights


class Material:
    """
    This class represents a material.
    """

    def __init__(
        self,
        color: tuples.Color = WHITE,
        ambient: float = 0.1,
        diffuse: float = 0.9,
        specular: float = 0.9,
        shininess: float = 200.0,
    ):
        """
        Constructor for the Material class.
        """
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def set_material_properties(self, **kwargs):
        """
        Sets the material properties.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the material.
        """
        return f"Material(color={self.color}, ambient={self.ambient}, diffuse={self.diffuse}, specular={self.specular}, shininess={self.shininess})"

    def __repr__(self):
        """
        Returns a string representation of the material.
        """
        return f"Material(color={self.color}, ambient={self.ambient}, diffuse={self.diffuse}, specular={self.specular}, shininess={self.shininess})"

    def __eq__(self, other):
        """
        Checks if the material is equal to the other.
        """
        return (
            self.color == other.color
            and self.ambient == other.ambient
            and self.diffuse == other.diffuse
            and self.specular == other.specular
            and self.shininess == other.shininess
        )
