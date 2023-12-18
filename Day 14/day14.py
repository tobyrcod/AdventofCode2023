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

CYCLE = [NORTH, WEST, SOUTH, EAST]
NUM_CYCLES = 1000000000

height, width = len(lines), len(lines[0])
print(f'height: {height}, width: {width}')

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
    EAST: lambda c: -c[1],
    WEST: lambda c: c[1]
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

def calc_load():
    return sum(map(calc_rock_load, rocks))

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

def find_rocks_period():
    past_rocks = list()
    past_rocks.append(set(rocks))
    for i in range(NUM_CYCLES):
        for direction in CYCLE:
            move_rocks(direction)

        if rocks in past_rocks:
            offset = past_rocks.index(rocks)
            print(f'repeats state {offset} after {i - offset + 1} iterations')
            return offset, i - offset + 1

        past_rocks.append(set(rocks))
    return 0, -1

def apply_cycles(num_cycles):
    for i in range(num_cycles):
        for direction in CYCLE:
            move_rocks(direction)

offset, period = find_rocks_period()
apply_cycles((NUM_CYCLES - offset) % period if period != -1 else NUM_CYCLES)
print(f'total load after {NUM_CYCLES} cycles: {calc_load()}')
