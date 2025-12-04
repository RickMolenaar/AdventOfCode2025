from copy import deepcopy

def parse_input(file = 'day04.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day04example.txt')

def format_input(inp: list[str]):
    grid = {}
    for y, line in enumerate(inp):
        l = {}
        for i, c in enumerate(line):
            l[i] = 0 if c == '.' else 1
        grid[y] = l
    return grid

def get_accessible(grid):
    accessible = set()
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == 0:
                continue
            adjacent = 0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    try:
                        neigh = grid[y + dy][x + dx]
                    except KeyError:
                        continue
                    adjacent += neigh
            if adjacent < 4:
                accessible.add((x, y))
    return accessible

def solve(inp, part, example):
    if part == 1:
        return len(get_accessible(inp))
    acc = get_accessible(inp)
    tot = 0
    while acc:
        tot += len(acc)
        for x, y in acc:
            inp[y][x] = 0
        acc = get_accessible(inp)
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
