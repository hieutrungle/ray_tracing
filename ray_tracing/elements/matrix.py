"""
Matrices for ray tracing.
"""

import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import numpy as np
import math
import ray_tracing.elements.tuples as tuples
import ray_tracing.utils.utils as utils


class Matrix:
    """
    Matrix for ray tracing.
    """

    def __init__(self, entry_list):
        self.matrix = entry_list
        self.rows = len(entry_list)
        self.columns = len(entry_list[0])
        self.shape = (self.rows, self.columns)

    def __getitem__(self, index):
        i, j = index
        return self.matrix[i][j]

    def __setitem__(self, index, value):
        i, j = index
        self.matrix[i][j] = value

    def __repr__(self):
        texts = ""
        for row in self.matrix:
            texts += str(row) + "\n"
        return texts

    def __eq__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            return False
        for i in range(self.rows):
            for j in range(self.columns):
                if not utils.equal(self.matrix[i][j], other.matrix[i][j]):
                    return False
        return True

    def __neq__(self, other):
        return not self.__eq__(other)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            results = self.matrix_multiplication(other)
        elif isinstance(other, (int, float)):
            results = self.scalar_multiplication(other)
        elif isinstance(other, tuples.Tuple):
            results = self.tuple_multiplication(other)
            if results.is_point():
                results = tuples.Point(results[0], results[1], results[2])
            elif results.is_vector():
                results = tuples.Vector(results[0], results[1], results[2])
        return results

    def matrix_multiplication(self, other):
        """
        Matrix multiplication.
        """

        # np implementation
        results = np.array(self.matrix) @ np.array(other.matrix)
        results = results.tolist()

        # naive implementation without optimization
        # results = []
        # for i in range(self.rows):
        #     row = []
        #     for j in range(other.columns):
        #         entry = 0
        #         for k in range(self.columns):
        #             entry += self.matrix[i][k] * other.matrix[k][j]
        #         row.append(entry)
        #     results.append(row)
        return Matrix(results)

    def scalar_multiplication(self, other):
        """
        Scalar multiplication.
        """

        # np implementation
        results = np.array(self.matrix) * other
        results = results.tolist()

        # naive implementation without optimization
        # results = []
        # for i in range(self.rows):
        #     row = []
        #     for j in range(self.columns):
        #         row.append(self.matrix[i][j] * other)
        #     results.append(row)
        return Matrix(results)

    def tuple_multiplication(self, other):
        """
        Tuple multiplication.
        """

        # np implementation
        tuple_in_matrix_form = [element for element in other]
        tuple_in_matrix_form = np.array(tuple_in_matrix_form)[np.newaxis].T
        results = np.array(self.matrix) @ tuple_in_matrix_form
        results = results.T.tolist()[0]

        # naive implementation without optimization
        # results = []
        # for i in range(self.rows):
        #     entry = 0
        #     for j in range(self.columns):
        #         entry += self.matrix[i][j] * other[j]
        #     results.append(entry)
        return tuples.Tuple(results[0], results[1], results[2], results[3])

    def transpose(self):
        """
        Transpose the matrix.
        """

        # np implementation
        results = np.array(self.matrix).T.tolist()

        # naive implementation without optimization
        # results = []
        # for i in range(self.columns):
        #     row = []
        #     for j in range(self.rows):
        #         row.append(self.matrix[j][i])
        #     results.append(row)
        return Matrix(results)

    def determinant(self):
        """
        Calculate the determinant of the matrix.
        """

        if self.rows != self.columns:
            raise ValueError("The matrix is not square.")

        if self.rows == 2:
            det = (
                self.matrix[0][0] * self.matrix[1][1]
                - self.matrix[0][1] * self.matrix[1][0]
            )
        else:
            det = 0
            for i in range(self.columns):
                det = det + self.matrix[0][i] * self.cofactor(0, i)
        return det

    def submatrix(self, row_idx, column_idx):
        """
        Calculate the submatrix of the matrix.
        Remove the row_idx and column_idx of the matrix.
        """

        results = []
        for i in range(self.rows):
            if i == row_idx:
                continue
            row = []
            for j in range(self.columns):
                if j == column_idx:
                    continue
                row.append(self.matrix[i][j])
            results.append(row)
        return Matrix(results)

    def minor(self, row_idx, column_idx):
        """
        Calculate the minor of the matrix.
        """

        return self.submatrix(row_idx, column_idx).determinant()

    def cofactor(self, row_idx, column_idx):
        """
        Calculate the cofactor of the matrix.
        """

        minor = self.minor(row_idx, column_idx)
        if (row_idx + column_idx) % 2 == 0:
            return minor
        else:
            return -minor

    def is_invertible(self):
        """
        Check if the matrix is invertible.
        """

        return self.determinant() != 0

    def inverse(self):
        """
        Calculate the inverse of the matrix.
        """

        if not self.is_invertible():
            raise ValueError("The matrix is not invertible.")

        det = self.determinant()
        results = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                cofactor = self.cofactor(i, j)
                row.append(float(cofactor / det))
            results.append(row)
        return Matrix(results).transpose()

    def round_matrix(self, digits=4):
        """
        Round the matrix.
        """

        results = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(round(self.matrix[i][j], digits))
            results.append(row)
        return Matrix(results)


class IdentityMatrix(Matrix):
    """
    Identity matrix.
    """

    def __init__(self, size=4):
        entry_list = []
        for i in range(size):
            row = []
            for j in range(size):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            entry_list.append(row)
        super().__init__(entry_list)


class TranslationMatrix(Matrix):
    def __init__(self, x, y, z):
        super().__init__([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])


class ScalingMatrix(Matrix):
    def __init__(self, x, y, z):
        super().__init__([[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])


class RotationXMatrix(Matrix):
    def __init__(self, angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        super().__init__(
            [[1, 0, 0, 0], [0, cos, -sin, 0], [0, sin, cos, 0], [0, 0, 0, 1]]
        )


class RotationYMatrix(Matrix):
    def __init__(self, angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        super().__init__(
            [[cos, 0, sin, 0], [0, 1, 0, 0], [-sin, 0, cos, 0], [0, 0, 0, 1]]
        )


class RotationZMatrix(Matrix):
    def __init__(self, angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        super().__init__(
            [[cos, -sin, 0, 0], [sin, cos, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        )


class RotationMatrix(Matrix):
    def __init__(self, angle_x, angle_y, angle_z, order="xyz"):
        x_rotation = RotationXMatrix(angle_x)
        y_rotation = RotationYMatrix(angle_y)
        z_rotation = RotationZMatrix(angle_z)
        if order == "xyz":
            super().__init__(z_rotation * y_rotation * x_rotation)
        elif order == "xzy":
            super().__init__(y_rotation * z_rotation * x_rotation)
        elif order == "yxz":
            super().__init__(z_rotation * x_rotation * y_rotation)
        elif order == "yzx":
            super().__init__(x_rotation * z_rotation * y_rotation)
        elif order == "zxy":
            super().__init__(y_rotation * x_rotation * z_rotation)
        elif order == "zyx":
            super().__init__(x_rotation * y_rotation * z_rotation)


class ShearingMatrix(Matrix):
    def __init__(self, xy, xz, yx, yz, zx, zy):
        super().__init__(
            [
                [1, xy, xz, 0],
                [yx, 1, yz, 0],
                [zx, zy, 1, 0],
                [0, 0, 0, 1],
            ]
        )
