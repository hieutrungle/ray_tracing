import numpy as np


class Tuple:
    """
    A tuple with 4 values
    """

    def __init__(self, x, y, z, w):
        self.tuple = (x, y, z, w)

    def __getitem__(self, index):
        return self.tuple[index]

    def __setitem__(self, index, value):
        self.tuple = list(self.tuple)
        self.tuple[index] = value
        self.tuple = tuple(self.tuple)

    def __eq__(self, other):
        return np.allclose(self.tuple, other.tuple)

    def __add__(self, other):
        return Tuple(*(a + b for a, b in zip(self.tuple, other.tuple)))

    def __sub__(self, other):
        return Tuple(*(a - b for a, b in zip(self.tuple, other.tuple)))

    def __neg__(self):
        return Tuple(*(-a for a in self.tuple))

    def __mul__(self, scalar):
        return Tuple(*(a * scalar for a in self.tuple))

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ZeroDivisionError
        return Tuple(*(a / scalar for a in self.tuple))

    def __abs__(self):
        return np.sqrt(sum(a * a for a in self.tuple))

    def __repr__(self):
        return (
            f"Tuple({self.tuple[0]}, {self.tuple[1]}, {self.tuple[2]}, {self.tuple[3]})"
        )

    def __str__(self):
        return (
            f"Tuple({self.tuple[0]}, {self.tuple[1]}, {self.tuple[2]}, {self.tuple[3]})"
        )

    def is_point(self):
        return self.tuple[3] == 1

    def is_vector(self):
        return self.tuple[3] == 0

    def set_tuple(self, x, y, z, w):
        self.tuple = (x, y, z, w)

    def magnitude(self):
        return np.sqrt(sum(a * a for a in self.tuple))

    def normalize(self):
        return self / self.magnitude()

    def dot(self, other):
        return sum(a * b for a, b in zip(self.tuple, other.tuple))

    def cross(self, other):
        if not self.is_vector() or not other.is_vector():
            raise ValueError("Cross product is only defined for vectors")
        return Vector(
            self.tuple[1] * other.tuple[2] - self.tuple[2] * other.tuple[1],
            self.tuple[2] * other.tuple[0] - self.tuple[0] * other.tuple[2],
            self.tuple[0] * other.tuple[1] - self.tuple[1] * other.tuple[0],
        )

    # def reflect(self, normal):
    #     return self - normal * 2 * self.dot(normal)


class Point(Tuple):
    """
    A point in 3D space
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1)

    def __repr__(self):
        return f"Point({self.tuple[0]}, {self.tuple[1]}, {self.tuple[2]})"

    def __str__(self):
        return f"Point({self.tuple[0]}, {self.tuple[1]}, {self.tuple[2]})"

    def __add__(self, other):
        results = super().__add__(other)
        return Point(results.tuple[0], results.tuple[1], results.tuple[2])

    def __sub__(self, other):
        results = super().__sub__(other)
        if isinstance(other, Point):
            return Vector(results.tuple[0], results.tuple[1], results.tuple[2])
        elif isinstance(other, Vector):
            return Point(results.tuple[0], results.tuple[1], results.tuple[2])

    def x(self):
        return self.tuple[0]

    def y(self):
        return self.tuple[1]

    def z(self):
        return self.tuple[2]

    def w(self):
        return 1

    def set_point(self, x, y, z):
        self.set_tuple(x, y, z, 1)


class Vector(Tuple):
    """
    A vector in 3D space
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0)

    def __repr__(self):
        return f"Vector({self.tuple[0]}, {self.tuple[1]}, {self.tuple[2]})"

    def __str__(self):
        return f"Vector({self.tuple[0]}, {self.tuple[1]}, {self.tuple[2]})"

    def __add__(self, other):
        results = super().__add__(other)
        if not isinstance(other, Vector):
            return Vector(results.tuple[0], results.tuple[1], results.tuple[2])
        elif isinstance(other, Point):
            return Point(results.tuple[0], results.tuple[1], results.tuple[2])

    def x(self):
        return self.tuple[0]

    def y(self):
        return self.tuple[1]

    def z(self):
        return self.tuple[2]

    def w(self):
        return 0

    def set_vector(self, x, y, z):
        self.set_tuple(x, y, z, 0)


class Color(Tuple):
    """
    A color in RGB space
    """

    def __init__(self, r, g, b, a=0):
        super().__init__(r, g, b, a)

    def __repr__(self):
        return (
            f"Color({self.tuple[0]}, {self.tuple[1]}, {self.tuple[2], self.tuple[3]})"
        )

    def __str__(self):
        return (
            f"Color({self.tuple[0]}, {self.tuple[1]}, {self.tuple[2], self.tuple[3]})"
        )

    def r(self):
        return self.tuple[0]

    def g(self):
        return self.tuple[1]

    def b(self):
        return self.tuple[2]

    def a(self):
        return self.tuple[3]

    def set_color(self, r, g, b, a=0):
        self.set_tuple(r, g, b, a)

    def hadamard_product(self, other):
        return Color(*[a * b for a, b in zip(self.tuple, other.tuple)])
