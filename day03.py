from copy import deepcopy

def parse_input(file = 'day03.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day03example.txt')

def format_input(inp: list[str]):
    banks = []
    for line in inp:
        banks.append([int(v) for v in line.rstrip()])
    return banks

def solve(inp: list[list[int]], part, example):
    tot = 0
    for bank in inp:
        highest = max(bank)
        if bank.index(highest) == len(bank) - 1:
            for v in range(highest - 1, 0, -1):
                if v in bank:
                    tot += int(str(v) + str(highest))
                    break
        else:
            if bank.count(highest) > 1:
                tot += int(str(highest) + str(highest))
            else:
                for v in range(highest - 1, 0, -1):
                    if v in bank[bank.index(highest) + 1:]:
                        tot += int(str(highest) + str(v))
                        break
    return tot

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
