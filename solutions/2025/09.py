from typing import Any



def a(input: str) -> Any:
    coords = [tuple(map(int,p.split(","))) for p in input.splitlines()]
    
    max_surface = 0
    for i in range(len(coords)):
        for j in range(len(coords)):
            surface = calc_surface(coords[i], coords[j])
            if surface > max_surface:
                max_surface = surface
            
    return max_surface

def calc_surface(p0, p1):
    return (abs(p0[0] - p1[0])+1) * (abs(p0[1] - p1[1]+1))


def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)

    px1, py1 = polygon[0]
    for i in range(n+1):
        px2, py2 = polygon[i % n]

        # Check if point lies on edge
        if (min(px1, px2) <= x <= max(px1, px2) and 
            min(py1, py2) <= y <= max(py1, py2) and
            (px2 - px1) * (y - py1) == (py2 - py1) * (x - px1)):
            return True

        # Standard ray casting
        if ((py1 > y) != (py2 > y)):
            xinters = px1 + (y - py1) * (px2 - px1) / (py2 - py1)
            if xinters == x:  # on boundary
                return True
            if xinters > x:
                inside = not inside

        px1, py1 = px2, py2

def get_all_points(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    xmin, xmax = min(x0, x1), max(x0, x1)
    ymin, ymax = min(y0, y1), max(y0, y1)
    return [(x, y) for x in range(xmin, xmax+1) 
                   for y in range(ymin, ymax+1)]


def rectangle_edge_points(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    
    xmin, xmax = sorted((x0, x1))
    ymin, ymax = sorted((y0, y1))

    points = set()

    # bottom edge (xmin → xmax at y = ymin)
    for x in range(xmin, xmax + 1):
        points.add((x, ymin))

    # top edge (xmin → xmax at y = ymax)
    for x in range(xmin, xmax + 1):
        points.add((x, ymax))

    # left edge (ymin → ymax at x = xmin)
    for y in range(ymin, ymax + 1):
        points.add((xmin, y))

    # right edge (ymin → ymax at x = xmax)
    for y in range(ymin, ymax + 1):
        points.add((xmax, y))

    return list(points)


from multiprocessing import Pool, Manager, cpu_count
from tqdm import tqdm

def check_rectangle(args):
    i, j, coords, shared_max, lock = args
    p0 = coords[i]
    p1 = coords[j]

    # Compute surface early
    surface = calc_surface(p0, p1)

    # Early prune
    if surface <= shared_max.value:
        return 0

    # Compute rectangle edge points
    edge_points = rectangle_edge_points(p0, p1)

    # Check polygon containment
    for pt in edge_points:
        if not point_in_polygon(pt, coords):
            return 0

    # If valid and bigger, update global max safely
    with lock:
        if surface > shared_max.value:
            shared_max.value = surface

    return surface


def b(input: str):
    coords = [tuple(map(int,p.split(","))) for p in input.splitlines()]
    n = len(coords)

    # Build unique rectangle tasks
    tasks = []
    seen = set()
    for i in range(n):
        for j in range(n):
            if (j, i) in seen:
                continue
            seen.add((i, j))
            tasks.append((i, j))

    # Shared max between processes
    manager = Manager()
    shared_max = manager.Value('i', 0)
    lock = manager.Lock()

    # Pack arguments
    task_args = [(i, j, coords, shared_max, lock) for i, j in tasks]

    # Parallel with progress bar
    with Pool(cpu_count()) as pool:
        for _ in tqdm(pool.imap_unordered(check_rectangle, task_args),
                      total=len(task_args)):
            pass

    return shared_max.value