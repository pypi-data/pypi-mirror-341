import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CA21062UNO.metodos_numericos import SistemasLineales as sl
from CA21062UNO.metodos_numericos import EcuacionesNoLineales as enl

def mostrar_sistema(A, b, nombre):
    print(f"\n### Análisis del sistema: {nombre} ###\n")
    print("Matriz de coeficientes A:")
    print(A)
    print("\nVector de términos independientes b:")
    print(b)
    print("\n" + "&&" * 30 + "\n")

def probar_metodos_lineales(A, b, nombre, verbose=False):
    mostrar_sistema(A, b, nombre)

    metodos = {
        '* Eliminación de Gauss': lambda A, b: sl.eliminacion_gauss(A, b, verbose=verbose),
        '* Gauss-Jordan': lambda A, b: sl.gauss_jordan(A, b, verbose=verbose),
        '* Regla de Cramer': sl.cramer,
        '* Descomposición LU': lambda A, b: sl.descomposicion_lu(A, b, verbose=verbose),
        '* Método de Jacobi': lambda A, b: sl.jacobi(A, b, verbose=verbose),
        '* Método de Gauss-Seidel': lambda A, b: sl.gauss_seidel(A, b, verbose=verbose)
    }

    for nombre_metodo, metodo in metodos.items():
        try:
            print(f"\n>>> Ejecutando: {nombre_metodo}")
            solucion = metodo(np.copy(A), np.copy(b))
            print("Solución obtenida:", np.round(solucion, 10))
            residual = np.linalg.norm(A @ solucion - b)
            print(f"Error (residual): {residual:.10f}")
        except Exception as e:
            print(f"Error durante la ejecución: {str(e)}")
        print("\n" + "&&" * 30)

def probar_metodos_no_lineales(verbose=False):
    print("\n### Comprobando métodos para ecuaciones no lineales ###\n")

    config = {
        'tol': 1e-8,
        'max_iter': 100,
        'verbose': verbose
    }

    def f(x): return x**3 - x - 2

    try:
        print(">>> Método de Bisección:")
        resultado = enl.biseccion(f, 1.0, 2.0, **config)
        print(f"Raíz estimada: {resultado:.10f}")
        print(f"Valor de f en la raíz: {f(resultado):.10f}")
    except Exception as e:
        print(f"Error en Bisección: {str(e)}")
    print("\n" + "&&" * 30)

def main():
    print("\n" + "*" * 60)
    print("*        EJECUCIÓN COMPLETA DE PRUEBAS NUMÉRICAS        *")
    print("*" * 60 + "\n")

    verbose = False

    sistemas = [
        {
            'nombre': "Sistema A - Matriz 2x2 aleatoria",
            'A': np.array([[2, -1], [3, 4]], dtype=float),
            'b': np.array([1, 7], dtype=float)
        },
        {
            'nombre': "Sistema B - Matriz 3x3 bien condicionada",
            'A': np.array([[5, 2, 1], [1, 6, 2], [3, 2, 7]], dtype=float),
            'b': np.array([12, 19, 33], dtype=float)
        },
        {
            'nombre': "Sistema C - Matriz 3x3 con elementos aleatorios",
            'A': np.array([[1, -2, 3], [4, 5, -6], [7, -8, 9]], dtype=float),
            'b': np.array([4, -2, 5], dtype=float)
        }
    ]

    for sistema in sistemas:
        probar_metodos_lineales(sistema['A'], sistema['b'], sistema['nombre'], verbose)

    probar_metodos_no_lineales(verbose)

    print("\n" + "*" * 60)
    print("*            TODAS LAS PRUEBAS HAN FINALIZADO            *")
    print("*" * 60 + "\n")

if __name__ == "__main__":
    main()