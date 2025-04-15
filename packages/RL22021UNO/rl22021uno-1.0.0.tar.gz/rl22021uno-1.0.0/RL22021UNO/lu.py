import numpy as np

def LU_descomposicion(A):

    A = np.array(A, dtype=float)
    n = A.shape[0]
    
    L = np.zeros_like(A)
    U = np.copy(A)
    
    for i in range(n):
        
        L[i, i] = 1.0
        
        
        for j in range(i+1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]
    
    return L, U

def LU_solver(A, B):
   
    L, U = LU_descomposicion(A)
    
    
    Y = np.linalg.solve(L, B)
    
    
    X = np.linalg.solve(U, Y)
    
    return X
