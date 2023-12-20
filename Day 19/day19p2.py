import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')
    split_index = lines.index('')

ratings = {'x': 0, 'm': 1, 'a': 2, 's': 3}

# Returns the ranges that fit the condition, and the ranges that don't
def split_ranges(ranges, index, bound_value, bounding_lower):
    (lower, upper) = ranges[index]
    accepting = list(ranges)
    rejecting = list(ranges)

    # We are defining a new minimum
    if bounding_lower:
        # The maximum value we can take is below the new minimum
        if upper <= bound_value:
            return None, rejecting

        # The minimum value we can take is already above the bound
        if lower > bound_value:
            return accepting, None

        accepting[index] = (bound_value + 1, upper)
        rejecting[index] = (lower, bound_value)
        return accepting, rejecting

    # We are defining a new maximum

    # If the minimum value we can take is above the new maximum
    if lower >= bound_value:
        return None, rejecting

    # If the maximum value we can take is already below the bound
    if upper < bound_value:
        return accepting, None

    accepting[index] = (lower, bound_value - 1)
    rejecting[index] = (bound_value, upper)
    return accepting, rejecting

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
            rules.append((result, lambda ranges, r=rating, b=bound, o=operator: split_ranges(ranges, r, b, o == '>')))
        else:
            rules.append((result, lambda ranges: (ranges, None)))

    workflows[name] = rules

# For graph method to work, need to verify 'no loops' assumption.
# Verify there are no loops (names should only appear 2 times, and 1 time for 'in')
# With input.txt: Counter({2: 540, 1: 1})

# Need to find the critical regions of acceptance and rejection
# Start with (1-4000, 1-4000, 1-4000, 1-4000) and range split until accept or reject is hit

frontier = [('in', [(1, 4000), (1, 4000), (1, 4000), (1, 4000)])]
accepting_ranges = []
while frontier:
    (name, part_ranges) = frontier.pop()
    rule_rejecting_ranges = part_ranges

    workflow = workflows[name]
    for result, splitter in workflow:
        rule_accepting_ranges, rule_rejecting_ranges = splitter(rule_rejecting_ranges)
        if rule_accepting_ranges:
            if result == 'A':
                accepting_ranges.append(rule_accepting_ranges)
            elif result != 'R':
                frontier.append((result, rule_accepting_ranges))

total_accepting_ratings = sum([np.prod([upper - lower + 1 for (lower, upper) in ranges]) for ranges in accepting_ranges])
print(total_accepting_ratings)
