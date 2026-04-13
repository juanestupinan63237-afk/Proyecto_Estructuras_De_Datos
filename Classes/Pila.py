class Pila:
    """
    A Last-In, First-Out (LIFO) Stack implementation.
    
    This class is designed to store dictionaries representing system 
    states or operations for undo/redo functionality.
    """
    def __init__ (self):
        """Initializes an empty stack."""
        self.__datos__ = []

    def Desapilar (self):
        """
        Pops the top element off the stack and returns it.
        
        Returns:
            dict: The last element added to the stack.
        Raises:
            IndexError: If the stack is empty.
        """
        return self.__datos__.pop()
       
    def Apilar (self , dicc: dict):
        """
        Pushes a new dictionary onto the top of the stack.
        
        Args:
            dicc (dict): The data or state to be saved.
        """
        self.__datos__.append (dicc)

    def isEmpty (self):
        """
        Checks if the stack is currently empty.
        
        Returns:
            bool: True if empty, False otherwise.
        """
        return len(self.__datos__) == 0
    
    def resetPila (self):
        """Removes all items from the stack, resetting it to an empty state."""
        self.__datos__ = []