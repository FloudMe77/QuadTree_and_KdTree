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
