def biseccion(f, a, b, tol=1e-6, max_iter=1000):
    """
    Encuentra la raíz de una función f en el intervalo [a, b] usando el método de bisección.
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función no cambia de signo en el rango proporcionado.")

    iteraciones = 0
    while (b - a) / 2 > tol and iteraciones < max_iter:
        xr = (a + b) / 2
        if f(xr) == 0:
            return xr, iteraciones
        elif f(a) * f(xr) < 0:
            b = xr
        else:
            a = xr
        iteraciones += 1

    return (a + b) / 2, iteraciones