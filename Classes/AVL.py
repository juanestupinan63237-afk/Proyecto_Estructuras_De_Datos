from Classes.NodeAVL import Node
from Classes.FlightSB import Flight
class AVLTree:
    def __init__(self):
        self.root = None

    def insertNodeAVL(self, value: Flight):
        self.root = self.__insertNodeAVL(self.root, value)

    def __insertNodeAVL(self, node : Node, value: Flight):
        if node is None:
            node = Node(value)
            return node
        if value.getCode() < node.getFlightCode():
            node.setLeftSon(self.__insertNodeAVL(node.getLeftSon(), value))
        elif value.getCode() > node.getFlightCode():
            node.setRightSon(self.__insertNodeAVL(node.getRightSon(), value))
        else:
            raise Exception(f"This Node already exists in our AVL Tree...")
        return node
