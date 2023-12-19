import collections

import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')

MAZE = np.array([list(row) for row in lines])
HEIGHT, WIDTH = MAZE.shape

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

EMPTY = {"."}

_list_mirrors = ["/", "\\"]
MIRRORS = set(_list_mirrors)
MIRROR_FUNCS = dict(zip(_list_mirrors, [lambda c: (-c[1],-c[0]), lambda c: (c[1], c[0])]))

_list_splitters = ["|", "-"]
SPLITTERS = set(_list_splitters)
SPLITTER_DIRECTIONS = dict(zip(_list_splitters, [{UP, DOWN}, {LEFT, RIGHT}]))

def is_valid_position(position):
    y, x = position
    return 0 <= y < HEIGHT and 0 <= x < WIDTH

def new_position(position, direction):
    y, x = position
    dy, dx = direction
    return y + dy, x + dx

frontier = collections.deque()
frontier.append(((0, 0), RIGHT))
seen_light = dict()

while frontier:
    light = frontier.pop()
    position, direction = light

    if not is_valid_position(position):
        continue
    if position not in seen_light:
        seen_light[position] = set()
    if direction in seen_light[position]:
        continue
    seen_light[position].add(direction)

    obstacle = MAZE[position]
    if obstacle in EMPTY:
        frontier.append((new_position(position, direction), direction))
        continue

    if (splitter := obstacle) in SPLITTERS:
        split_directions = SPLITTER_DIRECTIONS[splitter]
        if direction in split_directions:
            frontier.append((new_position(position, direction), direction))
            continue

        for split_direction in split_directions:
            frontier.append((new_position(position, split_direction), split_direction))
        continue

    if (mirror := obstacle) in MIRRORS:
        new_direction = MIRROR_FUNCS[mirror](direction)
        frontier.append((new_position(position, new_direction), new_direction))

print(len(seen_light))
