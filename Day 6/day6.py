file = open("input.txt")
lines = file.read().splitlines()
file.close()

races = zip(*[map(int, line[line.index(':') + 2:].split()) for line in lines])

winning_prod = 1
for race_length, goal_distance in races:
    hold_times = list(range(1, race_length))
    distance_travelled = map(lambda hold_time: hold_time*(race_length-hold_time), hold_times)
    winning_prod *= len([dist for dist in distance_travelled if dist > goal_distance])
print(winning_prod)
