from copy import deepcopy

def parse_input(file = 'day11.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day11example.txt')

def format_input(inp: list[str]):
    machines = {}
    for line in inp:
        vals = line.split()
        machines[vals[0].rstrip(':')] = vals[1:]
    return machines

cache = {}
def find_paths(machines, current, target):
    if (current, target) in cache:
        return cache[(current, target)]
    amount = 0
    for next_machine in machines[current]:
        if next_machine == target:
            amount += 1
        elif next_machine in machines:
            amount += find_paths(machines, next_machine, target)
    cache[(current, target)] = amount
    return amount

def solve(inp, part, example):
    global cache
    cache = {}
    if part == 1:
        if example:
            return
        return find_paths(inp, 'you', 'out')
    return find_paths(inp, 'svr', 'fft') * find_paths(inp, 'fft', 'dac') * find_paths(inp, 'dac', 'out') + \
        find_paths(inp, 'svr', 'dac') * find_paths(inp, 'dac', 'fft') * find_paths(inp, 'fft', 'out')

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
