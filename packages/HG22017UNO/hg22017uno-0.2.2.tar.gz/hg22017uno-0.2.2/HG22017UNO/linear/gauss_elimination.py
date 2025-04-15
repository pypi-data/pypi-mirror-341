def gauss_elimination(matrix, results):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de eliminación de Gauss.
    :param matrix: Matriz de coeficientes (lista de listas).
    :param results: Vector de resultados (lista).
    :return: Solución del sistema (lista).
    """
    n = len(matrix)
    for i in range(n):
        # Pivoteo
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
            results[j] -= factor * results[i]

    # Sustitución hacia atrás
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = results[i]
        for j in range(i + 1, n):
            x[i] -= matrix[i][j] * x[j]
        x[i] /= matrix[i][i]
    return x