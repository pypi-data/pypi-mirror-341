# EM15008UNO

Esta libreria permite resolver sistemas de ecuaciones lineales y no lineales usando métodos clásicos como:

## Métodos incluidos:
- Eliminación de Gauss
- Gauss-Jordan
- Cramer
- Descomposición LU
- Jacobi
- Gauss-Seidel
- Bisección

## Instalación
```bash
pip install EM15008UNO
```
## Programación Orientada a Objetos (POO)

La librería `EM15008UNO` está diseñada utilizando principios de Programación Orientada a Objetos (POO). 

Se definen clases que agrupan métodos relacionados:

- `SistemasLineales`: contiene métodos como `gauss()`, `gauss_jordan()`, `cramer()`, `descomposicion_lu()`, `jacobi()` y `gauss_seidel()`.
- `SistemasNoLineales`: contiene el método `biseccion()`

### Ejemplo de uso:

```python
from EM15008UNO.lineales import SistemasLineales

A = [[2, 1, -1],
     [-3, -1, 2],
     [-2, 1, 2]]

b = [8, -11, -3]

sl = SistemasLineales()
x = sl.gauss(A, b)
print("Solución por Gauss:", x)
