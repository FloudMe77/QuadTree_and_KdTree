# testy zarówno zawierania się jak i znajdowania punktów
# dla całkowitoliczbowych i zmiennoprzecinkowych
# losowe testy na wszystkich randomowych testach
import tests.generate_tests as test
import brute_force as brute
from kd_tree import KdTree

def get_sets_from_array(kd_ans, brute_ans):
    for i in range(len(kd_ans)):
        kd_ans[i]=tuple(kd_ans[i])  
        brute_ans[i]=tuple(brute_ans[i])
    return set(kd_ans),set(brute_ans)

def _run_test_rectangle(points,ll,ur , k=2):
    kd_tree = KdTree(points, k)
    kd_ans = kd_tree.find_points_in_region((ll,ur))
    brute_ans = brute.brute_force_rectangle(points,ll,ur)
    set_kd, set_brute = get_sets_from_array(kd_ans, brute_ans)
    assert set_kd == set_brute, "Sety nie są identyczne"
    print("szukanie w prostokącie zaliczone")

def _run_test_contains(points):
    kd_tree = KdTree(points, 2)
    for point in points:
        assert kd_tree.check_contains(point), "nie znalezniono punktu"
    print("sprawdzanie przynależności punktu do zbioru zaliczone")

def run_circle_test():
    points = test.generate_random_on_circle(100,10,12)
    ll = (0,0)
    ur = (13,13)
    _run_test_rectangle(points,ll,ur)
    _run_test_contains(points)

def run_on_line_test():
    points = test.generate_random_on_line(100,1,1,0,20,2)
    ll = (4,3)
    ur = (13,20)
    _run_test_rectangle(points,ll,ur)
    _run_test_contains(points)

def run_grid_normal_test():
    points = test.generate_grid_normal(100,1,20,1,20)
    ll = (4,3)
    ur = (13,20)
    _run_test_rectangle(points,ll,ur)
    _run_test_contains(points)

def run_cross_on_axes_test():
    points = test.cross_on_axes(100,-10,10,-10,10)
    ll = (-4,-3)
    ur = (4,8)
    _run_test_rectangle(points,ll,ur)
    _run_test_contains(points)

def run_random_points_test():
    points = test.random_points(100,-10,50,-10,50)
    ll = (-4,-3)
    ur = (13,20)
    _run_test_rectangle(points,ll,ur)
    _run_test_contains(points)

def run_clasters_test():
    points = test.generate_clasters(100,3,-10,50,-10,50)
    ll = (-4,-3)
    ur = (13,20)
    _run_test_rectangle(points,ll,ur)
    _run_test_contains(points)

def run_random_points_on_rectangle_test():
    points = test.generate_random_points_on_rectangle(100,-10,50,-10,50)
    ll = (-15,-3)
    ur = (13,20)
    _run_test_rectangle(points,ll,ur)
    _run_test_contains(points)

def run_standard_distribution_test():
    points = test.generate_standard_distribution(100,10,20,3,10)
    ll = (-15,-3)
    ur = (13,20)
    _run_test_rectangle(points,ll,ur)
    _run_test_contains(points)

def run_multidimensional_cluster_test():
    points = test.generate_multidimensional_cluster(5,2,10,4)
    ll = (-3,0,0,0)
    ur = (10,10,10,10)
    _run_test_rectangle(points,ll,ur,4)
    # _run_test_contains(points,4)

def start_generate_test():
    # Pobierz wszystkie funkcje w globalnym zakresie, które zaczynają się od "run"
    run_functions = [func for name, func in globals().items() if callable(func) and name.startswith("run")]

    # Uruchom każdą funkcję
    for func in run_functions:
        print(f"Uruchamianie: {func.__name__}")
        func()


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