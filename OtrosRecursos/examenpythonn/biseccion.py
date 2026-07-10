from math import sin,cos,tan,asin,acos,atan,sqrt,log,exp
from math import sinh,cosh,tanh,asinh,acosh,atanh
print('Metodo de Bisseccion\n')
ec=input('De la funcion a resolver: ')  
x1=float(input('de el extremo inferior del intervalo aproximado: '))
x2=float(input('de el extremo superior del intervalo aproximado: '))
errordeseado=float(input('De el error deseado: '))
 

def f(x):
    return eval(ec)

 
while True:
    xmed=(x1+x2)/2
    fxmed=f(xmed)
    if fxmed==0.0:
        break
 
    if (f(x1)*f(xmed))<0:
        x1=x1
        x2=xmed
    else:
        x1=xmed
        x2=x2
    error=abs(x2-x1)
    if error<errordeseado:
        break
    print(f'a{x1} b{x2} f(a){f(x1)} xr{xmed} f(xr){f(xmed)}')
 

print ('La raíz es',xmed)
input(' ')