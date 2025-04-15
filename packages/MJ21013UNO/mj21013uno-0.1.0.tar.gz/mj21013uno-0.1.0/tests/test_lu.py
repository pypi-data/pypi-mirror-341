from src.lineales import lu

def test_lu():
    a = [
        [1, 4, -2],
        [3, -2, 5],
        [2, 3, 1]
    ]
    b = [3, 14, 11]

    solucion = lu(a, b)

    # verificar
    assert solucion == [1, 2, 3], f"Error: {solucion}"