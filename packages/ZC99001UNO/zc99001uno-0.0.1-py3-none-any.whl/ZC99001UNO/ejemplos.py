# sistema_solver/ejemplos.py

if __name__ == "__main__":
    from lineal import gauss_eliminacion, gauss_jordan
    # etc.

    # Ejemplo: Gauss
    A1 = [[2,1,-1],
          [-3,-1,2],
          [-2,1,2]]
    b1 = [8, -11, -3]
    sol_gauss = gauss_eliminacion(A1, b1)
    print("Solución Gauss:", sol_gauss)

    # Ejemplo: Bisección
    from no_lineal import biseccion

    def f(x):
        return x**2 - 2

    raiz = biseccion(f, 0, 2)
    print("Raíz aproximada usando bisección:", raiz)
