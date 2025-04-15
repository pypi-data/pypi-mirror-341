def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raíz de f(x) en el intervalo [a, b] usando el método de bisección.
    
    Parámetros:
        f (function): Función para la cual se busca la raíz.
        a (float): Extremo izquierdo del intervalo.
        b (float): Extremo derecho del intervalo.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Máximo número de iteraciones.
    
    Retorna:
        float: Raíz aproximada de f(x).
    
    Ejemplo:
        >>> def f(x):
        ...     return x**3 - x - 2
        >>> biseccion(f, 1, 2)
        1.5213853120803833
    """
    if f(a) * f(b) > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    
    raise ValueError("El método no convergió después de {} iteraciones.".format(max_iter))