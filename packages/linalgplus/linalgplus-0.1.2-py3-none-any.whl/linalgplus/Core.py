class Matrix:
    def __init__(self, data):
        self.data = data
        if not self.__ensure_matrix():
            raise ValueError("All rows must have the same length.")
        if not self.__ensure_values():
            raise ValueError("Matrix must contain only numbers.")

        self.shape = self._get_shape()
        self.is_square = self.shape[0] == self.shape[1]

    def _get_shape(self):
        return (len(self.data), len(self.data[0])) if self.data else (0, 0)

    def __ensure_matrix(self):
        return all(l == len(self.data[0]) for l in [len(row) for row in self.data])

    def __ensure_values(self):
        for row in self.data:
            for cell in row:
                if not isinstance(cell, (int, float)):
                    return False
        return True

    def to_string(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.data])

    def __repr__(self):
        return self.__repr_recursive()

    def __repr_recursive(self, depth=0):
        if depth == len(self.data):
            return ""
        return str(self.data[depth]) + "\n" + self.__repr_recursive(depth + 1)

    def __str__(self):
        return self.to_string()

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False

        if other.shape != self.shape:
            return False

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if other.data[i][j] != self.data[i][j]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
