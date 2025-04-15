import numpy as np

def cramer(A, b):
    n = len(A)
    det_A = np.linalg.det(A)

    if det_A == 0:
        raise ValueError("El sistema no tiene solución única.")

    soluciones = []
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        soluciones.append(np.linalg.det(Ai) / det_A)
    
    return np.array(soluciones)
