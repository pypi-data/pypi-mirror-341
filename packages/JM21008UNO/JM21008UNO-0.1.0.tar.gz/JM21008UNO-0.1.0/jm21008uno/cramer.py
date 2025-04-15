import numpy as np

def resolver_cramer(matriz_coeficientes, vector_terminos):
    """
    Resuelve un sistema de ecuaciones lineales Ax = B usando el método de Cramer.
    """
    # Convertir las matrices a tipo float para evitar problemas de precisión
    matriz_coeficientes = np.array(matriz_coeficientes, dtype=float)
    vector_terminos = np.array(vector_terminos, dtype=float)

    # Determinante de la matriz de coeficientes
    determinante = np.linalg.det(matriz_coeficientes)
    if np.isclose(determinante, 0):
        raise ValueError("El sistema no tiene solución única.")

    # Número de incógnitas
    n = len(vector_terminos)
    soluciones = np.zeros(n)

    # Calcular cada incógnita usando el método de Cramer
    for i in range(n):
        matriz_temp = matriz_coeficientes.copy()
        matriz_temp[:, i] = vector_terminos  # Reemplazar la columna i por el vector de términos independientes
        determinante_temp = np.linalg.det(matriz_temp)
        print(f"Determinante temporal para columna {i}: {determinante_temp}")
        soluciones[i] = determinante_temp / determinante

    return soluciones