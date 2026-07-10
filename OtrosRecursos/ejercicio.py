from sympy import *
from sympy.parsing.sympy_parser import parse_expr # Leer función introducida
from sympy.plotting import plot

def derivada():
    try:
        x = symbols('x') #Declarar variable independiente
        funcion = input()#función por teclado: producto(*), exponente(**)
        fx = parse_expr(funcion)#convierte la entrada en un formato legible para sympy
        derivada = diff(fx,x)#Derivada de la función, en función de x
        plot(derivada,(x,-15,10))
        return derivada
    except:
        print("Introduce la función correctamente")
        
        
def integral():
    try:
        x = symbols('x') #Declarar variable independiente
        funcion = input()
        fx = parse_expr(funcion)
        integral = integrate(fx,x)
        plot(integral,(x,-15,10))
        return integral
    except:
        print("Introduce la función correctamente")

seleccion=""

while seleccion!="3":    
    seleccion=input("Elige una opción:\n1.-Integrar una función\n2.-Derivar una función\n3.-Salir")
    if seleccion=='1':
        print(integral())
    if seleccion=='2':
        print(derivada())
    if seleccion=='3':
        print("\nAdios")