import numpy as np

def gauss_elimination(A, b):
    """Resuelve Ax = b usando eliminación de Gauss."""
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    for i in range(n):
        max_row = i + np.argmax(np.abs(A[i:, i]))
        if i != max_row:
            A[[i, max_row]] = A[[max_row, i]]
            b[[i, max_row]] = b[[max_row, i]]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]
    x = np.zeros(n)
    for i in reversed(range(n)):
        x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i][i]
    return x

def gauss_jordan(A, b):
    """Resuelve Ax = b usando Gauss-Jordan."""
    A = A.astype(float)
    b = np.array(b, dtype=float).reshape(-1, 1)
    Ab = np.hstack([A, b])
    n = len(b)
    for i in range(n):
        Ab[i] = Ab[i] / Ab[i, i]
        for j in range(n):
            if i != j:
                Ab[j] -= Ab[j, i] * Ab[i]
    return Ab[:, -1]

def cramer(A, b):
    """Resuelve Ax = b usando la Regla de Cramer."""
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

def lu_decomposition(A, b):
    """Resuelve Ax = b usando descomposición LU."""
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    A = A.astype(float)
    b = b.astype(float)

    for i in range(n):
        for k in range(i, n):
            U[i][k] = A[i][k] - sum(L[i][j] * U[j][k] for j in range(i))
        for k in range(i, n):
            if i == k:
                L[i][i] = 1
            else:
                L[k][i] = (A[k][i] - sum(L[k][j] * U[j][i] for j in range(i))) / U[i][i]

    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    x = np.zeros(n)
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

def jacobi(A, b, tol=1e-10, max_iter=100):
    """Resuelve Ax = b usando el método de Jacobi."""
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    x = np.zeros(n)
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    return x

def gauss_seidel(A, b, tol=1e-10, max_iter=100):
    """Resuelve Ax = b usando el método de Gauss-Seidel."""
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    x = np.zeros(n)
    for _ in range(max_iter):
        x_old = np.copy(x)
        for i in range(n):
            s1 = sum(A[i][j] * x[j] for j in range(i))
            s2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            x[i] = (b[i] - s1 - s2) / A[i][i]
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            return x
    return x

def bisection(f, a, b, tol=1e-10, max_iter=100):
    """Encuentra la raíz de f(x) = 0 en [a, b] usando bisección."""
    if f(a) * f(b) > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2
