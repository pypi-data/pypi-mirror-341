import numpy as np

def biseccion(f, a, b, tol=1e-10, max_iter=1000):
 
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
    
    for iter in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            print(f"Convergió después de {iter+1} iteraciones")
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    raise ValueError(f"El método de Bisección no convergió después de {max_iter} iteraciones")
