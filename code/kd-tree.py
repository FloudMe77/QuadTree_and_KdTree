from copy import deepcopy
import math
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


class KdTreeNode:
    def __init__(self,points,amount_of_dimensions,depth,rectangle=None):
        self.amount_of_dimensions = amount_of_dimensions
        self.depth = depth
        self.points = points
        self.left = None
        self.right = None
        if rectangle:
            self.rectangle = rectangle
        else:
            self.rectangle = Rectangle(None,None,points)
        self.build()

    def build(self):
        if len(self.points)==1: return
        self.points.sort(key = lambda x: x.cords[self.depth])
        median = math.ceil(len(self.points)/2)
        axes = self.points[median-1].cords[self.depth%self.amount_of_dimensions]
        print(axes)
        left_rec, right_rec = self.devide_on_half_rectangle(self.rectangle, (self.depth)%self.amount_of_dimensions, axes)
        self.left = KdTreeNode(self.points[0:median], self.amount_of_dimensions, (self.depth+1)%self.amount_of_dimensions, left_rec )
        self.right = KdTreeNode(self.points[median:], self.amount_of_dimensions, (self.depth+1)%self.amount_of_dimensions, right_rec )
    
    def print_tree(self):
        print(self.points,self.depth, self.rectangle)
        if self.left:
            self.left.print_tree()
        if self.right:
            self.right.print_tree()

    # możliwe, że powinna zostać przeniesiona gdzieś indziej
    def devide_on_half_rectangle(self,rec, dimension_numer, axes):
        # jeden to dolny, czy tam po lewej
        # drugi to górny czy tam po prawej
        lower_left_1 = rec.lower_left
        upper_right_2 = rec.upper_right

        upper_right_1_cords = deepcopy(rec.upper_right.cords)
        upper_right_1_cords[dimension_numer] = axes
        upper_right_1 = Point(upper_right_1_cords)

        lower_left_2_cords = deepcopy(rec.lower_left.cords)
        lower_left_2_cords[dimension_numer] = axes
        lower_left_2 = Point(lower_left_2_cords)
        
        return Rectangle(lower_left_1,upper_right_1), Rectangle(lower_left_2,upper_right_2)
    
    def search_in_recangle(self,region):
        
        if self.left is None and self.right is None: # jesteśmy w liściu
            # print(self.points)
            print(region.points_in_rectangle(self.points),"cos")
            return region.points_in_rectangle(self.points)
        if region.is_contained(self.rectangle):
            print(self.points)
            return self.points
        if region.is_intersect(self.rectangle):
            return self.left.search_in_recangle(region) + self.right.search_in_recangle(region)
        return []
    
class KdTree:
    def __init__(self, points, amount_of_dimensions, begining_axis=0):
        points = [Point(point,e+1) for e,point in enumerate(points)]
        self.begining_axis = begining_axis
        self.root = KdTreeNode(points,amount_of_dimensions,begining_axis,Rectangle(None,None,points))
        self.amount_of_dimensions = amount_of_dimensions
        self.points = points
        
    def search_in_recangle(self, region):
        print(region)
        region = self.root.rectangle.intersection(region)
        return self.root.search_in_recangle(region)

    
test = [(-5,1.5),(-3,4),(-2.5,1),(-5,7),(-2,6),(5,0),(0,3),(7,1),(2,7),(3,5)]
a = KdTree(test,2)
print(a.root.print_tree())

print(a.search_in_recangle(Rectangle(Point((-3,0)),Point((10,10)))))
# print([12,32]+[53,1])
