from typing import Any


def a(input: str) -> Any:
    """
    Solution for part A.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """
    turns = input.splitlines()
    position = 50
    zero_count = 0
    for turn in turns:
        direction = turn[0]
        amount = int(turn[1:])
        if direction == "R":
            position += amount
        else:
            position -= amount
        position = position % 100
        if position == 0:
            zero_count += 1


    return zero_count


def b(input: str) -> Any:
    turns = input.splitlines()
    position = 50
    zero_count = 0
    for turn in turns:
        direction = turn[0]
        amount = int(turn[1:])

        # count full cycles
        zero_count += amount // 100
        # normalize
        amount %= 100

        old_position = position

        if direction == "R":
            position += amount
        else:
            position -= amount
        # increase when out of valid bounds 0-99, unless it was already 0 before
        if old_position != 0 and position <= 0 or position >= 100:
            zero_count += 1
        position %= 100
        
    return zero_count
