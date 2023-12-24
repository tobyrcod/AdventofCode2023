from typing import Dict, List
from utils.graph import Vector2, Grid
from collections import deque
from queue import Queue

# New ideas:
# https://aoc-puzzle-solver.streamlit.app
# https://www.youtube.com/watch?v=6fG8T5bEPv4

# I tried for too many hours to get a single DFS working with a global seen set,
# but completely forgot that cycles exist!

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')

MAZE: Grid = Grid([list(row) for row in lines])

START: Vector2 = MAZE.top_left + Vector2(1, 0)
END: Vector2 = MAZE.bottom_right - Vector2(1, 0)

# First step: Construct a Graph with DFS where nodes are intersections of grid
nodes: set[Vector2] = {START, END}
edges: Dict[Vector2, List[tuple[Vector2, int]]] = {START: list(), END: list()}

# frontier: (current_pos, previous_node, cost)
frontier: deque[tuple[Vector2, Vector2, set[Vector2]]] = deque()
frontier.append((START, START, {START}))
while frontier:
    current_pos, previous_node, seen = frontier.pop()
    cost = len(seen) - 1

    # Found the end
    if current_pos == END:
        edges[previous_node].append((END, cost))
        continue

    neighbors = MAZE.get_neighbourhood(current_pos, exclude_values=set('#'))
    neighbors.difference_update(seen)

    # Found a dead-end
    if len(neighbors) == 0:
        continue

    # Found a simple corridor
    if len(neighbors) == 1:
        neighbor = neighbors.pop()
        frontier.append((neighbor, previous_node, seen | {neighbor}))
        continue

    # Found an intersection
    if (current_pos, cost) in edges[previous_node]:
        continue
    edges[previous_node].append((current_pos, cost))
    if current_pos not in edges:
        edges[current_pos] = list()
    edges[current_pos].append((previous_node, cost))
    # Start new paths blocking the way we came, until we hit the next intersection or the end
    for neighbor in neighbors:
        frontier.append((neighbor, current_pos, {current_pos, neighbor}))

print('bfs')

# BFS Traverse simplified graph to find the longest path
frontier: deque[tuple[Vector2, set[Vector2], int]] = deque()
frontier.append((START, {START}, 0))
max_cost: int = -1
while frontier:
    current_node, seen, cost = frontier.popleft()

    if current_node == END:
        max_cost = max(max_cost, cost)
        continue

    for neighbour_node, edge_cost in edges[current_node]:
        if neighbour_node in seen:
            continue
        frontier.append((neighbour_node, seen | {neighbour_node}, cost + edge_cost))

print(max_cost)
