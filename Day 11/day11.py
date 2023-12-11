import numpy as np

file = open("input.txt")
lines = file.read().splitlines()
file.close()

SYMBOL_SPACE = '.'
SYMBOL_GALAXY = '#'

EXPANSION_SCALE = 1_000_000

universe = np.array([list(line) for line in lines], dtype=object)
observed_shape = universe.shape

# Expand the universe
axis_expansion = list()
for axis in range(len(observed_shape)):
    empty = set((np.where(np.all(universe == SYMBOL_SPACE, axis=axis)))[0])
    axis_expansion.append(empty)

# Get the galaxies
galaxies = np.argwhere(universe == SYMBOL_GALAXY)

# Find the distance between galaxies
def galaxy_distance(g1, g2):
    # Valid as galaxies are allows to path through other galaxies,
    # so no collisions/pathfinding is needed
    y1, x1 = g1
    y2, x2 = g2

    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    travelled_x = set(range(x1+1, x2+1))
    travelled_y = set(range(y1+1, y2+1))

    distances_x = [EXPANSION_SCALE if x in axis_expansion[0] else 1 for x in travelled_x]
    distances_y = [EXPANSION_SCALE if y in axis_expansion[1] else 1 for y in travelled_y]

    return sum(distances_x) + sum(distances_y)


# Find the distances between every pair of galaxies
total_distance = 0
for i, g1 in enumerate(galaxies):
    for g2 in galaxies[i+1:]:
        total_distance += galaxy_distance(g1, g2)
print(total_distance)
