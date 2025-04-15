def eliminacion_gauss(A, b):
    n = len(b)
    for i in range(n):
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        suma = sum(A[i][j] * x[j] for j in range(i+1, n))
        x[i] = (b[i] - suma) / A[i][i]
    return x

def gauss_jordan(A, b):
    n = len(b)
    for i in range(n):
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        b[i] /= factor
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
    return b

def cramer(A, b):
    from numpy.linalg import det
    import numpy as np
    D = det(A)
    if D == 0:
        raise ValueError("El sistema no tiene solución única")
    n = len(b)
    x = []
    for i in range(n):
        Ai = [row[:] for row in A]
        for j in range(n):
            Ai[j][i] = b[j]
        x.append(det(Ai)/D)
    return x

def descomposicion_lu(A, b):
    import numpy as np
    from scipy.linalg import lu
    P, L, U = lu(A)
    y = np.linalg.solve(L, b)
    x = np.linalg.solve(U, y)
    return x

def jacobi(A, b, tol=1e-10, max_iter=100):
    import numpy as np
    x = [0 for _ in b]
    n = len(A)
    for _ in range(max_iter):
        x_new = [0 for _ in x]
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]
        if np.linalg.norm(np.array(x_new) - np.array(x)) < tol:
            return x_new
        x = x_new
    return x

def gauss_seidel(A, b, tol=1e-10, max_iter=100):
    import numpy as np
    x = [0 for _ in b]
    n = len(A)
    for _ in range(max_iter):
        x_new = x[:]
        for i in range(n):
            suma = sum(A[i][j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]
        if np.linalg.norm(np.array(x_new) - np.array(x)) < tol:
            return x_new
        x = x_new
    return x
