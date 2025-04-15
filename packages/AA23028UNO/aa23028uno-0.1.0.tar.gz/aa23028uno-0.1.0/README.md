# AA23028UNO

Librería de métodos numéricos para resolver sistemas de ecuaciones lineales y no lineales.

## Métodos implementados

- Eliminación de Gauss
- Gauss-Jordan
- Cramer
- Descomposición LU
- Jacobi
- Gauss-Seidel
- Bisección

## Instalación

```bash
pip install AA23028UNO
```

## Ejemplo de uso general

```python
import numpy as np
from AA23028UNO import *

A = np.array([[2,1,-1],[ -3,-1,2],[ -2,1,2]], dtype=float)
b = np.array([8, -11, -3], dtype=float)

x = gauss_elimination(A, b)
print(x)
```

## Ejemplos de cada método

### Eliminación de Gauss
```python
x = gauss_elimination(A, b)
print("Gauss:", x)
```

### Gauss-Jordan
```python
x = gauss_jordan(A, b)
print("Gauss-Jordan:", x)
```

### Cramer
```python
x = cramer(A, b)
print("Cramer:", x)
```

### Descomposición LU
```python
x = lu_decomposition(A, b)
print("LU:", x)
```

### Jacobi
```python
x = jacobi(A, b)
print("Jacobi:", x)
```

### Gauss-Seidel
```python
x = gauss_seidel(A, b)
print("Gauss-Seidel:", x)
```

### Bisección
```python
def f(x):
    return x**3 - x - 2
root = bisection(f, 1, 2)
print("Bisección:", root)
```

Consulta `examples.py` para más ejemplos y casos de uso.
