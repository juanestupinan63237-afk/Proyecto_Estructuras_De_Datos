class Nodo:

    def __init__ (self , valor):
        self.valor = valor
        self.izq = None
        self.der = None

    def ExisteIzq (self):
        return (self.izq) is not None
    def ExisteDer (self):
        return (self.der) is not None

class Arbol:

    def __init__(self):
        self.raiz = None

    def InsertarNodo (self , valor):
        if self.raiz is None:
            self.raiz = Nodo (valor)
        else:
            self.__Insertar (valor , self.raiz)
    def __Insertar (self , valor , nodo_actual : Nodo):
        if valor < nodo_actual.valor:
            if nodo_actual.ExisteIzq ():
                self.__Insertar (valor , nodo_actual.izq)
            else:
                nodo_actual.izq = Nodo (valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.ExisteDer ():
                self.__Insertar (valor , nodo_actual.der)
            else:
                nodo_actual.der = Nodo (valor)
        else: 
            raise Exception ("Ya existe el valor ingresado...")
    def RecorridoPreOrden (self , nodo_actual: Nodo ,resultado: list):
        if nodo_actual is not None:
            resultado.append (nodo_actual.valor)
            self.RecorridoPreOrden (nodo_actual.izq , resultado)
            self.RecorridoPreOrden (nodo_actual.der , resultado)
        return resultado
    def IniciarRecorrido (self):
        return self.RecorridoPreOrden (self.raiz , [])
        
arbol = Arbol ()
for i in range (0 , 20):
    arbol.InsertarNodo (i)

print (arbol.IniciarRecorrido())

arbol.InsertarNodo (5)

