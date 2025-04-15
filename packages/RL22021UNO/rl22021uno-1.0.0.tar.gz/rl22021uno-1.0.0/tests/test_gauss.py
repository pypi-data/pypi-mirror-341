from RL22021UNO.gauss import pivoteo_parcial, eliminacion_gaussiana, sustitucion_hacia_atras

def test_gauss():
    A = [[4,2,5],
         [2,5,8],
         [5,4,3]]
    B = [60.70, 92.90, 56.30]

    AB = pivoteo_parcial(A, B, vertabla=True)
    AB = eliminacion_gaussiana(AB, vertabla=True)
    X = sustitucion_hacia_atras(AB, vertabla=True)

    print('Solución X:')
    print(X)
