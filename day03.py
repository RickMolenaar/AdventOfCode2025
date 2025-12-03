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

def find_highest_jolts(bank, digits):
    if digits == 1:
        return max(bank)
    highest_possible = max(bank[:len(bank) + 1 - digits])
    return int(str(highest_possible) + str(find_highest_jolts(bank[bank.index(highest_possible) + 1:], digits - 1)))

def solve(inp: list[list[int]], part, example):
    tot = 0
    for bank in inp:
        if part == 1:
            tot += find_highest_jolts(bank, 2)
        else:
            tot += find_highest_jolts(bank, 12)
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
