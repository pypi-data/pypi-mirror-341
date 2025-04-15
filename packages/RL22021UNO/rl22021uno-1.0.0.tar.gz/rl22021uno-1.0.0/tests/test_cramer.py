from RL22021UNO.cramer import cramer

def test_cramer():
    A = [
        [4, 2, 5],
        [2, 5, 8],
        [5, 4, 3]
    ]
    B = [60.70, 92.90, 56.30]

    X = cramer(A, B, vertabla=True)

    print("\nSolución obtenida con Cramer:")
    print(X)
