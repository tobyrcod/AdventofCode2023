file = open("input1.txt")
lines = file.read().splitlines()
file.close()

def part1():
    codes = []
    for line in lines:
        # pointers
        left = 0
        right = len(line) - 1

        # digits
        first = last = None
        while not (first and last):  # Assuming first and last digits always present
            lc = line[left]
            rc = line[right]

            if not first and lc.isdigit():
                first = lc

            if not last and rc.isdigit():
                last = rc

            left += 1
            right -= 1

        codes.append(int(first + last))

    print(sum(codes))




