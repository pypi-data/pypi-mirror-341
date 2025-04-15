import numpy as np

class SistemasLineales:
    def _eliminacion_hacia_adelante(self, A, b):
        A = np.array(A, dtype = float)
        b = np.array(b, dtype = float)
        n = len(b)

        #Construccion de la matriz aumentada.
        M = np.hstack([A, b.reshape(-1, 1)])

        #Eliminacion hacia adelante
        for i in range(n):
            #Pivote parcial
            max_row = np.argmax(abs(M[i:, i])) + i
            if M[max_row, i] == 0:
                raise ValueError("El sistema no tiene solucion unica.")
            M[[i, max_row]] = M[[max_row, i]]

            #Eliminacion.
            for j in range(i + 1, n):
                factor = M[j, i]/M[i, i]
                M[j, i:] -= factor * M[i, i:]
        return M

    def gauss(self, A, b):
        """
        Resuelve un sistema de ecuaciones lineales, usando la eliminación de Gauss.

        Parámetros necesarios:
        A -> Matriz de coeficientes (debe ser lista de listas o np.array)
        b -> Vector de términos independientes (debe ser una lista o np.array)

        Retornara la solucion.
        x -> vector solucion.
        """
        M = self._eliminacion_hacia_adelante(A, b)
        n = len(b)
        x = np.zeros(n)

        #Sustitucion hacia atras.
        for i in range(n - 1, -1, -1):
            x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n]))/M[i, i]
        
        return x

    def gauss_jordan(self, A, b):
        """
        Resuelve un sistema de ecuaciones lineales, usando la eliminación de Gauss-Jordan.

        Parámetros necesarios:
        A -> Matriz de coeficientes (debe ser lista de listas o np.array)
        b -> Vector de términos independientes (debe ser una lista o np.array)

        Retornara la solucion.
        x -> vector solucion.
        """
        M = self._eliminacion_hacia_adelante(A, b)
        n = len(b)

        for i in range(n - 1, -1, -1):
            M[i] = M[i] / M[i, i]
            for j in range(i):
                M[j] = M[j] - M[j, i] * M[i]
        
        return M[:, -1]

    def cramer(self, A, b):
        """
        Resuelve un sistema de ecuaciones lineales usando la regla de Cramer.

        Parámetros necesarios:
        A -> Matriz de coeficientes.
        b -> Vector de términos independientes.

        Retorno:
        x -> vector solucion.
        """
        A = np.array(A, dtype = float)
        b = np.array(b, dtype = float)
        n = len(b)

        det_A = np.linalg.det(A)
        if det_A == 0:
            raise ValueError("El sistema no tiene solución única (determinante = 0).")
        
        x = np.zeros(n)
        for i in range(n):
            Ai = A.copy()
            Ai[:, i] = b
            x[i] = np.linalg.det(Ai) / det_A
        
        return x

    def descomposicion_lu(self, A, b):
        """
        Resuelve un sistema de ecuaciones lineales usando descomposición LU.

        Parámetros:
        A -> Matriz de coeficientes.
        b -> Vector de términos independientes.

        Retorno:
        x -> Vector solución.
        """
        A = np.array(A, dtype = float)
        b = np.array(b, dtype = float)
        n = len(A)

        L = np.eye(n)
        U = A.copy()

        for i in range(n):
            if U[i, i] == 0:
                raise ValueError("Cero en el pivote. No se puede continuar sin pivoteo.")
            for j in range(i+1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, i:] = U[j, i:] - factor * U[i, i:]
        
        #Sustitucion hacia adelante.
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i, :i], y[:i])

        #Sustitucion hacia atras.
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:]))/U[i, i]
        
        return x

    def _metodo_iterativo(self, A, b, tol = 1e-10, max_iter = 100, usar_gauss_seidel = False):
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = len(A)
        x = np.zeros(n)

        for _ in range(max_iter):
            x_new = np.copy(x)

            for i in range(n):
                s1 = sum(A[i][j] * (x_new[j] if usar_gauss_seidel else x[j]) for j in range(i))
                s2 = sum(A[i][j] * x[j] for j in range(i+1, n))
                x_new[i] = (b[i] - s1 - s2) / A[i][i]

            if np.linalg.norm(x_new - x, ord=np.inf) < tol:
                return x_new

            x = x_new

        raise ValueError("El método iterativo no convergió.")

    def jacobi(self, A, b, tol=1e-10, max_iter=100):
        """
        Resuelve un sistema de ecuaciones lineales usando el método de Jabobi.

        Parámetros:
        A -> Matriz de coeficientes.
        b -> Vector de términos independientes.
        tol -> Tolerancia para el criterio de parada.
        max_iter -> Número máximo de iteraciones.
        
        Retorno:
        x -> Vector solucion.
        """
        return self._metodo_iterativo(A, b, tol, max_iter, usar_gauss_seidel=False)

    def gauss_seidel(self, A, b, x0=None, tol=1e-10, max_iter=100):
        """
        Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.

        Parámetros:
        A -> Matriz de coeficientes.
        b -> Vector de términos independientes.
        tol -> Tolerancia para el criterio de parada.
        max_iter -> Número máximo de iteraciones.
        
        Retorno:
        x -> Vector solucion.
        """
        return self._metodo_iterativo(A, b, tol, max_iter, usar_gauss_seidel=True)
