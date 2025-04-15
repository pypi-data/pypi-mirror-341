# SC19013UNO

**SC19013UNO** es una librería en Python que proporciona métodos numéricos para resolver:

- **Sistemas de ecuaciones lineales** (como el método de Gauss, Gauss-Jordan, Jacobi, etc.).
- **Ecuaciones no lineales** (como el método de Bisección).

---

## Estructura del Proyecto
SC19013UNO/ 
├── SC19013UNO/
│ ├── init.py # Inicialización del paquete 
│ ├── lineales.py # Métodos para sistemas lineales 
│ └── no_lineales.py # Métodos para ecuaciones no lineales 
├── tests/ # Archivos de prueba 
│ ├── test_lineales.py # Pruebas para métodos lineales 
│ └── test_no_lineales.py # Pruebas para métodos no lineales 
├── setup.py # Configuración para instalación 
└── LICENSE # Licencia del proyecto



---

## Instalación

### Instalación usando `pip`:

1. Si tienes `pip` instalado, puedes instalar la librería directamente desde PyPI:

   ```bash
   pip install SC19013UNO

## Ejemplo: Resolver un Sistema Lineal
from SC19013UNO.lineales import SolucionadorLineales

A = [[4, 1, 2],
     [3, 5, 1],
     [1, 1, 3]]
b = [4, 7, 3]

solucion = SolucionadorLineales.jacobi(A, b)
print(solucion)


## Ejemplo: Resolver una Ecuación No Lineal (Método de Bisección)

import math
from SC19013UNO.no_lineales import SolucionadorNoLineales

## Definir la función
f = lambda x: math.cos(x) - x

### Encontrar la raíz en el intervalo [0, 1]
raiz = SolucionadorNoLineales.biseccion(f, 0, 1)
print(raiz)


## Métodos Disponibles
### Para Sistemas Lineales (Clase SolucionadorLineales):
gauss(A, b)

gauss_jordan(A, b)

cramer(A, b)

lu(A, b)

jacobi(A, b, x0, tol, max_iter)

gauss_seidel(A, b, x0, tol, max_iter)

### Para Ecuaciones No Lineales (Clase SolucionadorNoLineales):
biseccion(f, a, b, tol, max_iter)