from __future__ import annotations
from dataclasses import dataclass
from typing import List, Callable
import numpy as np


@dataclass(frozen=True)
class Vector2:
    x: float
    y: float

    def magnitude(self):
        return pow(pow(self.x, 2) + pow(self.y, 2), 0.5)

    @property
    def as_index(self):
        return self.y, self.x

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


class Grid:

    _cardinal_directions = {Vector2(0, 1), Vector2(1, 0), Vector2(-1, 0), Vector2(0, -1)}
    _diagonal_directions = {Vector2(1, 1), Vector2(-1, 1), Vector2(-1, -1), Vector2(1, -1)}

    def __init__(self, array: np.array):
        self.array = array
        self.height, self.width = array.shape

    def __getitem__(self, coord: Vector2):
        return self.array[coord.as_index]

    def find_all(self, item) -> List[Vector2]:
        return [Vector2(x, y) for y, x in np.argwhere(self.array == item)]

    def find_first(self, item) -> Vector2:
        # Silly but works for now
        return self.find_all(item)[0]

    def is_valid_position(self, coord: Vector2):
        return 0 <= coord.y < self.height and 0 <= coord.x < self.width

    def get_neighbourhood(self, coord: Vector2,
                          include_self: bool = False,
                          include_cardinals: bool = True,
                          include_diagonals: bool = False,
                          include_invalid: bool = False):
        directions = set()
        if include_cardinals:
            directions |= Grid._cardinal_directions
        if include_diagonals:
            directions |= Grid._diagonal_directions
        if include_self:
            directions |= {Vector2(0, 0)}

        return {coord + direction for direction in directions
                if include_invalid | self.is_valid_position(coord + direction)}


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