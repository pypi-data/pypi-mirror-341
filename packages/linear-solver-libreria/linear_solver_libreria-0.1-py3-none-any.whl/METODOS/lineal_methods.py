from json import tool
import numpy as np

def gauss_elimination(A, B):
    
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)
    n = len(B)

    #  eliminación
    for k in range(n - 1):
        for i in range(k + 1, n):
            if A[k][k] == 0:
                raise ZeroDivisionError("División por cero.")
            factor = A[i][k] / A[k][k]
            A[i, k:] = A[i, k:] - factor * A[k, k:]
            B[i] = B[i] - factor * B[k]

    #  sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (B[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x

#GAUSS JORDAN
def gauss_jordan(A, B):
    
    n=len(A)
    M=[row[:]+[B_elem] for row, B_elem in zip (A,B)]
    for i in range (n):
    #pivote sea 1
     pivote=M[i][i]
    if pivote==0:
        raise ValueError ("DIVISION  POR CERO . EL SISTEMA NO PUEDE RESOLVERLO")
    M[i]=[elem / pivote for elem in M[i]]
    
    #hacer ceros en la columna del pivotee
    
    for j in range (n):
        if i !=j:
            factor = M[j][i]
            M[j]=[M[j][k]-factor * M[i][k] for k in  range (n+1)]
    return [fila[-1 ]for fila in [M]]
# CRAMER _


def cramer(A, B):
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("EL SISTEMA NO HAY SOLUCION ")
    
    n = len(B)
    x = []
    
    for i in range(n):
        Ai = np.copy(A)
        Ai[:, i] = B
        x.append(np.linalg.det(Ai) / det_A)
    
    return x

# descomposion LU
def lu_decomposicion (A,B):
    A=np.array(A, dtype=float)
    B=np.array(B,dtype=float)
    n=len(B)
    L=np.eye(n)
    U=A.copy()
    
    for i in range(n):
        for j in range (i+1, n):
            factor = U[j][i] / U[i][i]
            L[j][i]=factor
            U[j]-= factor *U[i]
            
        y=np.zeros(n)
    for i in range(n):
            y[i]= (y[i] - np.dot(L[i, :i], y[:i]))
            x=np.zeros(n)
            for i in range (n-1, -1, -1):
                x[i]= (y[i] - np.dot (U[i, i+1:], x[i+1:])) / U[i][i]
                return x
            
            # METODO JACOBI
def jacobi(A, B, tol=1e-10, max_iter=100):
    
    n=len(A)
    x=[0.0 ]* n
    for _ in range (max_iter):
        x_new = x.copy()
        
        for i in range (n):
            s=sum(A[i][j]* x[j] for j in range(n) if j !=1)
            x_new[i] = (B[i]-s) / A [i][i]
            if all (abs(x_new[i]-x[i]) <tol for i in range (n)):
                return x_new
            x= x_new
            return x
        
        #METODO  Gauss-Seidel
def Gauss_Seidel (A, B, tol=1e-10, max_iter=100):
  
    n = len(A)
    x = [0.0] * n

    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (B[i] - s1 - s2) / A[i][i]
        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            return x_new
        x = x_new

    return x
