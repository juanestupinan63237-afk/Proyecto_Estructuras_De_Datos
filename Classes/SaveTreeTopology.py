from Classes.NodeAVL import Node
from Classes.BSTTree import BST

class SavetreeTopology: 

    def __init__ (self , arbol: BST):
        self.arbol = arbol

    def _nodo_a_dicc (self , nodo: Node):
        if nodo is None:
            return None
        return {
            "codigo": nodo.flight.code,
            "origen" : nodo.flight.getOrigin (),
            "destino" : nodo.flight.getDestination(),
            "horaSalida" : nodo.flight.getDepartureTime(),
            "precioBase" : nodo.flight.getBasePrice(),
            "pasajeros" : nodo.flight.getNumberPassengers(),
            "promocion" : nodo.flight.getPromotion(),
            "alerta" : nodo.flight.getAlert(),
            "izquierdo": self._nodo_a_dicc(nodo.leftSon),
            "derecho": self._nodo_a_dicc(nodo.rightSon)
        }

    def SaveTree(self):
        return self._nodo_a_dicc(self.arbol.root)