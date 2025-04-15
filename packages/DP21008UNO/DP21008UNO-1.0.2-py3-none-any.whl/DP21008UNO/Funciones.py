import numpy as np

# Funcion auxiliar para determinar que la matriz coeficientes sea cuadrada
def es_cuadrada(matrix):
    '''
    Entradas:
        matrix: matriz de numpy para verificar que sea cuadrada

    Se lanza un error cuando no es cuadrada
    '''
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("La matriz de coeficientes debe ser cuadrada.")

# Función para verificar si la diagonal principal tiene ceros y ajustar filas
def ajustar_diagonal(matrix, vector):
    '''
    Entradas:
        matrix: matriz array de numpy con los coeficientes del sistema
        vector: vector array de numpy con las constantes del sistema

    Salidas:
        matrix y vector reordenados para que la diagonal no tenga 0 de ser posible
    '''
    es_cuadrada(matrix)
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            for j in range(i + 1, len(matrix)):
                if matrix[j][i] != 0:
                    # Intercambiar filas en la matriz de coeficientes
                    matrix[[i, j]] = matrix[[j, i]]
                    # Intercambiar valores correspondientes en constantes
                    vector[[i, j]] = vector[[j, i]]
                    break
            else:
                raise ValueError(f"No se puede ajustar la diagonal. Columna {i} son todos ceros.")
    return matrix, vector


# Funcion para resolver mediante Gauss
def gauss(coeficientes, constantes):
    '''
    Entradas:
        coeficientes: matriz array de numpy con los coeficientes del sistema
        constantes: vector array de numpy con las constantes del sistema

    Salidas:
        soluciones: vector de soluciones del sistema
    '''
    coeficientes, constantes = ajustar_diagonal(coeficientes, constantes)
    coeficientes = np.array(coeficientes, dtype=float)
    constantes = np.array(constantes, dtype=float)
    n = len(constantes)
    # Crear matriz extendida coeficientes|constantes
    ecuaciones = np.hstack([coeficientes, constantes.reshape(-1, 1)])
    for i in range(n):
        # Verificar si el pivote es cero y cambiar filas si es necesario
        if ecuaciones[i, i] == 0:
            for j in range(i + 1, n):
                if ecuaciones[j, i] != 0:
                    ecuaciones[[i, j]] = ecuaciones[[j, i]]  # Intercambio de filas
                    break
            else:
                raise ValueError(f"No se puede continuar, pivote en posición ({i}, {i}) es cero.")
        # Dividir fila [i] entre el pivote
        ecuaciones[i] = ecuaciones[i] / ecuaciones[i, i]
        for j in range(n):
            if i < j:
                # Operar entre filas para que los elementos de abajo sean 0
                ecuaciones[j] -= ecuaciones[j, i] * ecuaciones[i]
    # Calcular soluciones
    soluciones = np.zeros(n)
    for i in range(n - 1, -1, -1): # Desde la ultima hasta la primer fila
        suma = 0 # Reiniciar suma
        for j in range(i + 1, n): # Columnas de izquierda a derecha
            suma += ecuaciones[i, j] * soluciones[j]  # coeficiente por valores de variable ya obtenidos
        soluciones[i] = ecuaciones[i, -1] - suma  # X+a = b -> X = b-a 
    return soluciones


# Funcion para resolver mediante Gauss-Jordan
def gauss_jordan(coeficientes, constantes):
    '''
    Entradas:
        coeficientes: matriz array de numpy con los coeficientes del sistema
        constantes: vector array de numpy con las constantes del sistema

    Salidas:
        soluciones: vector de soluciones del sistema
    '''
    coeficientes, constantes = ajustar_diagonal(coeficientes, constantes)
    coeficientes = np.array(coeficientes, dtype=float)
    constantes = np.array(constantes, dtype=float)
    n = len(constantes)
    # Crear matriz extendida coeficientes|constantes
    ecuaciones = np.hstack([coeficientes, constantes.reshape(-1, 1)])
    for i in range(n):
        # Verificar si el pivote es cero y cambiar filas si es necesario
        if ecuaciones[i, i] == 0:
            for j in range(i + 1, n):
                if ecuaciones[j, i] != 0:
                    ecuaciones[[i, j]] = ecuaciones[[j, i]]  # Intercambio de filas
                    break
            else:
                raise ValueError(f"No se puede continuar, pivote en posición ({i}, {i}) es cero.")
        # Dividir fila [i] entre el pivote
        ecuaciones[i] = ecuaciones[i] / ecuaciones[i, i]
        for j in range(n):
            if i != j:
                # Operar entre filas para que los otros elementos de la columna sean 0
                ecuaciones[j] -= ecuaciones[j, i] * ecuaciones[i]
    # Retorna la ultima columna
    soluciones = ecuaciones[:, -1]
    return soluciones


# Funcion para resolver mediante jacobi
def jacobi(coeficientes, constantes, tol=1e-10, max_iter=1000):
    '''
    Entradas:
        coeficientes: matriz array de numpy con los coeficientes del sistema
        constantes: vector array de numpy con las constantes del sistema
        tol: tolerancia (1e-10 por defecto)
        max_iter: numero maximo de iteraciones a ejecutar (1000 por defecto)

    Salidas:
        soluciones: vector de soluciones del sistema
    '''
    coeficientes, constantes = ajustar_diagonal(coeficientes, constantes)
    n = len(constantes)
    x = np.zeros(n)
    x_new = np.zeros(n)
    for k in range(max_iter):
        for i in range(n):
            suma = 0
            for j in range(n):
                if j != i:
                    # Se utilizan los valores de iteración anterior (x)
                    suma += coeficientes[i, j] * x[j]
            # Se almacenan los valores en x_new
            x_new[i] = (constantes[i] - suma) / coeficientes[i, i]
        if np.linalg.norm(x_new - x) < tol:
            soluciones = x_new
            return soluciones
        # Se actualiza x con los valores de x_new de la última iteración
        x = x_new.copy()
    raise ValueError(f"No se logró la convergencia en {max_iter} iteraciones")


