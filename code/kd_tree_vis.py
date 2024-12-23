from copy import deepcopy
import math
from Point import Point
from Rectangle import Rectangle
from visualizer_bit.main import Visualizer



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
        vis.add_polygon(self.rectangle.get_all_vertix_from_rectangle_on_2d(), fill = False, alpha = 0.5)
        self.build()


    def build(self):
        if len(self.points)==1: return
        
        self.points.sort(key = lambda x: x.cords[self.depth])
        median = math.ceil(len(self.points)/2)
        axes = self.points[median-1].cords[self.depth%self.amount_of_dimensions]
        left_rec, right_rec = self.devide_on_half_rectangle(self.rectangle, (self.depth)%self.amount_of_dimensions, axes)
        self.left = KdTreeNode(self.points[0:median], self.amount_of_dimensions, (self.depth+1)%self.amount_of_dimensions, left_rec )
        self.right = KdTreeNode(self.points[median:], self.amount_of_dimensions, (self.depth+1)%self.amount_of_dimensions, right_rec )
    

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
            ans = region.points_in_rectangle(self.points)
            vis.add_point([(point.cords[0],point.cords[1]) for point in ans], color = "lime")
            return ans
        if region.is_contained(self.rectangle):
            vis.add_point([(point.cords[0],point.cords[1]) for point in self.points], color = "lime")
            return self.points
        if region.is_intersect(self.rectangle):
            return self.left.search_in_recangle(region) + self.right.search_in_recangle(region)
        return []
    
    


class KdTree:
    def __init__(self, points, amount_of_dimensions, begining_axis=0):
        points = [Point(point,e+1) for e,point in enumerate(points)]
        vis.add_point([(point.cords[0],point.cords[1]) for point in points],color = "orange")
        self.begining_axis = begining_axis
        self.root = KdTreeNode(points,amount_of_dimensions,begining_axis,Rectangle(None,None,points))
        self.amount_of_dimensions = amount_of_dimensions
        self.points = points

        
    def search_in_recangle(self, region):
        vis.add_polygon(region.get_all_vertix_from_rectangle_on_2d(), fill = False, color = "red",alpha=1)
        region = self.root.rectangle.intersection(region)
        
        return self.root.search_in_recangle(region)
        
vis=[]
def give_visualization(test,ll,ur):
    global vis
    vis = Visualizer()
    a = KdTree(test,2)

    print(a.search_in_recangle(Rectangle(Point(ll),Point(ur))))
    
    return vis
