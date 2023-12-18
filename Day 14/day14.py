file = open("input.txt")
lines = file.read().splitlines()
file.close()

MOVE_ROCK = 'O'
STATIONARY_ROCK = '#'
EMPTY = '.'

NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

height, width = len(lines), len(lines[0])

rocks = set()
stationary = set()
for y, row in enumerate(lines):
    for x, value in enumerate(row):
        if value == MOVE_ROCK:
            rocks.add((y, x))
        if value == STATIONARY_ROCK:
            stationary.add((y, x))

direction_sort_key = {
    NORTH: lambda c: c[0],
    SOUTH: lambda c: -c[0],
    EAST: lambda c: c[1],
    WEST: lambda c: -c[1]
}

direction_delta = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    EAST: (0, 1),
    WEST: (0, -1)
}

def is_position_valid(position):
    y, x = position
    return 0 <= y < height and 0 <= x < width

def is_position_clear(position):
    return is_position_valid(position) and position not in rocks and position not in stationary

def apply_move(position, delta):
    return position[0] + delta[0], position[1] + delta[1]

def move_rocks(direction):
    delta = direction_delta[direction]
    for rock in sorted(rocks, key=direction_sort_key[direction]):
        new_rock = rock
        while is_position_clear(new_position := apply_move(new_rock, delta)):
            new_rock = new_position

        if rock == new_rock:
            continue

        rocks.remove(rock)
        rocks.add(new_rock)

def calc_rock_load(rock):
    return height - rock[0]

def visualise():
    grid = [[EMPTY for x in range(width)] for y in range(height)]
    for y in range(height):
        for x in range(width):
            coord = (y, x)
            if coord in rocks:
                grid[y][x] = MOVE_ROCK
            elif coord in stationary:
                grid[y][x] = STATIONARY_ROCK

    for row in grid:
        print(row)

move_rocks(NORTH)

load = sum(map(calc_rock_load, rocks))
print(load)
