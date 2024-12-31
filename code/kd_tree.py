import math
from Point import Point
from Rectangle import Rectangle
from copy import deepcopy
# import tests.generate_tests as test
class KdTreeNode:
    def __init__(self,points, dimensions_amount,depth,rectangle, is_points_in_vertix=True):
        """
        inicjalizacja wierzchołka w strukturze kd_drzewa

        Args:
        points (list Point): Lista punktów jako krotki współrzędnych, które "obejmuje" dany wierzchołek
        dimensions_amount (int): Liczba wymiarów punktów
        depth (int): Głębokość wierzchołka w drzewie
        rectangle (Rectangle): prostokąt, który należy do tego wierzchołka
        is_points_in_vertix (bool): True - tablice punktów są zapisywane w każdym wierzchołku
                                    False - tylko w liściach
        """
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
        """
        zwykły binary search, wybierający skrajnie prawy spośród tych samych wartości w tablicy

        Args:
        t (list Point): Lista punktów 
        index (int): W tym przypadku określa w którym wymiarze szukamy
        val (int): Szukana wartość
        Return:
        Skrajnie prawy indeks punktu o wartości val
        """

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
        """
        zwykły binary search, wybierający skrajnie lewy spośród tych samych wartości w tablicy

        Args:
        t (list Point): Lista punktów 
        index (int): W tym przypadku określa w którym wymiarze szukamy
        val (int): Szukana wartość
        Return:
        Skrajnie lewy indeks punktu o wartości val
        """

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
        """
        Rekurencyjne budowanie kolejnych Node'ów w drzewie

        Args:
        points (list Point): Lista punktów jako krotki współrzędnych, które "obejmuje" dany wierzchołek
        """
        for _ in range(self.dimensions_amount):
            points.sort(key = lambda x: x.cords[self.dimension_number])
            median = math.ceil(len(points)/2)
            median = self.bsearch_right(points,self.dimension_number,points[median].cords[self.dimension_number])
            left_median = self.bsearch_left(points,self.dimension_number,points[median].cords[self.dimension_number])

            if median - left_median > 3*len(points)//4:
                self.depth +=1
                self.dimension_number = (self.dimension_number+1)%self.dimensions_amount
            else:
                break

        self.axis = points[median-1].cords[self.dimension_number]
        left_rec, right_rec = self._split_region(self.rectangle, self.dimension_number, self.axis)
        self.left = KdTreeNode(points[0:median], self.dimensions_amount, self.depth+1, left_rec, self.is_points_in_vertix )
        self.right = KdTreeNode(points[median:], self.dimensions_amount, self.depth+1, right_rec, self.is_points_in_vertix )
    
    def _split_region(self,rec, dimension_numer, axis):
        """
        Dzielenie prostokąta na dwa rozłączne prostokąty wzdłóż osi dzielącej

        Args:
        rec (Rectangle): prostokąt do podzielenia
        dimension_numer (int): numer wymiaru względem, którego dzielimy obszar
        axis (float): wartość wspłrzędnej lini podziału

        Return:
        Zwraca dwa rozłączne prostokąty
        """
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
        """
        Sprawdza, czy dany Node jest liściem

        Return:
        bool - czy Node jest liściem
        """
        return self.left is None and self.right is None

    def get_points(self):
        """
        Znajduje punkty, które "należą" do tego wierzchołka drzewa

        Return:
        list (Point) - lista punktów "należących" do tego wierzchołka drzewa
        """
        if self.is_points_in_vertix or self.is_leaf():
            return self.points
        else:
            return self.left.get_points() + self.right.get_points()

    def find_points_in_region(self,region):
        """
        Rekurencyjnie znajduje wszystkie punkty, które należą do drzewa ukorzenionego
        w tym wierzchołku w obszarze zadanym przez region

        Args:
        region (Rectangle) - prostokąt, w obrębie którego szukamy punktow
        Return:
        list (Point) - lista punktów zawierających sie w tym prostokącie
        """
        if self.is_leaf():
            is_in = region.is_point_in_rectangle(self.points[0])
            return self.points if is_in else []
        
        if region.is_contained(self.rectangle):
            return self.get_points()
        
        if region.is_intersect(self.rectangle):
            return self.left.find_points_in_region(region) + self.right.find_points_in_region(region)
        return []
    
    def check_contains(self,point):
        """
        Rekurencyjnie sprawdza, czy punkt znajduje się w drzewie ukorzenionym w tym wierzchołku

        Args:
        point (Point) - punkt, którego przynależność do drzewa chcemy sprwdzić
        Return:
        bool - czy punkt znajduje się w obrębię drzewa ukorzenionego w tym wierzchołku
        """
        if self.is_leaf():
            return point == self.points[0]
        if self.axis < point.cords[self.dimension_number]:
            return self.right.check_contains(point)
        return self.left.check_contains(point)
    
class KdTree:
    def __init__(self, points, dimensions_amount, begining_axis=0, is_points_in_vertix = False):
        """
        inicjalizacja samej struktury kd_drzewa

        Args:
        points (list): Lista punktów jako krotki współrzędnych
        dimensions_amount (int): Liczba wymiarów punktów
        begining_axis (int): Numer współrzędnej od której będziemy zaczynać podział zbioru punktów
        is_points_in_vertix (bool): True - tablice punktów są zapisywane w każdym wierzchołku
                                    False - tylko w liściach
        """

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
        """
        Znajduje punkty w zadanym obszarze

        Args:
        region (Rectangle lub list): prostokąt zadanych przez strukturę Rectangle
                                     lub tablice krotek współrzędnych lewego dolnego i prawego górnego rogu
        
        Return:
        zwraca tablice krotek współrzędnych punktów zawartch w prostokącie
        """
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
        """
        Sprawdza, czy punkt zawiera się w prostokącie

        Args:
        point (Point, list) - punkt zadanych przez strukturę Point
                              lub tablice krotek współrzędnych punktu
        Return:
        bool - czy punkt zawiera się w strukturze
        """
        if not isinstance(point, Point):
            if len(point) != self.dimensions_amount:
                raise ValueError("Podano nieprawidołowy punkt do znalezienia")
            point = Point(point)
        return self.root.check_contains(point)
    