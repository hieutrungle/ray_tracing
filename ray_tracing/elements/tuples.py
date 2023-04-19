import numpy as np


class Tuple:
    """
    A tuple with 4 coordinates
    """

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other):
        return np.allclose(
            [self.x, self.y, self.z, self.w], [other.x, other.y, other.z, other.w]
        )

    def __add__(self, other):
        new_tuple = Tuple(
            self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w
        )
        if new_tuple.w != 1 and new_tuple.w != 0:
            raise ValueError(
                "Tuple addition results in a tuple with w not being 1 or 0"
            )
        return new_tuple

    def __sub__(self, other):
        new_tuple = Tuple(
            self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w
        )
        if new_tuple.w != 1 and new_tuple.w != 0:
            raise ValueError(
                "Tuple subtraction results in a tuple with w not being 1 or 0"
            )
        return new_tuple

    def __neg__(self):
        return Tuple(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, scalar):
        return Tuple(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ZeroDivisionError
        return Tuple(self.x / scalar, self.y / scalar, self.z / scalar, self.w / scalar)

    def __abs__(self):
        return np.sqrt(self * self)

    def __repr__(self):
        return f"Tuple({self.x}, {self.y}, {self.z}, {self.w})"

    def __str__(self):
        return f"Tuple({self.x}, {self.y}, {self.z}, {self.w})"

    # sum of all coordinates
    def cumsum(self):
        return self.x + self.y + self.z + self.w

    def is_vector(self):
        return self.w == 0

    def is_point(self):
        return self.w == 1

    def magnitude(self):
        return np.sqrt(
            self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w
        )

    def normalize(self):
        return self * (1 / self.magnitude())

    def dot(self, other):
        if isinstance(other, Tuple):
            return (
                self.x * other.x
                + self.y * other.y
                + self.z * other.z
                + self.w * other.w
            )
        else:
            raise TypeError("Can only dot a tuple with another tuple")

    def cross(self, other):
        if self.is_vector() and other.is_vector():
            return Vector(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            )
        elif not self.is_vector():
            raise TypeError(
                "Can only perform the cross product on vectors. {self} is not a vector."
            )
        elif not other.is_vector():
            raise TypeError(
                "Can only perform the cross product on vectors. {other} is not a vector."
            )
        else:
            raise TypeError("Can only perform the cross product on vectors.")


class Point(Tuple):
    """
    A point in 3D space
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1)


class Vector(Tuple):
    """
    A vector in 3D space
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0)


