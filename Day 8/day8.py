file = open("input.txt")
lines = file.read().splitlines()
file.close()

instructions = [0 if c == 'L' else 1 for c in lines[0]]

edges = [line.split(" = ") for line in lines[2:]]
network = {a: b[1:-1].split(", ") for [a, b] in edges}

node = 'AAA'
step = 0
instructions_len = len(instructions)
while node != 'ZZZ':
    instruction = instructions[step % instructions_len]
    node = network[node][instruction]
    step += 1
print(step)
