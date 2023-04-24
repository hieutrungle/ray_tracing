import numpy as np


class Tuple:
    """
    A tuple_t with 4 values
    """

    def __init__(self, x, y, z, w):
        self.tuple_t = (x, y, z, w)

    def __getitem__(self, index):
        return self.tuple_t[index]

    def __setitem__(self, index, value):
        self.tuple_t = list(self.tuple_t)
        self.tuple_t[index] = value
        self.tuple_t = tuple(self.tuple_t)

    def __eq__(self, other):
        return np.allclose(self.tuple_t, other.tuple_t)

    def __add__(self, other):
        return Tuple(*(a + b for a, b in zip(self.tuple_t, other.tuple_t)))

    def __sub__(self, other):
        return Tuple(*(a - b for a, b in zip(self.tuple_t, other.tuple_t)))

    def __neg__(self):
        return Tuple(*(-a for a in self.tuple_t))

    def __mul__(self, scalar):
        return Tuple(*(a * scalar for a in self.tuple_t))

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ZeroDivisionError
        return Tuple(*(a / scalar for a in self.tuple_t))

    def __abs__(self):
        magnitude = self.magnitude()
        return magnitude

    def __repr__(self):
        return f"Tuple({self.tuple_t[0]}, {self.tuple_t[1]}, {self.tuple_t[2]}, {self.tuple_t[3]})"

    def __str__(self):
        return f"Tuple({self.tuple_t[0]}, {self.tuple_t[1]}, {self.tuple_t[2]}, {self.tuple_t[3]})"

    def is_point(self):
        return self.tuple_t[3] == 1

    def is_vector(self):
        return self.tuple_t[3] == 0

    def set_tuple(self, x, y, z, w):
        self.tuple_t = (x, y, z, w)

    def magnitude(self):
        # normalize the first 3 values
        magnitude = 0
        for i in range(len(self.tuple_t) - 1):
            magnitude += self.tuple_t[i] ** 2
        magnitude = float(np.sqrt(magnitude))
        return magnitude

    def normalize(self):
        return self / self.magnitude()

    def dot(self, other):
        return sum(a * b for a, b in zip(self.tuple_t, other.tuple_t))

    def cross(self, other):
        if not self.is_vector() or not other.is_vector():
            raise ValueError("Cross product is only defined for vectors")
        return Vector(
            self.tuple_t[1] * other.tuple_t[2] - self.tuple_t[2] * other.tuple_t[1],
            self.tuple_t[2] * other.tuple_t[0] - self.tuple_t[0] * other.tuple_t[2],
            self.tuple_t[0] * other.tuple_t[1] - self.tuple_t[1] * other.tuple_t[0],
        )

    def round(self, precision=5):
        return Tuple(*(round(a, precision) for a in self.tuple_t))

    def to_point(self):
        return Point(self.tuple_t[0], self.tuple_t[1], self.tuple_t[2])

    def to_vector(self):
        return Vector(self.tuple_t[0], self.tuple_t[1], self.tuple_t[2])

    # def reflect(self, normal):
    #     return self - normal * 2 * self.dot(normal)


class Point(Tuple):
    """
    A point in 3D space
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1)

    def __repr__(self):
        return f"Point({self.tuple_t[0]}, {self.tuple_t[1]}, {self.tuple_t[2]})"

    def __str__(self):
        return f"Point({self.tuple_t[0]}, {self.tuple_t[1]}, {self.tuple_t[2]})"

    def __add__(self, other):
        results = super().__add__(other)
        return Point(results.tuple_t[0], results.tuple_t[1], results.tuple_t[2])

    def __sub__(self, other):
        results = super().__sub__(other)
        if isinstance(other, Point):
            return Vector(results.tuple_t[0], results.tuple_t[1], results.tuple_t[2])
        elif isinstance(other, Vector):
            return Point(results.tuple_t[0], results.tuple_t[1], results.tuple_t[2])

    def x(self):
        return self.tuple_t[0]

    def y(self):
        return self.tuple_t[1]

    def z(self):
        return self.tuple_t[2]

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
        return f"Vector({self.tuple_t[0]}, {self.tuple_t[1]}, {self.tuple_t[2]})"

    def __str__(self):
        return f"Vector({self.tuple_t[0]}, {self.tuple_t[1]}, {self.tuple_t[2]})"

    def __add__(self, other):
        results = super().__add__(other)
        if not isinstance(other, Vector):
            return Vector(results.tuple_t[0], results.tuple_t[1], results.tuple_t[2])
        elif isinstance(other, Point):
            return Point(results.tuple_t[0], results.tuple_t[1], results.tuple_t[2])

    def x(self):
        return self.tuple_t[0]

    def y(self):
        return self.tuple_t[1]

    def z(self):
        return self.tuple_t[2]

    def w(self):
        return 0

    def set_vector(self, x, y, z):
        self.set_tuple(x, y, z, 0)

    def reflect(self, normal: "Vector"):
        if not normal.is_vector():
            raise ValueError("Normal must be a vector")
        elif normal.magnitude() != 1:
            raise ValueError("Normal must be a unit vector")
        return self - normal * 2 * self.dot(normal)


class Color(Tuple):
    """
    A color in RGB space
    """

    def __init__(self, r, g, b, a=0):
        super().__init__(r, g, b, a)

    def __repr__(self):
        return f"Color({self.tuple_t[0]}, {self.tuple_t[1]}, {self.tuple_t[2], self.tuple_t[3]})"

    def __str__(self):
        return f"Color({self.tuple_t[0]}, {self.tuple_t[1]}, {self.tuple_t[2], self.tuple_t[3]})"

    def r(self):
        return self.tuple_t[0]

    def g(self):
        return self.tuple_t[1]

    def b(self):
        return self.tuple_t[2]

    def a(self):
        return self.tuple_t[3]

    def set_color(self, r, g, b, a=0):
        self.set_tuple(r, g, b, a)

    def hadamard_product(self, other):
        return Color(*[a * b for a, b in zip(self.tuple_t, other.tuple_t)])
