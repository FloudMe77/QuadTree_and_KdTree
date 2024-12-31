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

def generate_grid_normal(n, min_x,max_x,min_y,max_y):
    # n - ilość punktów w lini
    gap_x = (max_x-min_x)/(n-1)
    gap_y = (max_y-min_y)/(n-1)
    ans = []
    for i in range(n):
        for j in range(n):
            ans.append((min_x + i * gap_x, min_y + j * gap_y))
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

def random_points(n,min_x,max_x,min_y,max_y):
    res=[]
    for _ in range(n):
        res.append((np.random.uniform(min_x,max_x),np.random.uniform(min_y,max_y)))
    return res

def generate_clasters(n, m, min_x, max_x, min_y, max_y):

    # po poprawkach działa dobrze
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
        (min_x + (i+1)*(max_x-min_x), min_y + (i+1)*(max_y-min_y))
        for i in range(m)
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

def generate_random_points_on_rectangle(n, min_x, max_x, min_y, max_y):
    # Oblicz długości boków prostokąta
    width = max_x - min_x
    height = max_y - min_y
    perimeter = 2 * (width + height)
    
    # Losowo rozmieszczamy punkty na obwodzie
    points = []
    random_distances = np.random.uniform(0, perimeter, n)  # Losowe odległości na obwodzie

    for distance in random_distances:
        if distance <= width:  # Górny bok
            x = min_x + distance
            y = max_y
        elif distance <= width + height:  # Prawy bok
            x = max_x
            y = max_y - (distance - width)
        elif distance <= 2 * width + height:  # Dolny bok
            x = max_x - (distance - (width + height))
            y = min_y
        else:  # Lewy bok
            x = min_x
            y = min_y + (distance - (2 * width + height))

        points.append((x, y))

    return points

def add_outliners(n,list,min_x,max_x,min_y,max_y):
    outliners = random_points(n,5*min_x,5*max_x,5*min_y,5*max_y)
    return list+outliners

def generate_standard_distribution(n,mean_x, mean_y, std_x, std_y):
    """
    Generuje n punktów w jednym skupisku, korzystając z rozkładu normalnego.

    Args:
        mean_x (float): Średnia dla współrzędnej x.
        mean_y (float): Średnia dla współrzędnej y.
        std_x (float): Odchylenie standardowe dla współrzędnej x.
        std_y (float): Odchylenie standardowe dla współrzędnej y.
        n (int): Liczba punktów do wygenerowania.

    Returns:
        list: Lista punktów jako dwuelementowych krotek (x, y).
    """
    x_coords = np.random.normal(loc=mean_x, scale=std_x, size=n)
    y_coords = np.random.normal(loc=mean_y, scale=std_y, size=n)
    return list(zip(x_coords, y_coords))
## dorobić rozkład normalny

def generate_multidimensional_cluster(mean, std, n, k):
    """
    Generuje punkty w k-wymiarowej przestrzeni zgodnie z rozkładem normalnym.

    Args:
        mean (float): Średnia dla każdego wymiaru.
        std (float): Odchylenie standardowe dla każdego wymiaru.
        n (int): Liczba punktów do wygenerowania.
        k (int): Liczba wymiarów przestrzeni.

    Returns:
        np.ndarray: Macierz o wymiarach (n, k), gdzie każda kolumna to wymiar, a każdy wiersz to punkt.
    """
    # Tworzymy macierz punktów (n punktów, każdy o k wymiarach)
    points = np.random.normal(loc=mean, scale=std, size=(n, k))
    return points

## dodać funkcje zbiorczą