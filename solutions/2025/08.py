from functools import reduce
import math
from typing import Any


def get_distance(p0: tuple[int,int,int], p1: tuple[int,int,int]) -> float:
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    return math.sqrt((x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2)

def pop_chain(chains: list, p) -> set:
    for idx, c in enumerate(chains):
        if p in c:
            return chains.pop(idx) # pop and return chain
    return set([p]) # single link chain

def a(input: str) -> Any:
    distances = {}
    chains : list[set]= []
    coords = [tuple(map(int,c.split(","))) for c in input.splitlines()]
    for a in range(len(coords)):
        for b in range(len(coords)):
            if (b,a) in distances:
                continue
            if b == a:
                continue
            distances[(a,b)] = get_distance(coords[a],coords[b])
    distances_increasing = dict(sorted(distances.items(), key=lambda x: x[1]))
    limit = 1000
    for (p0,p1),distance in distances_increasing.items():
        if limit == 0:
            break
        print(f"From {coords[p0]} to {coords[p1]}, distance {distance}")
        new_chain = pop_chain(chains, p0) | pop_chain(chains,p1)
        chains.append(new_chain)
        limit -= 1
    three_largest_chains = sorted(chains, key=len)[-3:]
    res = reduce(lambda a,b: a*b, map(len,three_largest_chains))
    return res



def b(input: str) -> Any:
    distances = {}
    chains : list[set]= []
    coords = [tuple(map(int,c.split(","))) for c in input.splitlines()]
    for a in range(len(coords)):
        for b in range(len(coords)):
            if (b,a) in distances:
                continue
            if b == a:
                continue
            distances[(a,b)] = get_distance(coords[a],coords[b])
    distances_increasing = dict(sorted(distances.items(), key=lambda x: x[1]))
    for (p0,p1),distance in distances_increasing.items():
        print(f"From {coords[p0]} to {coords[p1]}, distance {distance}")
        new_chain = pop_chain(chains, p0) | pop_chain(chains,p1)
        chains.append(new_chain)
        if len(chains) == 1 and len(chains[0]) == len(coords):
            # one circuit!
            return coords[p0][0] * coords[p1][0]
