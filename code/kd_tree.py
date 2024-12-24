import math
from Point import Point
from Rectangle import Rectangle
import tests.generate_tests as test
class KdTreeNode:
    def __init__(self,points,amount_of_dimensions,depth,rectangle,is_points_in_vertix=True):
        if is_points_in_vertix or len(points)==1:
            self.points = points
        else:
            self.points = []
        self.amount_of_dimensions = amount_of_dimensions
        self.depth = depth
        self.left = None
        self.right = None
        self.is_points_in_vertix = is_points_in_vertix
        self.rectangle = rectangle
        self.build(points)

    def build(self,points):
        if len(points)==1: return
        points.sort(key = lambda x: x.cords[self.depth])
        median = math.ceil(len(points)/2)

        while median<len(points)-1 and points[median-1].cords[self.depth%self.amount_of_dimensions] == points[median].cords[self.depth%self.amount_of_dimensions]:
            median+=1

        self.axes = points[median-1].cords[self.depth%self.amount_of_dimensions]
        left_rec, right_rec = Rectangle.devide_on_half_Rectangle(self.rectangle, (self.depth)%self.amount_of_dimensions, self.axes)
        self.left = KdTreeNode(points[0:median], self.amount_of_dimensions, (self.depth+1)%self.amount_of_dimensions, left_rec )
        self.right = KdTreeNode(points[median:], self.amount_of_dimensions, (self.depth+1)%self.amount_of_dimensions, right_rec )
    
    def print_tree(self):
        print(self.points,self.depth, self.rectangle)
        if self.left:
            self.left.print_tree()
        if self.right:
            self.right.print_tree()

    def is_leaf(self):
        return self.left is None and self.right is None

    def get_points(self):
        if self.is_points_in_vertix or self.is_leaf():
            return self.points
        else:
            return self.left.get_points() + self.right.get_points()

    def search_in_recangle(self,region):
        
        if self.is_leaf():
            # print(self.points)
            print(region.points_in_rectangle(self.points),"cos")
            return region.points_in_rectangle(self.points)
        if region.is_contained(self.rectangle):
            points = self.get_points()
            print(points)
            return points
        if region.is_intersect(self.rectangle):
            return self.left.search_in_recangle(region) + self.right.search_in_recangle(region)
        return []
    
    def check_contains(self,point):
        print(self.rectangle)
        if self.is_leaf():
            return point == self.points[0]
        if self.axes < point.cords[(self.depth)%self.amount_of_dimensions]:
            return self.right.check_contains(point)
        return self.left.check_contains(point)
    
class KdTree:
    def __init__(self, points, amount_of_dimensions, begining_axis=0, is_points_in_vertix = False):
        # points jest tablicą krotek określających położenie punktu w przestrzeni
        for point in points:
            if len(point)!= amount_of_dimensions:
                raise ValueError("zbiór punktów nie zgadza się z deklarowaną ilością wymiarów")
            
        points = [Point(point) for point in points]
        # oś w zdłuż której będzie pierwszy podział
        self.begining_axis = begining_axis
        # korzeń drzewa, reszta tworzy się rekursywnie
        self.root = KdTreeNode(points, 
                               amount_of_dimensions, 
                               begining_axis, 
                               Rectangle.create_Rectangle_from_Point_list(points), 
                               is_points_in_vertix)
        self.amount_of_dimensions = amount_of_dimensions
        
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
        if not region.is_intersect(self.root.rectangle):
            return []
        region = self.root.rectangle.intersection(region)

        if return_tab_of_Points:
            return self.root.search_in_recangle(region)
        else:
            return [point.cords for point in self.root.search_in_recangle(region)]

    def check_contains(self,point):
        if not isinstance(point, Point):
            if len(point) != self.amount_of_dimensions:
                raise ValueError("Podano nieprawidołowy punkt do znalezienia")
            point = Point(point)
        return self.root.check_contains(point)
    
# test = test.generate_multidimensional_cluster(5,2,10,4)
# a = KdTree(test,2)
# print(a.root.print_tree())

# print(a.search_in_recangle(((-3,0,0),(10,10,0))))
# for poin in test:
#     print(a.check_contains(poin))
