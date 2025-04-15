import numpy as np

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(b)
    x = np.zeros_like(b) if x0 is None else x0
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x