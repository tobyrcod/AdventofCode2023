import heapq
import math

import numpy as np
from typing import List

with open('test1.txt', 'r') as file:
    lines = file.read().rsplit('\n')

MAP = np.array([list(row) for row in lines], dtype=object)
HEIGHT, WIDTH = MAP.shape

ROT_90 = math.radians(90)
DIRECTION_CHAR = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, -1): "<",
    (0, 1): ">"
}

def is_valid_position(position):
    y, x = position
    return 0 <= y < HEIGHT and 0 <= x < WIDTH

def new_position(position, direction):
    y, x = position
    dy, dx = direction
    return y + dy, x + dx

class Node:
    def __init__(self, position: tuple[int, int], bearing: float, bearing_count: int, cost: int, previous):
        self.position = position
        self.bearing = bearing
        self.bearing_count = bearing_count
        self.cost = cost
        self.previous = previous

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return f"{self.position} {self.cost} {DIRECTION_CHAR[get_bearing_direction(self.bearing)]}"

    def __repr__(self):
        return self.__str__()

def get_bearing_direction(theta: float):
    return int(-math.sin(theta)), int(math.cos(theta))

def get_moves(node: Node):
    theta = node.bearing

    facing = get_bearing_direction(theta)
    left = get_bearing_direction(theta + ROT_90)
    right = get_bearing_direction(theta - ROT_90)

    dirs = [(facing, theta), (left, theta+ROT_90), (right, theta-ROT_90)]
    poss = [(new_position(node.position, dir), theta) for (dir, theta) in dirs]
    return [(pos, theta) for (pos, theta) in poss if is_valid_position(pos)]

class MinHeap:
    def __init__(self):
        self.__elements: List[Node] = []

    def push(self, node: Node) -> None:
        heapq.heappush(self.__elements, node)

    def pop(self) -> Node:
        return heapq.heappop(self.__elements)

    def __bool__(self):
        return bool(self.__elements)

    def __str__(self):
        return str(self.__elements)

    def __len__(self):
        return len(self.__elements)

def find_min_path(end_pos: tuple[int, int]):
    start_pos = (0, 0)
    nodes = {start_pos: Node(start_pos, 0, 0, 0, None)}
    frontier = MinHeap()
    frontier.push(nodes[start_pos])

    while frontier:
        current_node: Node = frontier.pop()
        if current_node.position == end_pos:
            path = list()
            node = current_node
            while node:
                path.append(node)
                node = node.previous
            path.reverse()
            return path

        for position, bearing in get_moves(current_node):
            move_bearing_count = current_node.bearing_count + 1 if bearing == current_node.bearing else 1
            # if move_bearing_count > 3:
            #    continue

            cost = current_node.cost + int(MAP[position])
            move_node = nodes.get(position, None)
            if move_node and move_node.cost <= cost:
                continue

            nodes[position] = Node(position, bearing, move_bearing_count, cost, current_node)
            frontier.push(nodes[position])

    return None

path = find_min_path((HEIGHT - 1, WIDTH - 1))
if path:
    for node in path:
        MAP[node.position] = DIRECTION_CHAR[get_bearing_direction(node.bearing)]

print(MAP)

