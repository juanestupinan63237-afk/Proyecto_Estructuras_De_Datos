class Cola:
    def __init__(self):
        self.__datos__ = []
 
    def Encolar(self, datos):
        self.__datos__.append(datos)
 
    def Desencolar(self):
        if self.isEmpty():
            return None
        return self.__datos__.pop(0)
 
    def isEmpty(self):
        return len(self.__datos__) == 0
 
    def GetAll(self) -> list:
        """Returns a list of dicts with all queued flights without removing them."""
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
 
    def Size(self) -> int:
        return len(self.__datos__)