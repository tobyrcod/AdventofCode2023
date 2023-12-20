from queue import Queue
from typing import List

import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')
module_names, module_connections = zip(*(line.split(' -> ') for line in lines))

BUTTON_NAME = 'button'
BROADCASTER_NAME = 'broadcaster'

NUM_BUTTON_PRESSES = 1000

VERBOSE = False

def printv(message: str) -> None:
    if VERBOSE:
        print(message)

class Module:
    def __init__(self, name: str):
        self.name: str = name
        self.connection_names = []

    def receive_pulse(self, from_name: str, pulse: bool, press_count: int) -> List[tuple[str, str, int]]:
        printv(f'{from_name} -{pulse}-> {self.name}')
        return []

    def notify_connection_from(self, name) -> None:
        pass

    @property
    def in_default_state(self) -> bool:
        return True

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

class Broadcaster(Module):
    def receive_pulse(self, from_name: str, pulse: bool, press_count: int) -> List[tuple[str, str, int]]:
        super().receive_pulse(from_name, pulse, press_count)

        return [(self.name, connection_name, pulse)
                for connection_name in self.connection_names]

class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.state = False

    def receive_pulse(self, from_name: str, pulse: bool, press_count: int) -> List[tuple[str, str, int]]:
        super().receive_pulse(from_name, pulse, press_count)

        # If Flip-Flop receives a high pulse, it is ignored
        if pulse:
            return []

        # If Flip-Flop receives a low pulse, it flips between on and off
        self.state = not self.state

        # And sends a pulse matching its new state
        return [(self.name, connection_name, self.state)
                for connection_name in self.connection_names]

    @property
    def in_default_state(self) -> bool:
        return not self.state

    def __str__(self) -> str:
        return f'(%: {self.name}, {self.state})'

class Conjunction(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.memory = dict()

    def receive_pulse(self, from_name: str, pulse: bool, press_count: int) -> List[tuple[str, str, int]]:
        super().receive_pulse(from_name, pulse, press_count)

        if self.name == 'kj' and from_name == 'vn' and pulse:
            print(f'kj hit with high pulse from vn after {press_count} presses')

        # Remember the pulse received
        self.memory[from_name] = pulse

        return [(self.name, connection_name, self.pulse_to_send)
                for connection_name in self.connection_names]

    @property
    def in_default_state(self) -> bool:
        return not any(self.memory.values())

    @property
    def pulse_to_send(self) -> int:
        # If we remember high pulses for all inputs, send a low pulse, else send a high pulse
        return not all(self.memory.values())

    def notify_connection_from(self, name):
        self.memory[name] = False

    def __str__(self) -> str:
        return f'(&: {self.name}, {self.memory})'

# Build Nodes
modules = dict()
for module_name in module_names:
    if module_name == BROADCASTER_NAME:
        modules[module_name] = Broadcaster(module_name)
        continue

    module_type, module_name = module_name[0], module_name[1:]
    if module_type == '%':
        modules[module_name] = FlipFlop(module_name)
        continue

    if module_type == '&':
        modules[module_name] = Conjunction(module_name)

# Build Edges
connections = dict()
for i, module_name in enumerate(dict(modules)):
    module_connection_names = module_connections[i].split(', ')
    for module_connection_name in module_connection_names:
        # Add any modules we come across that send no signals, but still receive them
        if module_connection_name not in modules:
            modules[module_connection_name] = Module(module_connection_name)
        modules[module_connection_name].notify_connection_from(module_name)
    connections[module_name] = module_connection_names
    modules[module_name].connection_names = module_connection_names

# Push the button
def push_the_button(press_count):
    pulses = Queue()
    pulses.put((BUTTON_NAME, BROADCASTER_NAME, False))
    while not pulses.empty():
        (from_name, to_name, pulse_type) = pulses.get()

        new_pulses = modules[to_name].receive_pulse(from_name, pulse_type, press_count)
        for new_pulse in new_pulses:
            pulses.put(new_pulse)

def push_the_button_n_times(n: int):
    for _ in range(1, n+1):
        push_the_button(_)

# How many button pressed until rx receives low pulse?
# Only appearance of rx in configuration: &kj -> rx
# So rx will receive a low pulse when all of kj memories are high
# print(modules['kj']) => {'ln': False, 'dr': False, 'zx': False, 'vn': False}
# So we need &ln, &dr, &zx, &vn to be high at the same time
# print(modules['ln'], modules['dr'], modules['zx'], modules['vn'])
# (Or we need jv, qs, jm, pr to be low at the same time)
# Explore one by one to try and find cycles in them:
# kj hit with high pulse from ln after 4003 presses
# kj hit with high pulse from dr after 3863 presses
# kj hit with high pulse from zx after 3989 presses
# kj hit with high pulse from vn after 3943 presses
# Finally, assuming constant periods for each, find lcm:
print(np.lcm.reduce([4003, 3863, 3989, 3943]))
