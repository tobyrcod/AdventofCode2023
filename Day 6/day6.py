file = open("input.txt")
lines = file.read().splitlines()
file.close()

def part1():
    return zip(*[map(int, line[line.index(':') + 2:].split()) for line in lines])


def part2():
    return [[int(''.join(line[line.index(':') + 2:].split())) for line in lines]]


races = part2()
winning_prod = 1
for race_length, goal_distance in races:
    hold_times = list(range(1, race_length))
    distance_travelled = map(lambda hold_time: hold_time*(race_length-hold_time), hold_times)
    winning_prod *= len([dist for dist in distance_travelled if dist > goal_distance])
print(winning_prod)
