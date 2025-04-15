import numpy as np
from scipy.linalg import lu

# 1. Eliminación de Gauss
def gauss_elimination(A, b):
    n = len(b)
    A = A.astype(float)
    b = b.astype(float)
    
    for i in range(n):
        # Pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j] = A[j] - factor * A[i]
            b[j] = b[j] - factor * b[i]
    return b

# 2. Gauss-Jordan
def gauss_jordan(A, b):
    n = len(b)
    A = A.astype(float)
    b = b.astype(float)

    for i in range(n):
        # Hacemos el pivote 1
        factor = A[i][i]
        A[i] = A[i] / factor
        b[i] = b[i] / factor
        # Hacemos ceros en otras filas
        for j in range(n):
            if i != j:
                factor = A[j][i]
                A[j] = A[j] - factor * A[i]
                b[j] = b[j] - factor * b[i]
    return b

# 3. Regla de Cramer
def cramer(A, b):
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única")

    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        Ai = np.copy(A)
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    return x

# 4. Descomposición LU
def lu_decomposition(A, b):
    P, L, U = lu(A)
    # Ly = Pb
    y = np.linalg.solve(L, np.dot(P, b))
    # Ux = y
    x = np.linalg.solve(U, y)
    return x

# 5. Método de Jacobi
def jacobi(A, b, x0=None, tol=1e-10, max_iter=1000):
    n = len(A)
    x = np.zeros_like(b) if x0 is None else x0.copy()
    for _ in range(max_iter):
        x_new = np.zeros_like(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    return x

# 6. Método de Gauss-Seidel
def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=1000):
    n = len(A)
    x = np.zeros_like(b) if x0 is None else x0.copy()
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    return x

#Prueba:
if __name__ == "__main__":
    A = np.array([[2, 1], [5, 7]])
    b = np.array([11, 13])
    print("Solución usando Gauss-Jordan:")
    print(gauss_jordan(A, b))