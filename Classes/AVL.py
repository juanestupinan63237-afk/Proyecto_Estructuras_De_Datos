from Clases.NodeAVL import Node

class ArbolAVL:
    def __init__(self):
        self.root = None

    def insertNode(self, value):
        self.root = self.__insertNode(self.root, value)

    def __insertNode(self, node, value):
        if node is None:
            node = Node(value)
            return node

        if value < node.getValue():
            node.leftSon = self.__insertNode(node.getLeftSon(), value)
        elif value > node.getValue():
            node.rightSon = self.__insertNode(node.getRightSon(), value)
        else:
            raise Exception(f"El Nodo ya existe es el árbol")
        return node