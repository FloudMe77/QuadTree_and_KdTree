
from visualizer_bit.main import Visualizer
import math
from Point import Point
from Rectangle import Rectangle
import copy
# class KdTreeNode:
#     def __init__(self,points,amount_of_dimensions,depth,rectangle,is_points_in_vertix=True):
#         if is_points_in_vertix or len(points)==1:
#             self.points = points
#         else:
#             self.points = []

#         self.amount_of_dimensions = amount_of_dimensions
#         self.depth = depth
#         self.left = None
#         self.right = None
#         self.is_points_in_vertix = is_points_in_vertix
#         self.rectangle = rectangle
#         if len(points)==1:
#             vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = False, alpha = 0.5, color = "purple")
#             vis.add_point(points[0].cords,color = "orange")
#         self.build(points)

#     def build(self,points):
#         if len(points)==1: return
#         points.sort(key = lambda x: x.cords[self.depth])
#         while points[0].cords[self.depth]== points[-1].cords[self.depth]:
#             self.depth = (self.depth+1)%self.amount_of_dimensions
#             points.sort(key = lambda x: x.cords[self.depth])
#         median = math.ceil(len(points)/2)
        
#         while median<len(points)-1 and points[median-1].cords[self.depth%self.amount_of_dimensions] == points[median].cords[self.depth%self.amount_of_dimensions]:
#             median+=1

#         self.axes = points[median-1].cords[self.depth%self.amount_of_dimensions]
#         left_rec, right_rec = Rectangle.devide_on_half_Rectangle(self.rectangle, (self.depth)%self.amount_of_dimensions, self.axes)
#         self.left = KdTreeNode(points[0:median], self.amount_of_dimensions, (self.depth+1)%self.amount_of_dimensions, left_rec )
#         self.right = KdTreeNode(points[median:], self.amount_of_dimensions, (self.depth+1)%self.amount_of_dimensions, right_rec )
    
#     def print_tree(self):
#         print(self.points,self.depth, self.rectangle)
#         if self.left:
#             self.left.print_tree()
#         if self.right:
#             self.right.print_tree()

#     def is_leaf(self):
#         return self.left is None and self.right is None

#     def get_points(self):
#         if self.is_points_in_vertix or self.is_leaf():
#             return self.points
#         else:
#             return self.left.get_points() + self.right.get_points()

#     def search_in_recangle(self,region):
        
#         if self.is_leaf():
#             # print(self.points)
#             # print(region.points_in_rectangle(self.points),"cos")
#             vis.add_point([(point.cords[0],point.cords[1]) for point in region.points_in_rectangle(self.points)], color = "lime")
#             return region.points_in_rectangle(self.points)
#         if region.is_contained(self.rectangle):
#             points = self.get_points()
#             print(points)
#             vis.add_point([(point.cords[0],point.cords[1]) for point in points], color = "lime")
#             return points
#         if region.is_intersect(self.rectangle):
#             return self.left.search_in_recangle(region) + self.right.search_in_recangle(region)
#         return []
    
#     def check_contains(self,point):
#         if self.is_leaf():
#             return point == self.points[0]
#         if self.axes < point.cords[(self.depth)%self.amount_of_dimensions]:
#             return self.right.check_contains(point)
#         return self.left.check_contains(point)
    
# class KdTree:
#     def __init__(self, points, amount_of_dimensions, begining_axis=0, is_points_in_vertix = False):
#         # points jest tablicą krotek określających położenie punktu w przestrzeni
#         for point in points:
#             if len(point)!= amount_of_dimensions:
#                 raise ValueError("zbiór punktów nie zgadza się z deklarowaną ilością wymiarów")
            
#         points = [Point(point) for point in points]
#         vis.add_point([(point.cords[0],point.cords[1]) for point in points],color = "blue")
#         # oś w zdłuż której będzie pierwszy podział
#         self.begining_axis = begining_axis
#         # korzeń drzewa, reszta tworzy się rekursywnie
#         self.root = KdTreeNode(points, 
#                                amount_of_dimensions, 
#                                begining_axis, 
#                                Rectangle.create_Rectangle_from_Point_list(points), 
#                                is_points_in_vertix)
#         self.amount_of_dimensions = amount_of_dimensions
        
#     def search_in_recangle(self, region, return_tab_of_Points = False):
#         vis.add_polygon(region.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "grey",alpha=0.4)
#         if not isinstance(region, Rectangle):
#             if len(region) == 2 and \
#                  len(region[0])==self.amount_of_dimensions and \
#                  len(region[1])==self.amount_of_dimensions: 
#                 lower_left = Point(region[0])
#                 upper_right = Point(region[1])
#                 region = Rectangle(lower_left,upper_right)
#             else:
#                 raise ValueError("otrzymany region jest niepoprawny")
        
#         if not region.upper_right.follow(region.lower_left):
#             raise ValueError("otrzymany region ma złą kolejność wierzchołków")
        
#         if not region.is_intersect(self.root.rectangle):
#             return []
#         region = self.root.rectangle.intersection(region)

#         if return_tab_of_Points:
#             return self.root.search_in_recangle(region)
#         else:
#             return [point.cords for point in self.root.search_in_recangle(region)]

#     def check_contains(self,point):
#         if not isinstance(point, Point):
#             if len(point) != self.amount_of_dimensions:
#                 raise ValueError("Podano nieprawidołowy punkt do znalezienia")
#             point = Point(point)
#         return self.root.check_contains(point)
    
