from RL22021UNO.jacobi import jacobi

def test_jacobi():
    A = [
        [4, -1, 0, 0],
        [-1, 4, -1, 0],
        [0, -1, 4, -1],
        [0, 0, -1, 3]
    ]
    B = [15, 10, 10, 10]

    X = jacobi(A, B, tol=1e-10, max_iter=100)

    print("\nSolución obtenida con el método de Jacobi:")
    print(X)
