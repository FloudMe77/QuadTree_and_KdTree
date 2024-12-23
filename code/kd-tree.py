from copy import deepcopy
import math
from Point import Point
from Rectangle import Rectangle

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
    def __init__(self, points, amount_of_dimensions, begining_axis=0, is_points_in_vertix = True):
        # points jest tablicą krotek określających położenie punktu w przestrzeni
        # for point in points:
        for point in points:
            if len(point)!= amount_of_dimensions:
                raise ValueError("zbiór punktów nie zgadza się z deklarowaną ilością wymiarów")
            
        points = [Point(point) for point in points]
        # oś w zdłuż której będzie pierwszy podział
        self.begining_axis = begining_axis
        # korzeń drzewa, reszta tworzy się rekursywnie
        self.root = KdTreeNode(points,amount_of_dimensions,begining_axis,Rectangle(None,None,points))
        self.amount_of_dimensions = amount_of_dimensions
        self.points = points
        
    def search_in_recangle(self, region, return_tab_of_Points = False):
        print(region)
        if not isinstance(region, Rectangle):
            if len(region) == 2 and \
                 len(region[0])==self.amount_of_dimensions and \
                 len(region[1])==self.amount_of_dimensions: 
                lower_left = Point(region[0])
                upper_right = Point(region[1])
                region = Rectangle(lower_left,upper_right)
            else:
                raise ValueError("otrzymany region jest niepoprawny")
        
        if not region.upper_right.follow(region.lower_left):
            raise ValueError("otrzymany region ma złą kolejność wierzchołków")
        
        region = self.root.rectangle.intersection(region)

        if return_tab_of_Points:
            return self.root.search_in_recangle(region)
        else:
            return [point.cords for point in self.root.search_in_recangle(region)]

    
test = [(-5,1.5),(-3,4),(-2.5,1),(-5,7),(-2,6),(5,0),(0,3),(7,1),(2,7),(3,5)]
a = KdTree(test,2)
print(a.root.print_tree())

print(a.search_in_recangle(((-3,0),(10,10))))
# print([12,32]+[53,1])
