with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')
hailstones = [[list(map(int, vector3.split(','))) for vector3 in line.split('@')] for line in lines]
MIN, MAX = 200000000000000, 400000000000000


def find_path_intersection(start1, direction1, start2, direction2):
    """
    Paths of the form: position = start + time * direction,
    So we need: start1 + time1 * direction1 = start2 + time2 * direction2,
    And we solve each for time1 and time2
    """
    x1, y1 = start1
    dx1, dy1 = direction1
    x2, y2 = start2
    dx2, dy2 = direction2

    # If we are parallel, we never intersect
    if dx1 * dy2 == dx2 * dy1:
        return False

    # If we are not parallel, find the intersection point
    t1 = (dy2 * (x2 - x1) + dx2 * (y1 - y2)) / (dx1 * dy2 - dx2 * dy1)
    t2 = (dy1 * (x2 - x1) + dx1 * (y1 - y2)) / (dx1 * dy2 - dx2 * dy1)

    # If the intersection requires either of the paths to go backwards, we ignore it
    if t1 < 0 or t2 < 0:
        return None

    # Now we know it exists and in the future, return the point of intersection
    return x1 + t1 * dx1, y1 + t1 * dy1


hit_count = 0
for i in range(len(hailstones)):
    [*start1, _], [*direction1, _] = hailstones[i]
    for j in range(i+1, len(hailstones)):
        [*start2, _], [*direction2, _] = hailstones[j]
        if intersect := find_path_intersection(start1, direction1, start2, direction2):
            x, y = intersect
            if MIN <= x <= MAX and MIN <= y <= MAX:
                hit_count += 1

print(hit_count)
