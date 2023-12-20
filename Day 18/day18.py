from __future__ import annotations
from dataclasses import dataclass
from typing import List

with open('test1.txt', 'r') as file:
    lines = file.read().rsplit('\n')

@dataclass(frozen=True)
class Vector2:
    x: float
    y: float

    def magnitude(self):
        return pow(pow(self.x, 2) + pow(self.y, 2), 0.5)

    def __mul__(self, other: [int, float, Vector2]):
        if isinstance(other, (int, float)):
            return Vector2(self.y * other, self.x * other)
        if isinstance(other, Vector2):
            return Vector2(self.y * other.y, self.x * other.x)
        raise TypeError(f'Unsupported Operand for Vector2 Multiplication with {type(other)}')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return self.__mul__(-1)

    def __add__(self, other: Vector2):
        return Vector2(self.y + other.y, self.x + other.x)

    def __sub__(self, other: Vector2):
        return self.__add__(-other)

    def __str__(self):
        return f'({self.y}, {self.x})'

    def __repr__(self):
        return self.__str__()

class Curve:
    def __init__(self, points: List[Vector2]):
        self.points = points

    def calc_perimeter(self):
        perimeter = 0
        length = len(self.points)
        for i in range(1, len(self.points) + 1):
            perimeter += (self.points[i % length] - self.points[i - 1]).magnitude()
        return perimeter

# (direction, meters, colour)
dig_plan = [(d, int(n), c[2:-1]) for [d, n, c] in [line.split(' ') for line in lines]]

direction_key_vector = {
    'U': Vector2(-1, 0),
    'D': Vector2(1, 0),
    'L': Vector2(0, -1),
    'R': Vector2(0, 1)
}

points = []
start_pos = Vector2(0, 0)
current_pos = start_pos
for (direction_key, distance, color) in dig_plan:
    direction = direction_key_vector[direction_key]
    current_pos += direction * distance
    points.append(current_pos)

curve = Curve(points)
print(curve.calc_perimeter())

