def resolver_lu(A, b):
    import numpy as np

    if np.linalg.det(A) == 0:
        raise ValueError("La matriz es singular y no se puede descomponer.")

    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        L[i][i] = 1

    for j in range(n):
        for i in range(j + 1):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))

        for i in range(j, n):
            L[i][j] = (A[i][j] - sum(L[i][k] * U[k][j] for k in range(j))) / U[j][j]

    # Forward substitution to solve Ly = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    # Backward substitution to solve Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x