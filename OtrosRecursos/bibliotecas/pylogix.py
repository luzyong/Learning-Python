from pylogix import PLC
with PLC() as comm:
    comm.IPAddress = '192.168.1.9'
    ret = comm.Read('MyTagName') #original con un solo tag
    print(ret.TagName, ret.Value, ret.Status)
    #Leyendo varios tags desde una lista
    lista = ['Tag1','Tag2','Tag3']
    for i in range(0,2):
        ret = comm.Read(lista[i])
        print(ret.TagName, ret.Value, ret.Status)

