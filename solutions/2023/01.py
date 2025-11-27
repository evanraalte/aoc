from curses.ascii import isdigit
nums = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def a(input : str) -> str:
    lines = input.splitlines()
    print(input)
    total = 0
    for line in lines:
        digits = []
        for char in line:
            if isdigit(char):
                digits.append(int(char))
        total += digits[0]*10 + digits[-1]
    return total


def b(input : str) -> str:
    lines = input.splitlines()
    total = 0
    for line in lines:
        digits = []
        for k,v in nums.items():
            digits += [(i,v) for i in range(len(line)) if line.startswith(k, i)]
            digits += [(i,v) for i in range(len(line)) if line.startswith(str(v), i)]
        digits.sort()
        total += digits[0][1]*10 + digits[-1][1]
    return total
