from Point import Point
from copy import deepcopy

class Rectangle:
    def __init__(self,lower_left,upper_right,list_of_Point=None):
        if list_of_Point:
            self.lower_left, self.upper_right = self.from_Point_list(list_of_Point)
        else:
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

    def is_intersect(self,other):
        
        lower_left_1_cords, upper_right_1_cords = self.lower_left.cords, self.upper_right.cords
        lower_left_2_cords, upper_right_2_cords = other.lower_left.cords, other.upper_right.cords

        # Sprawdź brak przecięcia dla każdego wymiaru
        for i in range(len(lower_left_1_cords)):  # Zakładamy, że lower_left_1_cords, upper_right_1_cords, lower_left_2_cords, upper_right_2_cords mają ten sam wymiar
            if upper_right_1_cords[i] < lower_left_2_cords[i] or upper_right_2_cords[i] < lower_left_1_cords[i]:
                return False  # Prostokąty się nie przecinają
        return True  # Prostokąty się przecinają
    
    def is_contained(self, other):
        """
        Sprawdza, czy other zawiera się w self.
        """
        # R2 = (lower_left_2_cords, upper_right_2_cords) to prostokąt `other`
        # R1 = (lower_left_1_cords, upper_right_1_cords) to prostokąt `self`
        lower_left_1_cords, upper_right_1_cords = self.lower_left.cords, self.upper_right.cords
        lower_left_2_cords, upper_right_2_cords = other.lower_left.cords, other.upper_right.cords

        # Sprawdź zawieranie dla każdego wymiaru
        for i in range(len(lower_left_1_cords)):  # Zakładamy, że lower_left_1_cords, upper_right_1_cords, lower_left_2_cords, upper_right_2_cords mają tę samą długość
            if not (lower_left_1_cords[i] <= lower_left_2_cords[i] <= upper_right_2_cords[i] <= upper_right_1_cords[i]):
                return False  # R2 nie jest w całości w R1
        return True  # R2 jest w całości w R1
    
    def intersection(self, other):
        lower_left_1_cords, upper_right_1_cords = self.lower_left.cords, self.upper_right.cords
        lower_left_2_cords, upper_right_2_cords = other.lower_left.cords, other.upper_right.cords
        ll = deepcopy(lower_left_1_cords)
        ur = deepcopy(upper_right_1_cords)
        for i in range(len(lower_left_1_cords)):  # Zakładamy, że lower_left_1_cords, upper_right_1_cords, lower_left_2_cords, upper_right_2_cords mają tę samą długość
            ll[i] = max(ll[i],lower_left_1_cords[i],lower_left_2_cords[i])
            ur[i] = min(ur[i],upper_right_1_cords[i],upper_right_2_cords[i])
        return Rectangle(Point(ll),Point(ur))  # R2 jest w całości w R1
    
    def points_in_rectangle(self,points):
        res = []
        for point in points:
            print(point)
            for amount_of_dimensions,cord in enumerate(point.cords):
                flag = True
                if not (self.lower_left.cords[amount_of_dimensions] <= cord <= self.upper_right.cords[amount_of_dimensions]):
                    flag = False
                    break
            if flag:
                res.append(point)
        return res
    def get_all_vertix_from_rectangle_on_2d(self):
        x1,y1 = self.lower_left.cords
        x2,y2 = self.upper_right.cords
        return [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]