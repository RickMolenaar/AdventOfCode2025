from copy import deepcopy

def parse_input(file = 'day02.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day02example.txt')

def format_input(inp: list[str]):
    ranges_raw = inp[0].split(',')
    ranges = []
    for s in ranges_raw:
        v0, v1 = s.split('-')
        ranges.append((int(v0), int(v1)))
    return ranges

def divisors(n):
    return [i for i in range(1, n) if n % i == 0]

def get_invalids(min_n, max_n, all_repeats):
    invalid = []
    if all_repeats:
        ds = divisors(len(str(min_n)))
    else:
        ds = [len(str(min_n)) // 2] if len(str(min_n)) % 2 == 0 else []
    for d in ds:
        v0 = int(str(min_n)[:d])
        v1 = int(str(max_n)[:d])
        for v_start in range(v0, v1 + 1):
            repeats = (len(str(min_n)) // d)
            v = int(repeats * str(v_start))
            if min_n <= v <= max_n:
                invalid.append(v)
    return invalid


def solve(inp, part, example):
    invalid = set()
    for r in inp:
        l0 = len(str(r[0]))
        l1 = len(str(r[1]))
        if l0 == l1:
            invalid = invalid.union(get_invalids(r[0], r[1], part == 2))
        else:
            lim = int(l0 * '9')
            invalid = invalid.union(get_invalids(r[0], lim, part == 2))
            invalid = invalid.union(get_invalids(lim + 1, r[1], part == 2))
    return sum(invalid)

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
