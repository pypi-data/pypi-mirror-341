import numpy as np

class SistemasLineales:
    @staticmethod
    def gauss(A, b, usar_pivoteo=True, mostrar=False):
        n = len(b)
        if A.shape != (n, n):
            raise ValueError("La matriz A debe ser cuadrada y del mismo tamaño que b")

        M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])

        if mostrar:
            print("\nIniciando Gauss:")
            print(M)

        for i in range(n):
            if usar_pivoteo:
                fila_max = np.argmax(np.abs(M[i:, i])) + i
                if fila_max != i:
                    M[[i, fila_max]] = M[[fila_max, i]]
                    if mostrar:
                        print(f"\nCambio de fila {i} con {fila_max}")
                        print(M)

            if np.abs(M[i, i]) < 1e-12:
                raise ValueError("Pivote cero. Sistema posiblemente sin solución única.")

            for j in range(i + 1, n):
                factor = M[j, i] / M[i, i]
                M[j, i:] -= factor * M[i, i:]
                if mostrar:
                    print(f"\nFila {j} actualizada:")
                    print(M)

        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            suma = np.dot(M[i, i + 1:n], x[i + 1:n]) if i < n - 1 else 0.0
            x[i] = (M[i, -1] - suma) / M[i, i]
        return x

    @staticmethod
    def gauss_jordan(A, b, usar_pivoteo=True, mostrar=False):
        n = len(b)
        if A.shape != (n, n):
            raise ValueError("A debe ser cuadrada")

        M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])

        if mostrar:
            print("\nIniciando Gauss-Jordan:")
            print(M)

        for i in range(n):
            if usar_pivoteo:
                fila_max = np.argmax(np.abs(M[i:, i])) + i
                if fila_max != i:
                    M[[i, fila_max]] = M[[fila_max, i]]

            pivote = M[i, i]
            if abs(pivote) < 1e-12:
                raise ValueError("Pivote cero detectado")

            M[i] /= pivote
            for j in range(n):
                if j != i:
                    M[j] -= M[j, i] * M[i]
        return M[:, -1]

    @staticmethod
    def cramer(A, b):
        n = len(b)
        if A.shape != (n, n):
            raise ValueError("A debe ser cuadrada")

        det_A = np.linalg.det(A)
        if abs(det_A) < 1e-12:
            raise ValueError("Determinante cero. Sistema sin solución única.")

        x = np.zeros(n)
        for i in range(n):
            Ai = A.copy()
            Ai[:, i] = b
            x[i] = np.linalg.det(Ai) / det_A
        return x

    @staticmethod
    def lu(A, b, usar_pivoteo=True, mostrar=False):
        n = len(b)
        if A.shape != (n, n):
            raise ValueError("A debe ser cuadrada")

        L = np.eye(n)
        U = A.astype(float)
        P = np.eye(n)
        b = b.astype(float)

        for i in range(n):
            if usar_pivoteo:
                fila_max = np.argmax(np.abs(U[i:, i])) + i
                if fila_max != i:
                    U[[i, fila_max]] = U[[fila_max, i]]
                    L[[i, fila_max], :i] = L[[fila_max, i], :i]
                    P[[i, fila_max]] = P[[fila_max, i]]
                    b[[i, fila_max]] = b[[fila_max, i]]

            for j in range(i + 1, n):
                L[j, i] = U[j, i] / U[i, i]
                U[j, i:] -= L[j, i] * U[i, i:]

        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i, :i], y[:i])

        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]
        return x

    @staticmethod
    def jacobi(A, b, x0=None, tol=1e-8, iter_max=100, mostrar=False):
        n = len(b)
        x = x0 if x0 is not None else np.zeros(n)
        for it in range(iter_max):
            nuevo_x = np.zeros(n)
            for i in range(n):
                suma = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x[i+1:])
                nuevo_x[i] = (b[i] - suma) / A[i, i]
            if np.linalg.norm(nuevo_x - x, ord=np.inf) < tol:
                return nuevo_x
            if mostrar:
                print(f"Iteración {it+1}: {nuevo_x}")
            x = nuevo_x
        return x

    @staticmethod
    def gauss_seidel(A, b, x0=None, tol=1e-8, iter_max=100, mostrar=False):
        n = len(b)
        x = x0 if x0 is not None else np.zeros(n)
        for it in range(iter_max):
            viejo_x = x.copy()
            for i in range(n):
                suma1 = np.dot(A[i, :i], x[:i])
                suma2 = np.dot(A[i, i+1:], viejo_x[i+1:])
                x[i] = (b[i] - suma1 - suma2) / A[i, i]
            if np.linalg.norm(x - viejo_x, ord=np.inf) < tol:
                return x
            if mostrar:
                print(f"Iteración {it+1}: {x}")
        return x

class EcuacionesNoLineales:
    @staticmethod
    def biseccion(f, a, b, tol=1e-8, iter_max=100, mostrar=False):
        if f(a) * f(b) >= 0:
            raise ValueError("La función no cambia de signo en el intervalo dado")

        for i in range(iter_max):
            medio = (a + b) / 2
            if mostrar:
                print(f"Paso {i+1}: intervalo [{a}, {b}], medio = {medio}, f(medio) = {f(medio)}")
            if abs(f(medio)) < tol or (b - a) / 2 < tol:
                return medio
            if f(a) * f(medio) < 0:
                b = medio
            else:
                a = medio
        return (a + b) / 2