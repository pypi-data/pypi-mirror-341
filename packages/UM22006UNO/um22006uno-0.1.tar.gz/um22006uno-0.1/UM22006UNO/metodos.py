
import numpy as np
from scipy.linalg import lu
from scipy.optimize import bisect

def gauss_elimination(A, b):
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    for i in range(n):
        for j in range(i+1, n):
            ratio = A[j][i] / A[i][i]
            A[j][i:] -= ratio * A[i][i:]
            b[j] -= ratio * b[i]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i][i+1:], x[i+1:])) / A[i][i]
    return x

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

def lu_decomposition(A, b):
    P, L, U = lu(A)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x

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

def biseccion(f, a, b, tol=1e-10, max_iter=100):
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo.")
    for _ in range(max_iter):
        c = (a + b) / 2
        if f(c) == 0 or (b - a) / 2 < tol:
            return c
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2

if __name__ == "__main__":
    A = np.array([[2.0, 1.0], [5.0, 7.0]])
    b = np.array([11.0, 13.0])
    print("Gauss:", gauss_elimination(A.copy(), b.copy()))
    print("Gauss-Jordan:", gauss_jordan(A.copy(), b.copy()))
    print("Cramer:", cramer(A.copy(), b.copy()))
    print("LU:", lu_decomposition(A.copy(), b.copy()))
    print("Jacobi:", jacobi(A.copy(), b.copy()))
    print("Gauss-Seidel:", gauss_seidel(A.copy(), b.copy()))
    f = lambda x: x**3 - x - 2
    print("Bisección:", biseccion(f, 1, 2))
