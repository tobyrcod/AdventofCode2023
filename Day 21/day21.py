from utils.graph import Vector2, Grid
from queue import Queue
import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')

PART = 2
map = np.array([list(row) for row in lines], dtype=str)
GRID = Grid(map)

rocks = GRID.find_all('#')
start = GRID.find_first('S')

# If we have an odd number of steps remaining, we can't return.
# If we have an even number of steps remaining, we can return (go back and forth over and over from where you came)
START_STEPS = 64
frontier: Queue[tuple[Vector2, int]] = Queue()
frontier.put((start, START_STEPS))
seen: set[Vector2] = {start}
reachable = set()

while not frontier.empty():
    current_pos, steps_remaining = frontier.get()
    tile: str = GRID[current_pos]
    if tile == '#':
        continue

    if steps_remaining % 2 == 0:
        reachable.add(current_pos)

    if steps_remaining <= 0:
        continue

    neighbourhood = GRID.get_neighbourhood(current_pos)
    for neighbor in neighbourhood:
        if neighbor in seen:
            continue
        seen.add(neighbor)
        frontier.put((neighbor, steps_remaining - 1))

print(len(reachable))

