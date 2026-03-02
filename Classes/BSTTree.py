from Classes.NodeAVL import Node
from Classes.FlightSB import Flight
from graphviz import Digraph

class BST:
    def __init__(self):
        self.root = None

    def insertNode(self, value: Flight):
        self.root = self.__insertNode(self.root, value)

    def __insertNode(self, node : Node, value: Flight):
        if node is None:
            node = Node(value)
            return node

        if value.getCode() < node.getFlightCode():
            node.leftSon = self.__insertNode(node.getLeftSon(), value)
        elif value.getCode() > node.getFlightCode():
            node.rightSon = self.__insertNode(node.getRightSon(), value)
        else:
            raise Exception(f"This Node already exists in our AVL. Thanks for your attention")
        return node

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

    def __searchNode(self, node, code):
        if node is None:
            return False
        if code < (node.getFlightCode()):
            return self.__searchNode(node.getLeftSon(), code)
        elif code > node.getFlightCode():
            return self.__searchNode(node.getRightSon(), code)
        else:
            return True

    def RenderTree(self):
        dot = Digraph()
        # Fondo transparente para integrarse con el CSS
        dot.attr('graph', bgcolor='transparent', ranksep='0.6', nodesep='0.4')
        # CONFIGURACIÓN DEL CÍRCULO NEÓN
        dot.attr('node',
                shape='circle',     # ¡Mantenemos los círculos!
                style='filled',     # Rellenos
                fillcolor='#1b212c',# Fondo oscuro interno del círculo
                color='#00f2ff',    # Borde Cian Neón
                fontcolor='#00f2ff',# Texto Cian Neón
                fontname='Arial Bold',
                fontsize='12',
                penwidth='2',       # Borde más grueso para efecto neón
                width='0.6',        # Tamaño uniforme
                height='0.6')

        # Flechas estilizadas
        dot.attr('edge', color='#444d5e', penwidth='1.5', arrowhead='vee', arrowsize='0.8')

        def AddNode(n):
            if n:
                # Usar id(n) para identificador único
                node_id = str(id(n))
                label_text = str(n.getFlightCode())
                # Crear el nodo circular neón
                dot.node(node_id, label=label_text)
                if n.getLeftSon():
                    dot.edge(node_id, str(id(n.getLeftSon())))
                    AddNode(n.getLeftSon())
                if n.getRightSon():
                    dot.edge(node_id, str(id(n.getRightSon())))
                    AddNode(n.getRightSon())

        if self.root:
            AddNode(self.root)
        # Generar el SVG y hacerlo responsivo
        svg = dot.pipe(format='svg').decode("utf-8")
        return svg.replace('<svg ', '<svg width="100%" height="auto" ')