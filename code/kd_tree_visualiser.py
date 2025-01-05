
from visualizer_bit.main import Visualizer
import math
from utils.Point import Point
from utils.Rectangle import Rectangle
from copy import deepcopy

########
begin_points_color = "black"
added_to_structer_color = '#40BFEF'
grid_constr_color = "tab:orange"

########
vis_stack=[]
tab_of_line=[]
########
class KdTreeNode_vis:
    def __init__(self,points, dimensions_amount,depth,rectangle, is_points_in_vertix=True):
        
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
    
    def bsearch_left(self,t,index,val):
        p=0
        r=len(t)-1
        while p<r:
            
            i=(p+r)//2
            if t[i].cords[index]<val:
                p=i+1
            else:
                r=i
        return p

    def build(self,points):
        for _ in range(self.dimensions_amount):
            points.sort(key = lambda x: x.cords[self.dimension_number])
            median = math.ceil(len(points)/2)
            median-=1
            median = self.bsearch_right(points,self.dimension_number,points[median].cords[self.dimension_number])
            left_median = self.bsearch_left(points,self.dimension_number,points[median].cords[self.dimension_number])
            median+=1

            if median - left_median > 3*len(points)//4 or median == len(points):
                self.depth +=1
                self.dimension_number = (self.dimension_number+1)%self.dimensions_amount
            else:
                break

        self.axis = points[median-1].cords[self.dimension_number]
        left_rec, right_rec = self._split_region(self.rectangle, self.dimension_number, self.axis)
        vis.add_line_segment((right_rec.lower_left.cords, left_rec.upper_right.cords), color = grid_constr_color, alpha = 0.5)
        tab_of_line.append((right_rec.lower_left.cords, left_rec.upper_right.cords))
        self.line = (right_rec.lower_left.cords, left_rec.upper_right.cords)
        vis.remove_figure(vis_stack[-1])
        vis_stack.pop()
        self.left = KdTreeNode_vis(points[0:median], self.dimensions_amount, self.depth+1, left_rec, self.is_points_in_vertix )
        self.right = KdTreeNode_vis(points[median:], self.dimensions_amount, self.depth+1, right_rec, self.is_points_in_vertix )
    
    def _split_region(self,rec, dimension_numer, axis):
        # jeden to dolny, czy tam po lewej
        # drugi to górny czy tam po prawej
        lower_left_1 = rec.lower_left
        upper_right_2 = rec.upper_right

        upper_right_1_cords = deepcopy(rec.upper_right.cords)
        upper_right_1_cords[dimension_numer] = axis
        upper_right_1 = Point(upper_right_1_cords)

        lower_left_2_cords = deepcopy(rec.lower_left.cords)
        lower_left_2_cords[dimension_numer] = axis
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
            is_in = region.is_point_in_rectangle(self.points[0])
            if is_in:
                tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "green", alpha=0.2)
                vis.add_point([point.cords for point in self.points],color="lime")
            else:
                tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "red", alpha=0.2)
            
            vis.remove_figure(tmp)
            return self.points if is_in else []
        
        if region.is_contained(self.rectangle):
            points = self.get_points()
            tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "green", alpha=0.2)
            vis.add_point([point.cords for point in points],color="lime")
            vis.remove_figure(tmp)
            return points
        
        if region.is_intersect(self.rectangle):
            tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "grey", alpha=0.2)
            vis.remove_figure(tmp)
            return self.left.find_points_in_region(region) + self.right.find_points_in_region(region)
        tmp = vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "red", alpha=0.2)
        vis.remove_figure(tmp)
        return []
    
    def check_contains(self,point):
        if self.is_leaf():
            return point == self.points[0]
        if self.axis < point.cords[self.dimension_number]:
            return self.right.check_contains(point)
        return self.left.check_contains(point)
    
class KdTree_vis:
    def __init__(self, points, dimensions_amount, begining_axis=0):
        # points jest tablicą krotek określających położenie punktu w przestrzeni
        self.points = deepcopy(points)
        for point in points:
            if len(point)!= dimensions_amount:
                raise ValueError("zbiór punktów nie zgadza się z deklarowaną ilością wymiarów")
        vis.add_point(points,color = begin_points_color)
        points = [Point(point) for point in points]
        # oś w zdłuż której będzie pierwszy podział
        self.begining_axis = begining_axis
        # korzeń drzewa, reszta tworzy się rekursywnie
        self.root = KdTreeNode_vis(points, 
                               dimensions_amount, 
                               begining_axis, 
                               Rectangle(list_of_Point=points))
        self.dimensions_amount = dimensions_amount
        
    def find_points_in_region(self, region):
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
        
        vis.add_polygon(region.get_all_vertix_from_rectangle_on_2d(), fill = True, color = "blue",alpha=0.2)
        region = self.root.rectangle.intersection(region)
        return [point.cords for point in self.root.find_points_in_region(region)]

    def check_contains(self,point):
        if not isinstance(point, Point):
            if len(point) != self.dimensions_amount:
                raise ValueError("Podano nieprawidołowy punkt do znalezienia")
            point = Point(point)
        return self.root.check_contains(point)
    
vis=[]
class Visualization:
    def give_visualization_of_create(self,test, draw_final=False, draw_gif=False, name = "kd_tree visualization"):
        global vis_stack
        global tab_of_line
        global vis
        vis_stack = []
        tab_of_line = []
        vis = Visualizer()
        vis.clear()
        self.kd_tree = KdTree_vis(test,2)    
        if draw_final:
            self.draw_vis(name,vis)
        if draw_gif:
            self.draw_gif(name,vis)
        return vis
    
    def give_visualization_of_search(self,region,draw_final=False, draw_gif=False, name = "kd_tree visualization",print_output = False):
        global vis
        global tab_of_line
        global vis_stack
        if not isinstance(region, Rectangle):
            if len(region) == 2 and \
                 len(region[0])==2 and \
                 len(region[1])==2: 
                lower_left = Point(region[0])
                upper_right = Point(region[1])
                region = Rectangle(lower_left,upper_right)
            else:
                raise ValueError("otrzymany region jest niepoprawny")
        find_ll = region.lower_left.cords
        find_ur = region.upper_right.cords
        vis_stack = []
        vis = Visualizer()
        vis.clear()
        vis.add_point(self.kd_tree.points,color = added_to_structer_color)
        vis.add_line_segment(tab_of_line,color=grid_constr_color,alpha = 0.4)
        if print_output:
            print(self.kd_tree.find_points_in_region(Rectangle(Point(find_ll),Point(find_ur))))
        else:
            self.kd_tree.find_points_in_region(Rectangle(Point(find_ll),Point(find_ur)))
        
        if draw_final:
            self.draw_vis(name,vis)
        if draw_gif:
            self.draw_gif(name,vis)
        return vis
    
    def draw_gif(self, name, vis):
        vis.add_title(name)
        vis.show_gif()
    
    def draw_vis(self, name, vis):
        vis.add_title(name)
        vis.show()