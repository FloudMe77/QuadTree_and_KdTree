from Point import Point
from Rectangle import Rectangle
from visualizer_bit.main import Visualizer

class QuadTree:
    # Struktura danych Quad-tree
    def __init__(self, rectangle, max_points=3, depth=0, visualizer=None):
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.rectangle = rectangle
        self.max_points = max_points
        self.points = []
        self.depth = depth
        self.divided = False  # Flag for checking if this rectangle is divided
        self.vis = visualizer

        if self.vis:
            self.vis.add_polygon(
                self.rectangle.get_all_vertix_from_rectangle_on_2d(),
                fill=False,
                color="tab:orange"
            )

    def divide(self):
        x_1, y_1 = self.rectangle.lower_left.cords
        x_2, y_2 = self.rectangle.upper_right.cords

        c_x = (x_1 + x_2) / 2
        c_y = (y_1 + y_2) / 2
        center = Point((c_x, c_y))

        bounds = (Point((x_1, y_1)), Point((x_2, y_2)), Point((x_2, y_1)), Point((x_1, y_2)))

        self.sw = QuadTree(
            Rectangle(bounds[0].lower_left(center), bounds[0].upper_right(center)),
            max_points=self.max_points, depth=self.depth + 1, visualizer=self.vis)
        self.ne = QuadTree(
            Rectangle(bounds[1].lower_left(center), bounds[1].upper_right(center)),
            self.max_points, self.depth + 1, self.vis)
        self.se = QuadTree(
            Rectangle(bounds[2].lower_left(center), bounds[2].upper_right(center)),
            self.max_points, self.depth + 1, self.vis)
        self.nw = QuadTree(
            Rectangle(bounds[3].lower_left(center), bounds[3].upper_right(center)),
            self.max_points, self.depth + 1, self.vis)

        self.divided = True

    def insert(self, point):
        if point.amount_of_dimensions != 2:
            raise ValueError("Niepoprawny wymiar punktów! \nQuadtree obsługuje tylko punkty dwueymiarowe!")
        if not self.rectangle.is_point_in_rectangle(point):
            return False
        if len(self.points) < self.max_points:
            self.points.append(point)
            if self.vis:
                self.vis.add_point(point.cords, color="#40BFEF")
            return True

        if not self.divided:
            self.divide()

        return (self.se.insert(point) or self.ne.insert(point) or
                self.sw.insert(point) or self.nw.insert(point))

    def search(self, boundary, found_points):
        if self.vis and self.depth == 0:
            self.vis.add_polygon(
                boundary.get_all_vertix_from_rectangle_on_2d(),
                fill=True,
                color="blue",
                alpha=0.1
            )
        
        if not self.rectangle.is_intersect(boundary):
            return False
        if self.vis:
            tmp = self.vis.add_polygon(
                self.rectangle.get_all_vertix_from_rectangle_on_2d(),
                fill=True,
                color="grey",
                alpha=0.2
            )
        for point in self.points:
            if boundary.is_point_in_rectangle(point):
                found_points.append(point)
                if self.vis:
                    self.vis.add_point(point.cords, color="lime")
        self.vis.remove_figure(tmp)

        if self.divided:
            self.se.search(boundary, found_points)
            self.ne.search(boundary, found_points)
            self.sw.search(boundary, found_points)
            self.nw.search(boundary, found_points)
        return found_points

def build_quadtree(points_tuples, max_points=3, visualizer=None):
    points, bounds = find_rectangle_conv_to_point(points_tuples)
    quadtree = QuadTree(bounds, max_points=max_points, visualizer=visualizer)
    for point in points:
        quadtree.insert(point)
    return quadtree

def find_rectangle_conv_to_point(points):
    lower_left = points[0]
    upper_right = points[0]
    res = [Point(points[0])]

    for point in points[1:]:
        lower_left = [(min(lower_left[i], point[i])) for i in range(2)]
        upper_right = [(max(upper_right[i], point[i])) for i in range(2)]
        res.append(Point(point))
    
    return res, Rectangle(Point(lower_left), Point(upper_right))