# Funcion para resolver mediante Gauss-Seidel
def gauss_seidel(coeficientes, constantes, tol=1e-10, max_iter=1000):
    '''
    Entradas:
        coeficientes: matriz array de numpy con los coeficientes del sistema
        constantes: vector array de numpy con las constantes del sistema
        tol: tolerancia (1e-10 por defecto)
        max_iter: numero maximo de iteraciones a ejecutar (1000 por defecto)

    Salidas:
        soluciones: vector de soluciones del sistema
    '''
    coeficientes, constantes = ajustar_diagonal(coeficientes, constantes)
    n = len(constantes)
    x = np.zeros(n)
    for k in range(max_iter):
        # Se almacena x_prev para comparar luego mediante normailzación
        x_prev = x.copy()
        for i in range(n):
            suma = 0
            for j in range(n):
                if j != i:
                    # Se usan los valores de la iteración actual inmediata (x)
                    suma += coeficientes[i,j]*x[j]
            x[i] = (constantes[i] - suma) / coeficientes[i,i]
        if np.linalg.norm(x - x_prev) < tol:
            soluciones = x
            return soluciones
    raise ValueError(f"No se logró la convergencia en {max_iter} iteraciones")


# Funcion para resolver mediante Cramer
def cramer(coeficientes, constantes):
    '''
    Entradas:
        coeficientes: matriz array de numpy con los coeficientes del sistema
        constantes: vector array de numpy con las constantes del sistema

    Salidas:
        soluciones: vector de soluciones del sistema
    '''
    es_cuadrada(coeficientes)
    n = coeficientes.shape[0]
    
    # Calcular el determinante de la matriz de coeficientes (linalg.det de la libería numpy calcula el determinante)
    det_coeficientes = np.linalg.det(coeficientes)
    if det_coeficientes == 0:
        raise ValueError("El sistema no tiene solución única (determinante es 0).")
    
    soluciones = np.zeros(n)
    for i in range(n):
        # Copia la matriz de coeficientes
        matriz_modificada = coeficientes.copy()
        # Reemplaza la columna actual i por el vector constantes
        matriz_modificada[:, i] = constantes
        # Calcular determinante de la matriz modificada
        det_modificado = np.linalg.det(matriz_modificada)
        # Calcular cada solución al dividir el determinante de la matriz modificada entre el de la original
        soluciones[i] = det_modificado / det_coeficientes
    
    # Pueden haber inexactitudes debido a los cálculos de determinantes
    return soluciones


# Funcion para resolver mediante LU
def lu(coeficientes, constantes):
    '''
    Entradas:
        coeficientes: matriz array de numpy con los coeficientes del sistema
        constantes: vector array de numpy con las constantes del sistema

    Salidas:
        soluciones: vector de soluciones del sistema
    '''
    coeficientes, constantes = ajustar_diagonal(coeficientes, constantes)
    coeficientes = np.array(coeficientes, dtype=float)
    constantes = np.array(constantes, dtype=float)
    n = len(coeficientes)
    L = np.zeros((n, n))
    U = coeficientes.copy()
    # Inicializar L como matriz identidad (diagonal principal son solo 1, todo lo demás son 0)
    for i in range(n):
        L[i, i] = 1.0
    # Factorización LU
    for i in range(n):
        for j in range(n):
            if i < j:
                # L: L[j, i] = (j, i)/(i, i)
                L[j, i] = U[j, i] / U[i, i]
                # U: Fila j = Fila j - (j, i)/(i, i)*(Fila i)
                U[j, :] -= U[j, i] * U[i, :] / U[i, i]
    # Sustitución hacia adelante (Ly = constantes)
    y = np.zeros(n)
    for i in range(n):
        suma = 0
        for j in range(i):
            suma += L[i, j] * y[j]
        y[i] = constantes[i] - suma
    # Sustitución hacia atrás (Ux = y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += U[i, j] * x[j]
        x[i] = (y[i] - suma) / U[i, i]
    soluciones = x
    return soluciones


# Funcion para resolver mediante biseccion
def biseccion(f, a, b, tol=1e-10, max_iter=1000):
    '''
    Entradas:
        f: funcion lambda
        a: limite inferior del rango
        b: limite superior del rango
        tol: tolerancia (1e-10 por defecto)
        max_iter: numero maximo de iteraciones a ejecutar (1000 por defecto)

    Salidas:
        solucion: variable de coma flotante
    '''
    if f(a) * f(b) >= 0:
        raise ValueError(f"La función no cambia de signo en el rango [{a}, {b}]")
    for i in range(max_iter+1):
        if (b - a) / 2 <= tol:
            break
        xr = (a + b) / 2
        if f(xr) == 0:
            return xr, i
        elif f(a) * f(xr) < 0:
            b = xr
        else:
            a = xr
    # Al alcanzar la maxima iteracion o cumplir con la tol, devuelve la mejor aproximacion encontrada
    solucion = (a + b) / 2
    return solucion
