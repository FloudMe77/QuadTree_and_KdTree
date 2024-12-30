import math
from Point import Point
from Rectangle import Rectangle
from copy import deepcopy
# import tests.generate_tests as test
class KdTreeNode:
    def __init__(self,points, dimensions_amount,depth,rectangle, is_points_in_vertix=True):
        if is_points_in_vertix or len(points)==1:
            self.points = points
        else:
            self.points = []
        self.dimensions_amount = dimensions_amount
        self.depth = depth
        self.dimension_number = self.depth%self.dimensions_amount
        self.left = None
        self.right = None
        self.is_points_in_vertix = is_points_in_vertix
        self.rectangle = rectangle
        if len(points)>1:
            self.build(points)

    def bsearch_right(self,t,index,val):
        p=0
        r=len(t)-1
        while p<r:
            
            i=math.ceil((p+r)/2)
            print(i)
            if t[i].cords[index]<=val:
                p=i
            else:
                r=i-1
        return p
    
    def build(self,points):
        points.sort(key = lambda x: x.cords[self.dimension_number])
        median = math.ceil(len(points)/2)

        median = self.bsearch_right(points,self.dimension_number,points[median].cords[self.dimension_number])

        self.axes = points[median-1].cords[self.dimension_number]
        left_rec, right_rec = self.split_region(self.rectangle, self.dimension_number, self.axes)
        self.left = KdTreeNode(points[0:median], self.dimensions_amount, self.depth+1, left_rec, self.is_points_in_vertix )
        self.right = KdTreeNode(points[median:], self.dimensions_amount, self.depth+1, right_rec, self.is_points_in_vertix )
    
    def split_region(self,rec, dimension_numer, axes):
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

    def find_points_in_region(self,region):
        
        if self.is_leaf():
            # print(self.points)
            return region.points_in_rectangle(self.points)
        
        if region.is_contained(self.rectangle):
            return self.get_points()
        
        if region.is_intersect(self.rectangle):
            return self.left.find_points_in_region(region) + self.right.find_points_in_region(region)
        return []
    
    def check_contains(self,point):
        print(self.rectangle)
        if self.is_leaf():
            return point == self.points[0]
        if self.axes < point.cords[self.dimension_number]:
            return self.right.check_contains(point)
        return self.left.check_contains(point)
    
class KdTree:
    def __init__(self, points, dimensions_amount, begining_axis=0, is_points_in_vertix = False):
        # points jest tablicą krotek określających położenie punktu w przestrzeni
        for point in points:
            if len(point)!= dimensions_amount:
                raise ValueError("zbiór punktów nie zgadza się z deklarowaną ilością wymiarów")
            
        points = [Point(point) for point in points]
        # oś w zdłuż której będzie pierwszy podział
        self.begining_axis = begining_axis
        # korzeń drzewa, reszta tworzy się rekursywnie
        self.root = KdTreeNode(points, 
                               dimensions_amount, 
                               begining_axis, 
                               Rectangle(list_of_Point=points), 
                               is_points_in_vertix)
        self.dimensions_amount = dimensions_amount
        
    def find_points_in_region(self, region):
        print(region)
        if not isinstance(region, Rectangle):
            if len(region) == 2 and \
                 len(region[0])==self.dimensions_amount and \
                 len(region[1])==self.dimensions_amount: 
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

        return [point.cords for point in self.root.find_points_in_region(region)]

    def check_contains(self,point):
        if not isinstance(point, Point):
            if len(point) != self.dimensions_amount:
                raise ValueError("Podano nieprawidołowy punkt do znalezienia")
            point = Point(point)
        return self.root.check_contains(point)
    

test = [(-5,1.5),(-3,4),(-2.5,1),(-5,7),(-2,6),(5,0),(0,3),(7,1),(2,7),(3,5)]
t3 = [(-5,),(-3,),(-2.5,),(-2,),(5,),(0,),(7,),(2,),(3,)]
a = KdTree(test,2)
print(a.root.print_tree())

print(a.find_points_in_region(((-1,1),(4,6))))