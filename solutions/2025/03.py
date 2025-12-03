from typing import Any

def best_n_digit_number(n, bank: str) -> int:
    remove = len(bank) - n
    stack = []
    for digit in bank:
        while remove > 0 and stack and stack[-1] < digit:
            stack.pop()
            remove -= 1
        
        stack.append(digit)

    if remove > 0:
        stack = stack[:-remove]  
    return int("".join(stack))

def a(input: str) -> Any:
    total = 0
    for bank in input.splitlines():
        total += best_n_digit_number(2, bank)
    return total


def b(input: str):
    total = 0
    for bank in input.splitlines():
        total += best_n_digit_number(12, bank)
    return total

