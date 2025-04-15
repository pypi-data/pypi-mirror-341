from src.lineales import jacobi

def test_jacobi():
    a = [
        [10, 2, -3],
        [4, 7, -1],
        [-2, 1, 4]
    ]
    b = [1, -1, 5]
    
    solucion = jacobi(a, b)
    
    # verificar
    assert solucion == [0.65, -0.28, 1.64], f"Error: {solucion}"