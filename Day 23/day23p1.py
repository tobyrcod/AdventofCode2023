from typing import List

from utils.graph import Vector2, Grid
from queue import Queue
import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')

GRID = Grid(np.array([list(row) for row in lines], dtype=str))

START = GRID.top_left + Vector2(1, 0)
END = GRID.bottom_right - Vector2(1, 0)

SLOPE_DIRECTIONS = {'^': Vector2(0, -1), '>': Vector2(1, 0), 'v': Vector2(0, 1), '<': Vector2(-1, 0)}

path_costs: List[int] = []
agents: Queue[tuple[Vector2, set[Vector2], int]] = Queue()
agents.put((START, set(), 0))
while not agents.empty():
    current_pos, seen, cost = agents.get()
    new_seen = set(seen)
    new_seen.add(current_pos)

    # Have we reached the end?
    if current_pos == END:
        path_costs.append(cost)
        continue

    # Can we proceed?
    tile = GRID[current_pos]
    if tile == '#':
        continue

    # Are we slipping?
    slip = SLOPE_DIRECTIONS.get(tile, None)
    if slip:
        if (slip_pos := current_pos + slip) not in seen:
            agents.put((slip_pos, new_seen, cost + 1))
        continue

    # No? Make a regular move
    for neighbour in GRID.get_neighbourhood(current_pos):
        if neighbour in seen:
            continue

        agents.put((neighbour, new_seen, cost + 1))

print(path_costs[-1])
