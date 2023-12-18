# Great help for part2, and introducing me to functools @cache:
# https://advent-of-code.xavd.id/writeups/2023/day/12/
from functools import cache

SYMBOL_OPERATIONAL = '.'
SYMBOL_DAMAGED = '#'
SYMBOL_UNKNOWN = '?'

UNFOLDS = 5

file = open("input.txt")
lines = file.read().splitlines()
file.close()

lines = [line.split() for line in lines]

if UNFOLDS > 0:
    lines = [['?'.join([record] * UNFOLDS), ','.join([groups] * UNFOLDS)] for record, groups in lines]

condition_records = [(record, tuple(map(int, groups.split(',')))) for record, groups in lines]

@cache
def num_ways_to_make_pattern(record, groups):
    if not record:
        return len(groups) == 0

    first, remaining = record[0], record[1:]

    if not groups:
        return SYMBOL_DAMAGED not in set(record)

    group = groups[0]

    if first == SYMBOL_OPERATIONAL:
        return num_ways_to_make_pattern(remaining, groups)

    if first == SYMBOL_DAMAGED:
        if len(record) < group:
            return 0
        if any(c == SYMBOL_OPERATIONAL for c in record[:group]):
            return 0
        if len(record) > group and record[group] == SYMBOL_DAMAGED:
            return 0

        return num_ways_to_make_pattern(record[group + 1:], groups[1:])

    operational = num_ways_to_make_pattern(f'{SYMBOL_OPERATIONAL}{remaining}', groups)
    damaged = num_ways_to_make_pattern(f'{SYMBOL_DAMAGED}{remaining}', groups)
    return operational + damaged


def solve():
    total_ways = 0
    for record, groups in condition_records:
        ways = num_ways_to_make_pattern(record, groups)
        total_ways += ways
    print(total_ways)


solve()
