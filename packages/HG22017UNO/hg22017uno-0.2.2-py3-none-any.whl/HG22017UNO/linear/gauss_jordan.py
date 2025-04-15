def gauss_jordan(matrix, results):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Jordan.
    :param matrix: Matriz de coeficientes (lista de listas).
    :param results: Vector de resultados (lista).
    :return: Solución del sistema (lista).
    """
    n = len(matrix)
    for i in range(n):
        # Normalizar la fila actual
        factor = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= factor
        results[i] /= factor

        # Hacer ceros en la columna actual
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(n):
                    matrix[k][j] -= factor * matrix[i][j]
                results[k] -= factor * results[i]
    return results