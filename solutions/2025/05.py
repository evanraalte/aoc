from typing import Any
from functools import reduce

def a(input: str) -> Any:
    fresh_ranges, ingredient_ids = input.split("\n\n")
    fresh_ranges = fresh_ranges.splitlines()
    ingredient_ids = ingredient_ids.splitlines()

    fresh_ranges_parsed = []

    for r in fresh_ranges:
        start, stop = r.split("-")
        start, stop = int(start), int(stop)
        fresh_ranges_parsed.append((start,stop))

    total = 0

    for ingr in ingredient_ids:
        ingr = int(ingr)
        for f_min, f_max in fresh_ranges_parsed:
            if ingr >= f_min and ingr <= f_max:
                total += 1
                print(f"Added {ingr}")
                break
    return total


def merge_int_intervals(intervals):
    intervals.sort()

    merged = []
    cur_s, cur_e = intervals[0]

    for s, e in intervals[1:]:
        if s <= cur_e:        # overlapping or touching
            cur_e = max(cur_e, e)
        else:
            merged.append((cur_s, cur_e))
            cur_s, cur_e = s, e

    merged.append((cur_s, cur_e))
    return merged

def b(input: str) -> Any:
    fresh_ranges, _ = input.split("\n\n")
    fresh_ranges = fresh_ranges.splitlines()

    intervals = []

    for r in fresh_ranges:
        start, stop = r.split("-")
        start, stop = int(start), int(stop)
        intervals.append((start,stop))

    merged = merge_int_intervals(intervals)

    total = 0
    for _from, _to in merged:
        total += _to - _from + 1
    return total