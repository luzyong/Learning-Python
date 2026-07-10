import math
#lee un solo archivo, recorre toda la tabla en búsqueda del archivo, si no existe, arroja un error
def ReadPage(id):
    for i in range(int(page)):
        if(tablapagina[i][1]==id):
            print(tablapagina[i][1])
        else:
            print('El archivo que intenta leer no existe')
    
#lee toda la tabla    
def ReadPages():
    print(tablapagina[:])
#escribe en la tabla
def WritePage(id, buffer):
    global fallo
    #si la pagina tiene espacios vacíos, escribe
    if(tablapagina[buffer][1]==None):
        tablapagina[buffer][1]=id
        fallo+=1
    else:
        #si la páginaya tiene ese valor almacenado, no hace nada
        if(tablapagina[buffer][1]==id):
            None
        else:
        #si la página no tiene ese valor, sobreescribe
            tablapagina[buffer][1]=id
            fallo+=1

def DeletePage(id):
    #recorre toda la tabla y busca todas las ubicaciones del archivo para eliminarlo
    for i in range(int(framesize)):
        if(tablapagina[i][1]==id):
            tablapagina[i][1]=None
#funcion principal
def inicio():
        global n
        parte = 0
        #n para poder comprobar el FIFO
        while n<8:
            archivo=input("nombre del archivo")
            tamaño=input("tamaño del archivo")           
            #para archivos de tamaño menor o igual al tamaño de página
            if int(tamaño)<=int(page):
                for i in range (int(framesize)):
                    if(tablapagina[i][1]==None):
                        ind=i
                        break;
                WritePage(archivo,ind)
            #para archivos de tamaño mayor al tamaño de la página        
            elif int(tamaño)>int(page):
                #para saber cuántos marcos tendrá la tabla
                m=int(tamaño)/int(page)
                marcos=math.ceil(m)
                for i in range (marcos):
                    for i in range(int(framesize)):
                        if(tablapagina[i][1]==None):
                            ind=i
                            break;
                    
                    parte+=marcos
                    if(parte==int(page)):
                        WritePage(archivo,ind)
                    else:
                        WritePage(archivo,ind)
                    
                    

            ReadPages()
            
            
            n+=1     
            
#creación de la tabla de paginación                
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
    #Elección de la acción
    while respuesta!='SALIR':
        respuesta=input('¿Qué deseas hacer: Eliminar, Escribir, Salir')
        if(respuesta.upper()=='ELIMINAR'):
            eliminar=input('Nombre del archivo a eliminar')
            DeletePage(eliminar) 
            ReadPage(eliminar)
            ReadPages()
        else:
            n=0
            inicio()
else:
    print("error, sobrepasa la memoria")    
#print(pagina[:20])