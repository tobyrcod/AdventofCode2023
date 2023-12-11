import numpy as np

file = open("input.txt")
lines = file.read().splitlines()
file.close()

SYMBOL_SPACE = '.'
SYMBOL_GALAXY = '#'

universe = np.array([list(line) for line in lines], dtype=object)
observed_shape = universe.shape

# Expand the universe
for axis in range(len(observed_shape)):
    empty = (np.where(np.all(universe == SYMBOL_SPACE, axis=axis)))[0]
    repeats = np.ones(observed_shape[axis], dtype=int)
    repeats[empty] += 1
    universe = np.repeat(universe, repeats=repeats, axis=1-axis)

# Get the galaxies
galaxies = np.argwhere(universe == SYMBOL_GALAXY)

# Find the distance between galaxies
def galaxy_distance(g1, g2):
    # Valid as galaxies are allows to path through other galaxies,
    # so no collisions/pathfinding is needed
    x1, y1 = g1
    x2, y2 = g2
    return abs(x1 - x2) + abs(y1 - y2)

# Find the distances between every pair of galaxies
total_distance = 0
for i, g1 in enumerate(galaxies):
    for g2 in galaxies[i+1:]:
        total_distance += galaxy_distance(g1, g2)
print(total_distance)
