import numpy as np

def cramer(A, b):
    detA = np.linalg.det(A)
    if detA == 0:
        raise ValueError("El sistema no tiene solución única.")
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        Ai = np.copy(A)
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / detA
    return x