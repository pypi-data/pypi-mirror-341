from src.lineales import gauss_jordan

def test_gauss_jordan():
    a = [
        [1, -1, 3],
        [1, 1, 1],
        [2, 2, -1]
    ]
    b = [13, 11, 7]
    
    solucion = gauss_jordan(a, b)
    
    # verificar
    assert solucion == [2, 4, 5], f"Error: {solucion}"