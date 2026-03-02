from Classes.NodeAVL import Node
from Classes.FlightSB import Flight

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