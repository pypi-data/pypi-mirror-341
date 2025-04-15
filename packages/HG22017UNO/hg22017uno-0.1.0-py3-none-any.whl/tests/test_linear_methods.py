import unittest
from solver.linear.gauss_elimination import gauss_elimination
from solver.linear.gauss_jordan import gauss_jordan
from solver.linear.cramer_rule import cramer_rule
from solver.linear.lu_decomposition import lu_decomposition

class TestLinearMethods(unittest.TestCase):

    def test_gauss_elimination(self):
        matrix = [[2, 1, -1], [3, 2, -1], [1, 1, 1]]
        b = [8, 13, 3]
        result = gauss_elimination(matrix, b)
        expected = [2, 3, 1]
        self.assertEqual(result, expected)

    def test_gauss_jordan(self):
        matrix = [[2, 1, -1], [3, 2, -1], [1, 1, 1]]
        b = [8, 13, 3]
        result = gauss_jordan(matrix, b)
        expected = [2, 3, 1]
        self.assertEqual(result, expected)

    def test_cramer_rule(self):
        matrix = [[2, 1, -1], [3, 2, -1], [1, 1, 1]]
        b = [8, 13, 3]
        result = cramer_rule(matrix, b)
        expected = [2, 3, 1]
        self.assertEqual(result, expected)

    def test_lu_decomposition(self):
        matrix = [[2, 1, -1], [3, 2, -1], [1, 1, 1]]
        b = [8, 13, 3]
        result = lu_decomposition(matrix, b)
        expected = [2, 3, 1]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()