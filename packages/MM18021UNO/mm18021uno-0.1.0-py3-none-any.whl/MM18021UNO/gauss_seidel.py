import numpy as np

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(A)
    x = np.zeros_like(b) if x0 is None else x0.copy()

    for it in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        # Verificar convergencia
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new

        x = x_new

    raise ValueError("El método de Gauss-Seidel no convergió en las iteraciones permitidas")
