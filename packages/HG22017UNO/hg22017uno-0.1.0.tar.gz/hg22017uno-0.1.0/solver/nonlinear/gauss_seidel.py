import numpy as np

def gauss_seidel(matrix, results, initial_guess, tolerance=1e-10, max_iterations=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.
    :param matrix: Matriz de coeficientes (lista de listas).
    :param results: Vector de resultados (lista).
    :param initial_guess: Vector inicial (lista).
    :param tolerance: Tolerancia para la convergencia.
    :param max_iterations: Número máximo de iteraciones.
    :return: Solución del sistema (lista).
    """
    n = len(matrix)
    x = initial_guess[:]
    for _ in range(max_iterations):
        x_new = x[:]
        for i in range(n):
            sum_ = sum(matrix[i][j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (results[i] - sum_) / matrix[i][i]
        if np.linalg.norm(np.array(x_new) - np.array(x), ord=np.inf) < tolerance:
            return x_new
        x = x_new
    raise ValueError("El método de Gauss-Seidel no converge.")