import numpy as np
from typing import List, Tuple, Union, Optional

def gauss_elimination(A: np.ndarray, b: np.ndarray) -> np.ndarray:

    A = A.astype(float).copy()
    b = b.astype(float).copy()
    n = len(b)
    
    for i in range(n):

        max_row = i + np.argmax(abs(A[i:, i]))
        if max_row != i:
            A[[i, max_row]] = A[[max_row, i]]
            b[[i, max_row]] = b[[max_row, i]]
            
        pivot = A[i, i]
        if abs(pivot) < 1e-10:
            raise ValueError("La matriz es singular o casi singular")
            
        # Eliminación
        for j in range(i+1, n):
            factor = A[j, i] / pivot
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]
    

    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
        
    return x

def gauss_jordan(A: np.ndarray, b: np.ndarray) -> np.ndarray:

    
    A = A.astype(float).copy()
    b = b.astype(float).copy().reshape(-1, 1)
    augmented = np.hstack((A, b))
    n, m = A.shape
    
   
    for i in range(n):
        # Pivoteo parcial
        max_row = i + np.argmax(abs(augmented[i:, i]))
        if max_row != i:
            augmented[[i, max_row]] = augmented[[max_row, i]]
            
        pivot = augmented[i, i]
        if abs(pivot) < 1e-10:
            raise ValueError("La matriz es singular o casi singular")
            
        
        augmented[i] = augmented[i] / pivot
        
        
        for j in range(n):
            if j != i:
                factor = augmented[j, i]
                augmented[j] = augmented[j] - factor * augmented[i]
                
    # Extraer solución
    x = augmented[:, -1]
    return x

def cramer(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    n = len(b)
    
    # Calcular determinante de A
    det_A = np.linalg.det(A)
    if abs(det_A) < 1e-10:
        raise ValueError("La matriz es singular (determinante = 0)")
    
    # Calcular la solución
    x = np.zeros(n)
    for i in range(n):
        # Crear una copia de A
        A_i = A.copy()
        # Reemplazar la columna i con el vector b
        A_i[:, i] = b
        # Calcular determinante
        det_A_i = np.linalg.det(A_i)
        # Aplicar regla de Cramer
        x[i] = det_A_i / det_A
        
    return x

def lu_decomposition(A: np.ndarray, b: np.ndarray) -> np.ndarray:

    A = A.astype(float).copy()
    b = b.astype(float).copy()
    n = len(b)
    
    # Descomposición LU
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    
    for i in range(n):
        # Elementos de U (filas)
        for j in range(i, n):
            U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
        
        # Elementos de L (columnas)
        L[i, i] = 1.0  # Diagonal de L son 1s
        for j in range(i+1, n):
            if abs(U[i, i]) < 1e-10:
                raise ValueError("La matriz no permite descomposición LU sin pivoteo")
            L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]
    
    # Resolver Ly = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i, j] * y[j] for j in range(i))
    
    # Resolver Ux = y
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        if abs(U[i, i]) < 1e-10:
            raise ValueError("La matriz es singular o casi singular")
        x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i+1, n))) / U[i, i]
    
    return x

def jacobi(A: np.ndarray, b: np.ndarray, tol: float = 1e-10, max_iter: int = 100) -> np.ndarray:
    """
    Resuelve un sistema de ecuaciones lineales utilizando el método iterativo de Jacobi.
    
    Args:
        A: Matriz de coeficientes
        b: Vector de términos independientes
        tol: Tolerancia para convergencia
        max_iter: Número máximo de iteraciones
        
    Returns:
        Vector solución
    """
    A = A.astype(float).copy()
    b = b.astype(float).copy()
    n = len(b)
    
    # Comprobar diagonal dominante
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            print("Advertencia: La matriz no es diagonal dominante, puede no converger")
            break
    
    # Inicializar solución
    x = np.zeros(n)
    x_new = np.zeros(n)
    
    # Iteraciones
    for iter_count in range(max_iter):
        for i in range(n):
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        
        # Verificar convergencia
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        
        # Actualizar x para la siguiente iteración
        x = x_new.copy()
    
    print(f"Advertencia: El método de Jacobi no convergió después de {max_iter} iteraciones")
    return x

def gauss_seidel(A: np.ndarray, b: np.ndarray, tol: float = 1e-10, max_iter: int = 100) -> np.ndarray:

    A = A.astype(float).copy()
    b = b.astype(float).copy()
    n = len(b)
    
    
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            print("Advertencia: La matriz no es diagonal dominante, puede no converger")
            break
    
    #solucion
    x = np.zeros(n)
    
    # Iteraciones
    for iter_count in range(max_iter):
        x_old = x.copy()
        
        for i in range(n):
            # Sumar términos con x_k+1 (valores ya calculados)
            s1 = sum(A[i, j] * x[j] for j in range(i))
            # Sumar términos con x_k (valores anteriores)
            s2 = sum(A[i, j] * x_old[j] for j in range(i+1, n))
            
            x[i] = (b[i] - s1 - s2) / A[i, i]
        
        # Verificar convergencia
        if np.linalg.norm(x - x_old) < tol:
            return x
    
    print(f"Advertencia: El método no convergió después de {max_iter} iteraciones")
    return x

def bisection(f: Callable[[float], float], a: float, b: float, tol: float = 1e-10, max_iter: int = 100) -> float:

    if f(a) * f(b) >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        
        if abs(fc) < tol:
            return c
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
        
        # También podemos verificar si el intervalo es suficientemente pequeño
        if abs(b - a) < tol:
            return c
    
    print(f"Advertencia: El método de bisección no convergió después de {max_iter} iteraciones")
    return (a + b) / 2

def solve_nonlinear_system_bisection(funcs: List[Callable], bounds: List[Tuple[float, float]], 
                                      tol: float = 1e-6, max_iter: int = 100) -> np.ndarray:

    n = len(funcs)
    if n != len(bounds):
        raise ValueError("El número de funciones debe ser igual al número de variables")
    
    x = np.zeros(n)
    
    # Este es un enfoque muy simplificado que asume que las variables son independientes
    # En la práctica, los sistemas no lineales requieren métodos más complejos como Newton-Raphson
    for i in range(n):
        a, b = bounds[i]
        x[i] = bisection(funcs[i], a, b, tol, max_iter)
    
    return x