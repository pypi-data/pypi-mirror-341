import unittest
from solver.nonlinear.jacobi import jacobi_method
from solver.nonlinear.gauss_seidel import gauss_seidel_method
from solver.nonlinear.bisection import bisection_method

class TestNonlinearMethods(unittest.TestCase):

    def test_jacobi_method(self):
        equations = [
            "x + y = 10",
            "2*x + 3*y = 24"
        ]
        initial_guess = [0, 0]
        solution = jacobi_method(equations, initial_guess)
        self.assertAlmostEqual(solution[0], 6.0, places=1)
        self.assertAlmostEqual(solution[1], 4.0, places=1)

    def test_gauss_seidel_method(self):
        equations = [
            "x + y = 10",
            "2*x + 3*y = 24"
        ]
        initial_guess = [0, 0]
        solution = gauss_seidel_method(equations, initial_guess)
        self.assertAlmostEqual(solution[0], 6.0, places=1)
        self.assertAlmostEqual(solution[1], 4.0, places=1)

    def test_bisection_method(self):
        func = lambda x: x**2 - 4
        a, b = 0, 3
        root = bisection_method(func, a, b)
        self.assertAlmostEqual(root, 2.0, places=1)

if __name__ == '__main__':
    unittest.main()