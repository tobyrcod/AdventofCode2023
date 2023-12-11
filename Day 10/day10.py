import time

import numpy as np
from bidict import bidict
from collections import deque

np.set_printoptions(linewidth=np.inf)

file = open("input.txt")
lines = file.read().splitlines()
file.close()

lines = np.array([np.array(list(line)) for line in lines])
height, width = lines.shape

def is_valid_coord(y, x):
    return 0 <= x < width and 0 <= y < height

s_positions = np.argwhere(lines == 'S')
assert len(s_positions) == 1

# Coordinates in (y, x) form, with (0, 0) top left
cardinal_directions = {
    # North
    'N': np.array([-1, 0]),
    # South
    'S': np.array([1, 0]),
    # East
    'E': np.array([0, 1]),
    # West
    'W': np.array([0, -1])
}
connection_directions = {
    # Vertical Pipe: connecting N and S
    '|': np.array([cardinal_directions['N'], cardinal_directions['S']]),
    # Horizontal Pipe: connecting E and W
    '-': np.array([cardinal_directions['E'], cardinal_directions['W']]),
    # 90-Bend: connecting N and E
    'L': np.array([cardinal_directions['N'], cardinal_directions['E']]),
    # 90-Bend: connecting N and W
    'J': np.array([cardinal_directions['N'], cardinal_directions['W']]),
    # 90-Bend: connecting S and W
    '7': np.array([cardinal_directions['S'], cardinal_directions['W']]),
    # 90-Bend: connecting S and E
    'F': np.array([cardinal_directions['S'], cardinal_directions['E']])
}
connection_directions['S'] = np.append(connection_directions['|'], (connection_directions['-']), axis=0)

def solve(part1=True):
    s_pos = tuple(s_positions[0])
    position = s_pos
    previous_positions = bidict()

    # Find the pipe cycle
    while s_pos not in previous_positions:
        # Get the symbol of our current position
        symbol = lines[position]
        # Get the neighbours of our position:
        #   So long as they are on the grid,
        #   We haven't already got this node in the path,
        #   and we aren't the previous coord of this position (as the start node loops)
        neighbours = {tuple(coord) for coord in connection_directions[symbol] + position
                      if is_valid_coord(*coord) and tuple(coord) not in previous_positions
                      and position != previous_positions.inverse.get(tuple(coord))}

        # We have the neighbour positions we need to check
        next_pipe_pos = None
        for neighbour in neighbours:
            # Check that the neighbour is a pipe
            symbol_neighbour = lines[neighbour]
            pipe_directions = connection_directions.get(symbol_neighbour, None)
            if pipe_directions is None:
                continue

            # Check that this pipe connects to our position
            pipe_connections = {tuple(coord) for coord in pipe_directions + neighbour
                                if is_valid_coord(*coord)}
            if position in pipe_connections:
                next_pipe_pos = neighbour
                break

        if not next_pipe_pos:
            raise Exception(f'No connecting pipe found for: {position}')

        previous_positions[next_pipe_pos] = position
        position = next_pipe_pos

    # Use the pipe cycle to find the furthest from start
    path = previous_positions.inverse.keys()
    if part1:
        return len(path) / 2

    # We are solving for part2,
    # so we now need to find the interior regions made by the path
    # First, find ALL regions made by the path with floodfill

    SYMBOL_EMPTY = " "
    SYMBOL_INSIDE = "I"
    SYMBOL_OUTSIDE = "O"

    # Use the path to solve for what 'S' should be
    c1, c2 = previous_positions[s_pos], previous_positions.inverse[s_pos]
    d1, d2 = (c1[0] - s_pos[0], c1[1] - s_pos[1]), (c2[0] - s_pos[0], c2[1] - s_pos[1])
    s_symbol = None
    for symbol, directions in connection_directions.items():
        if np.any(np.all(directions == d1, axis=1)) and np.any(np.all(directions == d2, axis=1)):
            s_symbol = symbol
            break
    if not s_symbol:
        raise Exception('Could not find the symbol for S')
    lines[s_pos] = s_symbol

    # Create the network describing the regions
    network = np.full((height, width), SYMBOL_EMPTY, dtype=object)
    for coord in path:
        network[coord] = lines[coord]

    # Quickly cache all the pipes that connect south
    south = cardinal_directions['S']
    pipes_south = set()
    for symbol, directions in connection_directions.items():
        if symbol == 'S':
            continue
        if np.any(np.all(directions == south, axis=1)):
            pipes_south.add(symbol)

    # Use shooting ray out from point and counting crossings method of point inside poly
    for y in range(height):
        outside = True
        for x in range(width):
            symbol = network[y][x]

            if symbol in pipes_south:
                outside = not outside
                continue

            if symbol == SYMBOL_EMPTY:
                network[y][x] = SYMBOL_OUTSIDE if outside else SYMBOL_INSIDE

            x += 1
        y += 1

    interior_positions = np.argwhere(network == SYMBOL_INSIDE)
    print(len(interior_positions))
    return


answer = solve(part1=False)

# Unused Code from when I used floodfill method (could still use, but not needed)
"""
def find_first(network, c):
    for y, row in enumerate(network):
        for x, value in enumerate(row):
            if value == c:
                return y, x
    return None

def floodfill(network, start_coord, symbol):
    def get_neighbours(y, x):
        return {tuple(coord) for coord in connection_directions['S'] + (y, x)
                if is_valid_coord(*coord)}

    frontier = deque()
    frontier.append(start_coord)
    seen = set(start_coord)
    while frontier:
        coord = frontier.pop()
        if network[coord] != SYMBOL_EMPTY:
            continue

        network[coord] = symbol
        for neighbour in get_neighbours(*coord):
            if neighbour in seen:
                continue
            frontier.append(neighbour)
            seen.add(neighbour)

region_id = 0
found_all_regions = False
while not found_all_regions:
    coord = find_first(network, SYMBOL_EMPTY)
    if coord:
        floodfill(network, coord, str(region_id))
        region_id += 1
    else:
        found_all_regions = True

# Now we have all the regions, we calculate if they are inside or outside
for id in range(region_id):
    region = str(id)
    coord = find_first(network, region)
    if not coord:
        raise Exception(f'Cant find region with id {id}')
    cross_count = 0
    y, x = coord
    row = network[y]
    for symbol in row[x:]:
        if symbol == "|":
            cross_count += 1
    print(id, cross_count)
    network[network == region] = SYMBOL_OUTSIDE if cross_count % 2 == 0 else SYMBOL_INSIDE
print(network)
interior_positions = np.argwhere(network == SYMBOL_INSIDE)
print(len(interior_positions))
"""
