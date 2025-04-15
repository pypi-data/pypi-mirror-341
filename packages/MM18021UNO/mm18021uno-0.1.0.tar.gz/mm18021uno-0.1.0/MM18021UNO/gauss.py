import numpy as np

def gauss(A, b):
    n = len(b)
    A = A.astype(float)
    b = b.astype(float)

    for i in range(n):
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]
    
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i,i+1:], x[i+1:])) / A[i][i]
    
    return x
