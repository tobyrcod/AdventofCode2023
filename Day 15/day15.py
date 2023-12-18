file = open("input.txt")
initialization_sequence = file.read().split(',')
file.close()

def hash(str):
    current_value = 0
    for c in str:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value

print(sum(map(hash, initialization_sequence)))
