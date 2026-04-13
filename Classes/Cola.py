class Cola:
    """
    A First-In, First-Out (FIFO) Queue implementation for Flight management.
    """
    
    def __init__(self):
        """Initializes an empty queue."""
        self.__datos__ = []

    def Encolar(self, datos):
        """
        Adds an element to the back of the queue.
        
        Args:
            datos (Flight): The flight object to be added.
        """
        self.__datos__.append(datos)

    def Desencolar(self):
        """
        Removes and returns the front element of the queue.
        
        Returns:
            Flight or None: The first flight in line, or None if empty.
        """
        if self.isEmpty():
            return None
        return self.__datos__.pop(0)

    def isEmpty(self):
        """Checks if the queue is empty."""
        return len(self.__datos__) == 0

    def Size(self):
        """Returns the number of elements in the queue."""
        return len(self.__datos__)

    def GetAll(self) -> list:
        """
        Transforms the queue into a list of dictionaries.
        
        Useful for JSON responses, adding a 'position' key to each flight.
        
        Returns:
            list: A collection of serialized flight data.
        """
        result = []
        for i, vuelo in enumerate(self.__datos__):
            result.append({
                "position":         i + 1,
                "code":             vuelo.getCode(),
                "origin":           vuelo.getOrigin(),
                "destination":      vuelo.getDestination(),
                "departureTime":    vuelo.getDepartureTime(),
                "basePrice":        vuelo.getBasePrice(),
                "numberPassengers": vuelo.getNumberPassengers(),
                "priority":         vuelo.getPriority(),
                "promotion":        vuelo.getPromotion(),
                "alert":            vuelo.getAlert(),
            })
        return result