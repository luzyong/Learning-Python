numeros=[]
def leer(ruta):
    archivo = open(ruta,encoding='utf-8')
    for linea in archivo:
        numeros.append(float(linea.strip()))
    archivo.close()
def suma():
    suma=0
    for num in numeros:
        if num>=0:
            suma+=num
    return round(suma,2)
