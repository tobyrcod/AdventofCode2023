import numpy as np
from bidict import bidict

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
directions = {
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
    '|': np.array([directions['N'], directions['S']]),
    # Horizontal Pipe: connecting E and W
    '-': np.array([directions['E'], directions['W']]),
    # 90-Bend: connecting N and E
    'L': np.array([directions['N'], directions['E']]),
    # 90-Bend: connecting N and W
    'J': np.array([directions['N'], directions['W']]),
    # 90-Bend: connecting S and W
    '7': np.array([directions['S'], directions['W']]),
    # 90-Bend: connecting S and E
    'F': np.array([directions['S'], directions['E']])
}
connection_directions['S'] = np.append(connection_directions['|'], (connection_directions['-']), axis=0)

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
print(len(path) / 2)


