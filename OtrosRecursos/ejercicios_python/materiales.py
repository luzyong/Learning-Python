import max
archivo = open("./materials.txt",encoding='utf-8')
diccionario ={}
for linea in archivo:
    materiales=linea.split(', ')
    diccionario[materiales[0]]=float(materiales[1].strip())

maximo=max.maximo(diccionario)

for key,value in diccionario.items():
    if key==maximo:
        print("{}|{}|MAX".format(key,value))
    else:
        print("{}|{}".format(key,value))
    