class Point:
    def __init__(self,cords,number=None):
        # number only for debug
        self.cords = cords
        self.amount_of_dimensions = len(self.cords)
        self.number = number

    def __str__(self):
        return f"({self.cords}),{self.number}"
    
    def __repr__(self):
        return self.__str__()

    def follow(self,other):
        if self.amount_of_dimensions != other.amount_of_dimensions:
            raise ValueError("niepoprawne wymiary porównywanych punktów")
        for i in range(self.amount_of_dimensions):
            if self.cords[i] < other.cords[i]:
                return False
        return True
    
    def precedens(self,other):
        if self.amount_of_dimensions != other.amount_of_dimensions:
            raise ValueError("niepoprawne wymiary porównywanych punktów")
        for i in range(self.amount_of_dimensions):
            if self.cords[i] > other.cords[i]:
                return False
        return True