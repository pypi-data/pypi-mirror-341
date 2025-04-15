from src.lineales import gauss_elimination

def test_gauss_elimination():
    a = [
        [2, 6, 1],
        [1, 2, -1],
        [5, 7, -4]
    ]
    b = [7, -1, 9]
    
    solucion = gauss_elimination(a, b)
    
    # verificar
    assert solucion == [10, -3, 5], f"Error: {solucion}"