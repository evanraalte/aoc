import re
from typing import Any


def a(input: str) -> Any:
    """
    Solution for part A.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """
    # input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    matches = re.findall(r"mul\((\d+),(\d+)\)", input)
    total = 0
    for m in matches:
        x,y = m
        total += int(x)*int(y)
    return total


def b(input: str) -> Any:
    """
    Solution for part B.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """
    # input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    matches = re.findall(r"mul\((\d+),(\d+)\)", input)
    total = 0
    enabled = True
    pos = 0
    for m in matches:
        x,y = m
        last_pos = pos
        # get position of expression.
        pos = input.find(f"mul({x},{y})")
        if "don't()" in input[last_pos:pos]:
            enabled = False
        if "do()" in input[last_pos:pos]:
            enabled = True
        if enabled:
            total += int(x)*int(y)
    return total
