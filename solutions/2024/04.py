from typing import Any


def a(input: str) -> Any:
    """
    Solution for part A.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """

    # TODO: Implement solution for part A
    input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    occurences = 0
    lines = input.splitlines()
    # horizontal checks
    for l in lines:
        occurences += l.count("XMAS")
        occurences += l.count("SAMX")

    # vertical checks:
    for row in range(len(lines) - 4+1):
        cols = len(lines[0])
        for m in range(cols):
            tmp = "".join(lines[n][m] for n in range(row, row+4))
            if tmp in ["XMAS", "SAMX"]:
                print("Vertical")
                occurences += 1

    # diagonals
    rows = len(lines)
    cols = len(lines[0])

    for r in range(rows - 3):
        for c in range(cols - 3):
            # ↘ diagonal
            tmp = "".join(lines[r+i][c+i] for i in range(4))
            if tmp in ("XMAS", "SAMX"):
                occurences += 1

    for r in range(rows - 3):
        for c in range(3, cols):
            # ↙ diagonal
            tmp = "".join(lines[r+i][c-i] for i in range(4))
            if tmp in ("XMAS", "SAMX"):
                occurences += 1

    return occurences


def b(input: str) -> Any:
    """
    Solution for part B.

    Args:
        input: The puzzle input as a string

    Returns:
        The answer as something that can be parsed as string
    """

#     input = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX"""


    pattern_variants = [
        ["M.S",
         ".A.",
         "M.S"],
        # the other unique orientations (rotations/reflections)
        ["S.M",
         ".A.",
         "S.M"],
        ["M.M",
         ".A.",
         "S.S"],
        ["S.S",
         ".A.",
         "M.M"],
    ]

    lines = input.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    occurrences = 0

    def match_at(r, c, pat):
        # pat is list of 3 strings length 3, '.' is wildcard
        for i in range(3):
            for j in range(3):
                ch = pat[i][j]
                if ch == ".":
                    continue
                if lines[r + i][c + j] != ch:
                    return False
        return True

    for r in range(rows - 2):
        for c in range(cols - 2):
            for pat in pattern_variants:
                if match_at(r, c, pat):
                    occurrences += 1

    return occurrences
