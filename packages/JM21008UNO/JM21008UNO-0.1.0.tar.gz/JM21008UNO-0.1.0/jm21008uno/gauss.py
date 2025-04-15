import numpy as np

def resolver_gauss(A, B):
    """Resuelve un sistema de ecuaciones lineales Ax = B usando el método de Gauss."""
    casicero = 1e-15  # Considerar como 0

    # Convertir las matrices a tipo float para evitar truncamiento
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    # Matriz aumentada
    AB = np.concatenate((A, B.reshape(-1, 1)), axis=1)

    # Dimensiones de la matriz aumentada
    tamano = np.shape(AB)
    n = tamano[0]

    # Pivoteo parcial por filas
    for i in range(0, n - 1):
        columna = abs(AB[i:, i])
        dondemax = np.argmax(columna)
        if dondemax != 0:
            # Intercambiar filas
            temporal = np.copy(AB[i, :])
            AB[i, :] = AB[dondemax + i, :]
            AB[dondemax + i, :] = temporal

    # Eliminación hacia adelante
    for i in range(0, n - 1):
        pivote = AB[i, i]
        if abs(pivote) < casicero:
            raise ValueError("El sistema no tiene solución única.")
        for k in range(i + 1, n):
            factor = AB[k, i] / pivote
            AB[k, :] = AB[k, :] - AB[i, :] * factor

    # Sustitución hacia atrás
    X = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += AB[i, j] * X[j]
        if abs(AB[i, i]) < casicero:
            raise ValueError("El sistema no tiene solución única.")
        X[i] = (AB[i, -1] - suma) / AB[i, i]

    return X