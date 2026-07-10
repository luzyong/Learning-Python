import base64
import os

from cryptography.fernet import Fernet


def menu():#Creamos una funcion para mostrar las opciones del menu
    print("1. Ingrese y salve alumno")
    print("2. Modifique alumno")
    print("3. Elimine alumno")
    print("4. Lea alumnos almacenados")
    print("5. Seleccione un archivo y lea la información")
    print("6. Salir")
    opc = input("Digita una opcion: ")
    print()
    return opc #Retornamos la opcion que el usuario elija

def ingresar(ubicacion, key): #Creamos una funcion para crear el archivo y guardar los datos
    nombre = input("Ingrese nombre: ")
    apellido = input("Ingrese apellido: ")
    nacimiento = input("Ingrese fecha de nacimiento: ")
    materias = input("Ingrese las materias separadas por coma(,): ")


    nombreArchivo = nombre + "_" + apellido + ".txt" #Definimos el nombre el archivo con su extension .txt y almacenamos en la variable nombreArchivo
    try: #Creamos la excepcion en caso de que el directorio no exista
        crearAlumn = open(ubicacion+nombreArchivo, "w") #Para crear el archivo externo con (w)
        #Agregamos los datos del alumno al archivo
        crearAlumn.write("Nombre: " + nombre + "\n")
        crearAlumn.write("Apellido: " + apellido + "\n")
        crearAlumn.write("Nacimiento: " + nacimiento + "\n")
        crearAlumn.write("Materias: " + materias)
        crearAlumn.close() #Cerramos el archivo
        cifrar(key, ubicacion+nombreArchivo)

    except:
        #En caso de que el directorio este malo caera aqui
        print("El directorio no existe")


def modificar(ubicacion, key): #Para modificar la informacion del archivo
    try:
        contenido = os.listdir(ubicacion)#Listamos los archivos que esten en ese directorio y se guardaran en una matriz

        if len(contenido) > 0:
            #En caso de que la longitud de la lista sea mayor que cero entra aqui
            eliminar(ubicacion)#Eliminamos el archivo que vamos a actualizar
            ingresar(ubicacion, key)#Y pedimos los datos nuevamente
            print("Se actualizo el estudiante exitosamente\n")
        else:
            print("No se ha registrado nigun alumno")#En caso de que el directorio este vacia entra aqui
        print()#Damos un salto de lina
    except:
        # En caso de que el diretorio este malo entra aqui
        print("El diretorio no existee")

def mostrar(ubicacion): #Mostramos todos los archivos de los alumnos que se a creado en dicha ubicacion
    try:
        #Manejamos la excepcion en caso de que halla error
        contenido = os.listdir(ubicacion)#Listados los nombres de los archivos en una lista
        if len(contenido) > 0:
            #En caso de que la longitud sea mayor que 0 caera aqui
           contenido.sort(reverse = True) #Ordenamos la lista con los nombres de los directorios en forma descendiente
           print("Archivos")
           for i in contenido:
               #Mostramos todos los archivos que existan en esta direccion
               print(i)
           print()
        else:
            #En caso de que no exista ningun archivo llega aqui
            print("No se ha registrado nigun alumno")
    except:
        #En caso de que halla un error en el try caera aqui
        print("El diretorio no existe")


def eliminar(ubicacion):
    try:
        #Manejamos la excepcion en caso de que halla error
        contenido = os.listdir(ubicacion) #Listamos los directorios en una lista
        if len(contenido) > 0:

            # Si la longitud de la lista es mayor que 0(Que haya un archivo o mas)
            print("Alumnos")
            for i in range(len(contenido)):
                #Mostramos todos los archivos desde 0 hasta la longitud
                print(i, ". ", contenido[i][:-4]) #[:-4] para quitar la exension(.txt)

            alumno = int(input("Digita un alumno: "))#Pedimos un alumno desde 0 hasta la longitud de la lista

            while alumno < 0 or alumno >= len(contenido):
                #Entrara aqui en caso de que el usuario elija una opcion fuera de rango y repectira infinitamente hasta que ingrese una opcion correcta
                print("Opcion incorrecta")
                for i in range(len(contenido)):
                    print(i, ". ", contenido[i][:-4])
                alumno = int(input("Digita un alumno: "))

            os.remove(ubicacion + contenido[alumno]) #Finalmente eliminamos el archivo del directorio
            print("Se elimino correctamente\n")
        else:
            #Entra aqui en caso de que no exista ningun archivo en el directorio
            print("No se ha registrado nigun alumno")
    except:
        #Entra aqui en caso de que de error en el try
        print("El diretorio no existe")
def cifrar(key, alumno):

    fernet = Fernet(key)
    with open(alumno, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)
    with open(alumno, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def desencriptar(key, ubicacion):
    try:
        contenido = os.listdir(ubicacion)  # Listamos los directorios en una lista
        if len(contenido) > 0:
            print("Alumnos")
            for i in range(len(contenido)):
                # Mostramos todos los archivos desde 0 hasta la longitud
                print(i, ". ", contenido[i][:-4])  # [:-4] para quitar la exension(.txt)

            alumno = int(input("Digita un alumno: "))  # Pedimos un alumno desde 0 hasta la longitud de la lista

            while alumno < 0 or alumno >= len(contenido):
                # Entrara aqui en caso de que el usuario elija una opcion fuera de rango y repectira infinitamente hasta que ingrese una opcion correcta
                print("Opcion incorrecta")
                for i in range(len(contenido)):
                    print(i, ". ", contenido[i][:-4])
                alumno = int(input("Digita un alumno: "))
            fernet = Fernet(key)

            with open(ubicacion+contenido[alumno], "rb") as enc_file:
                encrypted = enc_file.read()

            decrypted = fernet.decrypt(encrypted)

            with open(contenido[alumno], 'wb') as dec_file:
                dec_file.write(decrypted)

            decrypted = decrypted.decode()
            print("\nDatos:\n" + decrypted, "\n")
        else:
            print("Directorio vacio")
    except:
        print("El diretorio no existe")


def principal():
    key = "UltimaPractica"
    for i in range(32 - len(key)):
        key += " "#La complemento con espacios, por que solo acepta 32 bytes en base 64
    key = base64.b64encode(bytes(key, "UTF-8"))

    #Esta es la primer funcion que se ejecutara y se encargara de llamar cada opcion, segun elija el usuario
    ubicacion = "D:/IntroduccionARedes/Alumnos/"#Direccion donde se guardaran los archivos
    while True:
        #Ciclo infinito. El usuario elige cuando quiera salir (opcion 5)
        opc = menu()
        if opc == "1":
            ingresar(ubicacion, key)
        elif opc == "2":
            modificar(ubicacion, key)
        elif opc == "3":
            eliminar(ubicacion)
        elif opc == "4":
            mostrar(ubicacion)
        elif opc == "5":
            desencriptar(key, ubicacion)
        elif opc == "6":
            break

        else:
            #Entra aqui en caso de que el usuaro elija una opcion que no esta en el menu
            print("Opcion incorrecta, intentelo de nuevo")


principal()#Aqui empieza el programa