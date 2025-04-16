from typing import Union
from lib.Core import Matrix
from lib.Operations import Operations
from lib.Factorization import Factorization
from lib.Norms import Norm
import math
import copy


class Properties:

    @staticmethod
    def is_square(m: Matrix) -> bool:
        """
        A matrix is square if the number of rows is equal to the number of columns.
        """

        return m.is_square

    @staticmethod
    def is_zero(m: Matrix) -> bool:
        """
        A matrix is zero if all the elements are 0.
        """

        return all(all(cell == 0 for cell in row) for row in m.data)

    @staticmethod
    def is_one(m: Matrix) -> bool:
        """
        A matrix is one if all the elements are 1."""

        return all(all(cell == 1 for cell in row) for row in m.data)

    @staticmethod
    def is_identity(m: Matrix) -> bool:
        """
        A matrix is identity if all the diagonal
          elements are 1 and all other elements are 0.
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j and m.data[i][j] != 1:
                    return False
                if i != j and m.data[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_upper_triangular(m: Matrix) -> bool:
        """
        A matrix is upper triangular if all the entries below the main diagonal are zero.
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i < j and m.data[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_lower_triangular(m: Matrix) -> bool:
        """
        A matrix is lower triangular if all the entries above the main diagonal are zero.
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i > j and m.data[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_triangular(m: Matrix) -> bool:
        return Properties.is_lower_triangular(m) or Properties.is_upper_triangular(m)

    @staticmethod
    def is_symmetric(m: Matrix) -> bool:
        """
        A matrix is symmetric if its transpose is equal to itself.
        """

        return m.data == Operations.transpose(m).data

    @staticmethod
    def is_skew_symmetric(m: Matrix) -> bool:
        """
        A matrix is skew-symmetric if its transpose is equal to its negative.
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")
        # Check if the matrix is equal to the negative of its transpose
        return m.data == [[-cell for cell in row] for row in Operations.traspose(m).data]

    @staticmethod
    def is_diagonal(m: Matrix) -> bool:
        """
        A matrix is diagonal if all the non-diagonal elements are zero.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")
        for i, row in enumerate(m.data):
            for j, val in enumerate(row):
                if i != j and val != 0:
                    return False
        return True

    @staticmethod
    def is_antidiagonal(m: Matrix) -> bool:
        """
        A matrix is antidiagonal if all the non-antidiagonal elements are zero.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")
        for i, row in enumerate(m.data):
            for j, val in enumerate(row):
                if not (j == m.shape[1] - i - 1) and val != 0:
                    return False
        return True

    @staticmethod
    def is_scalar(m: Matrix) -> bool:
        """
        A matrix is scalar if all the diagonal elements are equal and all the non-diagonal elements are zero.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")
        first_diagonal = m.data[0][0]
        for i, row in enumerate(m.data):
            for j, val in enumerate(row):
                if i == j and val != first_diagonal:
                    return False
                if i != j and val != 0:
                    return False
        return True

    @staticmethod
    def is_permutation(m: Matrix) -> bool:
        """
        A matrix is a permutation matrix if it is square, and each row and column contains exactly one entry of 1 and all other entries are 0.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")
        n = m.shape[0]

        # Check rows: each row must have exactly one 1 and the rest 0
        for row in m.data:
            if row.count(1) != 1 or any(cell not in (0, 1) for cell in row):
                return False

        # check rows
        for i in range(n):
            total = sum(m.data[i])
            if total != 1:
                return False

        # check columns
        traspose = Operations.transpose(m)
        for i in range(n):
            total = sum(traspose.data[i])
            if total != 1:
                return False
        return True

    @staticmethod
    def is_normal(m: Matrix) -> bool:
        """
        matrix * matrix^T == matrix^T * matrix
        """

        return Operations.multiply(m, Operations.transpose(
            m)).data == Operations.multiply(Operations.transpose(m), m).data

    @staticmethod
    def is_unitary(m: Matrix) -> bool:
        """
        A matrix is unitary if its conjugate transpose is equal to its inverse.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        m_t = Operations.transpose(m)

        left = Operations.multiply(m_t, m).data  # U^T U
        right = Operations.multiply(m, m_t).data  # U U^T
        identity = Operations.identity(m.shape[0])

        return left == identity and right == identity

    @staticmethod
    def is_toeplitz(m: Matrix) -> bool:
        """
        A matrix is Toeplitz if all diagonals from top-left to bottom-right are constant.

        A[i][j]=A[i−1][j−1] for all i>0 and j>0.
        """

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i > 0 and j > 0:
                    if m.data[i][j] != m.data[i - 1][j - 1]:
                        return False
        return True

    @staticmethod
    def is_hankel(m: Matrix) -> bool:
        """
        A matrix is Hankel if all anti-diagonals (from top-right to bottom-left) are constant.

        A[i][j]=A[i-1][j+1] for all i-1>0 and j<m.shape[1]-1.
        """

        for i in range(1, m.shape[0]):
            for j in range(m.shape[1] - 1):
                if m.data[i][j] != m.data[i - 1][j + 1]:
                    return False
        return True

    @staticmethod
    def is_idempotent(m: Matrix) -> bool:
        """
        A matrix is idempotent if m * m = m.
        """
        return Operations.multiply(m, m).data == m.data

    @staticmethod
    def is_nidempotent(m: Matrix) -> bool:
        """
        A matrix is idempotent if m * m != m.
        """
        return Operations.multiply(m, m).data != m.data

    @staticmethod
    def is_singular(m: Matrix) -> bool:
        """
        A matrix is singular if its determinant is zero.

        A singular matrix is non-invertible
        """
        return Operations.determinant(m) == 0

    @staticmethod
    def is_invertible(m: Matrix) -> bool:
        """
        If the determinant of the matrix is zero
        then the matrix is not invertible or else the matrix is invertible.
        """

        return Operations.determinant(m) != 0

    @staticmethod
    def is_sparse(m: Matrix) -> bool:
        """
        A matrix is sparse if the number of zero elements is greater than the number of non-zero elements.
        """

        total_elements = m.shape[0] * m.shape[1]
        zero_count = sum(cell == 0 for row in m.data for cell in row)
        nonzero_count = total_elements - zero_count
        return zero_count > nonzero_count

    @staticmethod
    def is_magic_square(m: Matrix) -> bool:
        """
        A matrix is a magic square if the sum of each row, column, and diagonal is the same.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")
        n = m.shape[0]
        magic_sum = sum(m.data[0])
        # Check rows
        for row in m.data:
            if sum(row) != magic_sum:
                return False
        # Check columns
        for j in range(n):
            if sum(m.data[i][j] for i in range(n)) != magic_sum:
                return False
        # Check main diagonal
        for i in range(n):
            if m.data[i][i] != magic_sum:
                return False

        if sum(m.data[i][n - 1 - i] for i in range(n)) != magic_sum:
            return False

        return True

    @staticmethod
    def is_upper_bidiagonal(m: Matrix) -> bool:
        """
        A matrix is upper bidagonal if it has nonzero entries only
        on the main diagonal and the first superdiagonal.
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j or i == j - 1:
                    continue
                elif m.data[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_lower_bidiagonal(m: Matrix) -> bool:
        """
        A matrix is lower bidagonal if it has nonzero entries only
        on the main diagonal and the first subdiagonal.
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j or i == j + 1:
                    continue
                elif m.data[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_tridiagonal(m: Matrix) -> bool:
        """
        Nonzero only on main diagonal + first diagonals above and below
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j or i == j - 1 or i == j + 1:
                    continue
                elif m.data[i][j] != 0:
                    return False

    @staticmethod
    def is_band(m: Matrix, bandwidth: Union[int, float] = 1) -> bool:
        """
        A matrix is banded if it has non-zero entries only within a certain bandwidth.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        # Check the bandwidth of the matrix
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if abs(i - j) > bandwidth and m.data[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_row_stochastic(m: Matrix) -> bool:
        """
        A matrix is row stochastic if all the rows sum to 1.
        """
        for row in m.data:
            row_sum = 0
            for cell in row:
                if cell < 0:
                    return False
                row_sum += cell
            if row_sum != 1:
                return False
        return True

    @staticmethod
    def is_column_stochastic(m: Matrix) -> bool:
        """
        A matrix is column stochastic if all the columns sum to 1.
        """
        for j in range(m.shape[1]):
            col_sum = 0
            for i in range(m.shape[0]):
                if m.data[i][j] < 0:
                    return False
                col_sum += m.data[i][j]
            if col_sum != 1:
                return False
        return True

    @staticmethod
    def is_doubly_stochastic(m: Matrix) -> bool:
        """
        A matrix is doubly stochastic if it is both row and column stochastic.
        """

        for row in m.data:
            row_sum = 0
            for cell in row:
                if cell < 0:
                    return False
                row_sum += cell
            if row_sum != 1:
                return False

        for j in range(m.shape[1]):
            col_sum = 0
            for i in range(m.shape[0]):
                if m.data[i][j] < 0:
                    return False
                col_sum += m.data[i][j]
            if col_sum != 1:
                return False
        return True

    @staticmethod
    def is_diagonal_dominant(m: Matrix) -> bool:
        """
        A matrix is diagonally dominant if the absolute value of each diagonal
          element is greater than or equal to the sum of
          the absolute values of the other elements in that row.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(m.shape[0]):
            diag_sum = sum(abs(cell) for i, cell in enumerate(m.data[i]))
            if abs(m.data[i][i]) < diag_sum / 2:
                return False
        return True

    @staticmethod
    def is_projection(m: Matrix) -> bool:
        """
        A matrix is a projection matrix if P^2 = P.
        """
        return Operations.multiply(m, m).data == m.data

    @staticmethod
    def is_circulant(m: Matrix) -> bool:
        """"
        A matrix is circulant if each row is a right cyclic shift of the previous row.
        """

        if not m.is_square:
            return False

        def helper(i):
            if i == m.shape[0] - 1:
                return True

            row = m.data[i]
            next_row = m.data[i+1]

            # shift rigth
            row = row[-1:] + row[:-1]
            if row != next_row:
                return False

            return helper(i + 1)

        return helper(0)

    @staticmethod
    def is_involutory(m: Matrix) -> bool:
        """"
        A matrix is involutory if P^2 = I, where I is the identity matrix.
        """
        clone = Operations.multiply(m, m)
        return Properties.is_identity(clone)

    @staticmethod
    def is_stochastic(m: Matrix, tolerance=1e-9) -> bool:
        """
        A matrix is stochastic if all the elements are non-negative and each row and column sums to 1.
        """

        if not all(m.data[i][j] >= 0 for i in range(m.shape[0]) for j in range(m.shape[1])):
            return False

        for row in m.data:
            if abs(sum(row) - 1) > tolerance:
                break
        else:
            return True

        for row in Operations.transpose(m).data:
            if abs(sum(row) - 1) > tolerance:
                break
        else:
            return True

        return False

    @staticmethod
    def is_positive_definite(m: Matrix) -> bool:
        """
        A matrix is positive definite if all its leading principal minors are positive.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        eigenvalues, _ = Factorization.eigen_decomposition(m)
        return all(eigenvalue > 0 for eigenvalue in eigenvalues)

    @staticmethod
    def is_diagonalizable(m: Matrix) -> bool:
        """
        A matrix is diagonalizable if it has n linearly independent eigenvectors.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        _, eigenvectors = Factorization.eigen_decomposition(m)
        matrix_form = Operations.transpose(Matrix(data=eigenvectors))

        return Properties.is_invertible(matrix_form)

    @staticmethod
    def is_positive_semidefinite(m: Matrix) -> bool:
        """
        A matrix is positive semidefinite if all its eigenvalues are non-negative.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        if not Properties.is_symmetric(m):
            return False

        eigenvalues, _ = Factorization.eigen_decomposition(m)
        return all(eigenvalue >= 0 for eigenvalue in eigenvalues)

    @staticmethod
    def is_metzler(m: Matrix) -> bool:
        """
        A matrix is Metzler if all its off-diagonal elements are non-negative.
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(len(m.shape[0])):
            for j in range(len(m.shape[1])):
                if i != j and m.data[i][j] < 0:
                    return False
        return True

    @staticmethod
    def is_normalized(m: Matrix, axis="column") -> bool:
        """
        A matrix is normalized if all its elements are between 0 and 1.
        """
        EPS = 1e-12  # small value to avoid floating point errors

        if axis == "row":
            for row in m.data:
                norm = math.sqrt(sum([cell ** 2 for cell in row]))
                if abs(norm - 1) > EPS:
                    return False
        else:
            for row in Operations.transpose(m).data:
                norm = math.sqrt(sum([cell ** 2 for cell in row]))
                if abs(norm - 1) > EPS:
                    return False
        return True

    @staticmethod
    def is_element_wise_normalized(m: Matrix) -> bool:
        for row in m.data:
            for cell in row:
                if cell < 0 or cell > 1:
                    return False
        return True

    @staticmethod
    def is_hermitian(m: Matrix) -> bool:
        """
        A matrix is Hermitian if it is equal to its own conjugate transpose.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")
        return Operations.transpose(Operations.conjugate(m)).data == m.data

    @staticmethod
    def is_skew_hermitian(m: Matrix) -> bool:
        """
        A matrix is skew-Hermitian if it is equal to the negative of its own conjugate transpose.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")
        return Operations.transpose(Operations.conjugate(m)).data == Operations.scalar_multiply(m, -1).data

    @staticmethod
    def is_orthonormal_rows(m: Matrix) -> bool:

        if not Properties.is_normalized(m, axis="row"):
            return False

        def _recursive_helper(i: int) -> bool:
            if i == m.shape[0] - 1:
                return True
            # Check if the row is orthogonal to all previous rows
            for j in range(i, m.shape[0]):
                for k in range(j + 1, m.shape[0]):
                    prod = Operations.dot_product(
                        Matrix([m.data[j]]), Matrix([m.data[k]]))
                    if prod != 0:
                        return False

            return _recursive_helper(i + 1)

        return _recursive_helper(0)

    @staticmethod
    def is_orthonormal_columns(m: Matrix) -> bool:

        return Properties.is_orthonormal_rows(Operations.transpose(m))

    @staticmethod
    def is_symmetric_positive_definite(m: Matrix) -> bool:
        """
            A matrix is symmetric positive semidefinite if:
            - It is symmetric
            - All eigenvalues are greater than  0
        """
        if not Properties.is_symmetric(m):
            return False

        eigenvalues, _ = Factorization.eigen_decomposition(m)
        return all(eigenvalue > 0 for eigenvalue in eigenvalues)

    @staticmethod
    def is_symmetric_positive_semidefinite(m: Matrix) -> bool:
        """
            A matrix is symmetric positive semidefinite if:
            - It is symmetric
            - All eigenvalues are greater than or equal to 0
        """
        if not Properties.is_symmetric(m):
            return False

        eigenvalues, _ = Factorization.eigen_decomposition(m)
        return all(eigenvalue >= 0 for eigenvalue in eigenvalues)

    @staticmethod
    def is_stochastic_row_normalized(m: Matrix) -> bool:

        for row in m.data:
            row_sum = sum(row)
            if row_sum != 1:
                return False
            for cell in row:
                if cell < 0:
                    return False
        return True

    @staticmethod
    def is_nilpotent_of_index_k(m: Matrix, k: int) -> bool:
        """
            A matrix is nilpotent of index k if:
            - A^(k) = 0
            - A^(k-1) != 0
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        deep_copy = copy.deepcopy(m)

        for _ in range(k - 2):
            deep_copy = Operations.multiply(deep_copy, m)

        if Properties.is_zero(deep_copy):
            return False

        if not Properties.is_zero(Operations.multiply(deep_copy, m)):
            return False

        return True

    @staticmethod
    def is_upper_hessenberg(m: Matrix) -> bool:

        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i - j > 1 and m[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_lower_hessenberg(m: Matrix) -> bool:
        """
        A matrix is lower Hessenberg if all entries above the first superdiagonal are zero.
        """
        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if j - i > 1 and m[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_m_matrix(m: Matrix) -> bool:
        """
            A matrix is an M-matrix if:
            - It is square
            - All off-diagonal entries are <= 0
            - Matrix is invertible
            - All entries of A^{-1} are >= 0
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i != j and m.data[i][j] > 0:
                    return False

        if not Properties.is_invertible(m):
            return False

        inverse = Operations.inverse(m)

        # check if all entries of A^{-1} are >= 0
        return all([cell >= 0 for row in inverse.data for cell in row])

    @staticmethod
    def is_companion_matrix(m: Matrix) -> bool:

        if not m.is_square:
            raise ValueError("Matrix is not square")

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j + 1 and m.data[i][j] != 1:
                    return False

        transpose = Operations.transpose(m)
        for i in range(transpose.shape[0]):
            for j in range(transpose.shape[1]):
                if i == len(transpose.data) - 1:
                    pass
                else:
                    if transpose.data[i][j] != 0:
                        return False
        return True

    @staticmethod
    def is_involutory_symmetric(m: Matrix) -> bool:
        """
            A matrix is involutory symmetric if:
            - It is symmetric
            - It is involutory
        """

        m2 = Operations.multiply(m, m)

        if m2 != Operations.identity(m2.shape[0]):
            return False

        if Properties.is_symmetric(m):
            return True

    @staticmethod
    def is_jordan_block(m: Matrix) -> bool:
        """
            Check if a matrix is a Jordan block:
            - Constant on main diagonal
            - 1s on superdiagonal
            - 0 elsewhere
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")

        lambda_value = m.data[0][0]
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j:
                    if m[i][j] != lambda_value:
                        return False
                elif i == j - 1:
                    if m[i][j] != 1:
                        return False
                else:
                    if m.data[i][j] != 0:
                        return False
        return True

    @staticmethod
    def is_contractive(m: Matrix) -> bool:

        eigenvalues, _ = Factorization.eigen_decomposition(m)
        eigenvalues = [abs(eigenvalue) for eigenvalue in eigenvalues]
        return all(eigenvalue < 1 for eigenvalue in eigenvalues)

    @staticmethod
    def is_expansive(m: Matrix) -> bool:
        """
        A matrix is expansive if all eigenvalues have magnitude > 1.
        """
        if not m.is_square:
            raise ValueError("Matrix must be square")

        eigenvalues, _ = Factorization.eigen_decomposition(m)

        abs_eigenvalues = [abs(ev) for ev in eigenvalues]

        return all(ev > 1 for ev in abs_eigenvalues)

    @staticmethod
    def is_unit_upper_triangular(m: Matrix) -> bool:

        if not m.is_square:
            raise ValueError("Matrix is not square")
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j and m.data[i][j] != 1:
                    return False
                if i > j and m.data[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_unit_lower_triangular(m: Matrix) -> bool:

        if not m.is_square:
            raise ValueError("Matrix is not square")
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j and m.data[i][j] != 1:
                    return False
                if i < j and m.data[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_symmetric_indefinite(m: Matrix) -> bool:

        flag = Operations.transpose(m) == m
        if not flag:
            return

        eigenvalues, _ = Factorization.eigen_decomposition(m)

        return any(eigenval for eigenval in eigenvalues if eigenval > 0) and any(eigenval for eigenval in eigenvalues if eigenval < 0)

    @staticmethod
    def is_quadratic_form_positive(m: Matrix) -> bool:
        """
        A quadratic form x^T A x is positive for all nonzero x
        if and only if A is symmetric positive definite.
        """
        if not m.is_square:
            raise ValueError("Matrix must be square")

        if not Properties.is_symmetric(m):
            return False

        eigenvalues, _ = Factorization.eigen_decomposition(m)

        return all(ev > 0 for ev in eigenvalues)

    @staticmethod
    def is_positive_operator(m: Matrix) -> bool:
        if not m.is_square:
            raise ValueError("Matrix must be square")

        if not Properties.is_symmetric(m):
            return False

        eigenvalues, _ = Factorization.eigen_decomposition(m)

        return all(ev >= 0 for ev in eigenvalues)

    @staticmethod
    def is_laplacian_matrix(m: Matrix) -> bool:
        """
            Check if a matrix is a Laplacian matrix:
            - Symmetric
            - Diagonal entries >= 0
            - Off-diagonal entries are 0 or -1
            - Each row sums to zero
        """

        if not m.is_square:
            raise ValueError("Matrix is not square")

        flag = Properties.is_symmetric(m)
        if not flag:
            return False

        for i in range(m.shape[0]):
            row_sum = sum(m.data[i])
            if row_sum != 0:
                return False
            for j in range(m.shape[1]):
                if i == j:
                    if m.data[i][j] < 0:
                        return False
                else:
                    if not (m.data[i][j] == 0 or m.data[i][j] == -1):
                        return False
        return True

    @staticmethod
    def is_adjacency_matrix(m: Matrix) -> bool:
        """
        Check if a matrix is an adjacency matrix:
        - Square
        - Entries are only 0 or 1
        """
        if not m.is_square:
            raise ValueError("Matrix must be square")

        for row in m.data:
            for cell in row:
                if cell not in (0, 1):
                    return False

        return True

    @staticmethod
    def is_stable(m: Matrix) -> bool:
        """
        A matrix is stable if all eigenvalues have negative real parts.
        """
        if not m.is_square:
            raise ValueError("Matrix must be square")

        eigenvalues, _ = Factorization.eigen_decomposition(m)

        eigenvalues = [complex(eigenvalue) for eigenvalue in eigenvalues]
        return all(eigenvalue.real < 0 for eigenvalue in eigenvalues)

    @staticmethod
    def is_discrete_stable(m: Matrix) -> bool:
        """
        A matrix is discrete stable if all eigenvalues have magnitude < 1.
        """
        if not m.is_square:
            raise ValueError("Matrix must be square")

        eigenvalues, _ = Factorization.eigen_decomposition(m)

        return all(abs(ev) < 1 for ev in eigenvalues)

    @staticmethod
    def is_characteristic_matrix(m: Matrix) -> bool:
        return Properties.is_adjacency_matrix(m)

    @staticmethod
    def is_well_conditioned(m: Matrix) -> bool:
        """
        A matrix is well-conditioned if its condition number is finite.
        """
        if not m.is_square:
            raise ValueError("Matrix must be square")

        _, S, _ = Factorization.svd(m)
        # arbitrary threshold for well-conditioned
        return (max(S) / min(S)) < 10000

    @staticmethod
    def is_ill_conditioned(m: Matrix) -> bool:
        """
        A matrix is ill-conditioned if its condition number is very large.
        Typically, if cond(A) > 10000, the matrix is considered ill-conditioned.
        """
        if not m.is_square:
            raise ValueError("Matrix must be square")

        _, S, _ = Factorization.svd(m)
        # arbitrary threshold for well-conditioned
        return (max(S) / min(S)) > 10000

    @staticmethod
    def is_similarity_transform(a: Matrix, b: Matrix) -> bool:
        if a.shape != b.shape:
            return False

        eigenvalues_a = Factorization.eigen_decomposition(a)[0]
        eigenvalues_b = Factorization.eigen_decomposition(b)[0]

        if sorted(eigenvalues_a) != sorted(eigenvalues_b):
            return False

        for eigenvalue in set(eigenvalues_a):
            geo_mult_A = Operations.geometric_multiplicity(a, eigenvalue)
            geo_mult_B = Operations.geometric_multiplicity(b, eigenvalue)
            if geo_mult_A != geo_mult_B:
                return False

        return True

    @staticmethod
    def is_schur_form(m: Matrix) -> bool:
        """
        Check if a matrix is in Schur form:
        - Square
        - Upper triangular
        """
        if not m.is_square:
            raise ValueError("Matrix must be square")

        return Properties.is_upper_triangular(m)

    @staticmethod
    def is_unit_norm_matrix(m: Matrix) -> bool:
        """
        A matrix is unit norm if the Frobenius norm of the matrix is equal to 1.
        """
        return Norm.frobenius(m) == 1

    @staticmethod
    def is_unipotent(m: Matrix) -> bool:

        eigen_values, _ = Factorization.eigen_decomposition(m)
        return all(val == 1 for val in eigen_values)
