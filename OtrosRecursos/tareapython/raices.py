#Para el ejercicio de la función x^3+4x^2-10
def function(x):
    funcion  = x**3 + 4*(x**2) - 10
    return funcion
def der(x):
    derivada = 3*(x**2) + 8*x
    return derivada
x0 = 2 #Aquí puede haber un input en vez de un 2
tolerancia = 0.001
tabla = []
diferencia = abs(2*tolerancia)
xi = x0
#Mientras la diferencia entre el valor nuevo y el valor anterior sea mayor que la tolerancia, se sigue iterando xi+1=xi-f(X)/df(x)
while (diferencia>=tolerancia):
    xnuevo = xi - function(xi)/der(xi)
    diferencia  = abs(xnuevo-xi)
    tabla.append([xi,xnuevo,diferencia])
    xi = xnuevo



print("xanterior   xnuevo  diferencia")
for elemento in tabla:
    print(elemento)
print('raiz en: ', xi)
print('con error de: ',diferencia)