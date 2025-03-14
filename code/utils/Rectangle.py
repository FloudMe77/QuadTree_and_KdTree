from utils.Point import Point
from copy import deepcopy

class Rectangle:

    def __init__(self,lower_left = None, upper_right = None, list_of_Point = None):

        if list_of_Point:
            self.lower_left, self.upper_right = self.from_Point_list(list_of_Point)

        else:
            if not lower_left.precedens(upper_right):
                raise ValueError(f"Prubujesz stworzyć prostokąt o błednych punktach skrajnych {lower_left},{upper_right}")
            self.lower_left = lower_left
            self.upper_right = upper_right
    

    def from_Point_list(self,list_of_Point):
        lower_left = list(list_of_Point[0].cords)
        upper_right = list(list_of_Point[0].cords)
        for point in list_of_Point[1:]:
            for axis,cord in enumerate(point.cords):
                lower_left[axis] = min(lower_left[axis], cord)
                upper_right[axis] = max(upper_right[axis], cord)
        return Point(lower_left), Point(upper_right)

    def __str__(self):
        return f"(ro jest prostokąt{self.lower_left}),{self.upper_right}"
    
    def __repr__(self):
        return self.__str__()

    def is_intersect(self, other):
    # Prostokąty nie przecinają się, jeśli jeden leży całkowicie po "prawej/górze" drugiego
        # if self.upper_right.precedens(other.lower_left) or other.upper_right.precedens(self.lower_left):
        #     return False # Prostokąty się nie przecinają
        return self.lower_left.precedens(other.upper_right) and other.lower_left.precedens(self.upper_right)
        
    
    def is_contained(self, other):
        """
        Sprawdza, czy other zawiera się w self.
        """
        return self.lower_left.precedens(other.lower_left) and other.upper_right.precedens(self.upper_right)
        
    
    def intersection(self, other):
        lower_left_1_cords, upper_right_1_cords = self.lower_left.cords, self.upper_right.cords
        lower_left_2_cords, upper_right_2_cords = other.lower_left.cords, other.upper_right.cords
        ll = deepcopy(lower_left_1_cords)
        ur = deepcopy(upper_right_1_cords)
        for i in range(len(lower_left_1_cords)):  # Zakładamy, że lower_left_1_cords, upper_right_1_cords, lower_left_2_cords, upper_right_2_cords mają tę samą długość
            ll[i] = max(ll[i],lower_left_1_cords[i],lower_left_2_cords[i])
            ur[i] = min(ur[i],upper_right_1_cords[i],upper_right_2_cords[i])
        return Rectangle(Point(ll),Point(ur))  # R2 jest w całości w R1
    
    def is_point_in_rectangle(self,point):
        return point.follow(self.lower_left) and point.precedens(self.upper_right)
    
    def get_all_vertix_from_rectangle_on_2d(self):
        x1,y1 = self.lower_left.cords
        x2,y2 = self.upper_right.cords
        return [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]