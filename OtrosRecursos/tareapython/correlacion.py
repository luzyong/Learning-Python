def covar(x,y,N):
    suma=0
    for elementoX,elementoY in zip(x,y):
        suma+=(elementoX)*(elementoY)
    return suma/N
def sumatoria(x,y,xmed,ymed):
    suma=0
    for elementoX,elementoY in zip(x,y):
        suma+=(elementoX-xmed)*(elementoY-ymed)
    return suma
def desv(lista,media,N):
    suma=0
    for elemento in lista:
        suma+=pow(elemento,2)
    med=pow(media,2)
    a=suma/N
    return pow(a-med,0.5)
def prom(x,N):
    suma=0
    for elemento in x:
        suma+=elemento
    return suma/N
x=[]
y=[]

observaciones=int(input("Introduzca el número de observaciones a realizar "))
for i in range(observaciones):
    xin=int(input("Ingrese el valor "+str(i+1)+" de x "))
    x.append(xin)
    yin=int(input("Ingrese el valor "+str(i+1)+" de y "))
    y.append(yin)

ymed = prom(y,observaciones)
xmed= prom(x,observaciones)
covarianza=covar(x,y,observaciones)
desviacionX=desv(x,xmed,observaciones)
desviacionY=desv(y,ymed,observaciones)
desviacion=desviacionX*desviacionY
correlacion=(covarianza-(xmed*ymed))/desviacion
print("La correlación entre tus variables es: {}".format(correlacion))
