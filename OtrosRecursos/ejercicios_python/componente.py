class Componente:
    def __init__(self,name,price,materials):
        self.nombre=name
        self.precio=float(price)
        self.materiales=materials

    def agregaMaterial(self,material):
        self.materiales.append(material)