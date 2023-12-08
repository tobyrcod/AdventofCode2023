import re
import numpy as np

file = open("input.txt")
lines = file.read().splitlines()
file.close()

instructions = [0 if c == 'L' else 1 for c in lines[0]]

edges = [line.split(" = ") for line in lines[2:]]
network = {a: b[1:-1].split(", ") for [a, b] in edges}

def part1(start_node='AAA', end_pattern=r'\bZZZ\b'):
    node = start_node
    step = 0
    instructions_len = len(instructions)
    end_pattern = re.compile(end_pattern)
    while not end_pattern.match(node):
        instruction = instructions[step % instructions_len]
        node = network[node][instruction]
        step += 1
    return step

def part2():
    """
    Assumptions:
    For the LCM method to work, the steps from the first XXA to XXZ nodes
    must be the same as the number of steps from XXZ to XXZ.
    I was hesitant about this approach because of this, but it seems to be intended
    """
    start_pattern = re.compile(r'\b\w{2}A\b')
    start_nodes = filter(start_pattern.match, network)
    cycles = map(lambda node: part1(start_node=node, end_pattern=r'\b\w{2}Z\b'), start_nodes)
    return np.lcm.reduce(list(cycles))

steps = part2()
print(steps)
