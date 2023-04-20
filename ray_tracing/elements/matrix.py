"""
Matrices for ray tracing.
"""

import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, package_path)

import numpy as np
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
        tuple_in_matrix_form = np.array(other.tuple)[np.newaxis].T
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

    def __init__(self, size):
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
