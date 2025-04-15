from RL22021UNO.gauss_jordan import gauss_jordan  

def test_gaussjordan():
    A = [
        [4, 2, 5],
        [2, 5, 8],
        [5, 4, 3]
    ]
    B = [60.70, 92.90, 56.30]

    X = gauss_jordan(A, B, vertabla=True)

    print("\nSolución obtenida:")
    print(X)
