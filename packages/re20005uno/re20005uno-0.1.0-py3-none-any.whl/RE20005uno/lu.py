import numpy as np

def lu_decomposition(A):
    n = len(A)
    L = np.zeros_like(A)
    U = np.zeros_like(A)
    
    for i in range(n):
        L[i, i] = 1
        for j in range(i, n):
            U[i, j] = A[i, j] - np.dot(L[i, :i], U[:i, j])
        for j in range(i+1, n):
            L[j, i] = (A[j, i] - np.dot(L[j, :i], U[:i, i])) / U[i, i]
    
    return L, U


def solve_lu(L, U, b):
    n = len(b)
    y = np.zeros_like(b, dtype=float)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])

    x = np.zeros_like(b, dtype=float)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]

    return x

if __name__ == "__main__":
    A = [
        [4, -2, 1],
        [3, 6, -1],
        [2, 1, 5]
    ]
    b = [1, 2, 3]
    
    L, U = lu_decomposition(A)
    resultado = solve_lu(L, U, b)
    print("Resultado:", resultado)
