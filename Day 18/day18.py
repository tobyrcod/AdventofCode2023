from __future__ import annotations
from dataclasses import dataclass
from utils.graph import Vector2, Polygon
from typing import List
import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')


# (direction, meters, colour)
dig_plan = [(d, int(n), c[2:-1]) for [d, n, c] in [line.split(' ') for line in lines]]
start_pos = Vector2(0, 0)

def get_part1_poly():
    poly = Polygon()

    directions = {'U': Vector2(0, 1), 'D': Vector2(0, -1),
                  'L': Vector2(-1, 0), 'R': Vector2(1, 0)}
    current_pos = start_pos
    for direction_key, distance, _ in dig_plan:
        current_pos += directions[direction_key] * distance
        poly.add_point(current_pos)

    return poly

def get_part2_poly():
    poly = Polygon()

    directions = {3: Vector2(0, 1), 1: Vector2(0, -1),
                  2: Vector2(-1, 0), 0: Vector2(1, 0)}
    current_pos = start_pos
    for *_, hex in dig_plan:
        distance, direction_key = int(hex[:-1], 16), int(hex[-1])
        current_pos += directions[direction_key] * distance
        poly.add_point(current_pos)

    return poly

poly = get_part2_poly()
print(poly.area_with_thickness)
