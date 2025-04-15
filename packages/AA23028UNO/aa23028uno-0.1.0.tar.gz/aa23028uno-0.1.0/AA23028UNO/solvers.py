"""
Modulo de metodos numericos para resolver sistemas de ecuaciones lineales y no lineales.
Incluye: Eliminacion de Gauss, Gauss-Jordan, Cramer, Descomposicion LU, Jacobi, Gauss-Seidel, Biseccion.

Cada funcion incluye un ejemplo de uso en el docstring.
"""

import numpy as np

def gauss_elimination(A, b):
    """
    Resuelve Ax = b usando eliminacion de Gauss.
    
    Ejemplo:
        >>> import numpy as np
        >>> A = np.array([[2,1,-1],[-3,-1,2],[-2,1,2]], dtype=float)
        >>> b = np.array([8, -11, -3], dtype=float)
        >>> gauss_elimination(A, b)
        array([ 2.,  3., -1.])
    """
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    for i in range(n):
        max_row = np.argmax(abs(A[i:, i])) + i
        if i != max_row:
            A[[i, max_row]] = A[[max_row, i]]
            b[[i, max_row]] = b[[max_row, i]]
        for j in range(i+1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
    return x

def gauss_jordan(A, b):
    """
    Resuelve Ax = b usando Gauss-Jordan.
    
    Ejemplo:
        >>> import numpy as np
        >>> A = np.array([[2,1,-1],[-3,-1,2],[-2,1,2]], dtype=float)
        >>> b = np.array([8, -11, -3], dtype=float)
        >>> gauss_jordan(A, b)
        array([ 2.,  3., -1.])
    """
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    M = np.hstack([A, b.reshape(-1,1)])
    for i in range(n):
        M[i] = M[i] / M[i, i]
        for j in range(n):
            if i != j:
                M[j] = M[j] - M[j, i] * M[i]
    return M[:, -1]

def cramer(A, b):
    """
    Resuelve Ax = b usando la regla de Cramer.
    
    Ejemplo:
        >>> import numpy as np
        >>> A = np.array([[2,1,-1],[-3,-1,2],[-2,1,2]], dtype=float)
        >>> b = np.array([8, -11, -3], dtype=float)
        >>> cramer(A, b)
        array([ 2.,  3., -1.])
    """
    detA = np.linalg.det(A)
    if detA == 0:
        raise ValueError("El sistema no tiene solución única.")
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        Ai = np.copy(A)
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / detA
    return x

def lu_decomposition(A, b):
    """
    Resuelve Ax = b usando descomposición LU.
    
    Ejemplo:
        >>> import numpy as np
        >>> A = np.array([[2,1,-1],[-3,-1,2],[-2,1,2]], dtype=float)
        >>> b = np.array([8, -11, -3], dtype=float)
        >>> lu_decomposition(A, b)
        array([ 2.,  3., -1.])
    """
    from scipy.linalg import lu_factor, lu_solve
    lu, piv = lu_factor(A)
    x = lu_solve((lu, piv), b)
    return x

def jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    """
    Resuelve Ax = b usando el método de Jacobi.
    
    Ejemplo:
        >>> import numpy as np
        >>> A = np.array([[10,2,1],[1,5,1],[2,3,10]], dtype=float)
        >>> b = np.array([7, -8, 6], dtype=float)
        >>> jacobi(A, b)
        array([...])
    """
    n = len(b)
    x = np.zeros_like(b) if x0 is None else x0.copy()
    for _ in range(max_iter):
        x_new = np.zeros_like(x)
        for i in range(n):
            s = np.dot(A[i, :], x) - A[i, i]*x[i]
            x_new[i] = (b[i] - s) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    return x

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100):
    """
    Resuelve Ax = b usando el método de Gauss-Seidel.
    
    Ejemplo:
        >>> import numpy as np
        >>> A = np.array([[10,2,1],[1,5,1],[2,3,10]], dtype=float)
        >>> b = np.array([7, -8, 6], dtype=float)
        >>> gauss_seidel(A, b)
        array([...])
    """
    n = len(b)
    x = np.zeros_like(b) if x0 is None else x0.copy()
    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    return x

def bisection(f, a, b, tol=1e-10, max_iter=100):
    """
    Encuentra una raíz de f(x)=0 en [a, b] usando bisección.
    
    Ejemplo:
        >>> def f(x): return x**3 - x - 2
        >>> bisection(f, 1, 2)
        1.521...
    """
    if f(a)*f(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a)/2 < tol:
            return c
        if f(a)*f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2
