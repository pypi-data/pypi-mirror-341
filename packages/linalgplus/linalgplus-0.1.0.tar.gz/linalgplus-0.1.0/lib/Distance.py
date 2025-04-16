from lib.Core import Matrix
from lib.Operations import Operations
from typing import List, Tuple, Union
import math


class Distance:

    @staticmethod
    def euclidean(a: Matrix, b: Matrix) -> Union[float, int]:
        """
        Computes the Euclidean distance between two matrices.
        The matrices must have the same shape.

        Formula: ||A - B|| = sqrt(sum((a_i - b_i)^2))
        where a_i and b_i are the elements of the matrices A and B respectively.

        """

        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        return math.sqrt(sum((a_b[0] - a_b[1]) ** 2 for a_b in zip(vec_a, vec_b)))

    @staticmethod
    def manhattan(a: Matrix, b: Matrix) -> Union[float, int]:
        """
        Computes the Manhattan distance between two matrices.
        The matrices must have the same shape.

        Formula: ||A - B||_1 = sum(abs(a_i - b_i))
        where a_i and b_i are the elements of the matrices A and B respectively.
        """

        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        return sum(abs(a_b[0] - a_b[1]) for a_b in zip(vec_a, vec_b))

    @staticmethod
    def cosine(a: Matrix, b: Matrix) -> Union[float, int]:
        """
        Calculate the cosine similarity between two matrices.
        The cosine similarity is a measure of similarity between two non-zero
        vectors of an inner product space. It is defined as the cosine of the
        angle between the vectors, which is also the dot product of the vectors
        divided by the product of their magnitudes.
        Formula:
            cos(theta) = (A . B) / (||A|| * ||B||)
        Where:
            - A . B is the dot product of matrices A and B.
            - ||A|| and ||B|| are the Euclidean norms of matrices A and B.
        Args:
            a (Matrix): The first input matrix.
            b (Matrix): The second input matrix.
        Returns:
            Union[float, int]: The cosine similarity value. Returns 0 if either
            matrix has a zero norm.
        Raises:
            ValueError: If the input matrices do not have the same shape.
        Notes:
            - The input matrices must have the same shape for the calculation.
            - The function flattens the matrices into vectors before computing
              the similarity.
        """

        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        dot_product = Operations.dot_product(vec_a, vec_b)

        norm_a = math.sqrt(sum(x ** 2 for x in vec_a))
        norm_b = math.sqrt(sum(x ** 2 for x in vec_b))

        return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0

    @staticmethod
    def chebyshev(a: Matrix, b: Matrix) -> Union[float, int]:
        """
        The Chebyshev distance is defined as the maximum absolute difference
        between corresponding elements of two matrices. It is also known as
        the L∞ (L-infinity) distance or maximum metric.
        Formula:
            d(a, b) = max(|a_i - b_i|) for all i
        Parameters:
            a (Matrix): The first input matrix.
            b (Matrix): The second input matrix.
        Returns:
            Union[float, int]: The Chebyshev distance between the two matrices.
        Raises:
            ValueError: If the input matrices do not have the same shape.
        Notes:
            - The input matrices must have the same shape for the distance
              to be computed.
            - The function internally flattens the matrices into vectors
              before computing the distance.

        """
        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        return max(abs(x - y) for x, y in zip(vec_a, vec_b))

    @staticmethod
    def minkowski(a: Matrix, b: Matrix, p: int) -> Union[float, int]:
        """
        Calculate the Minkowski distance between two matrices.
        The Minkowski distance is a generalization of both the Euclidean distance
        (when p=2) and the Manhattan distance (when p=1). It is defined as the
        p-th root of the sum of the absolute differences raised to the power of p.
        Args:
            a (Matrix): The first matrix. Must have the same shape as `b`.
            b (Matrix): The second matrix. Must have the same shape as `a`.
            p (int): The order of the Minkowski distance. Must be greater than or
                     equal to 1.
        Returns:
            Union[float, int]: The Minkowski distance between the two matrices.
        Raises:
            ValueError: If the shapes of `a` and `b` do not match.
            ValueError: If `p` is less than 1.
        Notes:
            - The matrices `a` and `b` are flattened into vectors before computing
              the distance.
            - The function uses `math.pow` to compute the p-th root of the sum.
        Example:
            >>> a = Matrix([[1, 2], [3, 4]])
            >>> b = Matrix([[5, 6], [7, 8]])
            >>> Distance.minkowski(a, b, 2)
            8.0
        """
        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")
        if p < 1:
            raise ValueError("Minkowski order 'p' must be >= 1")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        return math.pow(sum(abs(a_b[0] - a_b[1]) ** p for a_b in zip(vec_a, vec_b)), 1/p)

    @staticmethod
    def find_nearest_neighbor(target: Matrix, candidates: List[Matrix], distance_fn) -> Tuple[int, float]:
        """
        Returns the index and distance of the nearest neighbor.

        :param target: The matrix to compare against.
        :param candidates: A list of matrices.
        :param distance_fn: A function that takes (a, b) and returns a distance.
        :return: (index of closest matrix, distance)
        """

        nearest_index = -1
        dist = float('inf')

        for i, m in enumerate(candidates):
            cur_dist = distance_fn(target, m)
            if cur_dist < dist:
                dist = cur_dist
                nearest_index = i
        return candidates[nearest_index], dist

    @staticmethod
    def normalized_euclidean(a: Matrix, b: Matrix) -> Union[float, int]:
        """
        Calculate the normalized Euclidean distance between two matrices.
        This method computes the Euclidean distance between two matrices after
        normalizing their flattened vector representations. The normalization
        ensures that the vectors have a unit norm, making the distance calculation
        invariant to the magnitude of the original matrices.
        Args:
            a (Matrix): The first matrix.
            b (Matrix): The second matrix.
        Returns:
            Union[float, int]: The normalized Euclidean distance between the two matrices.
        Raises:
            ValueError: If the matrices do not have the same shape.
            ValueError: If either matrix results in a zero vector after flattening
                        (normalization is not possible for zero vectors).
        Notes:
            - The `Matrix` type is assumed to have a `shape` attribute and is compatible
              with the `Operations.flatten` method.
            - The `Operations.flatten` method is expected to convert a matrix into a
              one-dimensional list or vector.
        """
        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        norm_a = math.sqrt(sum(x ** 2 for x in vec_a))
        norm_b = math.sqrt(sum(x ** 2 for x in vec_b))

        if norm_a == 0 or norm_b == 0:
            raise ValueError("Cannot normalize a zero vector")

        vec_a_norm = [x / norm_a for x in vec_a]
        vec_b_norm = [x / norm_b for x in vec_b]

        return math.sqrt(sum((x - y) ** 2 for x, y in zip(vec_a_norm, vec_b_norm)))

    @staticmethod
    def bray_curtis(a: Matrix, b: Matrix) -> float:
        """
        Compute the Bray-Curtis distance between two matrices.
        The Bray-Curtis distance is a measure of dissimilarity between two
        non-negative vectors or matrices. It is defined as the sum of the
        absolute differences divided by the sum of the values.
        Parameters:
            a (Matrix): The first input matrix.
            b (Matrix): The second input matrix. Must have the same shape as `a`.
        Returns:
            float: The Bray-Curtis distance between the two matrices. Returns 0.0
            if the denominator is zero.
        Raises:
            ValueError: If the input matrices do not have the same shape.
        Notes:
            - The input matrices are flattened into vectors before computing the
              distance.
            - If the denominator is zero, the function returns 0.0 instead of
              raising an error.
        Example:
            >>> a = Matrix([[1, 2], [3, 4]])
            >>> b = Matrix([[4, 3], [2, 1]])
            >>> bray_curtis(a, b)
            0.3333333333333333
        """
        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        numerator = sum(abs(x - y) for x, y in zip(vec_a, vec_b))
        denominator = sum(x + y for x, y in zip(vec_a, vec_b))

        if denominator == 0:
            return 0.0  # Or optionally: raise ValueError("Zero denominator")

        return numerator / denominator

    @staticmethod
    def canberra(a: Matrix, b: Matrix) -> float:
        """
        Compute the Canberra distance between two matrices.
        The Canberra distance is a weighted version of the Manhattan distance, 
        where the absolute differences between elements are normalized by the 
        sum of their absolute values.
        Parameters:
            a (Matrix): The first input matrix.
            b (Matrix): The second input matrix.
        Returns:
            float: The Canberra distance between the two matrices.
        Raises:
            ValueError: If the input matrices do not have the same shape.
        Notes:
            - The input matrices must have the same shape.
            - If both elements being compared are zero, their contribution 
              to the distance is treated as zero.
        """
        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        total = 0.0
        for x, y in zip(vec_a, vec_b):
            numerator = abs(x - y)
            denominator = abs(x) + abs(y)
            if denominator != 0:
                total += numerator / denominator
            else:
                total += 0  # both x and y are 0

        return total

    @staticmethod
    def jaccard(a: Matrix, b: Matrix) -> float:
        """
        Compute the Jaccard distance between two binary matrices.
        The Jaccard distance is defined as 1 minus the Jaccard index, which is the
        size of the intersection divided by the size of the union of two sets.
        This implementation assumes the input matrices are binary (contain only 0s and 1s).
        Args:
            a (Matrix): The first binary matrix.
            b (Matrix): The second binary matrix.
        Returns:
            float: The Jaccard distance between the two matrices. Returns 0.0 if the
            union of the two matrices is empty.
        Raises:
            ValueError: If the input matrices do not have the same shape.
        Notes:
            - The matrices are flattened into vectors before computing the distance.
            - The result is 0.0 if both matrices are empty (i.e., their union is empty).
        """
        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        intersection = sum(1 for x, y in zip(vec_a, vec_b) if x == y == 1)
        union = sum(1 for x, y in zip(vec_a, vec_b) if x == 1 or y == 1)

        if union == 0:
            return 0.0  # or define as 1.0 depending on your convention

        return 1 - (intersection / union)

    @staticmethod
    def hamming(a: Matrix, b: Matrix) -> int:
        """
        Compute the Hamming distance between two matrices.
        The Hamming distance is defined as the number of positions at which 
        the corresponding elements of two matrices are different. The matrices 
        must have the same shape.
        Args:
            a (Matrix): The first input matrix.
            b (Matrix): The second input matrix.
        Returns:
            int: The Hamming distance between the two matrices.
        Raises:
            ValueError: If the input matrices do not have the same shape.
        Example:
            >>> a = Matrix([[1, 0, 1], [1, 1, 0]])
            >>> b = Matrix([[1, 1, 0], [1, 0, 0]])
            >>> hamming(a, b)
            3
        """

        if a.shape != b.shape:
            raise ValueError("Matrices must have the same shape")

        vec_a = Operations.flatten(a)
        vec_b = Operations.flatten(b)

        return sum(x != y for x, y in zip(vec_a, vec_b))
