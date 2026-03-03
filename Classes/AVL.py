from Classes.NodeAVL import Node
from Classes.FlightSB import Flight
from graphviz import Digraph

class AVLTree:
    def __init__(self):
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
                succesorNode = self.__minValueNode(node)
                node.setFlightCode(succesorNode.getFlightCode())
                node.setRightSon(self.__deleteNode(node.getRightSon(), succesorNode.getFlightCode()))

    def __minValueNode(self, node : Node):
        temporal = node
        while temporal.getLeftSon() is not None:
            temporal = temporal.getLeftSon()
        return temporal

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