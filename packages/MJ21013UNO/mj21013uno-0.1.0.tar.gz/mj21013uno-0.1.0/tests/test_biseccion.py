from src.no_lineales import biseccion

def test_biseccion():
    def f(x):
        return x**2 - 4  # La raíz es 2

    a = 0
    b = 3

    solucion = biseccion(f, a, b)

    # Verificar
    assert abs(solucion - 2) < 1e-5, f"Error: {solucion}"