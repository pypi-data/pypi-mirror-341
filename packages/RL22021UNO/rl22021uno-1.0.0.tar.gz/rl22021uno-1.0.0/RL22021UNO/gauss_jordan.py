import numpy as np

def gauss_jordan(A, B, vertabla=False, casicero=1e-15):
   
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    if B.ndim == 1:
        B = B.reshape(-1, 1)

    AB = np.concatenate((A, B), axis=1)
    n = len(AB)

    if vertabla:
        print("Matriz aumentada inicial:")
        print(AB)

    for i in range(n):
        # Pivoteo parcial
        max_fila = np.argmax(np.abs(AB[i:, i])) + i
        if np.abs(AB[max_fila, i]) < casicero:
            raise ValueError("La matriz es singular o tiene solución no única.")

        if max_fila != i:
            AB[[i, max_fila]] = AB[[max_fila, i]]
            if vertabla:
                print(f"Intercambio de filas {i} y {max_fila}:")
                print(AB)

        # Normaliza fila 
        AB[i] = AB[i] / AB[i, i]
        if vertabla:
            print(f"Fila {i} normalizada:")
            print(AB)


        for j in range(n):
            if i != j:
                factor = AB[j, i]
                AB[j] = AB[j] - factor * AB[i]
                if vertabla:
                    print(f"Eliminación en fila {j} usando fila {i}:")
                    print(AB)

    X = AB[:, -1]
    if vertabla:
        print("Matriz final (identidad | solución):")
        print(AB)
        print("Solución X:")
        print(X)

    return X
