import numpy as np
vector1=[]
vector2=[]
vector3=[]
incognita1=0
b1=[]
b2=[]
b3=[]
print("Sistema de ecuación del tipo \na1X+a2X+a3X = b1\na4X+a5X+a6X = b2\na7X+a8X+a9X = b3\n")
for i in range(3):
    for j in range(3):
        n=int(input("ingresa a"+str((i+1)*(j+1))+" del sistema"))
        if i==0:
            vector1.append(n)
        elif i==1:
            vector2.append(n)
        else:
            vector3.append(n)
    incognita1=float(input("Ingresa b"+str((i+1)*(j+1))+" del sistema"))
    if i==0:
        b1.append(incognita1)
    elif i==1:
        b2.append(incognita1)
    else:
        b3.append(incognita1)

# INGRESO

A = np.array([vector1,
              vector2,
              vector3])

B = np.array([b1,
              b2,
              b3])
# PROCEDIMIENTO
casicero = 1e-15 # Considerar como 0

# Evitar truncamiento en operaciones
A = np.array(A,dtype=float) 

# Matriz aumentada
AB = np.concatenate((A,B),axis=1)
AB0 = np.copy(AB)

# Pivoteo parcial por filas
tamano = np.shape(AB)
n = tamano[0]
m = tamano[1]

# Para cada fila en AB
for i in range(0,n-1,1):
    # columna desde diagonal i en adelante
    columna = abs(AB[i:,i])
    dondemax = np.argmax(columna)
    
    # dondemax no está en diagonal
    if (dondemax !=0):
        # intercambia filas
        temporal = np.copy(AB[i,:])
        AB[i,:] = AB[dondemax+i,:]
        AB[dondemax+i,:] = temporal
        
AB1 = np.copy(AB)

# eliminacion hacia adelante
for i in range(0,n-1,1):
    pivote = AB[i,i]
    adelante = i + 1
    for k in range(adelante,n,1):
        factor = AB[k,i]/pivote
        AB[k,:] = AB[k,:] - AB[i,:]*factor
AB2 = np.copy(AB)

# elimina hacia atras
ultfila = n-1
ultcolumna = m-1
for i in range(ultfila,0-1,-1):
    pivote = AB[i,i]
    atras = i-1 
    for k in range(atras,0-1,-1):
        factor = AB[k,i]/pivote
        AB[k,:] = AB[k,:] - AB[i,:]*factor
    # diagonal a unos
    AB[i,:] = AB[i,:]/AB[i,i]
X = np.copy(AB[:,ultcolumna])
X = np.transpose([X])


# SALIDA
print('Matriz aumentada:')
print(AB0)
print('solución de X: ')
print(X)