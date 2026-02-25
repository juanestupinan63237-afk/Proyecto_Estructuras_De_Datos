from Classes.NodeAVL import Node

class ArbolAVL:
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