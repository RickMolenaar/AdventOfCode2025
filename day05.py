from copy import deepcopy

def parse_input(file = 'day05.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day05example.txt')

def format_input(inp: list[str]):
    ingredients = []
    fresh_ranges = []
    step = 0
    for line in inp:
        if not line.strip():
            step = 1
        elif step == 0:
            i1, i2 = line.split('-')
            fresh_ranges.append((int(i1), int(i2)))
        else:
            ingredients.append(int(line))
    return (ingredients, fresh_ranges)

def solve(inp, part, example):
    ingredients, fresh_ranges = inp
    fresh = set()
    if part == 1:
        for ing in ingredients:
            for r in fresh_ranges:
                if ing in range(r[0], r[1] + 1):
                    fresh.add(ing)
                    break
        return len(fresh)
    
    updated = True
    fresh_ranges = sorted(fresh_ranges)
    while updated:
        new = [fresh_ranges[0]]
        updated = False
        i = 1
        while i < len(fresh_ranges):
            r_prev, r = new[-1], fresh_ranges[i]
            if r[0] <= r_prev[1]:
                if r[1] <= r_prev[1]:
                    i += 1
                    continue
                new.append((r_prev[1] + 1, r[1]))
                updated = True
            else:
                new.append(r)
            i += 1
        fresh_ranges = new
    tot = 0
    for r in fresh_ranges:
        tot += r[1] - r[0] + 1
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
