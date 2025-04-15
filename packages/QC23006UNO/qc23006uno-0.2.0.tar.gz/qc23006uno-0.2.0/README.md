# Métodos para Resolver Sistemas de Ecuaciones

Este documento describe los métodos para resolver sistemas de ecuaciones lineales y no lineales implementados en Python, junto con ejemplos básicos de uso y una breve explicacion de la funcion que hace cada metodo.

---

## 1. Eliminación de Gauss

**Descripción del metodo:**  
Reduce el sistema a una forma triangular superior mediante operaciones fila. Luego, aplica sustitución regresiva para hallar la solución.

**Ejemplo:**

```python
import numpy as np
from mi_modulo import gauss_elimination

A = np.array([[2, 1], [1, 3]])
b = np.array([8, 13])

x = gauss_elimination(A, b)
print(x)
```

---

## 2. Gauss-Jordan

**Descripción del metodo:**  
Extiende el método de Gauss hasta obtener una matriz identidad, lo que permite obtener la solución directamente sin sustitución regresiva.

**Ejemplo:**

```python
import numpy as np
from mi_modulo import gauss_jordan

A = np.array([[2, 1], [1, 3]])
b = np.array([8, 13])

x = gauss_jordan(A, b)
print(x)
```

---

## 3. Regla de Cramer

**Descripción del metodo:**  
Calcula la solución del sistema mediante determinantes, aplicando la regla de Cramer. Solo se puede aplicar si el determinante de la matriz es distinto de cero.

**Ejemplo:**

```python
import numpy as np
from mi_modulo import cramer

A = np.array([[2, 1], [1, 3]])
b = np.array([8, 13])

x = cramer(A, b)
print(x)
```

---

## 4. Descomposición LU

**Descripción del metodo:**  
Descompone la matriz en dos matrices triangulares: una inferior (L) y una superior (U), y resuelve el sistema en dos etapas.

**Ejemplo:**

```python
import numpy as np
from mi_modulo import lu_decomposition

A = np.array([[2, 1], [1, 3]])
b = np.array([8, 13])

x = lu_decomposition(A, b)
print(x)
```

---

## 5. Método de Jacobi

**Descripción del metodo:**  
Método iterativo que aproxima la solución partiendo de un valor inicial. Requiere, idealmente, que la matriz sea diagonalmente dominante para asegurar convergencia.

**Ejemplo:**

```python
import numpy as np
from mi_modulo import jacobi

A = np.array([[4, 1], [2, 3]])
b = np.array([1, 2])

x = jacobi(A, b)
print(x)
```

---

## 6. Método de Gauss-Seidel

**Descripción del metodo:**  
Similar a Jacobi, pero utiliza inmediatamente los nuevos valores calculados dentro de cada iteración, lo que suele acelerar la convergencia.

**Ejemplo:**

```python
import numpy as np
from mi_modulo import gauss_seidel

A = np.array([[4, 1], [2, 3]])
b = np.array([1, 2])

x = gauss_seidel(A, b)
print(x)
```

---

## 7. Método de Bisección

**Descripción del metodo:**  
Encuentra la raíz de una función continua evaluando el punto medio del intervalo `[a, b]` y reduciendo iterativamente el intervalo.

**Ejemplo:**

```python
from mi_modulo import bisection

f = lambda x: x**3 - x - 2
raiz = bisection(f, 1, 2)
print(raiz)
```

---

## 8. Bisección para Sistemas No Lineales

**Descripción del metodo:**  
Aplica el método de bisección a cada ecuación por separado, bajo la suposición (simplificada) de que las variables son independientes. Recomendado solo para casos muy simples.

**Ejemplo:**

```python
from mi_modulo import solve_nonlinear_system_bisection

funcs = [lambda x: x**2 - 4, lambda y: y**2 - 9]
bounds = [(0, 3), (0, 5)]

sol = solve_nonlinear_system_bisection(funcs, bounds)
print(sol)
```

---
