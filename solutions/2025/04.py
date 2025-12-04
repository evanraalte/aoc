from typing import Any
import itertools


def get_grid(input: str):
    grid = {}
    data = input.splitlines()
    x_len = len(data[0])
    y_len = len(data)
    for y in range(y_len):
        for x in range(x_len):
            grid[(x,y)] = data[y][x]
    return grid

around = set(itertools.product([-1,0,1],[-1,0,1]))
around.remove((0,0))

def can_remove(grid: dict):
    to_remove = []
    for coord, occupant in grid.items():
        if occupant == "@":
            neighbours = 0
            for delta in around:
                dx,dy = delta
                x,y = coord
                nx = x+dx
                ny = y+dy
                if (nx,ny) in grid and grid[(nx,ny)] == "@":
                    neighbours += 1
            if neighbours < 4:
                to_remove.append((x,y))

    return to_remove

def a(input: str) -> Any:
    grid = get_grid(input)
    return len(can_remove(grid))



def b(input: str) -> Any:
    grid = get_grid(input)
    total = 0
    while to_remove := can_remove(grid):
        for coord in to_remove:
            grid[coord] = "."
        removed = len(to_remove)
        total += removed
    return total
