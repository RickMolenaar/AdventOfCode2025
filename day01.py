from copy import deepcopy

def parse_input(file = 'day01.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day01example.txt')

def format_input(inp: list[str]):
    return inp

def solve(inp, part, example):
    dial = 50
    ans = 0
    for line in inp:
        move = int(line[1:])
        while move >= 100:
            ans += 1
            move -= 100
        if line[0] == 'L':
            dial -= move
        elif line[0] == 'R':
            dial += move
        else:
            raise
        if part == 1:
            dial = dial % 100
            if dial == 0:
                ans += 1
        else:
            if (dial <= 0 and (dial + move) == 0):
                ans -= 1
            if dial <= 0 or dial >= 100:
                ans += 1
            dial = dial % 100
    return ans

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
