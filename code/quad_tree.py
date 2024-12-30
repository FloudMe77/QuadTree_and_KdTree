import math
from Point import Point
from Rectangle import Rectangle
import tests.generate_tests as test

class QuadTree:
    # Struktura danych Quad-tree

    def __init__(self, rectangle, max_points = 3, depth = 0):
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.rectangle = rectangle
        self.max_points = max_points
        self.points = []
        self.depth = depth

        # Flag which is used to check if this rectangle is divided
        self.divided = False

    def divide(self):
        x_1, y_1 = self.rectangle.lower_left.cords
        x_2, y_2 = self.rectangle.upper_right.cords

        c_x = (x_1 + x_2) / 2
        c_y = (y_1 + y_2) / 2

        center = Point((c_x, c_y))

        bounds = (Point((x_1, y_1)), Point((x_2, y_2)), Point((x_2, y_1)), Point((x_1, y_2)))

        self.sw = QuadTree(Rectangle(bounds[0].lower_left(center), bounds[0].upper_right(center)), self.max_points, self.depth + 1)
        self.ne = QuadTree(Rectangle(bounds[1].lower_left(center), bounds[1].upper_right(center)), self.max_points, self.depth + 1)
        self.se = QuadTree(Rectangle(bounds[2].lower_left(center), bounds[2].upper_right(center)), self.max_points, self.depth + 1)
        self.nw = QuadTree(Rectangle(bounds[3].lower_left(center), bounds[3].upper_right(center)), self.max_points, self.depth + 1)

        self.divided = True

    def insert(self, point):
        if not self.rectangle.is_contained(point):
            return False
        if len(self.points) < self.max_points:
            self.points.append(point)
            return True

        if not self.divided:
            self.divide()

        return self.se.insert(point) or self.ne.insert(point) or self.sw.insert(point) or self.nw.insert(point)

    def search(self, boundary, found_points):
        if not self.rectangle.is_intersect(boundary):
            return False

        for point in self.points:
            if self.se.is_contained(point):
                found_points.append(point)

        if self.divided:
            self.se.search(boundary, found_points)
            self.ne.search(boundary, found_points)
            self.sw.search(boundary, found_points)
            self.nw.search(boundary, found_points)
        return found_points