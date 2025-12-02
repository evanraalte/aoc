from typing import Any


def a(input: str) -> Any:
    """
    Solution for part A.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """
    invalid_id_sum = 0
    ranges = [_range.split("-") for _range in input.split(",")]
    for _range in ranges:
        for _id in range(int(_range[0]),int(_range[1])+1):
            _id_str = str(_id)
            if len(_id_str) % 2 == 0:
                _part1 = _id_str[0:len(_id_str)//2]
                _part2 = _id_str[len(_id_str)//2:]
                if _part1 == _part2:
                    invalid_id_sum += _id
            else:
                continue

    return invalid_id_sum


def chunkstring(string, length):
    return [string[0+i:length+i] for i in range(0, len(string), length)]


def check_invalid(_id: int):
    _id = str(_id)
    if _id in (_id+_id)[1:-1]:
        return True
    return False

def b(input: str) -> Any:
    invalid_id_sum = 0
    ranges = [_range.split("-") for _range in input.split(",")]
    for _range in ranges:
        for _id in range(int(_range[0]),int(_range[1])+1):
            if check_invalid(_id):
                invalid_id_sum += _id
    return invalid_id_sum
