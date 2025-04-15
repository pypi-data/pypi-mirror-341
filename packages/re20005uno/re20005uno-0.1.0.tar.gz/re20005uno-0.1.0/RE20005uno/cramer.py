import numpy as np

def cramer(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    if A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada.")
    if A.shape[0] != b.shape[0]:
        raise ValueError("El tamaño de b debe coincidir con el número de filas de A.")

    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("La matriz no es invertible (determinante cero).")

    n = len(A)
    x = np.zeros_like(b, dtype=float)

    for i in range(n):
        A_copy = A.copy()
        A_copy[:, i] = b
        x[i] = np.linalg.det(A_copy) / det_A

    return x

if __name__ == "__main__":
    A = [
        [2, -1, 5],
        [1, 1, -3],
        [2, 4, 1]
    ]
    b = [-3, -2, 9]

    resultado = cramer(A, b)
    print("Resultado:", np.round(resultado, 4))