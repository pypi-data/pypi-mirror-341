import unittest
from jm21008uno.jacobi import resolver_jacobi

class TestJacobi(unittest.TestCase):

    def test_resolver_jacobi(self):
        # Test case 1: Simple 2x2 system (diagonal dominante)
        A = [[4, 1],
             [2, 3]]
        b = [15, 18]
        expected_solution = [3, 4]
        solution = resolver_jacobi(A, b, tol=1e-10, max_iterations=100)
        self.assertAlmostEqual(solution[0], expected_solution[0], places=1)
        self.assertAlmostEqual(solution[1], expected_solution[1], places=1)

        # Test case 2: No solution
        A_no_solution = [[1, 2],
                         [2, 4]]
        b_no_solution = [1, 2]
        with self.assertRaises(ValueError):
            resolver_jacobi(A_no_solution, b_no_solution)

        # Test case 3: Infinite solutions
        A_infinite = [[1, 2],
                      [2, 4]]
        b_infinite = [2, 4]
        with self.assertRaises(ValueError):
            resolver_jacobi(A_infinite, b_infinite)

if __name__ == '__main__':
    unittest.main()