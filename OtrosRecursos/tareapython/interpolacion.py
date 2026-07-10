x=int(input("Ingresa el punto a interpolar"))
y1=2
y2=10
x1=4
x2=8
y=((y2-y1)/(x2-x1))*(x-x1)+y1
print("El valor de y es:{}".format(y))