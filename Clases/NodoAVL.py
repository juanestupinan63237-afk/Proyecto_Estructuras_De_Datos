class Node:
    def __init__(self, value):
        self.value = value
        self.father = None
        self.leftSon = None
        self.rightSon = None

    def getValue(self):
        return self.value

    def setValue(self, node):
        self.value = node

    def getFather(self):
        return self.father

    def setFather(self, node):
        self.father = node

    def getLeftSon(self):
        return self.leftSon

    def setLeftSon(self, node):
        self.leftSon = node

    def getRightSon(self):
        return self.rightSon

    def setRightSon(self, node):
        self.rightSon = node