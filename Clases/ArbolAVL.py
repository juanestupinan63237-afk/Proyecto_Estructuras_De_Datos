from Clases.NodoAVL import Nodo

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self.__insertar(self.raiz, valor)

    def __insertar(self, nodo, valor):
        if nodo is None:
            nodo = Nodo(valor)
            return nodo

        if nodo.valor < valor:
            nodo.hijoIzquierdo = self.__insertar(nodo.hijoIzquierdo, valor)
        elif nodo.valor > valor:
            nodo.hijoDerecho = self.__insertar(nodo.hijoDerecho, valor)
        else:
            return nodo
        return nodo