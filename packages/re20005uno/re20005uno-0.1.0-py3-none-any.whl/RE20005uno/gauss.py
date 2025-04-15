import numpy as np
def gauss_elimination(A, b):
    n = len(A)
    for i in range(n):
    
        if A[i, i] == 0:
            raise ValueError("Matriz singular")
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]
    
    x = np.zeros_like(b)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]
    return x
