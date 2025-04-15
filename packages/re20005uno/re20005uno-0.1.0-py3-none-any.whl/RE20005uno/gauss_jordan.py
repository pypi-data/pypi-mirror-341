import numpy as np

def gauss_jordan(A, b):
    n = len(A)
  
    Ab = np.hstack([A, b.reshape(-1, 1)])  
    
    for i in range(n):
        Ab[i] = Ab[i] / Ab[i, i]  
        for j in range(n):
            if i != j:
                Ab[j] = Ab[j] - Ab[i] * Ab[j, i]
    
    return Ab[:, -1]  


if __name__ == "__main__":
    a = [
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ]
    b = [8, -11, -3]
    resultado = gauss_jordan(a, b)
    print("Resultado:", resultado)
