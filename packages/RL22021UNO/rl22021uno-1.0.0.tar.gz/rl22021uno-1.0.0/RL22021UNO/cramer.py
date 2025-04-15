import numpy as np

def cramer(A, B, vertabla=False):
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    n = A.shape[0]
    det_A = np.linalg.det(A)

    if np.isclose(det_A, 0):
        raise ValueError("El sistema no tiene solución única (determinante = 0)")

    X = np.zeros(n)

    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = B
        det_Ai = np.linalg.det(Ai)
        X[i] = det_Ai / det_A

        if vertabla:
            print(f"Determinante A_{i}: {det_Ai:.5f}")
            print(f"x_{i} = {X[i]:.5f}")

    return X
