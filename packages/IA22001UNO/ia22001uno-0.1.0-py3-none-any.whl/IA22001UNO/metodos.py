"""
IA22001UNO - Librería para resolver sistemas de ecuaciones lineales y no lineales

Esta librería contiene métodos numéricos para resolver sistemas de ecuaciones:
- Eliminación de Gauss
- Gauss-Jordan
- Crammer
- Descomposición LU
- Jacobi
- Gauss-Seidel
- Bisección
"""

import numpy as np

def eliminacion_gauss(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando Eliminación Gaussiana.
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes (n)
        
    Returns:
        x: Vector solución (n)
    """
    n = len(b)
    # Matriz aumentada
    M = np.hstack([A, b.reshape(-1, 1)])
    
    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        # Eliminación
        for j in range(i+1, n):
            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:])) / M[i, i]
    
    return x

def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando Gauss-Jordan.
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes (n)
        
    Returns:
        x: Vector solución (n)
    """
    n = len(b)
    M = np.hstack([A, b.reshape(-1, 1)])
    
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        # Normalizar la fila del pivote
        M[i] = M[i] / M[i, i]
        
        # Eliminación en todas las filas excepto la actual
        for j in range(n):
            if j != i:
                factor = M[j, i]
                M[j] -= factor * M[i]
    
    return M[:, -1]

def crammer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando la Regla de Cramer.
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes (n)
        
    Returns:
        x: Vector solución (n)
    """
    det_A = np.linalg.det(A)
    n = len(b)
    x = np.zeros(n)
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    
    return x

def descomposicion_lu(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando Descomposición LU.
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes (n)
        
    Returns:
        x: Vector solución (n)
    """
    n = len(b)
    L = np.eye(n)
    U = A.copy()
    
    # Descomposición LU
    for i in range(n):
        for j in range(i+1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]
    
    # Sustitución hacia adelante (Ly = b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    
    # Sustitución hacia atrás (Ux = y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    
    return x

def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Jacobi.
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes (n)
        x0: Vector inicial (n), opcional
        tol: Tolerancia para la convergencia
        max_iter: Número máximo de iteraciones
        
    Returns:
        x: Vector solución (n)
    """
    n = len(b)
    x = x0.copy() if x0 is not None else np.zeros(n)
    x_new = np.zeros(n)
    
    for _ in range(max_iter):
        for i in range(n):
            s = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s) / A[i, i]
        
        if np.linalg.norm(x_new - x) < tol:
            break
            
        x = x_new.copy()
    
    return x

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes (n)
        x0: Vector inicial (n), opcional
        tol: Tolerancia para la convergencia
        max_iter: Número máximo de iteraciones
        
    Returns:
        x: Vector solución (n)
    """
    n = len(b)
    x = x0.copy() if x0 is not None else np.zeros(n)
    
    for _ in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            s = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
            x[i] = (b[i] - s) / A[i, i]
        
        if np.linalg.norm(x - x_old) < tol:
            break
    
    return x

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raíz de una ecuación no lineal usando el método de Bisección.
    
    Args:
        f: Función a encontrar la raíz
        a: Límite inferior del intervalo
        b: Límite superior del intervalo
        tol: Tolerancia para la convergencia
        max_iter: Número máximo de iteraciones
        
    Returns:
        c: Aproximación de la raíz
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            break
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    
    return c