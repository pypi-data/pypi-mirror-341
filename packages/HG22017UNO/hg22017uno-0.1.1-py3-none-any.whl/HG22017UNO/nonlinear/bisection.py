def bisection_method(func, a, b, tolerance=1e-10, max_iterations=100):
    """
    Encuentra una raíz de una función no lineal usando el método de bisección.
    :param func: Función a evaluar.
    :param a: Límite inferior del intervalo.
    :param b: Límite superior del intervalo.
    :param tolerance: Tolerancia para la convergencia.
    :param max_iterations: Número máximo de iteraciones.
    :return: Raíz de la función.
    """
    if func(a) * func(b) >= 0:
        raise ValueError("El intervalo no contiene una raíz.")

    for _ in range(max_iterations):
        c = (a + b) / 2
        if abs(func(c)) < tolerance or (b - a) / 2 < tolerance:
            return c
        if func(a) * func(c) < 0:
            b = c
        else:
            a = c
    raise ValueError("El método de bisección no converge.")
