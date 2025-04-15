def resolver_gauss_jordan(A, b):
    n = len(b)
    # Crear una matriz aumentada
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    # Aplicar el método de Gauss-Jordan
    for i in range(n):
        # Hacer que el elemento diagonal sea 1
        pivot = M[i][i]
        if pivot == 0:
            raise ValueError("El sistema no tiene solución única o tiene infinitas soluciones.")
        for j in range(i, n + 1):
            M[i][j] /= pivot
        
        # Hacer que los elementos en la columna i sean 0
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]

    # Extraer la solución
    return [M[i][-1] for i in range(n)]