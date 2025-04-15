from PA23013UNO.metodos_lineales import (
    eliminacion_gauss,
    gauss_jordan,
    cramer,
    descomposicion_lu,
    jacobi,
    gauss_seidel,
)
from PA23013UNO.metodos_no_lineales import biseccion

# Sistema de ecuaciones lineales
A = [[3, -0.1, -0.2], [0.1, 7, -0.3], [0.3, -0.2, 10]]
b = [7.85, -19.3, 71.4]

print("=== Métodos para Sistemas Lineales ===")
print("Eliminación de Gauss:", eliminacion_gauss(A, b))
print("Gauss-Jordan:", gauss_jordan(A, b))
print("Regla de Cramer:", cramer(A, b))
print("Descomposición LU:", descomposicion_lu(A, b))

# Métodos iterativos
try:
    print("Jacobi:", jacobi(A, b))
except ValueError as e:
    print("Jacobi:", str(e))

try:
    print("Gauss-Seidel:", gauss_seidel(A, b))
except ValueError as e:
    print("Gauss-Seidel:", str(e))

# Ecuación no lineal
f = lambda x: x**3 - 2 * x - 5
a, b = 2, 3

print("\n=== Métodos para Ecuaciones No Lineales ===")
raiz, iteraciones = biseccion(f, a, b)
print(f"Raíz encontrada por Bisección: {raiz:.6f} en {iteraciones} iteraciones")