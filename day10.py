from copy import deepcopy
from scipy.optimize import milp, LinearConstraint
from numpy import array

def parse_input(file = 'day10.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day10example.txt')

class Machine(object):
    def __init__(self, s: str):
        values = s.split()
        assert '[' in values[0] and '{' in values[-1]
        self.lights = [0 if c == '.' else 1 for c in values[0].strip('[]')]
        self.joltage = list(map(int, values[-1].strip('{}').split(',')))
        self.buttons = [tuple(map(int, button.strip('()').split(','))) for button in values[1:-1]]

def format_input(inp: list[str]) -> list[Machine]:
    return [Machine(line) for line in inp]

def distribute_presses(presses: int, n_buttons: int, max_presses: list[int]):
    if n_buttons == 1:
        if presses <= max_presses[0]:
            yield [presses]
    elif sum(max_presses) >= presses:
        try:
            for i in range(min(presses, max_presses[0]) + 1):
                for dist in distribute_presses(presses - i, n_buttons - 1, max_presses[1:]):
                    yield [i] + dist
        except IndexError:
            print(presses, n_buttons, max_presses)
            raise

cache = {}

def get_presses_for_joltage(buttons: list[tuple[int]], target, best_minimum = 10**99, debug = False) -> int:
    key = (tuple(buttons), tuple(target))
    if key in cache:
        return cache[key]
    # print(buttons, target)
    if any(v > best_minimum for v in target):
        return 10**99
    possible_buttons = [
        [i for i, button in enumerate(buttons) if j in button] for j in range(len(target))
    ]
    critical_joltages = sorted([i for i in range(len(target)) if target[i] > 0], key = lambda i: (len(possible_buttons[i]) - 100 * (target[i] < 10), target[i]))
    to_set = critical_joltages[0]
    buttons_to_use = [buttons[i] for i in possible_buttons[to_set]]
    max_presses = [min(target[j] for j in button) for button in buttons_to_use]
    min_presses = 10**99
    best_set = None
    # if debug:
    #     print(target[to_set], len(buttons_to_use), max_presses)
    if not buttons_to_use:
        return 10**99
    if all(v > 0 for v in target):
        print(f'Distributing {target[to_set]} over {len(buttons_to_use)}')
    for presses in distribute_presses(target[to_set], len(buttons_to_use), max_presses):
        if debug:
            print(f'Trying {presses}, {buttons_to_use}')
        set_joltage = get_joltage(len(target), buttons_to_use, presses)
        if set_joltage == target:
            if debug:
                print(target)
                print(f'Setting {to_set}')
                print((presses, buttons_to_use))
                print(f'0 after this')
            cache[key] = target[to_set]
            return target[to_set]
        new_target = [target[i] - set_joltage[i] for i in range(len(target))]
        if any(v < 0 for v in new_target):
            if debug:
                print(f'{presses} is not valid ({new_target})')
            continue
        if debug:
            print(f'{presses} is valid')
        additional = get_presses_for_joltage([b for b in buttons if b not in buttons_to_use], new_target, debug = False)
        # if target[to_set] + additional == max(target):
        #     return target[to_set] + additional
        if additional:
            min_presses = min(min_presses, additional)
            if min_presses == additional:
                best_set = (presses, buttons_to_use)
    if debug:
        print(target)
        print(f'Setting {to_set}')
        print(best_set)
        print(f'{min_presses} after this')
    cache[key] = target[to_set] + min_presses
    return target[to_set] + min_presses
    
def get_joltage(n_joltage: int, buttons: list[tuple[int]], button_presses: list[int]):
    joltage = [0 for _ in range(n_joltage)]
    for i, button in enumerate(buttons):
        for c in button:
            joltage[c] += button_presses[i]
    return joltage

def find_solution(buttons, target: list[int]):
    m = [[1 if ind in button else 0 for button in buttons] for ind in range(len(target))]
    res = milp(
        [1 for _ in range(len(buttons))],
        integrality = [1 for _ in range(len(buttons))],
        constraints = LinearConstraint(m, target, target)
    )
    return int(sum(res.x))

def solve(inp: list[Machine], part, example):
    total = 0
    for i, machine in enumerate(inp):
        # if part == 2:
        #     print('{}/{}'.format(i+1, len(inp)))
        if part == 1:
            possibilities = 2**len(machine.buttons)
            min_presses = len(machine.buttons)
            for is_pressed in range(possibilities):
                lights = [0 for l in machine.lights]
                presses = 0
                for b in range(len(machine.buttons)):
                    if is_pressed % 2:
                        presses += 1
                        if presses >= min_presses:
                            break
                        for light in machine.buttons[b]:
                            lights[light] = not lights[light]
                    is_pressed >>= 1
                    if lights == machine.lights:
                        min_presses = presses
                        break
            total += min_presses
        else:
            total += find_solution(machine.buttons, machine.joltage)
    return total

def main():
    example_input = format_input(parse_example())
    actual_input = format_input(parse_input())
    for part in (1, 2):
        for example in (True, False):
            inp = deepcopy(example_input if example else actual_input)
            try:
                yield solve(inp, part, example)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                yield e
