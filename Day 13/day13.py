import numpy as np
file = open("input.txt")
lines = file.read().split("\n\n")
patterns = [np.asarray([list(row) for row in pattern]) for pattern in [line.split('\n') for line in lines]]
file.close()

# ---------------------------
# Fun Mini Golf Solution

NUM_ERRORS = 1

def hamming_distance(l, r):
    return sum(a != b for a, b in zip(l, r))

def find_row_mirror(pattern):
    return next((i for i in range(1, len(pattern)) if sum([hamming_distance(l, r) for l, r in zip(np.flip(pattern[:i], axis=0), pattern[i:])]) == NUM_ERRORS), 0)

def solve():
    return sum(100*find_row_mirror(pattern) + find_row_mirror(pattern.T) for pattern in patterns)

print(solve())

