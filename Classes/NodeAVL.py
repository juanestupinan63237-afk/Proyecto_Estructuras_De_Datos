from Classes.FlightSB import Flight

class Node:
    """
    Represents a single node in a Binary Search Tree (likely AVL).
    
    Each node stores a Flight object and maintains the structure of 
    the tree via left and right child references.
    """

    def __init__(self, flight: Flight):
        """
        Initializes a node with a flight and default height of 1.
        
        Args:
            flight (Flight): The flight object to be stored in this node.
        """
        self.flight = flight
        self.leftSon : Node = None
        self.rightSon : Node = None
        self.height = 1

    def getFlightCode(self):
        """Returns the integer code of the flight stored in the node."""
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
        """Returns the current height of the node for balancing purposes."""
        return self.height
    
    def setHeight(self, value):
        self.height = value

    def getFlight (self):
        return self.flight
    
    def setFlight(self, flight: Flight):
        self.flight = flight