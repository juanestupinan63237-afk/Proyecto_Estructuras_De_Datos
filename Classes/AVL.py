from Classes.NodeAVL import Node
from Classes.FlightSB import Flight
from graphviz import Digraph

class AVLTree:
    def __init__(self):
        self.root = None
        self.balanceo_activado = True

    def SwitchModoEstres (self):
        self.balanceo_activado = not self.balanceo_activado
        if self.balanceo_activado:
            self.BalanceAll ()

    def BalanceAll (self):
        self.root = self.__RecursiveBalance__ (self.root)

    def __RecursiveBalance__ (self , node: Node):
        if node is None:
            return None
        node.setLeftSon(self.__RecursiveBalance__(node.getLeftSon()))
        node.setRightSon(self.__RecursiveBalance__(node.getRightSon()))
        node.setHeight(1 + max(self.getHeight(node.getLeftSon()), 
                            self.getHeight(node.getRightSon())))
        return self.__BalanceNode__(node)

    def ResetTree (self):
        self.root = None

    def insertNodeAVL(self, value: Flight):
        self.root = self.__insertNodeAVL(self.root, value)

    def __insertNodeAVL(self, node: Node, value: Flight):
        if node is None:
            return Node(value)

        if value.getCode() < node.getFlightCode():
            node.setLeftSon(self.__insertNodeAVL(node.getLeftSon(), value))
        elif value.getCode() > node.getFlightCode():
            node.setRightSon(self.__insertNodeAVL(node.getRightSon(), value))
        else:
            raise Exception("This Node already exists in our AVL Tree...")

        node.setHeight(1 + max(self.getHeight(node.getLeftSon()), self.getHeight(node.getRightSon())))

        if self.balanceo_activado:
            return self.__BalanceNode__ (node)
        return node
    
    def __BalanceNode__ (self , node: Node):
            balance = self.getBalance(node)
            if balance > 1 and self.getBalance(node.getLeftSon()) >= 0:
                return self.rightRotate(node)
            if balance < -1 and self.getBalance(node.getRightSon()) <= 0:
                return self.leftRotate(node)
            if balance > 1 and self.getBalance(node.getLeftSon()) < 0:
                node.setLeftSon(self.leftRotate(node.getLeftSon()))
                return self.rightRotate(node)
            if balance < -1 and self.getBalance(node.getRightSon()) > 0:
                node.setRightSon(self.rightRotate(node.getRightSon()))
                return self.leftRotate(node)
            return node


    def getHeight(self, node):
        if node is None:
            return 0
        return node.getHeight()

    def searchNode(self, code):
        return self.__searchNode(self.root, code)

    def __searchNode(self, node, code):
        if node is None:
            return None
        if code < (node.getFlightCode()):
            return self.__searchNode(node.getLeftSon(), code)
        elif code > node.getFlightCode():
            return self.__searchNode(node.getRightSon(), code)
        else:
            return node

    def deleteNode(self, codeFlight):
        node = self.searchNode(codeFlight)

        if node is None:
            print(f"This node hasn't been found, therefore, it hasn't been deleted correctly since it doesn't exist")
            return
        self.root = self.__deleteNode(self.root, codeFlight)

    def __deleteNode(self, node : Node, code):
        if node is None:
            return node

        if code < node.getFlightCode():
            node.setLeftSon(self.__deleteNode(node.getLeftSon(), code))

        elif code > node.getFlightCode():
            node.setRightSon(self.__deleteNode(node.getRightSon(), code))

        else:
            if node.getLeftSon() is None and node.getRightSon() is None:
                return None

            elif node.getRightSon() is None:
                return node.getLeftSon()

            elif node.getLeftSon() is None:
                return node.getRightSon()

            else:
                successor = self.__minValueNode(node.getRightSon())
                node.setFlight(successor.getFlight())
                node.setRightSon(
                    self.__deleteNode(
                        node.getRightSon(),
                        successor.getFlight().getCode()
                    )
                )
        node.setHeight(1 + max(
            self.getHeight(node.getLeftSon()),
            self.getHeight(node.getRightSon())
        ))
        balance = self.getBalance(node)

        if balance > 1 and self.getBalance(node.getLeftSon()) >= 0:
            return self.rightRotate(node)

        if balance > 1 and self.getBalance(node.getLeftSon()) < 0:
            node.setLeftSon(self.leftRotate(node.getLeftSon()))
            return self.rightRotate(node)

        if balance < -1 and self.getBalance(node.getRightSon()) <= 0:
            return self.leftRotate(node)

        if balance < -1 and self.getBalance(node.getRightSon()) > 0:
            node.setRightSon(self.rightRotate(node.getRightSon()))
            return self.leftRotate(node)

        return node

    def __minValueNode(self, node : Node):
        temporal = node
        while temporal.getLeftSon() is not None:
            temporal = temporal.getLeftSon()
        return temporal

    def getBalance(self, node : Node):
        if node is None:
            return 0
        return (self.getHeight(node.getLeftSon()) - self.getHeight(node.getRightSon()))

    def rightRotate(self, node : Node):
        temporal1 = node.getLeftSon()
        temporal2 = temporal1.getRightSon()

        temporal1.setRightSon(node)
        node.setLeftSon(temporal2)
        node.setHeight(1 + max(
            self.getHeight(node.getLeftSon()),
            self.getHeight(node.getRightSon())
        ))

        temporal1.setHeight(1 + max(
            self.getHeight(temporal1.getLeftSon()),
            self.getHeight(temporal1.getRightSon())
        ))
        return temporal1

    def leftRotate(self, node : Node):
        temporal1 = node.getRightSon()
        temporal2 = temporal1.getLeftSon()

        temporal1.setLeftSon(node)
        node.setRightSon(temporal2)

        node.setHeight(1 + max(
            self.getHeight(node.getLeftSon()),
            self.getHeight(node.getRightSon())
        ))

        temporal1.setHeight(1 + max(
            self.getHeight(temporal1.getLeftSon()),
            self.getHeight(temporal1.getRightSon())
        ))

        return temporal1

    def FindNodeLessProfitable (self):
        FLIGTH: Node = self.root
        def Find (temp_root: Node):
            nonlocal FLIGTH
            if temp_root is not None:
                if temp_root.flight.getTotalPrice () < FLIGTH.flight.getTotalPrice():
                    FLIGTH = temp_root
            Find (temp_root.getLeftSon())
            Find (temp_root.getRightSon())
        Find (self.root)
        return FLIGTH

    def _nodo_a_dicc (self , nodo: Node):
        if nodo is None:
            return None
        return {
            "codigo": nodo.flight.getCode(),
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
        data = {
            "tipo" : "Topology",
            "arbol" : self._nodo_a_dicc (self.root)
        }
        return data
    
    def Render (self):
        dot = Digraph()
        dot.attr('graph', bgcolor='transparent', ranksep='0.6', nodesep='0.4')
        dot.attr('node',
                shape='circle',     
                style='filled',     
                fillcolor='#1b212c',
                color='#00f2ff',    
                fontcolor='#00f2ff',
                fontname='Arial Bold',
                fontsize='12',
                penwidth='2',     
                width='0.6',        
                height='0.6')
        dot.attr('edge', color='#444d5e', penwidth='1.5', arrowhead='vee', arrowsize='0.8')

        def AddNode(n):
            if n:
                node_id = str(id(n))
                label_text = str(n.getFlightCode())
                dot.node(node_id, label=label_text)
                if n.getLeftSon():
                    dot.edge(node_id, str(id(n.getLeftSon())))
                    AddNode(n.getLeftSon())
                if n.getRightSon():
                    dot.edge(node_id, str(id(n.getRightSon())))
                    AddNode(n.getRightSon())

        if self.root:
            AddNode(self.root)
        svg = dot.pipe(format='svg').decode("utf-8")
        return svg.replace('<svg ', '<svg width="100%" height="auto" ')
    
    def _dicc_a_nodo_topology(self, dicc: dict):
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

        nodo.setLeftSon(self._dicc_a_nodo_topology(dicc["izquierdo"]))
        nodo.setRightSon(self._dicc_a_nodo_topology(dicc["derecho"]))
        nodo.setHeight(1 + max(self.getHeight(nodo.getLeftSon()), 
                           self.getHeight(nodo.getRightSon())))
        return nodo

    def cargar_desde_dicc(self , dicc):
        self.root = None
        if dicc["tipo"] == "Topology":
            self.root = self._dicc_a_nodo_topology(dicc["arbol"])
            self.BalanceAll ()
        elif dicc["tipo"] == "INSERCION":
            nodos = dicc["vuelos"]
            self.cargar_desde_dicc_inserccion (nodos)

    def cargar_desde_dicc_inserccion (self ,vuelos: list ):
        for i in vuelos:
            codigo = int(i["codigo"])
            origen = i["origen"]
            destino = i["destino"]
            horaSalida = i ["horaSalida"]
            precioBase = int(i["precioBase"])
            pasajeros = int(i["pasajeros"])
            prioridad = int(i["prioridad"])
            promocion = i["promocion"]
            alerta = i["alerta"]
            self.insertNodeAVL (Flight (codigo , origen , destino , horaSalida , precioBase , pasajeros , prioridad , promocion , alerta))

    def tourPreOrden (self):
        resultado = []
        self.__tourPreOrden (self.root , resultado)
        return resultado
    
    def __tourPreOrden (self , current_root: Node , resultado: list):
        if current_root:
            resultado.append (current_root.getFlight())
            self.__tourPreOrden (current_root.getLeftSon())
            self.__tourPreOrden (current_root.getRightSon())