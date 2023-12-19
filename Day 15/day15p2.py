import re

file = open("input.txt")
initialization_sequence = [re.split('[=, -]', step) for step in file.read().split(',')]
file.close()

VERBOSE = False

def printv(string):
    if VERBOSE:
        print(string)

class Node:
    def __init__(self, lens, focal_length: int):
        self.lens = lens
        self.focal_length: int = focal_length

        self.next: Node = None
        self.previous: Node = None

    def __str__(self):
        return f'({self.lens}, {self.focal_length})'

    def __repr__(self):
        return self.__str__()


class LinkedList:
    def __init__(self):
        self.head: Node = None

    def add(self, lens, focal_length: int):
        if not self.__try_replace(lens, focal_length):
            self.__add_to_end(lens, focal_length)

    def __add_to_end(self, lens, focal_length: int):
        node = Node(lens, focal_length)
        if not self.head:
            self.head = node
            return

        current_node = self.head
        while current_node.next:
            current_node = current_node.next

        current_node.next = node
        node.previous = current_node

    def __try_replace(self, lens, focal_length: int):
        current_node = self.head
        while current_node and current_node.lens != lens:
            current_node = current_node.next

        if current_node is None:
            return False

        current_node.focal_length = focal_length
        return True

    def remove(self, lens):
        if not self.head:
            return

        current_node = self.head
        if current_node.lens == lens:
            self.__remove_head()
            return

        while current_node and current_node.lens != lens:
            current_node = current_node.next

        if current_node is None:
            return

        current_node.previous.next = current_node.next
        if current_node.next:
            current_node.next.previous = current_node.previous

    def __remove_head(self):
        if self.head is None:
            return

        self.head = self.head.next
        if self.head:
            self.head.previous = None

    def get_length(self):
        length = 0
        current_node = self.head
        while current_node:
            length += 1
            current_node = current_node.next
        return length

    def to_list(self):
        nodes = list()
        current_node = self.head
        while current_node:
            nodes.append(current_node)
            current_node = current_node.next
        return nodes

    def __str__(self):
        return ', '.join([str(node) for node in self.to_list()])


# ASCII String Helper Manual Arrangement Procedure - HASHMAP
class HashMap:
    def __init__(self):
        self.boxes = [LinkedList() for _ in range(256)]

    def add(self, lens, focal_length: int):
        key = self.__hash(lens)
        self.boxes[key].add(lens, focal_length)

    def remove(self, lens):
        key = self.__hash(lens)
        self.boxes[key].remove(lens)

    def get_installation(self):
        return [(i, box.to_list()) for i, box in enumerate(self.boxes) if len(str(box)) > 0]

    @staticmethod
    # Holiday ASCII String Helper - HASH
    def __hash(string: str):
        current_value = 0
        for c in string:
            current_value += ord(c)
            current_value *= 17
            current_value %= 256
        return current_value

    def __str__(self):
        return '\n'.join(f'Box {i}: {str(box)}' for i, box in enumerate(self.boxes) if len(str(box)) > 0)


hashmap = HashMap()
for step in initialization_sequence:
    lens, focal_length = step
    printv(f'After "{lens} {focal_length}"')
    if focal_length == '':
        hashmap.remove(lens)
    else:
        hashmap.add(lens, int(focal_length))
    printv(hashmap)
    printv('-------')

installation = hashmap.get_installation()
power = sum([(ibox + 1) * sum([(ilens + 1) * lens.focal_length for ilens, lens in enumerate(lenses)]) for (ibox, lenses) in installation])
print(power)
