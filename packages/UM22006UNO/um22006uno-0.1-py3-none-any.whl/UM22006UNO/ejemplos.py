import numpy as np
from UM22006UNO.gauss import gauss_elimination
from UM22006UNO.gauss_jordan import gauss_jordan
from UM22006UNO.cramer import cramer
from UM22006UNO.lu import lu_decomposition
from UM22006UNO.jacobi import jacobi
from UM22006UNO.gauss_seidel import gauss_seidel
from UM22006UNO.biseccion import biseccion

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