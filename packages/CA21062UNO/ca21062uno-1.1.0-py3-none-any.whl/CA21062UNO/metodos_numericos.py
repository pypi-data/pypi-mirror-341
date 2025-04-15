import numpy as np
from scipy.linalg import lu_factor, lu_solve, solve, det
from scipy.optimize import bisect

class SistemasLineales:
    @staticmethod
    def eliminacion_gauss(A, b, pivoteo=True, verbose=False):
        return solve(A, b)
    
    @staticmethod
    def gauss_jordan(A, b, pivoteo=True, verbose=False):
        return solve(A, b)
    
    @staticmethod
    def cramer(A, b):
        n = len(b)
        det_A = det(A)
        if np.abs(det_A) < 1e-12:
            raise ValueError("Matriz singular (determinante cero)")
        
        x = np.zeros(n)
        for i in range(n):
            Ai = A.copy()
            Ai[:, i] = b
            x[i] = det(Ai) / det_A
        
        return x
    
    @staticmethod
    def descomposicion_lu(A, b, pivoteo=True, verbose=False):
        lu, piv = lu_factor(A)
        return lu_solve((lu, piv), b)
    
    @staticmethod
    def jacobi(A, b, x0=None, tol=1e-8, max_iter=1000, verbose=False):
        n = len(b)
        x = x0 if x0 is not None else np.zeros(n)
        
        diag = np.abs(np.diag(A))
        suma_filas = np.sum(np.abs(A), axis=1) - diag
        if np.any(diag <= suma_filas):
            print("Advertencia: Matriz no estrictamente diagonal dominante")
        
        for k in range(max_iter):
            x_new = np.zeros(n)
            for i in range(n):
                s = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x[i+1:])
                x_new[i] = (b[i] - s) / A[i, i]
            
            residual = np.linalg.norm(A @ x_new - b)
            if verbose:
                print(f"Iter {k+1}: x = {x_new}, error = {residual:.6f}")
            
            if residual < tol:
                return x_new
            x = x_new
        
        raise ValueError(f"No convergencia en {max_iter} iteraciones")
    
    @staticmethod
    def gauss_seidel(A, b, x0=None, tol=1e-8, max_iter=1000, verbose=False):
        n = len(b)
        x = x0 if x0 is not None else np.zeros(n)
        
        diag = np.abs(np.diag(A))
        suma_filas = np.sum(np.abs(A), axis=1) - diag
        if np.any(diag <= suma_filas):
            print("Advertencia: Matriz no estrictamente diagonal dominante")
        
        for k in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                s1 = np.dot(A[i, :i], x[:i])
                s2 = np.dot(A[i, i+1:], x_old[i+1:])
                x[i] = (b[i] - s1 - s2) / A[i, i]
            
            residual = np.linalg.norm(A @ x - b)
            if verbose:
                print(f"Iter {k+1}: x = {x}, error = {residual:.6f}")
            
            if residual < tol:
                return x
        
        raise ValueError(f"No convergencia en {max_iter} iteraciones")


class EcuacionesNoLineales:
    @staticmethod
    def biseccion(f, a, b, tol=1e-8, max_iter=200, verbose=False):
        return bisect(f, a, b, xtol=tol, maxiter=max_iter)