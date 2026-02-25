from Clases.NodoAVL import Node

class ArbolAVL:
    def __init__(self):
        self.root = None

    def insertNode(self, value):
        self.root = self.__insertNode(self.root, value)

    def __insertNode(self, node, value):
        if node is None:
            node = Node(value)
            return node

        if node.value < value:
            node.leftSon = self.__insertNode(node.leftSon, value)
        elif node.value > value:
            node.rightSon = self.__insertNode(node.rightSon, value)
        else:
            return node
        return node