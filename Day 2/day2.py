import numpy as np

file = open("input.txt")
lines = file.read().splitlines()
file.close()

dict_color_code = {
    'red': np.array([1, 0, 0]),
    'green': np.array([0, 1, 0]),
    'blue': np.array([0, 0, 1])
}
def prep_cubes(cubes):
    cubes = cubes.split(', ')
    cubes = [tuple(cube.split(' ')) for cube in cubes]

    code = np.array([0, 0, 0])
    for (quantity, color) in cubes:
        code += int(quantity) * dict_color_code[color]
    return code

lines = [line[line.find(':') + 2:] for line in lines]
games = [line.split('; ') for line in lines]
games = [np.array([prep_cubes(cubes) for cubes in game]) for game in games]

games_max = [np.amax(game, axis=0) for game in games]

def part1():
    max = np.array([12, 13, 14])

    impossible_games = np.any(games_max - max > 0, axis=1)
    impossible = impossible_games.nonzero()[0]
    impossible += 1

    n = len(lines)
    games_sum = int(0.5 * n * (n + 1))

    print(games_sum - sum(impossible))

def part2():
    powers = np.prod(games_max, axis=1)
    print(sum(powers))

part2()
