from typing import Any


def a(input: str) -> Any:
    rows = input.splitlines()
    splits = 0
    rows[0] = rows[0].replace("S","|")
    rows = [list(r) for r in rows]
    for i in range(1,len(rows)):
        for j in range(0,len(rows[0])):
            if rows[i][j] == "^" and rows[i-1][j] == "|":
                splits += 1
                rows[i][j-1] = "|"
                rows[i][j+1] = "|"
            elif rows[i-1][j] == "|":
                rows[i][j] = "|"
    return splits



def calc_timelines(rows, position, cache=None):
    if cache is None:
        cache = {}

    if position in cache:
        return cache[position]

    i, j = position
    if i < len(rows) - 1:
        if rows[i+1][j] == "^":
            result = calc_timelines(rows, (i+1, j+1), cache) + \
                     calc_timelines(rows, (i+1, j-1), cache)
        else:
            result = calc_timelines(rows, (i+1, j), cache)
    else:
        result = 1

    cache[position] = result
    return result

def b(input: str) -> Any:
    rows = input.splitlines()
    timelines = 0
    start_pos = rows[0].find("S")
    timelines +=  calc_timelines(rows, (0,start_pos))
    return timelines