from PA23013UNO.metodos_lineales import (
    eliminacion_gauss,
    gauss_jordan,
    cramer,
    descomposicion_lu,
    jacobi,
    gauss_seidel,
)
from PA23013UNO.metodos_no_lineales import biseccion

# Ejemplo de sistema lineal
A = [[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]
b = [1, -2, 0]

print("=== Métodos para Sistemas Lineales ===")
print("Eliminación de Gauss:", eliminacion_gauss(A, b))
print("Gauss-Jordan:", gauss_jordan(A, b))
print("Regla de Cramer:", cramer(A, b))
print("Descomposición LU:", descomposicion_lu(A, b))
print("Jacobi:", jacobi(A, b))
print("Gauss-Seidel:", gauss_seidel(A, b))

# Ejemplo de ecuación no lineal
def f(x):
    return x**3 - x - 2

print("\n=== Métodos para Ecuaciones No Lineales ===")
print("Bisección:", biseccion(f, 1, 2))