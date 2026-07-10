import math
def ReadPage(id):
    for i in range(int(page)):
        if(tablapagina[i][1]==id):
            print(tablapagina[i][1])
        else:
            print('El archivo que intenta leer no existe')
    
def ReadPages():
    print(tablapagina[:])

def WritePage(id, buffer):
    vacia=True
    contador=int(framesize)
    indice=0
    parte=0
    for i in range (int(framesize)):
        if(tablapagina[i][1]==None):
            contador-=1
    if contador==0:
        vacia=False

    if int(buffer)<=int(page):
        if vacia:
            for i in range (int(framesize)):
                if(tablapagina[i][1]==None):
                    ind=i
                    break
            tablapagina[ind][1]=id
        elif indice<int(framesize):
            if tablapagina[indice][1]==id:
                None
            else:
                tablapagina[indice][1]==id
            indice+=1
        else:
            indice=0            

    elif int(buffer)>int(page):
        m=int(buffer)/int(page)
        marcos=math.ceil(m)
        for i in range (marcos):
            if vacia:
                for i in range (int(framesize)):
                    if(tablapagina[i][1]==None):
                        ind=i
                        break
                parte+=marcos
                if(parte==int(page)):
                    tablapagina[ind][1]=id
                else:
                    tablapagina[ind][1]=id
                
            elif indice<int(framesize):
                if tablapagina[indice][1]==id:
                    None
                else:
                    parte+=marcos
                    if(parte==int(page)):
                        tablapagina[ind][1]=id
                    else:
                        tablapagina[ind][1]=id
                indice+=1
            else:
                indice=0
            

def DeletePage(id):
    for i in range(int(framesize)):
        if(tablapagina[i][1]==id):
            tablapagina[i][1]=None

def inicio():
        global n
        parte = 0
        while n<8:
            archivo=input("nombre del archivo")
            tamaño=input("tamaño del archivo")           
            WritePage(archivo,tamaño)
            
                    
                    

            ReadPages()
            
            
            n+=1     
            
                
n=0
fallo = 0
respuesta=0
memory=1048576
page = input('tamaño de pagina:')
framesize = memory/int(page)
if int(page)<memory:
    tablapagina=[[None] * 2 for i in range(int(framesize))]
    for i in range(int(framesize)):
        tablapagina[i][0]=i

while respuesta!='SALIR':
    respuesta=input('¿Qué deseas hacer: Eliminar, Escribir, Salir')
    if(respuesta.upper()=='ELIMINAR'):
        eliminar=input('Nombre del archivo a eliminar')
        DeletePage(eliminar) 
        ReadPages()
    else:
        n=0
        inicio()
    
#print(pagina[:20])