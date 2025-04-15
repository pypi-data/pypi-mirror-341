# JM21008UNO

JM21008UNO es una librería de Python diseñada para resolver sistemas de ecuaciones lineales y no lineales utilizando varios métodos numéricos. Esta librería incluye implementaciones de los métodos de eliminación de Gauss, Gauss-Jordan, Cramer, descomposición LU y Jacobi, proporcionando una herramienta versátil para el campo de las matemáticas y la ingeniería.

## Métodos Disponibles

- **Eliminación de Gauss**: Resuelve sistemas de ecuaciones lineales mediante la eliminación de variables.
- **Gauss-Jordan**: Extensión del método de Gauss que reduce la matriz a su forma escalonada reducida.
- **Cramer**: Utiliza determinantes para resolver sistemas de ecuaciones lineales.
- **Descomposición LU**: Descompone una matriz en dos matrices, L (triangular inferior) y U (triangular superior), para facilitar la resolución del sistema.
- **Jacobi**: Método iterativo que encuentra la solución de sistemas de ecuaciones lineales.

## Instalación

Para instalar la librería, puedes usar `pip`:

```
pip install JM21008UNO
```

## Ejemplo de Uso

```python
from jm21008uno.gauss import resolver_gauss
from jm21008uno.gauss_jordan import resolver_gauss_jordan
from jm21008uno.cramer import resolver_cramer
from jm21008uno.lu_decomposition import resolver_lu
from jm21008uno.jacobi import resolver_jacobi

# Definir una matriz de coeficientes y un vector de términos independientes
A = [[2, 1, -1], [3, 3, 9], [3, 4, 2]]
b = [8, 0, 3]

# Resolver usando el método de eliminación de Gauss
solucion_gauss = resolver_gauss(A, b)

# Resolver usando el método de Gauss-Jordan
solucion_gauss_jordan = resolver_gauss_jordan(A, b)

# Resolver usando el método de Cramer
solucion_cramer = resolver_cramer(A, b)

# Resolver usando descomposición LU
solucion_lu = resolver_lu(A, b)

# Resolver usando el método de Jacobi
solucion_jacobi = resolver_jacobi(A, b)
```

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.