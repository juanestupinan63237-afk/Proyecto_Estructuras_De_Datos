from Classes.NodeAVL import Node
from Classes.FlightSB import Flight

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