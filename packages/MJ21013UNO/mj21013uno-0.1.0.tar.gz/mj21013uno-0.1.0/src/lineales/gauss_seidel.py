def gauss_seidel(a, b, max_iterations=100):
    n = len(a)
    tolerance = 1e-2

    x = [] # valor inicial
    for i in range(n):
        x.append(0.0)

    for iteration in range(max_iterations):
        new_x = []
        for i in range(n):
            # calcular los conocidos
            sum_before = 0.0
            for j in range(i):
                sum_before += a[i][j] * new_x[j]

            # calcular los desconocidos
            sum_after = 0.0
            for j in range(i + 1, n):
                sum_after += a[i][j] * x[j]

            xi = (b[i] - (sum_before + sum_after)) / a[i][i]
            new_x.append(xi)

        # verificar la convergencia
        has_converged = True
        for i in range(n):
            difference = abs(new_x[i] - x[i])
            if difference >= tolerance:
                has_converged = False
                break

        if has_converged:
            return new_x

        # actualizar con los nuevos valores
        x = new_x

    raise Exception("El metodo no convergio")
