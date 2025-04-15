def lu_decomposition(a):
    n = len(a)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        # Construir U
        for k in range(i, n):
            suma = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = a[i][k] - suma

        # Construir L
        for k in range(i, n):
            if i == k:
                L[i][i] = 1.0
            else:
                suma = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (a[k][i] - suma) / U[i][i]

    return L, U

def sustituir_adelante(L, b):
    n = len(b)
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    return y

def sustituir_atras(U, y):
    n = len(y)
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i+1, n))) / U[i][i]
    return x

def lu(a, b):
    L, U = lu_decomposition(a)
    y = sustituir_adelante(L, b)
    x = sustituir_atras(U, y)

    # Redondear 
    for i in range(len(x)):
        x[i] = round(x[i], 2)
    # Devolver el vector solución
    return x
