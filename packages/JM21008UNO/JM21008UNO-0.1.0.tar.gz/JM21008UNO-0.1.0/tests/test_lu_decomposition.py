import unittest
from jm21008uno.lu_decomposition import resolver_lu

class TestLUDecomposition(unittest.TestCase):

    def test_lu_decomposition(self):
        A = [[4, 3], [6, 3]]
        b = [10, 12]
        expected_solution = [1, 2]
        
        solution = resolver_lu(A, b)
        
        self.assertAlmostEqual(solution[0], expected_solution[0], places=5)
        self.assertAlmostEqual(solution[1], expected_solution[1], places=5)

    def test_lu_decomposition_singular_matrix(self):
        A = [[1, 2], [2, 4]]
        b = [5, 10]
        
        with self.assertRaises(ValueError):
            resolver_lu(A, b)

if __name__ == '__main__':
    unittest.main()