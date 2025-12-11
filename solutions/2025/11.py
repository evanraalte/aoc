from typing import Any

def find_num_paths_to(pos, des_pos, lut, seen, cache = None):
    if cache is None:
        cache = {}
    if (pos,des_pos) in cache:
        return cache[(pos,des_pos)]
    if pos in seen:
        return 0

    if pos == des_pos:
        return 1

    seen.add(pos)

    total = 0
    for nxt in lut[pos]:
        total += find_num_paths_to(nxt, des_pos, lut, seen, cache)

    seen.remove(pos)
    cache[(pos,des_pos)] = total
    return total

def a(input: str) -> Any:
    lut = {}
    for line in input.splitlines():
        key, values = line.split(": ")
        lut[key] = values.split(" ")
    seen = set()
    paths =  find_num_paths_to("you", "out", lut, seen)
    return paths

def b(input: str) -> Any:
    lut = {}
    for line in input.splitlines():
        key, values = line.split(": ")
        lut[key] = values.split(" ")
    lut["out"] = []
    seen = set()

    a = find_num_paths_to("svr", "dac", lut, seen)
    b = find_num_paths_to("dac", "fft", lut, seen)
    c = find_num_paths_to("fft", "out", lut, seen)

    d = find_num_paths_to("svr", "fft", lut, seen)
    e = find_num_paths_to("fft", "dac", lut, seen)
    f = find_num_paths_to("dac", "out", lut, seen)
    return a*b*c + d*e*f
