def jacobi(a, b, tolerancia=1e-10, max_iter=100):
    """
    Resuelve Ax = b usando el método de Jacobi.
    a: matriz de coeficientes
    b: vector de términos independientes
    tolerancia: error aceptable
    max_iter: número máximo de iteraciones
    """
    n = len(a)
    x = [0.0 for _ in range(n)]  # x inicial
    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            suma = sum(a[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / a[i][i]

        # verificar convergencia
        if all(abs(x_new[i] - x[i]) < tolerancia for i in range(n)):
            return [round(val, 2) for val in x_new]
        x = x_new

    raise Exception("El metodo no convergio")
