from src.lineales import gauss_seidel

def test_gauss_seidel():
    a = [
        [10, 2, 1],
        [1, 10, 1],
        [2, 3, 10]
    ]

    b = [14, 13, 17]

    solucion = gauss_seidel(a, b)

    # verificar
    # assert solucion == [1, 1, 1], f"Error: {solucion}"