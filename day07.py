from copy import deepcopy
from collections import defaultdict

def parse_input(file = 'day07.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day07example.txt')

def format_input(inp: list[str]):
    start = inp[0].index('S')
    splitters = defaultdict(list)
    for y in range(len(inp)):
        for x, c in enumerate(inp[y]):
            if c == '^':
                splitters[x].append(y)
                assert y % 2 == 0
    return (start, splitters, len(inp))

cache = {}

def get_splits(splitters: dict[int, list[int]], beam_pos: tuple[int, int], max_y) -> int:
    global cache
    if beam_pos in cache:
        return cache[beam_pos]
    
    beam_x, beam_y = beam_pos
    if beam_y >= max_y:
        cache[beam_pos] = 1
        return 1
    
    while beam_y not in splitters[beam_x]:
        beam_y += 2
        if beam_y >= max_y:
            cache[beam_pos] = 1
            return 1
    
    timelines = get_splits(splitters, (beam_x - 1, beam_y), max_y)
    timelines += get_splits(splitters, (beam_x + 1, beam_y), max_y)
    cache[beam_pos] = timelines
    return timelines
    

def solve(inp: tuple[int, dict[int, list[int]], int], part, example):
    start, splitters, max_y = inp
    
    if part == 1:
        beams = set([start])
        y = 0
        splits = 0
        while y <= max_y:
            new_beams = set()
            for beam_x in beams:
                if y in splitters[beam_x]:
                    splits += 1
                    new_beams.add(beam_x - 1)
                    new_beams.add(beam_x + 1)
                else:
                    new_beams.add(beam_x)
            beams = new_beams
            y += 2
        return splits
    else:
        return get_splits(splitters, (start, 0), max_y)

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
