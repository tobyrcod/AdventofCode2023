file = open("input.txt")
lines = file.read().splitlines()
file.close()

lines = [line[line.find(':') + 2:] for line in lines]
games = [[set(map(int, p.split())) for p in line.split(' | ')] for line in lines]

points = 0
for winner, given in games:
    matched = given.intersection(winner)
    if matched:
        score = pow(2, len(matched) - 1)
        points += score

print(points)
