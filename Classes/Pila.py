class Pila:
    def __init__ (self):
        self.__datos__ = []
    def Desapilar (self):
        return self.__datos__.pop()   
    def Apilar (self , dicc: dict):
        self.__datos__.append (dicc)