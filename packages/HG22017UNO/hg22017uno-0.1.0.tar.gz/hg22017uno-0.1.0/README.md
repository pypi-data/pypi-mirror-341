# Linear and Nonlinear Solver

This project provides a Python library for solving both linear and nonlinear systems of equations using various numerical methods. The library includes implementations of the following methods:

## Linear Methods
1. **Gauss Elimination**: A method for solving linear systems by transforming the system into an upper triangular matrix.
2. **Gauss-Jordan Elimination**: An extension of Gauss elimination that reduces the matrix to reduced row echelon form.
3. **Cramer's Rule**: A method for solving linear systems using determinants, applicable when the system has a unique solution.
4. **LU Decomposition**: A method that factors a matrix into a lower triangular matrix and an upper triangular matrix to simplify solving linear systems.

## Nonlinear Methods
1. **Jacobi Method**: An iterative method for solving a system of nonlinear equations.
2. **Gauss-Seidel Method**: An improvement over the Jacobi method that uses the latest available values for faster convergence.
3. **Bisection Method**: A root-finding method that repeatedly bisects an interval and selects a subinterval in which a root exists.

## Installation

To install the library, clone the repository and run the following command:

```
pip install .
```

## Usage

### Linear Methods

```python
from solver.linear.gauss_elimination import gauss_elimination
from solver.linear.gauss_jordan import gauss_jordan
from solver.linear.cramer_rule import cramer_rule
from solver.linear.lu_decomposition import lu_decomposition

# Example usage
matrix = [[2, 1, -1], [3, 3, 9], [3, 3, 5]]
b = [8, 0, 4]

solution = gauss_elimination(matrix, b)
```

### Nonlinear Methods

```python
from solver.nonlinear.jacobi import jacobi_method
from solver.nonlinear.gauss_seidel import gauss_seidel_method
from solver.nonlinear.bisection import bisection_method

# Example usage
def func(x):
    return x**3 - x - 2

root = bisection_method(func, 1, 2)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.