import numpy as np 

def gauss_elimination(A, b):
    """
    Resuelve el sistema Ax = b usando eliminacion gaussiana
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de terminos independientes (n)
    
    Returns:
        x: Vector solucion
    """
    n = len(b)
    # Matriz aumentada
    Ab = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    # Eliminacion hacia adelante
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(Ab[i:, i])) + i
        Ab[[i, max_row]] = Ab[[max_row, i]]
        
        # Eliminacion
        for j in range(i + 1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:] -= factor * Ab[i, i:]
    
    # Sustitucion hacia atras
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
    
    return x

def gauss_jordan(A, b):
    """
    Resuelve el sistema Ax = b usando Gauss-Jordan
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de terminos independientes (n)
    
    Returns:
        x: Vector solucion
    """
    n = len(b)
    Ab = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(Ab[i:, i])) + i
        Ab[[i, max_row]] = Ab[[max_row, i]]
        
        # Normalizar la fila del pivote
        Ab[i] = Ab[i] / Ab[i, i]
        
        # Eliminar en todas las filas
        for j in range(n):
            if j != i:
                Ab[j] -= Ab[j, i] * Ab[i]
    
    return Ab[:, -1]

def cramer(A, b):
    """
    Resuelve el sistema Ax = b usando la regla de Cramer
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de terminos independientes (n)
    
    Returns:
        x: Vector solución
    """
    det_A = np.linalg.det(A)
    n = len(b)
    x = np.zeros(n)
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    
    return x

def lu_decomposition(A, b):
    """
    Resuelve el sistema Ax = b usando descomposicion LU
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de terminos independientes (n)
    
    Returns:
        x: Vector solución
    """
    n = len(b)
    L = np.eye(n)
    U = A.astype(float)
    
    # Descomposición LU
    for i in range(n):
        for j in range(i+1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]
    
    # Sustitucion hacia adelante (Ly = b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    
    # Sustitucion hacia atras (Ux = y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    
    return x

def jacobi(A, b, tol=1e-6, max_iter=1000):
    """
    Resuelve el sistema Ax = b usando el metodo de Jacobi
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de terminos independientes (n)
        tol: Tolerancia para la convergencia
        max_iter: Numero maximo de iteraciones
    
    Returns:
        x: Vector solucion
    """
    n = len(b)
    x = np.zeros(n)
    x_new = np.zeros(n)
    
    for _ in range(max_iter):
        for i in range(n):
            s = np.dot(A[i, :], x) - A[i, i] * x[i]
            x_new[i] = (b[i] - s) / A[i, i]
        
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        
        x = x_new.copy()
    
    return x

def gauss_seidel(A, b, tol=1e-6, max_iter=1000):
    """
    Resuelve el sistema Ax = b usando el metodo de Gauss-Seidel
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de terminos independientes (n)
        tol: Tolerancia para la convergencia
        max_iter: Número máximo de iteraciones
    
    Returns:
        x: Vector solucion
    """
    n = len(b)
    x = np.zeros(n)
    
    for _ in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i+1:], x_old[i+1:])
            x[i] = (b[i] - s1 - s2) / A[i, i]
        
        if np.linalg.norm(x - x_old) < tol:
            return x
    
    return x