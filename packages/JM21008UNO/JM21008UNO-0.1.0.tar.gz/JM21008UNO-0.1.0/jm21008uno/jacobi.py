import numpy as np

def resolver_jacobi(A, b, x0=None, tol=1e-10, max_iterations=100):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método de Jacobi.
    """
    def es_diagonal_dominante(A):
        for i in range(len(A)):
            suma_fila = sum(abs(A[i, j]) for j in range(len(A)) if i != j)
            if abs(A[i, i]) <= suma_fila:
                return False
        return True

    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    if not es_diagonal_dominante(A):
        raise ValueError("La matriz no es diagonal dominante. El método de Jacobi puede no converger.")
    
    n = len(b)
    x = np.zeros_like(b) if x0 is None else np.array(x0, dtype=float)
    
    for it_count in range(max_iterations):
        x_new = np.copy(x)
        for i in range(n):
            sum_ax = np.dot(A[i, :], x) - A[i, i] * x[i]
            x_new[i] = (b[i] - sum_ax) / A[i, i]
        
        # Check for convergence
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        
        x = x_new
    
    raise ValueError("El método de Jacobi no convergió dentro del número máximo de iteraciones")