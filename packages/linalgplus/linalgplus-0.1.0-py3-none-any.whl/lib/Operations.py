from typing import Union
from lib.Core import Matrix
import copy


class Operations:

    @staticmethod
    def transpose(m: Matrix) -> Matrix:
        """
        Transposes the given matrix.
        """

        arr = [[m.data[j][i]
                for j in range(m.shape[0])] for i in range(m.shape[1])]

        return Matrix(arr)

    @staticmethod
    def scalar_multiply(m: Matrix, scalar: Union[int, float]) -> Matrix:
        """
        Multiplies each element of the matrix by the given scalar.
        """

        deep_copy = [[col * scalar for col in row] for row in m.data]
        return Matrix(deep_copy)

    @staticmethod
    def scalar_add(m: Matrix, scalar: Union[int, float]) -> Matrix:
        """
        Adds the given scalar to each element of the matrix.
        """

        deep_copy = [[col + scalar for col in row] for row in m.data]
        return Matrix(deep_copy)

    @staticmethod
    def scalar_sub(m: Matrix, scalar: Union[int, float]) -> Matrix:
        """
        Subtracts the given scalar from each element of the matrix.
        """

        deep_copy = [[col - scalar for col in row] for row in m.data]
        return Matrix(deep_copy)

    @staticmethod
    def subtract(m1: Matrix, m2: Matrix) -> Matrix:
        """
        Subtracts the second matrix from the first matrix.
        The matrices must have the same shape.
        """
        if m1.shape != m2.shape:
            raise ValueError("Matrix shapes do not match")

        copy = [[0] * m1.shape[1] for _ in range(m1.shape[0])]

        for i in range(m1.shape[0]):
            for j in range(m1.shape[1]):
                copy[i][j] = m1.data[i][j] - m2.data[i][j]

        return Matrix(copy)

    @staticmethod
    def add(m1: Matrix, m2: Matrix) -> Matrix:
        """
        Adds the second matrix to the first matrix.
        The matrices must have the same shape.
        """
        if m1.shape != m2.shape:
            raise ValueError("Matrix shapes do not match")

        copy = [[0] * m1.shape[1] for _ in range(m1.shape[0])]

        for i in range(m1.shape[0]):
            for j in range(m1.shape[1]):
                copy[i][j] = m1.data[i][j] + m2.data[i][j]

        return Matrix(copy)

    @staticmethod
    def determinant(m: Matrix) -> Union[int, float]:
        """
        Calculates the determinant of the given matrix.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        # base case for 2x2 matrix
        if m.shape[0] == 2 and m.shape[1] == 2:
            # determinant of a 2x2 matrix is ad - bc
            # | a b |
            # | c d |
            # det = a*d - b*c
            return m.data[0][0] * m.data[1][1] - m.data[0][1] * m.data[1][0]

        if m.shape[0] == 1 and m.shape[1] == 1:
            # determinant of a 1x1 matrix is the value itself
            return m.data[0][0]

        det = 0
        # find minor matrix by removing the first row and i-th column
        for j in range(m.shape[1]):
            minor = Matrix(data=[row[:j] + row[j + 1:]
                                 for row in m.data[1:]])
            # determinant of the minor matrix
            det += Operations.determinant(minor) * \
                m.data[0][j] * (-1) ** (0 + j)

        return det

    @staticmethod
    def multiply(m1: Matrix, m2: Matrix) -> Matrix:
        """
        Multiplies two matrices.
        The number of columns in the first matrix must be equal to the number of rows in the second matrix.
        """
        if m1.shape[1] != m2.shape[0]:
            raise ValueError("matrix shape dont match")

        copy = [[0] * m2.shape[1] for _ in range(m1.shape[0])]
        m2_t = Operations.transpose(m2)

        for i in range(m1.shape[0]):
            for j in range(m2.shape[1]):
                row = m1.data[i]
                col = m2_t.data[j]
                copy[i][j] = sum([x * y for x, y in zip(row, col)])

        return Matrix(copy)

    @staticmethod
    def identity(size: int) -> Matrix:
        """
        Create an identity matrix of given size
        """
        return Matrix([
            [1 if i == j else 0 for j in range(size)]
            for i in range(size)
        ])

    @staticmethod
    def inverse(m: Matrix) -> Matrix:
        """
        Compute the inverse of a square, non-singular matrix using Gauss-Jordan elimination.

        Cij = (−1)i+j det(Mij)
        adj = T(C)
        A-1 = (adj A)/(det A)
        """

        if Operations.determinant(m) == 0 or not m.is_square:
            raise ValueError("Matrix is not invertible")

        determinant = Operations.determinant(m)

        if determinant == 0:
            raise ValueError("Matrix is singular")

        cofactor = [[0] * m.shape[1] for _ in range(m.shape[0])]
        # Calculate the cofactor matrix
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                minor = Matrix(
                    data=[
                        [m.data[r][c] for c in range(m.shape[1]) if c != j]
                        for r in range(m.shape[0]) if r != i
                    ])

                cofactor[i][j] = ((-1) ** (i+j)) * \
                    Operations.determinant(minor)

        cofactor_transpose = Operations.transpose(Matrix(data=cofactor))

        return Operations.scalar_multiply(cofactor_transpose, 1 / determinant)

    @staticmethod
    def swap_rows(m: Matrix, i, j) -> Matrix:
        """
        Swaps two rows in the matrix.
        """
        if i == j:
            return m

        clone = Matrix(copy.deepcopy(m.data))
        clone.data[i], clone.data[j] = clone.data[j], clone.data[i]
        return clone

    @staticmethod
    def scale_row(m: Matrix, i, scalar: Union[int, float]) -> Matrix:
        """
        Scales a row by a given scalar.
        """
        clone = Matrix(copy.deepcopy(m.data))
        clone.data[i] = [scalar * x for x in clone.data[i]]
        return clone

    @staticmethod
    def trace(m: Matrix) -> Union[int, float]:
        """
        Calculates the trace of a square matrix.
        The trace is the sum of the diagonal elements.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")
        return sum(m.data[i][i] for i in range(m.shape[0]))

    @staticmethod
    def matrix_exponentiation(m: Matrix, n: int) -> Matrix:
        """
        raised to a power n.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        result = m
        for _ in range(n-1):
            result = Operations.multiply(result, m).data

        return Matrix(result)

    @staticmethod
    def flatten(m: Matrix) -> list:
        """
        Flattens a matrix into a single list.
        """
        return [item for row in m.data for item in row]

    @staticmethod
    def hadamard_product(m1: Matrix, m2: Matrix) -> Matrix:
        """
        Calculate the Hadamard product of two matrices.
        The Hadamard product is the element-wise product of two matrices.
        """

        if m1.shape != m2.shape:
            raise ValueError("Matrix shapes do not match")

        compressed = zip(m1.data, m2.data)
        result = Matrix([[0] * m1.shape[1] for _ in range(m1.shape[0])])

        for i, (row1, row2) in enumerate(compressed):
            for j, (col1, col2) in enumerate(zip(row1, row2)):
                result.data[i][j] = col1 * col2

        return result

    @staticmethod
    def conjugate(m: Matrix):
        """
        Compute the conjugate of a given matrix.
        This method creates a deep copy of the input matrix and replaces each 
        element with its complex conjugate.
        Args:
            m (Matrix): The input matrix whose elements are to be conjugated.
        Returns:
            Matrix: A new matrix with each element replaced by its complex conjugate.
        Note:
            The input matrix is not modified; a deep copy is created and returned.
        """
        deep_copy = copy.deepcopy(m)
        for i in range(deep_copy.shape[0]):
            for j in range(deep_copy.shape[1]):
                deep_copy.data[i][j] = complex(
                    deep_copy.data[i][j]).conjugate()

        return deep_copy

    @staticmethod
    def dot_product(m1: Matrix, m2: Matrix) -> Union[int, float]:
        """
        Calculate the dot product of two Vectors.
        The dot product is the sum of the element-wise products of two
        Vectors.
        """

        if m1.shape != m2.shape:
            raise ValueError("Matrix shapes do not match")

        if m1.shape[0] != 1 or m2.shape[0] != 1:
            raise ValueError("Not Vector")

        result = 0
        for j in range(m1.shape[1]):
            result += m1.data[0][j] * m2.data[0][j]

        return result

    @staticmethod
    def geometric_multiplicity(A: Matrix, eigenvalue) -> int:
        """
        Calculate the geometric multiplicity of a given eigenvalue.
        It is the dimension of the nullspace of (A - eigenvalue * I).

        Args:
        - A: Matrix object (must have .shape and .data)
        - eigenvalue: the eigenvalue (float or int)

        Returns:
        - int: dimension of the nullspace
        """

        # Step 1: Build (A - eigenvalue * I)
        n = A.shape[0]
        shifted = copy.deepcopy(A.data)
        for i in range(n):
            shifted[i][i] -= eigenvalue

        # Step 2: Find rank of (A - eigenvalue * I)
        rank = Operations.matrix_rank(shifted)

        # Step 3: Nullity = n - rank
        nullity = n - rank
        return nullity

    @staticmethod
    def matrix_rank(matrix_data, tol=1e-10):
        """
        Helper function: Compute rank of a matrix using Gaussian elimination.
        (for small matrices; not optimized for huge ones)

        Args:
        - matrix_data: list of lists (matrix)

        Returns:
        - int: rank
        """
        from copy import deepcopy

        A = deepcopy(matrix_data)
        n_rows = len(A)
        n_cols = len(A[0]) if A else 0
        rank = 0

        for r in range(min(n_rows, n_cols)):
            # Find pivot
            pivot_row = None
            for i in range(r, n_rows):
                if abs(A[i][r]) > tol:
                    pivot_row = i
                    break

            if pivot_row is None:
                continue

            # Swap pivot row to top
            A[r], A[pivot_row] = A[pivot_row], A[r]

            # Eliminate below
            for i in range(r+1, n_rows):
                factor = A[i][r] / A[r][r]
                for j in range(r, n_cols):
                    A[i][j] -= factor * A[r][j]

            rank += 1

        return rank
