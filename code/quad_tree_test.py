# testy zarówno zawierania się jak i znajdowania punktów
# dla całkowitoliczbowych i zmiennoprzecinkowych
# losowe testy na wszystkich randomowych testach
import tests.generate_tests as test
import brute_force as brute
from quad_tree import *

def get_sets_from_array(quadtree_ans, brute_ans):
    for i in range(len(quadtree_ans)):
        quadtree_ans[i]=tuple(quadtree_ans[i])
        brute_ans[i]=tuple(brute_ans[i])
    return set(quadtree_ans),set(brute_ans)

def _run_test_rectangle(points,ll,ur , k=2):
    quad_tree = build_quadtree(points)
    quadtree_ans = quad_tree.search(Rectangle(Point(ll), Point(ur)), [])
    brute_ans = brute.brute_force_rectangle(points,ll,ur)
    set_quad, set_brute = get_sets_from_array(quadtree_ans, brute_ans)
    if set_quad != set_brute:
        print("Zły wynik przeszukiwania w quadtree")
    return set_quad == set_brute

def _run_test_contains(points):
    QuadTree = build_quadtree(points)
    for point in points:
        if not QuadTree.contains(point):
            print("sprawdzanie przynależności punktu do zbioru niezaliczone")
            return False # nie znalezniono punktu
    return True

def run_circle_test():
    points = test.generate_random_on_circle(100,10,12)
    ll = (0,0)
    ur = (13,13)
    return _run_test_rectangle(points,ll,ur) and _run_test_contains(points)

def run_on_line_test():
    points = test.generate_random_on_line(100,1,1,0,20,2)
    ll = (4,3)
    ur = (13,20)
    return _run_test_rectangle(points,ll,ur) and _run_test_contains(points)
def run_grid_normal_test():
    points = test.generate_grid_normal(100,1,20,1,20)
    ll = (4,3)
    ur = (13,20)
    return _run_test_rectangle(points,ll,ur) and _run_test_contains(points)

def run_cross_on_axes_test():
    points = test.generate_cross_on_axes(100,-10,10,-10,10)
    ll = (-4,-3)
    ur = (4,8)
    return _run_test_rectangle(points,ll,ur) and _run_test_contains(points)

def run_uniform_distribution_test():
    points = test.generate_uniform_distribution(100,-10,50,-10,50)
    ll = (-4,-3)
    ur = (13,20)
    return _run_test_rectangle(points,ll,ur) and _run_test_contains(points)

def run_clasters_test():
    points = test.generate_clasters(100,3,-10,50,-10,50)
    ll = (-4,-3)
    ur = (13,20)
    return _run_test_rectangle(points,ll,ur) and _run_test_contains(points)

def run_random_points_on_rectangle_test():
    points = test.generate_random_points_on_rectangle(100,-10,50,-10,50)
    ll = (-15,-3)
    ur = (13,20)
    return _run_test_rectangle(points,ll,ur) and _run_test_contains(points)

def run_standard_distribution_test():
    points = test.generate_standard_distribution(100,10,20,3,10)
    ll = (-15,-3)
    ur = (13,20)
    return _run_test_rectangle(points,ll,ur) and _run_test_contains(points)


def start_generate_test():
    # Pobierz wszystkie funkcje w globalnym zakresie, które zaczynają się od "run"
    run_functions = [func for name, func in globals().items() if callable(func) and name.startswith("run")]
    n_test = len(run_functions)
    correct = 0
    str = ''
    # Uruchom każdą funkcję
    for func in run_functions:
        print("----------------------------------------------------")
        print(f"Uruchamianie: {func.__name__}")
        if func():
            print(f"Zaliczone: {func.__name__}")
            correct += 1
            str += "Z "
    print("----------------------------------------------------")
    print(f"Zaliczone {correct}/{n_test} testów")
    print(str)
    print("----------------------------------------------------")




# nie wiem czy jest potrzebne skoro poprzednie testy były bardziej wymagające niż to
# a to jest z wiki
def intiger_cords_rectangle():
    pass
def float_cords_rectangle():
    pass
def intiger_cords_point_search():
    pass
def float_cords_rectangle_point_search():
    pass