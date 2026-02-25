from Classes.NodeAVL import Node

class AVLTree:
    def __init__(self):
        self.root = None

    def insertNode(self, value):
        self.root = self.__insertNode(self.root, value)

    def __insertNode(self, node, value):
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

    def __countLeaves(self, node):
        if node is None:
            return 0
        if node.getLeftSon() is None and node.getRightSon() is None:
            return 1
        return self.__countLeaves(node.getLeftSon())+ self.__countLeaves(node.getRightSon())

    def preorderTour(self):
        self.__preorderTour(self.root)

    def __preorderTour(self, node):
        if node is None:
            return
        print(node.getFlightCode())
        self.__preorderTour(node.getLeftSon())
        self.__preorderTour(node.getRightSon())

    def unorderedTour(self):
        self.__unorderedTour(self.root)

    def __unorderedTour(self, node):
        if node is None:
            return
        self.__unorderedTour(node.getLeftSon())
        print(node.getFlightCode())
        self.__unorderedTour(node.getRightSon())

    def postOrderTour(self):
        self.__postOrderTour(self.root)

    def __postOrderTour(self, node):
        if node is None:
            return
        self.__postOrderTour(node.getLeftSon())
        self.__postOrderTour(node.getRightSon())
        print(node.getFlightCode())
