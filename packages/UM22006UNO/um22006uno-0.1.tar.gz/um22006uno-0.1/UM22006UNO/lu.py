import numpy as np
from scipy.linalg import lu

def lu_decomposition(A, b):
    P, L, U = lu(A)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x