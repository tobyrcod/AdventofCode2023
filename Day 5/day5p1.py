import math
from itertools import groupby

file = open("input.txt")
lines = file.read().splitlines()
file.close()

verbose = False
def printv(message):
    if not verbose:
        return
    print(message)

# TODO: Learn some proper passing methods (maybe regex) because this is a mess
# Split by empty array elements
lines = [list(g) for k, g in groupby(lines, key=bool) if k]

[seeds] = lines[0]
seeds = map(int, seeds[seeds.index(':') + 2:].split())

def parse_xy_map(xy_map):
    xy_rules = dict()
    for [y, x, length] in xy_map:
        xy_rules[x] = y
        if x + length not in xy_rules:
            xy_rules[x + length] = x + length
    return xy_rules

def apply_xy_rules(seed, xy_rules):
    min_key = -1
    for key in sorted(xy_rules.keys()):
        if key > seed:
            break
        min_key = key

    diff = 0 if min_key == -1 else xy_rules[min_key] - min_key
    return seed + diff

raw_maps = [[list(map(int, x.split())) for x in rm[1:]] for rm in lines[1:]]
rules = [parse_xy_map(rm) for rm in raw_maps]

min_location = math.inf
for seed in seeds:
    code = seed
    for rule in rules:
        printv(code)
        printv(rule)
        code = apply_xy_rules(code, xy_rules=rule)
        printv(code)
        printv('----')
    min_location = min(code, min_location)

print(min_location)
