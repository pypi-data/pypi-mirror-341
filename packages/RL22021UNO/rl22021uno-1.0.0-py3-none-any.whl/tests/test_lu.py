from RL22021UNO.lu import LU_solver

def test_lu():
    A = [
        [4, 2, 5],
        [2, 5, 8],
        [5, 4, 3]
    ]
    B = [60.70, 92.90, 56.30]

    X = LU_solver(A, B)

    print("\nSolución obtenida con Descomposición LU:")
    print(X)
