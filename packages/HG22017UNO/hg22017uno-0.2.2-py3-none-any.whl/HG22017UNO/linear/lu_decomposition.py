import numpy as np
from scipy.linalg import lu

def lu_decomposition(matrix, results):
    """
    Resuelve un sistema de ecuaciones lineales usando la descomposición LU.
    :param matrix: Matriz de coeficientes (lista de listas).
    :param results: Vector de resultados (lista).
    :return: Solución del sistema (lista).
    """
    P, L, U = lu(matrix)
    # Resolver Ly = Pb
    y = np.linalg.solve(L, np.dot(P, results))
    # Resolver Ux = y
    x = np.linalg.solve(U, y)
    return x