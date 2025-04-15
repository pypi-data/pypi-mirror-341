import numpy as np

def gauss_jordan(A, b):
    A = A.astype(float)
    b = b.astype(float).reshape(-1, 1)
    Ab = np.hstack([A, b])
    n = len(b)
    for i in range(n):
        Ab[i] = Ab[i] / Ab[i, i]
        for j in range(n):
            if i != j:
                Ab[j] = Ab[j] - Ab[j, i] * Ab[i]
    return Ab[:, -1]