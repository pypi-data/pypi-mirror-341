from lib.Operations import Operations
from lib.Core import Matrix
import random
import math
import copy
from typing import Union, Tuple, List


class Factorization:

    def eigen_decomposition(m: Matrix, max_iter=1000, e=1e-12) -> Tuple[List, List]:
        """
        Perform eigenvalue decomposition on a square matrix using the power iteration method.
        This function computes the eigenvalues and eigenvectors of a given square matrix.
        It uses the power iteration method to find the largest eigenvalue and its corresponding
        eigenvector, and then deflates the matrix to find subsequent eigenvalues and eigenvectors.
        Parameters:
            m (Matrix): The input square matrix for eigenvalue decomposition.
            max_iter (int, optional): The maximum number of iterations for the power iteration method.
                                      Defaults to 1000.
            e (float, optional): The convergence tolerance for the power iteration method.
                                 Defaults to 1e-12.
        Returns:
            Tuple[List, List]: A tuple containing:
                - A list of eigenvalues (List[float]).
                - A list of eigenvectors, where each eigenvector is represented as a flattened list (List[List[float]]).
        Raises:
            ValueError: If the input matrix `m` is not square.
        Notes:
            - The power iteration method is used to compute the largest eigenvalue and its corresponding
              eigenvector iteratively.
            - The deflation technique is applied to compute subsequent eigenvalues and eigenvectors by
              modifying the matrix to remove the influence of previously computed eigenvalues and eigenvectors.
            - The function assumes that the input matrix is symmetric or nearly symmetric for accurate results.
        Example:
            >>> m = Matrix(data=[[4, 1], [1, 3]])
            >>> eigenvalues, eigenvectors = eigen_decomposition(m)
            >>> print(eigenvalues)
            [5.0, 2.0]
            >>> print(eigenvectors)
            [[0.8944271909999159, 0.4472135954999579], [-0.4472135954999579, 0.8944271909999159]]
        """

        if not m.is_square:
            raise ValueError("Matrix must be square")
        n = m.shape[0]
        matrix_copy = copy.deepcopy(m)
        eigenvalues = []
        eigenvectors = []

        def power_iteration(m: Matrix) -> Tuple[Union[int, float], Matrix]:

            v = Matrix(data=[[1] for _ in range(m.shape[1])])

            largetst_eigenvalue = None
            largets_eigenvector = None
            for j in range(max_iter):

                w = Operations.multiply(m, v)
                norm = math.sqrt(sum(x**2 for x in Operations.flatten(w)))

                if norm < 1e-12:
                    return 0.0, v

                v_k_1 = Operations.scalar_multiply(w, 1/norm)

                Av = Operations.multiply(m, v_k_1)  # A * v
                numerator_matrix = Operations.multiply(
                    Operations.transpose(v_k_1), Av)
                denominator_matrix = Operations.multiply(
                    Operations.transpose(v_k_1), v_k_1)

                numerator = sum(Operations.flatten(numerator_matrix))
                denominator = sum(Operations.flatten(denominator_matrix))

                v = v_k_1  # Update v for the next iteration

                if largetst_eigenvalue is not None and (abs((numerator / denominator) - largetst_eigenvalue) < e):
                    break

                largetst_eigenvalue = numerator / denominator
                largets_eigenvector = v_k_1

            return largetst_eigenvalue, largets_eigenvector

        def deflate(A: Matrix, eigenvalue: float, eigenvector: Matrix) -> Matrix:
            n = len(eigenvector.data)

            # Normalize eigenvector
            norm = math.sqrt(sum([x[0]**2 for x in eigenvector.data]))
            v_norm = Operations.scalar_multiply(eigenvector, 1 / norm)

            # Create outer product vv^T
            outer = Matrix(data=[
                [v_norm.data[i][0] * v_norm.data[j][0] for j in range(n)]
                for i in range(n)
            ])

            # Create Identity matrix
            I = Matrix(data=[
                [1.0 if i == j else 0.0 for j in range(n)]
                for i in range(n)
            ])

            # (I - vv^T)
            projector = Operations.subtract(I, outer)

            # Deflate using: (I - vv^T) A (I - vv^T)
            left = Operations.multiply(projector, A)
            A_deflated = Operations.multiply(left, projector)

            return A_deflated

        for _ in range(n):  # n = number of eigenvalues you want
            eigenvalue, eigenvector = power_iteration(matrix_copy)
            eigenvalues.append(eigenvalue)
            eigenvectors.append(Operations.flatten(eigenvector))
            matrix_copy = deflate(matrix_copy, eigenvalue, eigenvector)

        return eigenvalues, eigenvectors

    def svd(m: Matrix) -> Tuple[Matrix, List, Matrix]:
        """
        Perform Singular Value Decomposition (SVD) on the given matrix.
        SVD decomposes a matrix `m` into three components: U, Σ, and V^T such that:
            m = U * Σ * V^T
        Args:
            m (Matrix): The input matrix to decompose.
        Returns:
            Tuple[Matrix, List, Matrix]: A tuple containing:
                - U (Matrix): An orthogonal matrix whose columns are the left singular vectors.
                - singular_values (List): A list of singular values in descending order.
                - Vt (Matrix): The transpose of an orthogonal matrix whose rows are the right singular vectors.
        Notes:
            - Singular values smaller than a threshold (1e-12) are considered negligible and skipped.
            - The input matrix `m` is assumed to be compatible with the operations defined in the `Operations` module.
        Raises:
            ValueError: If the input matrix is invalid or incompatible with the operations.
        Example:
            >>> U, singular_values, Vt = svd(matrix)
            >>> print(U)
            >>> print(singular_values)
            >>> print(Vt)
        """

        a = m
        at = Operations.transpose(a)
        aat = Operations.multiply(at, a)

        eigenvalues, eigenvectors = Factorization.eigen_decomposition(aat)
        eigenvalues_eigenvectors = list(zip(eigenvalues, eigenvectors))
        eigenvalues_eigenvectors.sort(key=lambda x: x[0], reverse=True)

        singular_values = [math.sqrt(ev) for ev, _ in eigenvalues_eigenvectors]
        dm = [[0 for _ in range(len(singular_values))]
              for _ in range(len(singular_values))]
        for i in range(len(singular_values)):
            dm[i][i] = singular_values[i]

        columns = []
        i = 0
        for _, eigen_vector in eigenvalues_eigenvectors:
            if singular_values[i] < 1e-12:
                # Singular value too small, skip this u_i
                i += 1
                continue
            aev = Operations.multiply(
                a, Operations.transpose(Matrix([eigen_vector])))
            Ui = Operations.scalar_multiply(
                aev, 1 / singular_values[i])

            columns.append(Operations.flatten(Ui))
            i += 1

        U = Operations.transpose(Matrix(columns))

        sorted_eigen_vectors = [vec[1] for vec in eigenvalues_eigenvectors]

        Vt = Operations.transpose(
            Matrix(data=[col for col in sorted_eigen_vectors]))

        return U, singular_values, Vt

    @staticmethod
    def LU_decomposition(m: Matrix) -> Tuple[Matrix, Matrix]:
        if not m.is_square:
            raise ValueError("Matrix must be square")

        n = m.shape[0]
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]

        for i in range(n):
            # Upper Triangular U
            for k in range(i, n):
                sum_ = sum(L[i][j] * U[j][k] for j in range(i))
                U[i][k] = m.data[i][k] - sum_

            # Lower Triangular L
            for k in range(i, n):
                if i == k:
                    L[i][i] = 1.0
                else:
                    sum_ = sum(L[k][j] * U[j][i] for j in range(i))
                    if U[i][i] == 0:
                        raise ZeroDivisionError("Zero pivot encountered.")
                    L[k][i] = (m.data[k][i] - sum_) / U[i][i]

        return Matrix(L), Matrix(U)

    @staticmethod
    def QR_decomposition(m: Matrix) -> Tuple[Matrix, Matrix]:
        import copy

        A = copy.deepcopy(m.data)
        n, d = m.shape
        Q = [[0.0] * d for _ in range(n)]
        R = [[0.0] * d for _ in range(d)]

        for j in range(d):
            v = [A[i][j] for i in range(n)]

            for i in range(j):
                R[i][j] = sum(Q[k][i] * A[k][j] for k in range(n))
                for k in range(n):
                    v[k] -= R[i][j] * Q[k][i]

            norm = (sum(v_i ** 2 for v_i in v)) ** 0.5
            if norm == 0:
                raise ValueError("Zero vector encountered in Gram-Schmidt")

            R[j][j] = norm
            for i in range(n):
                Q[i][j] = v[i] / norm

        return Matrix(Q), Matrix(R)

    @staticmethod
    def Cholesky_decomposition(m: Matrix) -> Matrix:
        if not m.is_square:
            raise ValueError("Matrix must be square")

        n = m.shape[0]
        L = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1):
                sum_ = sum(L[i][k] * L[j][k] for k in range(j))

                if i == j:
                    val = m.data[i][i] - sum_
                    if val < 0:
                        raise ValueError("Matrix is not positive-definite")
                    L[i][j] = val ** 0.5
                else:
                    L[i][j] = (m.data[i][j] - sum_) / L[j][j]

        return Matrix(L)
