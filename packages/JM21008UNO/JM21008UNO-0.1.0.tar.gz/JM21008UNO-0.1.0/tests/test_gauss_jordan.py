import unittest
from jm21008uno.gauss_jordan import resolver_gauss_jordan

class TestGaussJordan(unittest.TestCase):

    def test_simple_system(self):
        A = [[2, 1, -1],
             [-3, -1, 2],
             [-2, 1, 2]]
        b = [8, -11, -3]
        expected = [2, 3, -1]
        result = resolver_gauss_jordan(A, b)
        self.assertEqual(result, expected)

    def test_no_solution(self):
        A = [[1, 2, 3],
             [2, 4, 6],
             [3, 6, 9]]
        b = [1, 2, 3]
        with self.assertRaises(ValueError):
            resolver_gauss_jordan(A, b)

    def test_infinite_solutions(self):
        A = [[1, 2, 3],
             [2, 4, 6],
             [0, 0, 0]]
        b = [1, 2, 0]
        with self.assertRaises(ValueError):
            resolver_gauss_jordan(A, b)

    def test_complex_numbers(self):
        A = [[1, 1],
             [1, -1]]
        b = [2, 0]
        expected = [1, 1]
        result = resolver_gauss_jordan(A, b)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()