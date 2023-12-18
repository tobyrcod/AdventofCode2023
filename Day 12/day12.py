from itertools import product
from collections import Counter

SYMBOL_OPERATIONAL = '.'
SYMBOL_DAMAGED = '#'
SYMBOL_UNKNOWN = '?'

SHOULD_UNFOLD = True

file = open("input.txt")
lines = file.read().splitlines()
file.close()

lines = [
    (
        filter(None, groups.split('.')),
        pattern,
    )
    for groups, pattern in [line.split() for line in lines]]

dict_group_codes = dict()

def cross_groups(a, b):
    if not a:
        return b
    if not b:
        return a

    counts = dict()
    for (x, y) in product(a, b):
        key = f'{x},{y}'
        if x == '0':
            key = y
        elif y == '0':
            key = x

        if key not in counts:
            counts[key] = 0
        counts[key] += a[x] * b[y]
    return counts

def resolve_group(group):
    if not group:
        return Counter({'0': 1})

    codes = dict_group_codes.get(group)
    if codes:
        return codes

    unknowns = [i for i, symbol in enumerate(group) if symbol == SYMBOL_UNKNOWN]
    if len(unknowns) == 0:
        dict_group_codes[group] = Counter({str(len(group)): 1})
        return dict_group_codes[group]

    mid = unknowns[len(unknowns) // 2]
    left = group[:mid]
    right = group[mid+1:]

    damaged = resolve_group(left + SYMBOL_DAMAGED + right)
    operational = cross_groups(resolve_group(left), resolve_group(right))

    dict_group_codes[group] = Counter(damaged)
    if operational:
        dict_group_codes[group] += operational

    return dict_group_codes[group]

def solve():
    ways = 0
    for line in lines:
        groups, pattern = line
        dict_ways_to_make_pattern = None
        for group in groups:
            resolve_group(group)
            dict_ways_to_make_pattern = cross_groups(dict_ways_to_make_pattern, dict_group_codes[group])
        ways += dict_ways_to_make_pattern[pattern]

    print(ways)

solve()

