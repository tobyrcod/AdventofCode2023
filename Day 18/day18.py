from __future__ import annotations
from dataclasses import dataclass
from typing import List
import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')


@dataclass(frozen=True)
class Vector2:
    x: float
    y: float

    def magnitude(self):
        return pow(pow(self.x, 2) + pow(self.y, 2), 0.5)

    def __mul__(self, other: [int, float, Vector2]):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        raise TypeError(f'Unsupported Operand for Vector2 Multiplication with {type(other)}')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return self.__mul__(-1)

    def __add__(self, other: [int, float, Vector2]):
        if isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        raise TypeError(f'Unsupported Operand for Vector2 Addition with {type(other)}')

    def __sub__(self, other: [int, float, Vector2]):
        return self.__add__(-other)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()


class Polygon:
    def __init__(self, points: List[Vector2] = None):
        if points is None:
            points = []

        self.__points = points

    def add_point(self, point: Vector2):
        if not isinstance(point, Vector2):
            raise TypeError(f'Cannot add type {type(point)} to Curve')
        self.__points.append(point)

    @property
    def perimeter(self):
        perimeter = 0
        for i in range(len(self.__points)):
            perimeter += (self.__points[i] - self.__points[i - 1]).magnitude()
        return perimeter

    @property
    def area(self):
        # Shoelace formula (https://en.wikipedia.org/wiki/Shoelace_formula)
        area = 0
        length = len(self.__points)
        for i in range(length):
            a = self.__points[i]
            b = self.__points[(i + 1) % length]
            area += (a.x * b.y - b.x * a.y)
        return abs(area / 2)

    @property
    def area_with_thickness(self):
        # Need to adjust the area to include the thickness entire cells we are in, not just the points
        # The entire perimeter needs to be expanded 0.5 out to reach the edge of the cell from the center it is now
        # And then +1 for the external angles that needed to be expanded 0.75 each (360 degrees worth for a polygon)
        return int(self.area + 0.5 * self.perimeter + 1)

    def __str__(self):
        return ', '.join([str(p) for p in self.__points])


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
