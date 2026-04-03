from Classes.NodeAVL import Node
from Classes.FlightSB import Flight
from graphviz import Digraph
from Classes.NodeAVL import Node
from collections import deque

class BinaryTree:

    def __init__(self):
        self.root = None

    def countLeaves(self):
        numberLeaves = self.__countLeaves(self.root)
        return numberLeaves

    def __countLeaves(self, node: Node):
        if node is None:
            return 0
        if node.getLeftSon() is None and node.getRightSon() is None:
            return 1
        return self.__countLeaves(node.getLeftSon())+ self.__countLeaves(node.getRightSon())

    def showRoot(self):
        if self.root:
            print(f"The code for the first Flight we have registered in our database is: {self.root.getFlightCode()}")
        else:
            print(f"We currently have no flights registered in our database.\nPlease try again later or enter a Flight")



    def widthTour(self):
        if self.root is None:
            return
        queue = deque([self.root])
        while queue:
            pop = queue.popleft()
            print(pop)
            if pop.getLeftSon():
                queue.append(pop.getLeftSon())
            if pop.getRightSon():
                queue.append(pop.getRightSon())

    def preorderTour(self):
        self.__preorderTour(self.root)

    def __preorderTour(self, node):
        if node is None:
            return
        print(node.getFlightCode())
        self.__preorderTour(node.getLeftSon())
        self.__preorderTour(node.getRightSon())

    def inOrderTour(self):
        self.__inOrderTour(self.root)

    def __inOrderTour(self, node):
        if node is None:
            return
        self.__inOrderTour(node.getLeftSon())
        print(node.getFlightCode())
        self.__inOrderTour(node.getRightSon())

    def postOrderTour(self):
        self.__postOrderTour(self.root)

    def __postOrderTour(self, node):
        if node is None:
            return
        self.__postOrderTour(node.getLeftSon())
        self.__postOrderTour(node.getRightSon())
        print(node.getFlightCode())

    def searchNode(self, code):
        nodeFound = self.__searchNode(self.root, code)
        return nodeFound

    def __searchNode(self, node : Node, code):
        if node is None:
            return None
        if code < (node.getFlightCode()):
            return self.__searchNode(node.getLeftSon(), code)
        elif code > node.getFlightCode():
            return self.__searchNode(node.getRightSon(), code)
        else:
            return node
        
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
    
    def getHeight(self, current_root: Node):
        if current_root:
            izq = self.getHeight(current_root.getLeftSon())
            der = self.getHeight(current_root.getRightSon())
            return max(izq, der) + 1
        return 0
    
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
            self.insertNode (Flight (codigo , origen , destino , horaSalida , precioBase , pasajeros , prioridad , promocion , alerta))

class BST(BinaryTree):
    def __init__(self):
        super().__init__()
    def insertNode(self, value: Flight):
        self.root = self.__insertNode(self.root, value)

    def __insertNode(self, node : Node, value: Flight):
        if node is None:
            node = Node(value)
            return node
        if value.getCode() < node.getFlightCode():
            node.setLeftSon(self.__insertNode(node.getLeftSon(), value))
        elif value.getCode() > node.getFlightCode():
            node.setRightSon(self.__insertNode(node.getRightSon(), value))
        else:
            raise Exception(f"This Node already exists in our AVL. Thanks for your attention")
        return node