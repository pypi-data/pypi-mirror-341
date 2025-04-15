# zc99001uno/no_lineal.py

def biseccion(f, a, b, tol=1e-9, max_iter=100):
    """
    Encuentra una raíz de la ecuación f(x) = 0 en el intervalo [a, b]
    usando el método de bisección.

    Parámetros:
    -----------
    f : function
        Función univariada de la forma f(x).
    a, b : float
        Intervalo en el que se busca la raíz (f(a) y f(b) deben tener signos opuestos).
    tol : float
        Tolerancia de convergencia.
    max_iter : int
        Número máximo de iteraciones.

    Retorna:
    --------
    float
        Aproximación de la raíz.

    Ejemplo:
    --------
    >>> def f(x):
    ...     return x**2 - 2
    >>> raiz = biseccion(f, 0, 2)
    >>> raiz
    1.4142135623...
    """
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")

    for _ in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        if abs(fc) < tol:
            return c

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return (a + b) / 2
