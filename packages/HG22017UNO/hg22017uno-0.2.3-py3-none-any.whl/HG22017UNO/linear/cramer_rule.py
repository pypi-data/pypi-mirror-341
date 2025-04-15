import numpy as np

def cramer_rule(matrix, results):
    """
    Resuelve un sistema de ecuaciones lineales usando la regla de Cramer.
    :param matrix: Matriz de coeficientes (lista de listas).
    :param results: Vector de resultados (lista).
    :return: Solución del sistema (lista).
    """
    det_main = np.linalg.det(matrix)
    if det_main == 0:
        raise ValueError("El sistema no tiene solución única (determinante = 0).")

    n = len(matrix)
    solutions = []
    for i in range(n):
        temp_matrix = [row[:] for row in matrix]
        for j in range(n):
            temp_matrix[j][i] = results[j]
        solutions.append(np.linalg.det(temp_matrix) / det_main)
    return solutions