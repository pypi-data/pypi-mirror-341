
def gauss_elimination(a, b):
    n = len(b)

    # eliminacion
    for i in range(n):
        # encontrar la fila con el mayor valor
        max_value = 0
        max_row = i

        for row in range(i, n):
            value = abs(a[row][i])
            if value > max_value:
                max_value = value
                max_row = row

        # intercambiar filas
        if i != max_row:
            # guardar fila 
            temp_row = a[i]
            a[i] = a[max_row]
            a[max_row] = temp_row

            temp_value = b[i]
            b[i] = b[max_row]
            b[max_row] = temp_value

        # eliminar debajo del pivot
        for j in range(i + 1, n):
            factor = a[j][i] / a[i][i]

            # Actualizar fila j restando factor * fila i
            for k in range(i, n):
                a[j][k] = a[j][k] - factor * a[i][k]

            b[j] = b[j] - factor * b[i]

    # Sustitucion hacia atras
    x = []
    for _ in range(n):
        x.append(0) 

    # resolviendo las incognitas
    for i in range(n - 1, -1, -1):
        total = 0
        for j in range(i + 1, n):
            total = total + a[i][j] * x[j]

        x[i] = (b[i] - total) / a[i][i]
        x[i] = round(x[i], 2)

    return x

