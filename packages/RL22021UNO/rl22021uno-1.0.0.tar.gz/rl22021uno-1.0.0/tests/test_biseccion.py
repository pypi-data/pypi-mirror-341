from RL22021UNO.biseccion import biseccion

def test_biseccion():
    # Función de prueba: f(x) = x^2 - 4
    def f(x):
        return x**2 - 4

    a = 0
    b = 3
    raiz = biseccion(f, a, b, tol=1e-10, max_iter=100)

    print("\nRaíz obtenida con el método de Bisección:")
    print(raiz)
