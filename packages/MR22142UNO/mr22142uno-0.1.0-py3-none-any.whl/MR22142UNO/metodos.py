# MERTODO: eliminación de Gauss
#------------------------------------------------------------------------------------------

def gauss_elimination(a, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando eliminacion de Gauss.

    Parámetros:
    a -- matriz de coeficientes (lista de listas)
    b -- vector de constantes (lista)

    Retorna:
    Una lista con la solucion del sistema.
    """
    n = len(b)

    # Matriz aumentada
    for i in range(n):
        a[i].append(b[i])

    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo
        max_row = max(range(i, n), key=lambda r: abs(a[r][i]))
        a[i], a[max_row] = a[max_row], a[i]

        # Eliminacion
        for j in range(i + 1, n):
            factor = a[j][i] / a[i][i]
            for k in range(i, n + 1):
                a[j][k] -= factor * a[i][k]

    # Sustitucion hacia atras
    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]

    return x

# ----------------------------------------------------------------------------------------
# METODO: Gauss Jordan
#-----------------------------------------------------------------------------------------

def gauss_jordan(A, B):
    """
    Método de Gauss-Jordan para resolver sistemas de ecuaciones lineales Ax = B.

    Parámetros:
    A -- matriz de coeficientes (lista de listas)
    B -- vector de terminos independientes (lista)

    Retorna:
    Lista con la solución del sistema.
    """
    n = len(A)
    # Matriz aumentada
    M = [A[i] + [B[i]] for i in range(n)]

    for i in range(n):
        # Normalizar la fila
        divisor = M[i][i]
        if divisor == 0:
            raise ValueError("Division por cero detectada en el pivote.")
        M[i] = [x / divisor for x in M[i]]

        # Hacer ceros en la columna i (menos en la fila i)
        for j in range(n):
            if j != i:
                factor = M[j][i]
                M[j] = [M[j][k] - factor * M[i][k] for k in range(n + 1)]

    # Extraer solucion
    return [row[-1] for row in M]

#---------------------------------------------------------------------------------------------
# METODO: Cramer
#--------------------------------------------------------------------------------------------

def determinante(A):
    """
    Calcula el determinante de una matriz 2x2 o 3x3 usando recursión.

    Parámetros:
    A -- matriz cuadrada (lista de listas)

    Retorna:
    El determinante de la matriz A.
    """
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    elif n == 3:
        return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) -
                A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) +
                A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
    else:
        raise ValueError("Esta implementacion solo soporta matrices 2x2 o 3x3.")

def cramer(A, B):
    """
    Método de Cramer para resolver sistemas de ecuaciones Ax = B sin usar librerias externas.

    Parámetros:
    A -- matriz de coeficientes (lista de listas)
    B -- vector de términos independientes (lista)

    Retorna:
    Lista con la solucion del sistema.
    """
    det_A = determinante(A)
    
    if det_A == 0:
        raise ValueError("La matriz es singular, no se puede resolver el sistema.")

    n = len(B)
    soluciones = []

    for i in range(n):
        A_i = [row[:] for row in A]  # Crear una copia de la matriz A
        for j in range(n):
            A_i[j][i] = B[j]  # Reemplazar la columna i con el vector B

        soluciones.append(determinante(A_i) / det_A)

    return soluciones

# --------------------------------------------------------------------------------------------
# METODO: Descomposición LU
# --------------------------------------------------------------------------------------------

def descomposition_lu(A):
    """
    Descompone la matriz A en las matrices L (inferior) y U (superior)
    usando la factorización LU.

    Parámetros:
    A -- matriz cuadrada (lista de listas)

    Retorna:
    L -- matriz triangular inferior
    U -- matriz triangular superior
    """
    n = len(A)
    L = [[0] * n for _ in range(n)]
    U = [[0] * n for _ in range(n)]

    for i in range(n):
        # Rellenar la matriz U
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        
        # Rellenar la matriz L
        for j in range(i, n):
            if i == j:
                L[i][i] = 1
            else:
                L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]

    return L, U

# -------------------------------------------------------------------------------------------
# METODO: Jacobi
# -------------------------------------------------------------------------------------------

def jacobi(A, B, tol=1e-10, max_iter=1000):
    """
    Método de Jacobi para resolver sistemas de ecuaciones Ax = B.

    Parámetros:
    A -- matriz de coeficientes (lista de listas)
    B -- vector de terminos independientes (lista)
    tol -- tolerancia (por defecto 1e-10)
    max_iter -- numero maximo de iteraciones (por defecto 1000)

    Retorna:
    Lista con la solucion aproximada del sistema.
    """
    n = len(A)
    x = [0] * n  # Solución inicial
    x_new = x.copy()

    for it in range(max_iter):
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (B[i] - suma) / A[i][i]

        # Verificar convergencia
        if all(abs(x_new[i] - x[i]) < tol for i in range(n)):
            return x_new

        x = x_new.copy()

    raise ValueError("El metodo no converge en el numero maximo de iteraciones.")

# -------------------------------------------------------------------------------------
#  METODO: Gauss-seidel
# -------------------------------------------------------------------------------------

def gauss_seidel(A, B, tol=1e-10, max_iter=1000):
    """
    Método de Gauss-Seidel para resolver sistemas de ecuaciones Ax = B.

    Parámetros:
    A -- matriz de coeficientes (lista de listas)
    B -- vector de terminos independientes (lista)
    tol -- tolerancia (por defecto 1e-10)
    max_iter -- numero maximo de iteraciones (por defecto 1000)

    Retorna:
    Lista con la solucion aproximada del sistema.
    """
    n = len(A)
    x = [0] * n  # Solución inicial

    for it in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            suma = sum(A[i][j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (B[i] - suma) / A[i][i]

        # Verificar convergencia
        if all(abs(x_new[i] - x[i]) < tol for i in range(n)):
            return x_new

        x = x_new

    raise ValueError("El metodo no converge en el numero maximo de iteraciones.")



def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de Biseccion para encontrar la raíz de una función f(x) = 0.

    Parámetros:
    f -- función a evaluar
    a -- limite inferior del intervalo
    b -- limite superior del intervalo
    tol -- tolerancia aceptada para la raiz
    max_iter -- numero maximo de iteraciones

    Retorna:
    Aproximacion de la raiz si se encuentra dentro del intervalo.
    """
    if f(a) * f(b) > 0:
        raise ValueError("La funcion debe cambiar de signo en el intervalo [a, b].")

    for i in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    raise RuntimeError("El metodo no convergio en el numero maximo de iteraciones.")