import math
from Point import Point
from Rectangle import Rectangle
# import tests.generate_tests as test
########
begin_points_color = "black"
added_to_structer_color = "blue"
grid_constr_color = "pink"

########
vis_stack=[]
tab_of_line=[]
########
class KdTreeNode:
    def __init__(self,points, dimensions_amount,depth,rectangle, is_points_in_vertix=False):
        
        self.dimensions_amount = dimensions_amount
        self.depth = depth
        self.dimension_number = self.depth%self.dimensions_amount
        self.left = None
        self.right = None
        self.is_points_in_vertix = is_points_in_vertix
        self.rectangle = rectangle
        
        vis_stack.append(vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "grey",alpha=0.4))

        if is_points_in_vertix or len(points)==1:
            self.points = points
        else:
            self.points = []

        if len(points)>1:
            self.build(points)

        if self.is_leaf():
            vis.add_point(points[0].cords,color = added_to_structer_color)
            vis.remove_figure(vis_stack[-1])
            vis_stack.pop()

    def bsearch_right(self,t,index,val):
        p=0
        r=len(t)-1
        while p<r:
            
            i=math.ceil((p+r)/2)
            if t[i].cords[index]<=val:
                p=i
            else:
                r=i-1
        return p
    
    def build(self,points):
        points.sort(key = lambda x: x.cords[self.dimension_number])
        median = math.ceil(len(points)/2)
        # tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "grey",alpha=0.4)
        median = self.bsearch_right(points,self.dimension_number,points[median].cords[self.dimension_number])

        self.axes = points[median-1].cords[self.dimension_number]
        left_rec, right_rec = Rectangle.devide_on_half_Rectangle(self.rectangle, self.dimension_number, self.axes)
        vis.add_line_segment((right_rec.lower_left.cords, left_rec.upper_right.cords), color = grid_constr_color)
        tab_of_line.append((right_rec.lower_left.cords, left_rec.upper_right.cords))
        self.line = (right_rec.lower_left.cords, left_rec.upper_right.cords)
        vis.remove_figure(vis_stack[-1])
        vis_stack.pop()
        self.left = KdTreeNode(points[0:median], self.dimensions_amount, self.depth+1, left_rec, self.is_points_in_vertix )
        self.right = KdTreeNode(points[median:], self.dimensions_amount, self.depth+1, right_rec, self.is_points_in_vertix )
    
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
            ans = region.points_in_rectangle(self.points)
            if len(ans)>0:
                tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "green", alpha=0.2)
            else:
                tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "red", alpha=0.2)
            vis.add_point([point.cords for point in ans],color="lime")
            vis.remove_figure(tmp)
            return ans
        
        if region.is_contained(self.rectangle):
            points = self.get_points()
            tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "green", alpha=0.2)
            vis.add_point([point.cords for point in points],color="lime")
            vis.remove_figure(tmp)
            return points
        
        if region.is_intersect(self.rectangle):
            tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "grey", alpha=0.2)
            vis.remove_figure(tmp)
            return self.left.search_in_recangle(region) + self.right.search_in_recangle(region)
        print("cos")
        tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "red", alpha=0.2)
        vis.remove_figure(tmp)
        return []
    
    def check_contains(self,point):
        print(self.rectangle)
        if self.is_leaf():
            return point == self.points[0]
        if self.axes < point.cords[self.dimension_number]:
            return self.right.check_contains(point)
        return self.left.check_contains(point)
    
class KdTree:
    def __init__(self, points, dimensions_amount, begining_axis=0):
        # points jest tablicą krotek określających położenie punktu w przestrzeni
        self.points = copy.deepcopy(points)
        for point in points:
            if len(point)!= dimensions_amount:
                raise ValueError("zbiór punktów nie zgadza się z deklarowaną ilością wymiarów")
        vis.add_point(points)
        points = [Point(point) for point in points]
        # oś w zdłuż której będzie pierwszy podział
        self.begining_axis = begining_axis
        # korzeń drzewa, reszta tworzy się rekursywnie
        self.root = KdTreeNode(points, 
                               dimensions_amount, 
                               begining_axis, 
                               Rectangle(list_of_Point=points))
        self.dimensions_amount = dimensions_amount
        
    def search_in_recangle(self, region):
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
        
        vis.add_polygon(region.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "blue",alpha=0.4)
        print(region)
        region = self.root.rectangle.intersection(region)
        print(region)
        return [point.cords for point in self.root.search_in_recangle(region)]

    def check_contains(self,point):
        if not isinstance(point, Point):
            if len(point) != self.dimensions_amount:
                raise ValueError("Podano nieprawidołowy punkt do znalezienia")
            point = Point(point)
        return self.root.check_contains(point)
    

vis=[]
class visualization:
    def give_visualization_of_create(self,test):
        global vis
        vis = Visualizer()
        self.kd_tree = KdTree(test,2)

        # print(a.search_in_recangle(Rectangle(Point(ll),Point(ur))))
        
        return vis
    def give_visualization_of_search(self,find_ll,find_ur):
        global vis
        vis.clear()
        vis.add_point(self.kd_tree.points)
        for ll,ur in tab_of_line:
            vis.add_line_segment((ll,ur),color=grid_constr_color)
        print(self.kd_tree.search_in_recangle(Rectangle(Point(find_ll),Point(find_ur))))
        return vis