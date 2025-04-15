import numpy as np

def eliminacion_gauss(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando eliminación de Gauss.
    
    Parámetros:
        A (list or np.array): Matriz de coeficientes.
        b (list or np.array): Vector de términos independientes.
    
    Retorna:
        np.array: Solución del sistema.
    
    Ejemplo:
        >>> A = [[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]
        >>> b = [1, -2, 0]
        >>> eliminacion_gauss(A, b)
        array([ 1., -2., -2.])
    """
    n = len(b)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
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
    
    Parámetros:
        A (list or np.array): Matriz de coeficientes.
        b (list or np.array): Vector de términos independientes.
    
    Retorna:
        np.array: Solución del sistema.
    
    Ejemplo:
        >>> A = [[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]
        >>> b = [1, -2, 0]
        >>> gauss_jordan(A, b)
        array([ 1., -2., -2.])
    """
    n = len(b)
    augmented_matrix = np.hstack([A, b.reshape(n, 1)])
    
    for i in range(n):
        pivot = augmented_matrix[i, i]
        augmented_matrix[i, :] /= pivot
        
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j, i]
                augmented_matrix[j, :] -= factor * augmented_matrix[i, :]
    
    solution = augmented_matrix[:, -1]
    return solution


def cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando la regla de Cramer.
    
    Parámetros:
        A (list or np.array): Matriz de coeficientes.
        b (list or np.array): Vector de términos independientes.
    
    Retorna:
        np.array: Solución del sistema.
    
    Ejemplo:
        >>> A = [[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]
        >>> b = [1, -2, 0]
        >>> cramer(A, b)
        array([ 1., -2., -2.])
    """
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
    
    Ejemplo:
        >>> A = [[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]
        >>> b = [1, -2, 0]
        >>> descomposicion_lu(A, b)
        array([ 1., -2., -2.])
    """
    L, U = np.linalg.lu_factor(A)
    return np.linalg.lu_solve((L, U), b)


def jacobi(A, b, tol=1e-6, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Jacobi.
    
    Parámetros:
        A (list or np.array): Matriz de coeficientes.
        b (list or np.array): Vector de términos independientes.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Máximo número de iteraciones.
    
    Retorna:
        np.array: Solución aproximada del sistema.
    
    Ejemplo:
        >>> A = [[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]
        >>> b = [1, -2, 0]
        >>> jacobi(A, b)
        array([ 1., -2., -2.])
    """
    n = len(b)
    x = np.zeros(n)
    
    for _ in range(max_iter):
        x_new = np.zeros(n)
        for i in range(n):
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    
    raise ValueError("El método no convergió después de {} iteraciones.".format(max_iter))


def gauss_seidel(A, b, tol=1e-6, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Gauss-Seidel.
    
    Parámetros:
        A (list or np.array): Matriz de coeficientes.
        b (list or np.array): Vector de términos independientes.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Máximo número de iteraciones.
    
    Retorna:
        np.array: Solución aproximada del sistema.
    
    Ejemplo:
        >>> A = [[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]
        >>> b = [1, -2, 0]
        >>> gauss_seidel(A, b)
        array([ 1., -2., -2.])
    """
    n = len(b)
    x = np.zeros(n)
    
    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            s = sum(A[i, j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    
    raise ValueError("El método no convergió después de {} iteraciones.".format(max_iter))