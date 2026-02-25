class Node:
    def __init__(self, flight):
        self.flight = flight
        self.leftSon = None
        self.rightSon = None
        self.height = 1

    def getFlightCode(self):
        return self.flight.getCode()

    def setValue(self, node):
        self.value = node

    def getLeftSon(self):
        return self.leftSon

    def setLeftSon(self, node):
        self.leftSon = node

    def getRightSon(self):
        return self.rightSon

    def setRightSon(self, node):
        self.rightSon = node

    def getHeight(self):
        return self.height