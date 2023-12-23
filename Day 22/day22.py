with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')

# Shapes (x, y, z), z is up/down
shapes = [list([(a, b) for (a, b) in zip(*[map(int, point.split(',')) for point in line.split('~')])]) for line in lines]
shapes.sort(key=lambda shape: min(shape[2]))

# Step 1: Settle Shapes Downwards
# Ideas:
# We look top down and see empty grid
# We consider shapes by the ones closed to the bottom first
# We place the first shape as low as it can go
# We look top down and now see the top of that shape in the (x, y) span of the shape
# If any (x, y) of the new shape overlaps, it goes to z+1 of the old shape
# Repeat for all shapes

id_top = dict()
pos_id = dict()
id_resting_on = dict()

for new_id, shape in enumerate(shapes):
    # Get the shapes we are on top off
    X, Y, Z = shape
    over_shapes = set()
    for x in range(X[0], X[1]+1):
        for y in range(Y[0], Y[1]+1):
            if (x, y) in pos_id:
                over_shapes.add(pos_id[(x, y)])

    # Get the shape(s) that is highest
    max_top = 0
    top_ids = dict()
    for id in over_shapes:
        top = id_top[id]
        if top not in top_ids:
            top_ids[top] = set()
        top_ids[top].add(id)
        if top > max_top:
            max_top = top
    top_shapes = top_ids.get(max_top, [])

    # Move this shape's bottom to the top of these shapes
    id_top[new_id] = max_top + 1 + Z[1] - Z[0]
    for x in range(X[0], X[1]+1):
        for y in range(Y[0], Y[1]+1):
            pos_id[(x, y)] = new_id
    id_resting_on[new_id] = top_shapes

safe_to_disintegrate = set(id_resting_on.keys())
for resting_on in id_resting_on.values():
    if len(resting_on) == 1:
        safe_to_disintegrate.difference_update(resting_on)

print(len(safe_to_disintegrate))
