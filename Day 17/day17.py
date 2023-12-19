import heapq
import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')

PART = 2
MAP = np.array([list(map(int, list(row))) for row in lines], dtype=int)
HEIGHT, WIDTH = MAP.shape

class MinHeap:
    def __init__(self):
        self.__elements = []

    def push(self, *args):
        heapq.heappush(self.__elements, args)

    def pop(self):
        return heapq.heappop(self.__elements)

    def __bool__(self):
        return bool(self.__elements)

def is_valid_position(position: tuple[int, int]):
    return 0 <= position[0] < HEIGHT and 0 <= position[1] < WIDTH

def add_vector2(a: tuple[int, int], b: tuple[int, int]):
    return a[0] + b[0], a[1] + b[1]

def find_min_path(end_pos: tuple[int, int], max_direction, turn_minimum) -> int:
    start_pos = (0, 0)

    frontier = MinHeap()
    frontier.push(0, start_pos, (0, 1), 0)
    seen = set()

    while frontier:
        cost, position, direction, direction_count = frontier.pop()

        if position == end_pos:
            return cost

        if (state := (position, direction, direction_count)) in seen:
            continue

        seen.add(state)

        candidates = []
        if direction_count >= turn_minimum:
            candidates.append((add_vector2(position, new_direction := (direction[1], -direction[0])), new_direction, 1))
            candidates.append((add_vector2(position, new_direction := (-direction[1], direction[0])), new_direction, 1))
        if direction_count < max_direction:
            candidates.append((add_vector2(position, direction), direction, direction_count + 1))

        for new_position, new_bearing, new_bearing_count in candidates:
            if not is_valid_position(new_position):
                continue

            new_cost = cost + MAP[new_position]
            frontier.push(new_cost, new_position, new_bearing, new_bearing_count)

    return -1

max_directions = [3, 10]
turn_minimums = [0, 4]
path = find_min_path(end_pos=(HEIGHT - 1, WIDTH - 1), max_direction=max_directions[PART-1], turn_minimum=turn_minimums[PART-1])
print(path)


