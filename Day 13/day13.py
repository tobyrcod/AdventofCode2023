import sys

import numpy as np

file = open("input.txt")
lines = file.read().split("\n\n")
file.close()

patterns = [np.asarray([list(row) for row in pattern]) for pattern in [np.array(line.split('\n')) for line in lines]]

def find_row_mirror(pattern):
    # irow represents the row we are trying to see if it's the mirror
    return next((i for i in range(1, len(pattern)) if all([all(l == r) for l, r in zip(np.flip(pattern[:i], axis=0), pattern[i:])])), -1)

def solve():
    total = 0
    for pattern in patterns:
        # Horizontal Mirror
        mirror = find_row_mirror(pattern)
        if mirror != -1:
            total += 100 * mirror
            continue

        # Vertical Mirror
        mirror = find_row_mirror(pattern.T)
        if mirror != -1:
            total += mirror
    print(total)

solve()


def tests():
    assert list(zip([0, 1, 2], [3, 4, 5])) == [(0, 3), (1, 4), (2, 5)]
    assert list(zip(reversed([0, 1, 2]), [3, 4, 5])) == [(2, 3), (1, 4), (0, 5)]
    assert list(zip([0, 1], [3, 4, 5])) == [(0, 3), (1, 4)]
    assert list(zip([0, 1, 2], [3, 4])) == [(0, 3), (1, 4)]
    assert list(zip([0, 1, 2], [])) == []

