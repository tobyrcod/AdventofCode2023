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
MIRROR_FUNCS = dict(zip(_list_mirrors, [lambda c: (-c[1], -c[0]), lambda c: (c[1], c[0])]))

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

def calc_energy_from_light_origin(position, direction):
    frontier = collections.deque()
    frontier.append((position, direction))
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

    return len(seen_light)

def part1():
    return calc_energy_from_light_origin((0, 0), RIGHT)

def part2():
    max_energy = 0
    for y in range(HEIGHT):
        for light in [((y, 0), RIGHT), ((y, WIDTH-1), LEFT)]:
            energy = calc_energy_from_light_origin(*light)
            if energy > max_energy:
                max_energy = energy

    for x in range(WIDTH):
        for light in [((0, x), DOWN), ((HEIGHT-1, x), UP)]:
            energy = calc_energy_from_light_origin(*light)
            if energy > max_energy:
                max_energy = energy

    return max_energy

answer = part2()
print(answer)
