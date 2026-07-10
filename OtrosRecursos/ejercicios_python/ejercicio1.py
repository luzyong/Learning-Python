def promedio(lista):
    suma=0
    for num in lista:
        suma+=num
    promedio=suma/len(lista)
    return round(promedio,3)
n=0
tamaño=int(input("Ingresa el tamaño de tu lista:"))
lista=[]
negativo=[]
positivo=[]
while n<tamaño:
    try:
        elemento=float(input("ingresa un elemento numérico"))
    except ValueError:
        print("Ingresa un valor numérico entero, inténtalo de nuevo")
    else:
        lista.append(elemento)
        n+=1
for e in lista:
    if e<0:
        negativo.append(e)
    elif e>=0:
        positivo.append(e)

promedio_negativo=promedio(negativo)
promedio_positivo=promedio(positivo)

for i in range(2):
    if i==0:
        print("{}|{}|{}".format(i+1,positivo,promedio_positivo))
    if i ==1:
        print("{}|{}|{}".format(i+1,negativo,promedio_negativo))