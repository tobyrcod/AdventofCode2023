file = open("input.txt")
lines = file.read().splitlines()
file.close()

def part1():
    return zip(*[map(int, line[line.index(':') + 2:].split()) for line in lines])


def part2():
    return [[int(''.join(line[line.index(':') + 2:].split())) for line in lines]]

# Get the races we want to test for
races = part2()

# Trivial way still only took ~1s for part 2, but I want to make it better as I see easy quadratic here
def brute_force():
    winning_prod = 1
    for race_length, goal_distance in races:
        hold_times = list(range(1, race_length))
        distance_travelled = map(lambda hold_time: hold_time*(race_length-hold_time), hold_times)
        winning_prod *= len([dist for dist in distance_travelled if dist > goal_distance])
    print(winning_prod)


# Pure math solution by finding the intersection of distance travelled and goal distance
def math_solution():
    import math
    """
    Math Explanation:

    Let total time (t) be the race_length
    Distance travelled (d) is quadratic in hold time (h): d = h(t-h) = -h^2 + th
    We have to travel over goal_distance (g)
    So we want d > g => -h^2 + th > g
    Rearranging we get critical values at: h^2 - th + g = 0
    Solve using quadratic formula: x = (-b += root(b^2 - 4ac))/2a
    So h = (t += root(t^2 - 4g)) / 2
    To get a critical range with two critical points (c1, c2)
    We want to be an int above the goal, so we need to smallest int higher than the lower bound (b1)
    and the highest int smaller than the upper bound (b2)
    All values in this range [b1, b2] are above the goal distance (due to -h^2 "unhappy" shape of quadratic)
    Example: https://www.desmos.com/calculator/khx3f7oddp
    """
    winning_prod = 1
    for race_length, goal_distance in races:
        discriminant = pow(race_length, 2) - 4*goal_distance
        root = pow(discriminant, 0.5)
        c1, c2 = (race_length - root) / 2, (race_length + root) / 2
        b1, b2 = math.floor(c1 + 1), math.ceil(c2 - 1)
        num_solutions = b2 - b1 + 1
        winning_prod *= num_solutions
    print(winning_prod)

math_solution()
