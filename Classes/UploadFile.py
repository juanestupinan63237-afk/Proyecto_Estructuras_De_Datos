from Classes.NodeAVL import Node
from Classes.FlightSB import Flight
from Classes.AVL import AVLTree

class UploadFile:
    def __init__ (self , tree: AVLTree , dicc: dict):
        self.tree = tree
        self.dicc = dicc

    def _dicc_a_nodo(self, dicc: dict):
        if dicc is None:
            return None

        nodo = Node(Flight(int(dicc["codigo"]) , 
                           dicc["origen"] , 
                           dicc["destino"] , 
                           dicc ["horaSalida"] , 
                           dicc["precioBase"] , 
                           dicc["pasajeros"] ,
                           promotion=bool(dicc["promocion"]),
                           alert= bool(dicc["alerta"]),
                           priority= False))

        nodo.setLeftSon(self._dicc_a_nodo(dicc["izquierdo"]))
        nodo.setRightSon(self._dicc_a_nodo(dicc["derecho"]))
        return nodo

    def cargar_desde_dicc(self):
        self.tree.root = self._dicc_a_nodo(self.dicc)