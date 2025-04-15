import numpy as np


def pivoteo_parcial(A, B, vertabla=False):
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)
    if B.ndim == 1:
        B = B.reshape(-1, 1)
    AB = np.hstack((A, B))

    if vertabla:
        print('Matriz aumentada:')
        print(AB)
        print('Pivoteo parcial:')

    n = AB.shape[0]
    for i in range(n - 1):
        max_row = np.argmax(np.abs(AB[i:, i])) + i
        if max_row != i:
            AB[[i, max_row]] = AB[[max_row, i]]
            if vertabla:
                print(f'  Intercambiar filas: {i} y {max_row}')
                print(AB)

    return AB

def eliminacion_gaussiana(AB, vertabla=False, casicero=1e-15):
    n = AB.shape[0]
    for i in range(n - 1):
        pivote = AB[i, i]
        if abs(pivote) < casicero:
            raise ValueError(f"Pivote casi cero en fila {i}.")
        for j in range(i + 1, n):
            factor = AB[j, i] / pivote
            AB[j, :] -= factor * AB[i, :]
            if vertabla:
                print(f'  Eliminando fila {j} con factor {factor}')
    return AB

def sustitucion_hacia_atras(AB, vertabla=False):
    n = AB.shape[0]
    X = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = np.dot(AB[i, i+1:n], X[i+1:n])
        X[i] = (AB[i, -1] - suma) / AB[i, i]
        if vertabla:
            print(f'  x[{i}] = {X[i]}')
    return X



