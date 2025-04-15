def biseccion(f, a, b, tolerancia=1e-10, max_iter=100):
    if f(a) * f(b) >= 0:
        raise ValueError("a y b deben tener signos opuestos")

    for _ in range(max_iter):
        c = (a + b) / 2.0
        if abs(f(c)) < tolerancia or (b - a) / 2 < tolerancia:
            return c

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    raise Exception("El metodo no convergio")
