from linalgplus.Operations import Operations
from linalgplus.Core import Matrix
from linalgplus.Factorization import Factorization

"""
    This module contains the Norm class, which provides various methods for computing different types of norms.
    It includes methods for Frobenius norm, max norm, spectral norm, nuclear norm, p-norm, induced norm,
    condition number, Schatten norm, and relative norm.
"""


class Norm:

    @staticmethod
    def frobenius(m: Matrix):
        """
        Computes the Frobenius norm of a matrix.
        The Frobenius norm is defined as the square root of the sum of the absolute squares of its elements.
        It is equivalent to the L2 norm of the matrix when viewed as a vector.
        """

        return (sum((abs(cell) ** 2) for row in m.data for cell in row)) ** 0.5

    @staticmethod
    def max_norm(m: Matrix):
        """"
        Computes the max norm of a matrix.
        The max norm is defined as the maximum absolute value of its elements.
        It is equivalent to the L∞ norm of the matrix when viewed as a vector.
        """

        return max([abs(cell) for cell in Operations.flatten(m).data])

    @staticmethod
    def _get_singular_values(m: Matrix) -> list:
        """
            Private helper to get singular values of a matrix.
        """
        _, S, _ = Factorization.svd(m)
        return sorted(S, reverse=True)

    @staticmethod
    def spectral_norm(m: Matrix) -> float | int:
        """
            Computes the spectral norm (induced 2-norm) of a matrix.
            It is the largest singular value.
        """
        return max(Norm._get_singular_values(m))

    @staticmethod
    def nuclear_norm(m: Matrix) -> float | int:
        """
            Computes the nuclear norm (trace norm) of a matrix.
            It is the sum of the singular values.
        """
        return sum(Norm._get_singular_values(m))

    @staticmethod
    def p_norm(m: Matrix, p):
        """
        Computes the p-norm of a matrix.
        The p-norm is defined as the p-th root of the sum of the absolute values of its elements raised to the power of p.
        It is equivalent to the Lp norm of the matrix when viewed as a vector.
        """

        flatten = Operations.flatten(m).data
        return (sum(abs(cell) ** p for cell in flatten)) ** (1/p)

    @staticmethod
    def induced_norm(m: Matrix) -> float | int:
        """
        Computes the induced norm of a matrix.
        """

        _, S, _ = Factorization.svd(m)
        return max(S)

    @staticmethod
    def condition_number(m: Matrix) -> float:
        """
        Computes the condition number of a matrix.
        It is the ratio of the largest to the smallest singular value.
        """
        singular_values = Operations._get_singular_values(m)

        if min(singular_values) == 0:
            return float('inf')  # Matrix is singular

        return max(singular_values) / min(singular_values)

    @staticmethod
    def schatten_norm(m: Matrix, p: float = 2) -> float:
        """
        Computes the Schatten p-norm of a matrix.

        Args:
        - m: Matrix
        - p: Order of the norm (p >= 1 or p = inf)

        Returns:
        - float: Schatten p-norm
        """
        singular_values = Operations._get_singular_values(m)

        if p == float('inf'):
            return max(singular_values)

        return (sum(sigma**p for sigma in singular_values))**(1/p)

    @staticmethod
    def relative_norm(a: Matrix, b: Matrix) -> float:
        """
        Computes the relative norm between two matrices using Frobenius norm.

        Formula: ||A - B|| / ||A||
        """
        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape.")

        diff = Operations.subtract(a, b)

        numerator = Operations.schatten_norm(diff, p=2)   # Frobenius norm
        denominator = Operations.schatten_norm(a, p=2)     # Frobenius norm

        if denominator == 0:
            raise ZeroDivisionError("Reference matrix A has zero norm.")

        return numerator / denominator
