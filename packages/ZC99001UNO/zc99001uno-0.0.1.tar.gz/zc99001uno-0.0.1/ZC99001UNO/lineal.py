# sistema_solver/lineal.py

import copy

def gauss_eliminacion(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b
    usando el método de Eliminación de Gauss.

    Parámetros:
    -----------
    A : list of list of float
        Matriz de coeficientes (n x n).
    b : list of float
        Vector de términos independientes (n).

    Retorna:
    --------
    x : list of float
        Solución aproximada del sistema.

    Ejemplo:
    --------
    >>> A = [[2,1,-1],
              [-3,-1,2],
              [-2,1,2]]
    >>> b = [8, -11, -3]
    >>> gauss_eliminacion(A, b)
    [2.0, 3.0, -1.0]
    """
    # Copiamos matrices para no modificar las originales
    A = copy.deepcopy(A)
    b = copy.deepcopy(b)

    n = len(A)

    # Fase de eliminación
    for k in range(n - 1):
        for i in range(k + 1, n):
            if A[k][k] == 0:
                raise ValueError("El elemento pivote es cero, no se puede continuar.")
            factor = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
            b[i] -= factor * b[k]

    # Fase de sustitución hacia atrás
    x = [0] * n
    x[n - 1] = b[n - 1] / A[n - 1][n - 1]
    for i in range(n - 2, -1, -1):
        sum_ax = 0
        for j in range(i + 1, n):
            sum_ax += A[i][j] * x[j]
        x[i] = (b[i] - sum_ax) / A[i][i]

    return x


def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b
    usando el método de Gauss-Jordan.

    Parámetros:
    -----------
    A : list of list of float
        Matriz de coeficientes.
    b : list of float
        Vector de términos independientes.

    Retorna:
    --------
    x : list of float
        Solución del sistema.

    Ejemplo:
    --------
    >>> A = [[1,1,1],
             [0,2,5],
             [2,5,-1]]
    >>> b = [6, -4, 27]
    >>> gauss_jordan(A, b)
    [5.0, 3.0, -2.0]
    """
    A = copy.deepcopy(A)
    b = copy.deepcopy(b)
    n = len(A)

    # Gauss-Jordan
    for i in range(n):
        # Pivote
        pivote = A[i][i]
        if pivote == 0:
            raise ValueError("Pivote cero encontrado, no se puede continuar.")

        # Normalizar fila
        for j in range(i, n):
            A[i][j] /= pivote
        b[i] /= pivote

        # Eliminar en las demás filas
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]

    return b


def cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b
    usando la Regla de Cramer.

    Parámetros:
    -----------
    A : list of list of float
        Matriz de coeficientes (n x n).
    b : list of float
        Vector de términos independientes (n).

    Retorna:
    --------
    x : list of float
        Solución del sistema.

    Ejemplo:
    --------
    >>> A = [[2, -1],
             [1,  3]]
    >>> b = [0, 7]
    >>> cramer(A, b)
    [1.0, 2.0]
    """
    import numpy as np

    det_A = np.linalg.det(A)
    if abs(det_A) < 1e-14:
        raise ValueError("La matriz A es singular, no se puede aplicar Cramer.")

    n = len(A)
    x = []

    for i in range(n):
        # Reemplazar la columna i con b
        A_mod = copy.deepcopy(A)
        for row in range(n):
            A_mod[row][i] = b[row]
        det_mod = np.linalg.det(A_mod)
        xi = det_mod / det_A
        x.append(xi)

    return x


def descomposicion_lu(A, b):
    """
    Resuelve el sistema Ax = b utilizando Descomposición LU.

    Parámetros:
    -----------
    A : list of list of float
        Matriz de coeficientes (n x n).
    b : list of float
        Vector de términos independientes (n).

    Retorna:
    --------
    x : list of float
        Solución del sistema.

    Ejemplo:
    --------
    >>> A = [[4, 3],
             [6, 3]]
    >>> b = [10, 12]
    >>> descomposicion_lu(A, b)
    [1.5, 2.0]
    """
    import numpy as np
    import scipy.linalg as la

    # Convertir a arreglos de numpy
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)

    # Descomposición LU con scipy
    lu, piv = la.lu_factor(A_np)
    x_np = la.lu_solve((lu, piv), b_np)

    return x_np.tolist()


def jacobi(A, b, tol=1e-9, max_iter=100):
    """
    Resuelve el sistema Ax = b usando el método iterativo de Jacobi.

    Parámetros:
    -----------
    A : list of list of float
        Matriz de coeficientes (n x n).
    b : list of float
        Vector de términos independientes (n).
    tol : float
        Tolerancia de convergencia.
    max_iter : int
        Número máximo de iteraciones.

    Retorna:
    --------
    x : list of float
        Solución aproximada luego de la convergencia o del número máximo de iteraciones.

    Ejemplo:
    --------
    >>> A = [[10, -1, 2, 0],
             [-1, 11, -1, 3],
             [2, -1, 10, -1],
             [0, 3, -1, 8]]
    >>> b = [6, 25, -11, 15]
    >>> jacobi(A, b)
    [1.0, 2.0, -1.0, 1.0]  # ejemplo hipotético
    """
    import numpy as np

    n = len(A)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    x = np.zeros_like(b)
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        # Verificar convergencia
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new.tolist()
        x = x_new
    return x.tolist()


def gauss_seidel(A, b, tol=1e-9, max_iter=100):
    """
    Resuelve el sistema Ax = b usando el método iterativo de Gauss-Seidel.

    Parámetros:
    -----------
    A : list of list of float
        Matriz de coeficientes (n x n).
    b : list of float
        Vector de términos independientes (n).
    tol : float
        Tolerancia de convergencia.
    max_iter : int
        Número máximo de iteraciones.

    Retorna:
    --------
    x : list of float
        Solución aproximada luego de la convergencia o del número máximo de iteraciones.

    Ejemplo:
    --------
    >>> A = [[4,1],
             [2,3]]
    >>> b = [1, 2]
    >>> gauss_seidel(A, b)
    [0.090909..., 0.6363636...]  # ejemplo hipotético
    """
    import numpy as np

    n = len(A)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    x = np.zeros_like(b)
    for _ in range(max_iter):
        x_old = np.copy(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - s) / A[i][i]
        # Verificar convergencia
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            return x.tolist()
    return x.tolist()
