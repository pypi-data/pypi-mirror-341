import numpy as np

def jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(b)
    x = np.zeros_like(b) if x0 is None else x0
    D = np.diag(A)
    R = A - np.diagflat(D)
    for _ in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x