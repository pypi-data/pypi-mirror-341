import numpy as np

class Matrix:
    def __init__(self, data):
        self.data = np.array(data)

    def transpose(self):
        return Matrix(self.data.T)

    def add(self, other):
        if self.data.shape != other.data.shape:
            raise ValueError("Matrix dimensions must match for addition.")
        return Matrix(self.data + other.data)

    def multiply(self, other):
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Matrix A columns must match Matrix B rows for multiplication.")
        return Matrix(np.dot(self.data, other.data))

    def is_symmetric(self):
        return np.array_equal(self.data, self.data.T)

    def __repr__(self):
        return f"Matrix({self.data.tolist()})"


def generate_identity(n):
    return Matrix(np.eye(n, dtype=int))


def generate_tridiagonal(n, lower=-1, main=2, upper=-1):
    data = np.zeros((n, n), dtype=int)
    for i in range(n):
        data[i, i] = main
        if i > 0:
            data[i, i - 1] = lower
        if i < n - 1:
            data[i, i + 1] = upper
    return Matrix(data)


def generate_triband(n, bandwidth=1, value=1):
    data = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(max(0, i - bandwidth), min(n, i + bandwidth + 1)):
            data[i, j] = value
    return Matrix(data)


def generate_diagonal(values):
    return Matrix(np.diag(values))


def generate_upper_triangular(n, fill=1):
    data = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i, n):
            data[i, j] = fill
    return Matrix(data)


def generate_lower_triangular(n, fill=1):
    data = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1):
            data[i, j] = fill
    return Matrix(data)


def generate_symmetric(base):
    base = np.array(base)
    return Matrix((base + base.T) // 2)


def generate_toeplitz(first_row, first_col):
    n = len(first_col)
    m = len(first_row)
    data = np.zeros((n, m), dtype=int)
    for i in range(n):
        for j in range(m):
            if i - j >= 0:
                data[i][j] = first_col[i - j]
            else:
                data[i][j] = first_row[j - i]
    return Matrix(data)


def generate_hankel(first_col, last_row):
    n = len(first_col)
    m = len(last_row)
    data = np.zeros((n, m), dtype=int)
    for i in range(n):
        for j in range(m):
            if i + j < len(first_col):
                data[i][j] = first_col[i + j]
            else:
                data[i][j] = last_row[i + j - len(first_col) + 1]
    return Matrix(data)


def generate_circulant(first_row):
    n = len(first_row)
    data = np.zeros((n, n), dtype=int)
    for i in range(n):
        data[i] = first_row[-i:] + first_row[:-i]
    return Matrix(data)


def is_symmetric(matrix):
    data = matrix.data if isinstance(matrix, Matrix) else np.array(matrix)
    return np.array_equal(data, data.T)


def is_toeplitz(matrix):
    data = matrix.data if isinstance(matrix, Matrix) else np.array(matrix)
    rows, cols = data.shape
    for i in range(1, rows):
        for j in range(1, cols):
            if data[i, j] != data[i - 1, j - 1]:
                return False
    return True