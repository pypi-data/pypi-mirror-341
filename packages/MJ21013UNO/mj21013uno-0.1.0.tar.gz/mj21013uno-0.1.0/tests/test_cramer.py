from src.lineales import cramer

def test_cramer():
    a = [
        [1, 2, 1],
        [3, 1, 1],
        [2, 3, -1]
    ]
    b = [7, 5, 3]
    
    solucion = cramer(a, b)
    
    # verificar
    assert solucion == [0, 2, 3], f"Error: {solucion}"