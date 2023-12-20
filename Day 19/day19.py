import re

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')
    split_index = lines.index('')

operations = {'>': lambda a, b: a > b, '<': lambda a, b: a < b}
ratings = {'x': 0, 'm': 1, 'a': 2, 's': 3}

# workflow: {name: (function of the part, result if it's true)}
workflows = dict()
for line in lines[:split_index]:
    i = line.index("{")
    name = line[:i]

    rules = []
    for rule in line[i + 1:-1].split(','):
        *condition, result = rule.split(':')
        if condition:
            condition = condition[0]
            rating, operator, bound = ratings[condition[0]], condition[1], int(condition[2:])
            rules.append((lambda part, o=operator, r=rating, b=bound: operations[o](part[r], b), result))
        else:
            rules.append((lambda part: True, result))

    workflows[name] = rules

# part: (x, m, a, s)
part_pattern = r'(?<==)\d+'  # Find everything after the '=' until we hit a non digit char
parts = [tuple(map(int, re.findall(part_pattern, part))) for part in lines[split_index+1:]]

def rate_part(part: tuple[int, int, int, int]):
    workflow_name = 'in'
    while workflow_name:
        workflow = workflows[workflow_name]
        for condition, result in workflow:
            if condition(part):
                if result == 'A':
                    return True
                if result == 'R':
                    return False
                workflow_name = result
                break

total_rating = sum(sum(part) for part in parts if rate_part(part))
print(total_rating)
