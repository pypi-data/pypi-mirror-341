import numpy as np

def gauss_seidel(A, B, tol=1e-10, max_iter=1000):

    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)
    n = A.shape[0]
    
    X = np.zeros(n)  

    for iter in range(max_iter):
        X_new = np.copy(X)  
        for i in range(n):
            sum_ = 0
            for j in range(n):
                if i != j:
                    sum_ += A[i, j] * X_new[j]  
            X_new[i] = (B[i] - sum_) / A[i, i]
        
     
        if np.linalg.norm(X_new - X, ord=np.inf) < tol:
            print(f"Convergió después de {iter+1} iteraciones")
            return X_new
        
        X[:] = X_new  
    
    raise ValueError(f"El método de Gauss-Seidel no convergió después de {max_iter} iteraciones")
