import random
import numpy as np
def generate_random_on_circle(n,R,r):
    # okrąg w środku (0,0)
    # losuje punkty na ringu r,R
    if R<r:
        R,r = r,R
    ans = []
    for _ in range(n):
        fi = np.random.uniform(0,2*np.pi)
        x = np.random.uniform(r,R) * np.cos(fi)
        y = np.random.uniform(r,R) * np.sin(fi)
        ans.append((x,y))
    return ans

def generate_random_on_line(n,a,b,min_x,max_x,thick):
    ans = []
    for _ in range(n):
        x = np.random.uniform(min_x, max_x)
        y = a*x + b + np.random.uniform(-thick, thick)
        ans.append((x, y))
    return ans

def generate_grid_normal(n, lower_left, upper_right):
    # n - ilość punktów w lini
    x1,y1 = lower_left
    x2,y2 = upper_right
    gap_x = (x2-x1)/(n-1)
    gap_y = (y2-y1)/(n-1)
    ans = []
    for i in range(n):
        for j in range(n):
            ans.append((x1 + i * gap_x, y1 + j * gap_y))
    return ans

def generate_on_one_ax(n,min_x,max_x,y=0):
    ans=[]
    for _ in range(n):
        ans.append((np.random.uniform(min_x,max_x),y))
    return ans

def cross_on_axes(n,min_x,max_x,min_y,max_y):
    ans=[]
    for _ in range(n):
        if random.choice([True,False]):
            ans.append((np.random.uniform(min_x,max_x),0))
        else:
            ans.append((0, np.random.uniform(min_y,max_y)))
    return ans
def generate_points(n, m, min_x, max_x, min_y, max_y):

    # wzięte z chata
    """
    Generuje n punktów rozmieszczonych w m skupiskach na obszarze ograniczonym przez (min_x, max_x) i (min_y, max_y).

    Args:
        n (int): Liczba punktów do wygenerowania.
        m (int): Liczba skupisk.
        min_x (float): Minimalna wartość x.
        max_x (float): Maksymalna wartość x.
        min_y (float): Minimalna wartość y.
        max_y (float): Maksymalna wartość y.

    Returns:
        list: Lista punktów jako dwuelementowych krotek (x, y).
    """
    # Ustalenie centrów skupisk
    cluster_centers = [
        (np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y))
        for _ in range(m)
    ]
    
    # Przydział punktów do skupisk
    points_per_cluster = np.random.multinomial(n, [1/m] * m)
    
    points = []
    for i, center in enumerate(cluster_centers):
        cluster_x, cluster_y = center
        cluster_points = np.column_stack((
            np.random.normal(loc=cluster_x, scale=(max_x - min_x) / (4 * m), size=points_per_cluster[i]),
            np.random.normal(loc=cluster_y, scale=(max_y - min_y) / (4 * m), size=points_per_cluster[i]),
        ))
        points.extend([tuple(point) for point in cluster_points])
    
    return points