from queue import Queue
from typing import List

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

    def receive_pulse(self, from_name: str, pulse: bool) -> List[tuple[str, str, int]]:
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
    def receive_pulse(self, from_name: str, pulse: bool) -> List[tuple[str, str, int]]:
        super().receive_pulse(from_name, pulse)

        return [(self.name, connection_name, pulse)
                for connection_name in self.connection_names]

class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.state = False

    def receive_pulse(self, from_name: str, pulse: bool) -> List[tuple[str, str, int]]:
        super().receive_pulse(from_name, pulse)

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

    def receive_pulse(self, from_name: str, pulse: bool) -> List[tuple[str, str, int]]:
        super().receive_pulse(from_name, pulse)

        # Remember the pulse received
        self.memory[from_name] = pulse

        # If we remember high pulses for all inputs, send a low pulse, else send a high pulse
        pulse_to_send = not all(self.memory.values())

        return [(self.name, connection_name, pulse_to_send)
                for connection_name in self.connection_names]

    @property
    def in_default_state(self) -> bool:
        return not any(self.memory.values())

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
def push_the_button() -> tuple[int, int]:
    low_pulse_count = 0
    high_pulse_count = 0

    pulses = Queue()
    pulses.put((BUTTON_NAME, BROADCASTER_NAME, False))
    while not pulses.empty():
        (from_name, to_name, pulse_type) = pulses.get()

        high_pulse_count += pulse_type
        low_pulse_count += not pulse_type

        new_pulses = modules[to_name].receive_pulse(from_name, pulse_type)
        for new_pulse in new_pulses:
            pulses.put(new_pulse)

    return low_pulse_count, high_pulse_count

def push_the_button_n_times(n: int, stop_on_cycle: bool=False) -> tuple[int, int]:
    low_pulse_count = 0
    high_pulse_count = 0

    for _ in range(n):
        lph, hpc = push_the_button()
        low_pulse_count += lph
        high_pulse_count += hpc

    return low_pulse_count, high_pulse_count

def find_pulse_cycle() -> tuple[int, int, int]:
    period = None
    low_pulse_count = 0
    high_pulse_count = 0

    button_presses = 0
    while not period:
        button_presses += 1
        print(button_presses)
        lpc, hpc = push_the_button()
        low_pulse_count += lpc
        high_pulse_count += hpc

        if all((module.in_default_state for module in modules.values())):
            period = button_presses

    return period, low_pulse_count, high_pulse_count

low_pulse_count, high_pulse_count = push_the_button_n_times(1000)
print(low_pulse_count * high_pulse_count)
