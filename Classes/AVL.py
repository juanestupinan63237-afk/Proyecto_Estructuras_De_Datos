from Classes.NodeAVL import Node
from Classes.FlightSB import Flight
from graphviz import Digraph

class AVLTree:
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
        if code < node.getFlightCode():
            return self.__searchNode(node.getLeftSon(), code)
        elif code > node.getFlightCode():
            return self.__searchNode(node.getRightSon(), code)
        else:
            return True
        
    def RenderTree(self):
        dot = Digraph(comment='Árbol Binario')
        dot.attr('graph', size='6,6', ratio='compress')
        dot.attr('node', shape='circle', fixedsize='true', width='0.4', height='0.4', fontsize='6')
        dot.attr(ranksep='0.3', nodesep='0.3')
        dot.attr('edge', arrowsize='0.5')
        def AddNode(node: Node):
            if node:
                dot.node(str(id(node)), str(node.flight.code))
                if node.getLeftSon():
                    dot.edge(str(id(node)), str(id(node.getLeftSon())))
                    AddNode(node.getLeftSon())
                if node.getRightSon():
                    dot.edge(str(id(node)), str(id(node.getRightSon())))
                    AddNode(node.getRightSon())
        AddNode(self.root)
        svg = dot.pipe(format='svg').decode("utf-8")
        svg = svg.replace('<svg ', '<svg width="100%" height="100%" preserveAspectRatio="xMidYMid meet" ')
        return svg
