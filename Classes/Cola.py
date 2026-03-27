from collections import deque
class Cola:
    def __init__(self):
        self.__datos__ = []
    def Encolar (self, datos):
        self.__datos__.append(datos)
    def Desencolar (self):
        if self.isEmpty():
            return "Esta vacío"
        return self.__datos__.pop(0)
    def isEmpty(self):
        return len(self.__datos__) == 0
    