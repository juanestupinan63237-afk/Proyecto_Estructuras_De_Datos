class Flight:
    def __init__(self, code, origin, destination, departureTime, basePrice, numberPassengers, priority, promotion, alert):
        self.code = code
        self.origin = origin
        self.destination = destination
        self.departureTime = departureTime
        self.basePrice = basePrice
        self.numberPassengers = numberPassengers
        self.priority = priority
        self.promotion = promotion
        self.alert = alert

    def getCode(self):
        return self.code

    def setCode(self, value):
        self.code = value

    def getOrigin(self):
        return self.origin

    def setOrigin(self, value):
        self.origin = value

    def getDestination(self):
        return self.destination

    def setDestination(self, value):
        self.destination = value

    def getDepartureTime(self):
        return self.departureTime

    def setDepartureTime(self, value):
        self.departureTime = value

    def getBasePrice(self):
        return self.basePrice

    def setBasePrice(self, value):
        self.basePrice = value

    def getNumberPassengers(self):
        return self.numberPassengers

    def setNumberPassengers(self, value):
        self.numberPassengers = value

    def getPriority(self):
        return self.priority

    def setPriority(self, value):
        self.priority = value

    def getPromotion(self):
        return self.promotion

    def setPromotion(self, value):
        self.promotion = value

    def getAlert(self):
        return self.alert

    def setAlert(self, value):
        self.alert = value
    
    def getTotalPrice (self):
        resultado = self.getBasePrice * self.numberPassengers
        if self.alert :
            resultado += resultado*0.25
        return resultado