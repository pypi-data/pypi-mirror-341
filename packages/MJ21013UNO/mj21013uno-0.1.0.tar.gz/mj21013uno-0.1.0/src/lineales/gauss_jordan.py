# sistemas_ecuaciones/lineales/gauss_jordan.py

def gauss_jordan(a, b):
    n = len(a)

    for i in range(n):
        # pivoteo
        max_row = max(range(i, n), key=lambda r: abs(a[r][i]))
        if i != max_row:
            a[i], a[max_row] = a[max_row], a[i]
            b[i], b[max_row] = b[max_row], b[i]

        # normalizar (hacer 1 el pivote)
        pivot = a[i][i]
        a[i] = [x / pivot for x in a[i]]
        b[i] /= pivot

        # Hacer ceros 
        for j in range(n):
            if j != i:
                factor = a[j][i]
                a[j] = [a[j][k] - factor * a[i][k] for k in range(n)]
                b[j] -= factor * b[i]

    return b
