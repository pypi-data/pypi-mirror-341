# DP21008UNO

## 1er examen corto
Cálculo Numérico para desarrollo de aplicaciones

**DP21008UNO** es una librería en Python desarrollada por Julio César Dávila Peñate para resolver sistemas de ecuaciones lineales y encontrar raíces de funciones mediante diferentes métodos numéricos.

## 📦 Instalación

```bash
pip install DP21008UNO
```

**Nota:** numpy se instalará automáticamente como dependencia si no lo tienes instalado.

## 🚀 Funcionalidades

La librería incluye la implementación de los siguientes métodos:

### Métodos para sistemas de ecuaciones lineales:

- **Método de Gauss**
- **Método de Gauss-Jordan**
- **Método de Jacobi**
- **Método de Gauss-Seidel**
- **Método de Cramer**
- **Descomposición LU**

### Método para encontrar raíces:

- **Método de Bisección**

## 🧠 Uso

Aquí tienes un ejemplo básico de cómo usar la librería:

```python
import numpy as np
from DP21008UNO import *

# Sistema de ecuaciones Ax = b
A = np.array([[2.0, 1.0], [5.0, 7.0]])
b = np.array([11.0, 13.0])

sol_gauss = gauss(A.copy(), b.copy())
sol_jordan = gauss_jordan(A.copy(), b.copy())
sol_jacobi = jacobi(A.copy(), b.copy())
sol_seidel = gauss_seidel(A.copy(), b.copy())
sol_cramer = cramer(A.copy(), b.copy())
sol_lu = lu(A.copy(), b.copy())

print("Solución por Gauss:", sol_gauss)
print("Solución por Gauss-Jordan:", sol_jordan)
print("Solución por Jacobi:", sol_jacobi)
print("Solución por Gauss-Seidel:", sol_seidel)
print("Solución por Cramer:", sol_cramer)
print("Solución por LU:", sol_lu)

# Método de bisección
f = lambda x: x**3 - x - 2
sol_biseccion = biseccion(f, 1, 2)
print("Raíz encontrada por bisección:", sol_biseccion)
```

## 📚 Documentación

Cada función incluye una docstring con explicación de sus parámetros y funcionamiento. Aquí algunos ejemplos:

```python
def gauss(coeficientes, constantes):
    '''
    Entradas:
        coeficientes: matriz array de numpy con los coeficientes del sistema
        constantes: vector array de numpy con las constantes del sistema

    Salidas:
        soluciones: vector de soluciones del sistema
    '''
```
Se incluyen también comentarios que explican el funcionamiento para mayor comprensión de la ejecución de cada función.


## 👤 Autor

**Julio César Dávila Peñate**  
Correo: [dp21008@ues.edu.sv](mailto:dp21008@ues.edu.sv)

## 🪪 Licencia

Este proyecto tiene licencia MIT. 