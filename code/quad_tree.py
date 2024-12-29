import math
from Point import Point
from Rectangle import Rectangle
import tests.generate_tests as test

class QuadTree:
    # Struktura danych Quad-tree

    def __init__(self, rectangle, max_points = 3, depth = 0):
        self.sw = None
        self.se = None
        self.rectangle = rectangle
        self.max_points = max_points
        self.points = []
        self.depth = depth

        # Flag which is used to check if this rectangle is divided
        self.divided = False


        