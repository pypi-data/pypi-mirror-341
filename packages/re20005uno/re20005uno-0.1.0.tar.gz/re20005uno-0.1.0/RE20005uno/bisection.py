import numpy as np

def bisection(func, a, b, tol=1e-12, max_iter=10000):
    if func(a) * func(b) > 0:
        raise ValueError("Los extremos no cumplen la condición de cambio de signo")

    for _ in range(max_iter):
        c = (a + b) / 2
        fc = func(c)

        if abs(b - a) < tol or abs(fc) < tol:
            return c

        if func(a) * fc < 0:
            b = c
        else:
            a = c

    return c

if __name__ == "__main__":
    def f(x):
        return x**3 - x - 2

    a = 2.7  
    b = 2.9  

    resultado = bisection(f, a, b)
    print("Raíz encontrada:", np.round(resultado, 12))