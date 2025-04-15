import pytest
from matrixx import (
    Matrix,
    generate_identity,
    generate_tridiagonal,
    generate_triband,
    generate_diagonal,
    generate_upper_triangular,
    generate_lower_triangular,
    generate_symmetric,
    generate_toeplitz,
    generate_hankel,
    generate_circulant,
    is_symmetric,
    is_toeplitz
)

def test_identity():
    m = generate_identity(3)
    assert (m.data == [[1,0,0],[0,1,0],[0,0,1]]).all()

def test_addition():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    c = a.add(b)
    assert (c.data == [[6, 8], [10, 12]]).all()

def test_multiplication():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[2, 0], [1, 2]])
    result = a.multiply(b)
    assert (result.data == [[4, 4], [10, 8]]).all()

def test_symmetric():
    m = generate_symmetric([[1, 2], [3, 4]])
    assert is_symmetric(m)

def test_toeplitz():
    row = [1, 2, 3]
    col = [1, 4, 5]
    t = generate_toeplitz(row, col)
    expected = [[1, 2, 3], [4, 1, 2], [5, 4, 1]]
    assert (t.data == expected).all()
    assert is_toeplitz(t)

def test_hankel():
    h = generate_hankel([1, 2, 3], [3, 4, 5])
    expected = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    assert (h.data == expected).all()

def test_circulant():
    c = generate_circulant([1, 2, 3])
    expected = [[1, 2, 3], [3, 1, 2], [2, 3, 1]]
    assert (c.data == expected).all()

def test_upper_triangular():
    m = generate_upper_triangular(3)
    expected = [[1, 1, 1], [0, 1, 1], [0, 0, 1]]
    assert (m.data == expected).all()

def test_lower_triangular():
    m = generate_lower_triangular(3)
    expected = [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
    assert (m.data == expected).all()

def test_tridiagonal():
    m = generate_tridiagonal(4, -1, 2, -1)
    expected = [[2, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 2]]
    assert (m.data == expected).all()

def test_triband():
    m = generate_triband(5, bandwidth=2, value=1)
    expected = [
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1],
        [0, 0, 1, 1, 1]
    ]
    assert (m.data == expected).all()

def test_diagonal():
    d = generate_diagonal([1, 2, 3])
    expected = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
    assert (d.data == expected).all()
