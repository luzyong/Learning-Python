import componente

def promedio(objeto):
    suma=0
    for obj in objeto:
       suma+= len(obj.materiales)
    prom=suma/len(objeto)
    return prom
def descuento(objeto):
    discount=0
    if objeto>100:
        discount=objeto*0.10
    return round(discount,2)
materiales1=[]
materiales2=[]
materiales3=[]

tamaño1=int(input("ingresa el número de materiales para tu componente 1"))
tamaño2=int(input("ingresa el número de materiales para tu componente 2"))
tamaño3=int(input("ingresa el número de materiales para tu componente 3"))
nombre1=input("ingresa el nombre del componente 1")
nombre2=input("ingresa el nombre del componente 2")
nombre3=input("ingresa el nombre del componente 3")
precio1=input("ingresa el precio del componente 1")
precio2=input("ingresa el precio del componente 2")
precio3=input("ingresa el precio del componente 3")
for l in range(tamaño1):
    materiales1.append(input("ingresa el material {}".format(l+1)))

for l in range(tamaño2):
    materiales2.append(input("ingresa el material {}".format(l+1)))

for l in range(tamaño3):
    materiales3.append(input("ingresa el material {}".format(l+1)))

componente1=componente.Componente(nombre1,precio1,materiales1)
componente2=componente.Componente(nombre2,precio2,materiales2)
componente3=componente.Componente(nombre3,precio3,materiales3)
objetos=[componente1,componente2,componente3]
promedios=promedio(objetos)

for i in range(3):
    print("{}|{}|{}".format(objetos[i].nombre,objetos[i].precio,descuento(objetos[i].precio)))

print(promedios)