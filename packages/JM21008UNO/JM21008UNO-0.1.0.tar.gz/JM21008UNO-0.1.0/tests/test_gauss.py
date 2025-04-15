import unittest
import numpy as np
from jm21008uno.gauss import resolver_gauss

class TestGaussMethod(unittest.TestCase):

    def test_simple_system(self):
        A = np.array([[2, 1], [1, 3]])
        b = np.array([8, 13])
        expected_solution = np.array([3, 2])
        result = resolver_gauss(A, b)
        np.testing.assert_array_almost_equal(result, expected_solution, decimal=6)

    def test_no_solution(self):
        A = np.array([[1, 2], [2, 4]])
        b = np.array([5, 10])
        with self.assertRaises(ValueError):
            resolver_gauss(A, b)

    def test_infinite_solutions(self):
        A = np.array([[1, 2], [2, 4]])
        b = np.array([5, 10])
        with self.assertRaises(ValueError):
            resolver_gauss(A, b)

    def test_large_system(self):
        A = np.random.rand(100, 100)
        b = np.random.rand(100)
        solution = resolver_gauss(A, b)
        self.assertEqual(solution.shape, (100,))

class TestGauss(unittest.TestCase):
    def test_resolver_gauss(self):
        matriz = [[2, 1], [5, 7]]
        vector = [11, 13]
        resultado = resolver_gauss(matriz, vector)
        self.assertAlmostEqual(resultado[0], 7.1111, places=4)
        self.assertAlmostEqual(resultado[1], -3.2222, places=4)

if __name__ == '__main__':
    unittest.main()
