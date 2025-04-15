import unittest
import numpy as np
from jm21008uno.cramer import resolver_cramer

class TestCramer(unittest.TestCase):

    def test_resolver_cramer(self):
        # Test case 1: Simple 2x2 system
        A = [[3, 2], [1, 4]]
        B = [5, 6]
        expected = [2, 0.5]
        result = resolver_cramer(A, B)
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

        # Test case 2: Simple 3x3 system
        A = [[2, -1, 3], [1, 3, 2], [3, 2, -4]]
        B = [10, 13, -2]
        expected = [1, 2, 3]
        result = resolver_cramer(A, B)
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

        # Test case 3: Another 3x3 system
        A = [[1, 2, 1], [2, 3, 1], [1, -1, 2]]
        B = [4, 7, 3]
        expected = [1, 1, 1]
        result = resolver_cramer(A, B)
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

if __name__ == '__main__':
    unittest.main()