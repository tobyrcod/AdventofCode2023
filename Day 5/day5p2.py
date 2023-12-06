import math
from itertools import groupby

# https://www.reddit.com/r/adventofcode/s/lFc3UljtHJ

file = open("test1.txt")
lines = file.read().splitlines()
file.close()

lines = [list(g) for k, g in groupby(lines, key=bool) if k]

[seeds] = lines[0]
seeds = list(map(int, seeds[seeds.index(':') + 2:].split()))
seeds = [seeds[i:i+2] for i in range(0, len(seeds), 2)]
seeds = [(s, s+l-1) for [s, l] in seeds]

def parse_xy_map(xy_map):
    return [(x, x+length-1, y-x) for y, x, length in xy_map]

raw_maps = [[list(map(int, x.split())) for x in rm[1:]] for rm in lines[1:]]
maps = [parse_xy_map(rm) for rm in raw_maps]

# This feels very AABB collisions?...
for map in maps:
    # new seeds are seeds that have had a rule applied and are already shifted to the next stage
    seeds_next_map = list()
    for r1, r2, shift in map:
        # remaining seeds are new ranges that got missed by a rule
        seeds_next_rule = list()
        for s1, s2 in seeds:
            if r2 < s1 or s2 < r1:
                # There is no overlap between seeds and rule
                seeds_next_rule.append((s1, s2))
                continue
            if r1 < s1 <= r2 < s2:
                # The end of the rules overlaps with the start of the seeds
                seeds_next_map.append((s1 + shift, r2 + shift))
                seeds_next_rule.append((r2 + 1, s2))
                continue
            if s1 < r1 <= s2 < r2:
                # The start of the rules overlaps with the end of the seeds
                seeds_next_rule.append((s1, r1 - 1))
                seeds_next_map.append((r1 + shift, s2 + shift))
                continue
            if r1 <= s1 <= s2 <= r2:
                # All the seeds fit inside the rule
                seeds_next_map.append((s1 + shift, s2 + shift))
                continue
            if s1 <= r1 <= r2 <= s2:
                # All the rule fits inside the seed
                if s1 != r1:
                    seeds_next_rule.append((s1, r1))
                seeds_next_map.append((r1 + shift, r2 + shift))
                if r2 != s2:
                    seeds_next_rule.append((r2, s2))
                continue
            # One of these cases should always be true
            raise Exception(f"AABB logic is incorrect for seeds: {s1, s2}, rule: {r1, r2}")
        # The next rule only needs to check over the seeds that no other rule has already mapped
        seeds = seeds_next_rule
    # any rules that are unmapped remain the same
    seeds.extend(seeds_next_map)

# We only need to check the beginning of each seed range, as that is always the smallest
locations = [seed[0] for seed in seeds]
# Print the smallest of the locations
print(min(locations))


