from copy import deepcopy
from functools import reduce

def parse_input(file = 'day06.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip('\n'), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day06example.txt')

def format_input(inp: list[str]):
    return inp

def solve(inp, part, example):
    operators = inp[-1].split()
    if part == 1:
        operands = []
        for line in inp[:-1]:
            operands.append(list(map(int, line.split())))
        operands = [[ops[j] for ops in operands] for j in range(len(operands[0]))]
    else:
        dividers = []
        for i in range(len(inp[0])):
            if all(line[i] == ' ' for line in inp):
                dividers.append(i)
        dividers.append(max(len(line) for line in inp))
        operands = []
        prev_div = -1
        while dividers:
            div = dividers.pop(0)
            ops = [''] * (div - prev_div - 1)
            for line in inp[:-1]:
                for index in range(div - prev_div - 1):
                    if index >= len(ops) and example:
                        print(ops, index, div, prev_div)
                    ops[index] += line[prev_div + 1 + index]
            operands.append([int(op) for op in ops])
            prev_div = div

    tot = 0
    for i, ops in enumerate(operands):
        operator = operators[i]
        if operator == '+':
            tot += sum(ops)
        elif operator == '*':
            tot += reduce(lambda x, y: x * y, ops)
        else:
            raise
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
