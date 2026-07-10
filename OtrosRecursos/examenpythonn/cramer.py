import numpy as np
a=np.array([[1,2,4,8],[1,5,25,125],[1,7,49,343],[1,10,100,1000]])
b=np.array([-1,3,-1,-1]) # Nota La matriz a puede ser de cualquier dimension, aqui la ejemplificamos con una 3×3

d=np.linalg.det(a)

N=len(b); x=np.zeros(N)

for i in range(N):
    ai=a.copy();
    ai.T[i]=b
    di=np.linalg.det(ai)
    x[i]=di/d

def interpolacion(x,a):
    y=0
    for X in x:
        y=a[0]+a[1]*X+a[2]*X**2+a[3]*X**3
        print(y)
    #y=((y2-y1)/(x2-x1))*(x-x1)+y1


f=[2,5,7,10]
interpolacion(f,x)