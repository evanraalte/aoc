from typing import Any
from functools import reduce

def compute(a, operator, b):
    if operator == "*":
        return a*b
    return a+b

def a(input: str) -> Any:
    _rows = input.splitlines()
    rows = []
    for _row in _rows:
        cols = _row.split()
        rows.append([c for c in cols if c != ['']])

    operators = rows[-1]
    total = [int(c) for c in rows[0]]
    for row in rows[1:-1]:
        total = [
            compute(total[i], operators[i], int(row[i]))
        for i in range(len(total))]
    return sum(total)


def parse_operators(operators_row: str):
    operators = []
    for idx, c in enumerate(operators_row):
        if c in "*+":
            operators.append((c,idx))
    operators_new = []
    for idx in range(len(operators)):
        o, _min = operators[idx]
        _max = operators[idx+1][1] if idx < (len(operators) -1)  else len(operators_row)
        operators_new.append((o ,_min, _max))
    return operators_new


def b(input: str) -> Any:
    """
    Solution for part B.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """

    # TODO: Implement solution for part B
    _rows = input.splitlines()
    # find the operand indices
    operators = parse_operators(_rows[-1])
    col_sum = 0
    for op, _min, _max in operators:
        numbers = []
        for digit_idx in range(_min,_max):
            number = ""
            for _r in _rows[:-1]:
                number +=  _r[digit_idx]
            if not number.strip() == "":
                numbers.append( int(number.strip()))
        if op == "*":
            col_sum += reduce(lambda a,b: a*b, numbers )
        else:
            col_sum += reduce(lambda a,b: a+b, numbers )

    return col_sum
