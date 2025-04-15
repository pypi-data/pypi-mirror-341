import numpy as np

def eliminacion_gauss(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método de eliminación de Gauss.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    # Eliminación hacia adelante
    for i in range(n):
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]

    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x


def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método de Gauss-Jordan.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    augmented_matrix = np.hstack([A, b.reshape(-1, 1)])

    for i in range(n):
        pivot = augmented_matrix[i, i]
        augmented_matrix[i, :] /= pivot

        for j in range(n):
            if j != i:
                factor = augmented_matrix[j, i]
                augmented_matrix[j, :] -= factor * augmented_matrix[i, :]

    return augmented_matrix[:, -1]


def cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando la regla de Cramer.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("La matriz A es singular.")

    x = []
    for i in range(n):
        A_i = A.copy()
        A_i[:, i] = b
        x_i = np.linalg.det(A_i) / det_A
        x.append(x_i)

    return np.array(x)


def descomposicion_lu(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando descomposición LU.
    
    Parámetros:
        A (list or np.array): Matriz de coeficientes.
        b (list or np.array): Vector de términos independientes.
    
    Retorna:
        np.array: Solución del sistema.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    
    # Inicializa L y U
    L = np.eye(n)
    U = np.zeros((n, n))
    
    # Calcula L y U
    for j in range(n):  # Columna
        for i in range(j + 1):  # Fila para U
            U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
        for i in range(j + 1, n):  # Fila para L
            L[i, j] = (A[i, j] - sum(L[i, k] * U[k, j] for k in range(j))) / U[j, j]
    
    # Resuelve Ly = b (sustitución hacia adelante)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i, k] * y[k] for k in range(i))
    
    # Resuelve Ux = y (sustitución hacia atrás)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i, k] * x[k] for k in range(i + 1, n))) / U[i, i]
    
    return x


def gauss_seidel(A, b, tol=1e-6, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Gauss-Seidel.
    
    Parámetros:
        A (list or np.array): Matriz de coeficientes.
        b (list or np.array): Vector de términos independientes.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Máximo número de iteraciones.
    
    Retorna:
        np.array: Solución aproximada.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n)

    for k in range(max_iter):
        x_prev = x.copy()

        for i in range(n):
            s1 = sum(A[i, j] * x[j] for j in range(i))  # Suma de elementos actualizados
            s2 = sum(A[i, j] * x_prev[j] for j in range(i + 1, n))  # Suma de elementos anteriores
            x[i] = (b[i] - s1 - s2) / A[i, i]

        if np.linalg.norm(x - x_prev, ord=np.inf) < tol:  # Verificación de convergencia
            print(f"Convergencia alcanzada en {k + 1} iteraciones.")
            return x

    print(f"No se pudo converger en {max_iter} iteraciones.")
    return x


def jacobi(A, b, tol=1e-6, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Jacobi.
    
    Parámetros:
        A (list or np.array): Matriz de coeficientes.
        b (list or np.array): Vector de términos independientes.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Máximo número de iteraciones.
    
    Retorna:
        np.array: Solución aproximada.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n)
    x_new = np.zeros(n)

    for k in range(max_iter):
        for i in range(n):
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]

        if np.linalg.norm(x_new - x, ord=np.inf) < tol:  # Verificación de convergencia
            print(f"Convergencia alcanzada en {k + 1} iteraciones.")
            return x_new

        x = x_new.copy()

    print(f"No se pudo converger en {max_iter} iteraciones.")
    return x