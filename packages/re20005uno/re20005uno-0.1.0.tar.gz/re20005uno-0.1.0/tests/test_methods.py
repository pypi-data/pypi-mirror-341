import unittest
import numpy as np
from RE20005uno import gauss_elimination, gauss_jordan, cramer, lu_decomposition, jacobi, gauss_seidel, bisection

class TestLinearSolvers(unittest.TestCase):
    def test_gauss_elimination(self):
        A = np.array([[3, -2,  4], [1,  1,  1], [2,  3, -3]], dtype=float)
        b = np.array([9, 4, -3], dtype=float)
        result = gauss_elimination(A, b)
        self.assertEqual(list(result), [2.0, 3.0, -1.0])

    def test_gauss_jordan(self):
        A = np.array([[3, -2,  4], [1,  1,  1], [2,  3, -3]], dtype=float)
        b = np.array([9, 4, -3], dtype=float)
        result = gauss_jordan(A, b)
        self.assertEqual(list(result), [2.0, 3.0, -1.0])

    def test_cramer(self):
        A = np.array([[3, -2,  4], [1,  1,  1], [2,  3, -3]], dtype=float)
        b = np.array([9, 4, -3], dtype=float)
        result = cramer(A, b)
        self.assertEqual([float(x) for x in result], [2.0, 3.0, -1.0])

    def test_lu_decomposition(self):
        A = np.array([[4, 3], [6, 3]], dtype=float)
        b = np.array([10, 15], dtype=float)
        L, U = lu_decomposition(A)
        self.assertTrue(np.allclose(np.dot(L, U), A))

    def test_jacobi(self):
        A = np.array([[4, -1, 0, 0], [-1, 4, -1, 0], [0, -1, 4, -1], [0, 0, -1, 3]], dtype=float)
        b = np.array([15, 10, 10, 10], dtype=float)
        result = jacobi(A, b)
        self.assertEqual(list(result), [2.3333333333333335, 0.6666666666666667, -1.0, 2.0])

    def test_gauss_seidel(self):
        A = np.array([[4, -1, 0, 0], [-1, 4, -1, 0], [0, -1, 4, -1], [0, 0, -1, 3]], dtype=float)
        b = np.array([15, 10, 10, 10], dtype=float)
        result = gauss_seidel(A, b)
        self.assertEqual(list(result), [2.3333333333333335, 0.6666666666666667, -1.0, 2.0])

    def test_bisection(self):
        def func(x): return x**3 - 4*x - 9
        result = bisection(func, 2, 3)
        self.assertEqual(result, 2.8793852415718)

if __name__ == '__main__':
    unittest.main()

