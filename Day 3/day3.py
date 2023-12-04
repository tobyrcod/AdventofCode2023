import numpy as np

file = open("input.txt")
lines = file.read().splitlines()
file.close()

lines = [list(line) for line in lines]
height = len(lines)
width = len(lines[0])

def is_valid_pos(y, x):
    return 0 <= y < height and 0 <= x < width

def get_adjacent(y, x):
    return {(y + i, x + j) for i in range(-1, 2) for j in range(-1, 2)
            if (i, j) != (0, 0) and is_valid_pos(y + i, x + j)}

# First find all the numbers and encode them as ids
next_id = 0
position_id = dict()
id_number = dict()
symbols = set()
for y, line in enumerate(lines):
    left = -1
    for x, char in enumerate(line + ['.']):
        if char.isdigit():
            if left == -1:
                left = x
        else:
            # Have we been building a number
            if left != -1:
                # We have found the end of the number
                # encode it
                id_number[next_id] = int("".join(line[left:x]))
                for p in range(left, x):
                    position_id[(y, p)] = next_id
                next_id += 1

                # reset to find next number
                left = -1

            # Have we found a symbol
            if char != '.':
                symbols.add((y, x))

print(id_number)

# Now for each symbol, we find the set of ids in its neighbourhood
part_number_ids = set()
for symbol in symbols:
    for pos in get_adjacent(*symbol):
        id = position_id.get(pos, -1)
        if id != -1:
            part_number_ids.add(id)

part_numbers = [id_number[id] for id in part_number_ids]
print(sum(part_numbers))
