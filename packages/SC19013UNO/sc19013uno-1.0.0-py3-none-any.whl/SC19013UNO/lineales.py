import copy
import math

class SolucionadorLineales:
    """Clase que implementa métodos para resolver sistemas de ecuaciones lineales."""
    
    @staticmethod
    def gauss(A, b):
        n = len(b)
        M = [row[:] for row in A]
        for i in range(n):
            M[i].append(b[i])
        
        for i in range(n):
            # Pivoteo parcial
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            
            if M[i][i] == 0:
                raise ValueError("El sistema no tiene solución única.")
            
            # Eliminación hacia adelante (CORRECCIÓN IMPORTANTE)
            for k in range(i+1, n):
                factor = M[k][i] / M[i][i]
                for j in range(i, n+1):
                    M[k][j] -= factor * M[i][j]
        
        # Sustitución regresiva
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            x[i] = M[i][n]
            for j in range(i+1, n):
                x[i] -= M[i][j] * x[j]
            x[i] /= M[i][i]  # ¡División crucial que faltaba!
        return x

    @staticmethod
    def gauss_jordan(A, b):
        """Gauss-Jordan: Reduce A a la matriz identidad."""
        n = len(b)
        M = [row[:] for row in A]
        for i in range(n):
            M[i].append(b[i])
        
        for i in range(n):
            # Pivoteo
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            
            if M[i][i] == 0:
                raise ValueError("Sistema singular.")
            
            pivot = M[i][i]
            for j in range(i, n + 1):
                M[i][j] /= pivot
            
            for k in range(n):
                if k != i and M[k][i] != 0:
                    factor = M[k][i]
                    for j in range(i, n + 1):
                        M[k][j] -= factor * M[i][j]
        
        return [row[n] for row in M]

    @staticmethod
    def cramer(A, b):
        """Regla de Cramer (solo para sistemas pequeños)."""
        n = len(b)
        det_A = SolucionadorLineales.determinante(A)
        if det_A == 0:
            raise ValueError("El sistema no tiene solución única.")
        
        x = []
        for i in range(n):
            Ai = [row[:] for row in A]
            for j in range(n):
                Ai[j][i] = b[j]
            x.append(SolucionadorLineales.determinante(Ai) / det_A)
        return x

    @staticmethod
    def determinante(A):
        """Calcula el determinante de una matriz (recursivo)."""
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * SolucionadorLineales.determinante(submatrix)
        return det

    @staticmethod
    def lu(A, b):
        """Descomposición LU (sin pivoteo)."""
        n = len(b)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            L[i][i] = 1.0
            for j in range(i, n):
                U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
            for j in range(i + 1, n):
                L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]
        
        # Resolver Ly = b
        y = [0.0] * n
        for i in range(n):
            y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
        
        # Resolver Ux = y
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
        return x

    @staticmethod
    def jacobi(A, b, x0=None, tol=1e-6, max_iter=1000):
        """Método iterativo de Jacobi."""
        n = len(b)
        x = x0 if x0 is not None else [0.0] * n
        x_new = [0.0] * n
        
        # Verificar convergencia
        if not SolucionadorLineales._es_diagonalmente_dominante(A):
            print("Advertencia: La matriz no es diagonalmente dominante - convergencia no garantizada")
        
        for _ in range(max_iter):
            for i in range(n):
                if A[i][i] == 0:
                    raise ValueError(f"División por cero en A[{i}][{i}]")
                s = sum(A[i][j] * x[j] for j in range(n) if j != i)
                x_new[i] = (b[i] - s) / A[i][i]
            
            if math.sqrt(sum((x_new[i] - x[i]) ** 2 for i in range(n))) < tol:
                return x_new
            x = x_new.copy()
        raise RuntimeError(f"No convergió después de {max_iter} iteraciones")

    @staticmethod
    def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=1000):
        """Método iterativo de Gauss-Seidel."""
        n = len(b)
        x = x0 if x0 is not None else [0.0] * n
        
        # Verificar convergencia
        if not SolucionadorLineales._es_diagonalmente_dominante(A):
            print("Advertencia: La matriz no es diagonalmente dominante - convergencia no garantizada")
        
        for _ in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                if A[i][i] == 0:
                    raise ValueError(f"División por cero en A[{i}][{i}]")
                s1 = sum(A[i][j] * x[j] for j in range(i))
                s2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
                x[i] = (b[i] - s1 - s2) / A[i][i]
            
            if math.sqrt(sum((x[i] - x_old[i]) ** 2 for i in range(n))) < tol:
                return x
        raise RuntimeError(f"No convergió después de {max_iter} iteraciones")

    @staticmethod
    def _es_diagonalmente_dominante(A):
        """Verifica si la matriz es diagonalmente dominante."""
        for i in range(len(A)):
            suma_fila = sum(abs(A[i][j]) for j in range(len(A)) if j != i)
            if abs(A[i][i]) <= suma_fila:
                return False
        return True