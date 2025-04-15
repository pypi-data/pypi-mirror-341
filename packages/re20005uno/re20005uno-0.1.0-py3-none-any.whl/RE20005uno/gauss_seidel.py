import numpy as np

def gauss_seidel(A, b, max_iter=1000, tol=1e-10):
    x = np.zeros_like(b)
    for _ in range(max_iter):
        x_old = x.copy()
        for i in range(len(b)):
            x[i] = (b[i] - np.dot(A[i, :i], x[:i]) - np.dot(A[i, i+1:], x_old[i+1:])) / A[i, i]
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            break
    return x
    
    raise ValueError("El método no converge dentro del número máximo de iteraciones")


# Ejemplo de uso
if __name__ == "__main__":
    A = [
        [4, -1, 0, 0],
        [-1, 4, -1, 0],
        [0, -1, 4, -1],
        [0, 0, -1, 3]
    ]
    b = [15, 10, 10, 10]
    resultado = gauss_seidel(A, b)
    print("Resultado:", resultado)
