from copy import deepcopy
from collections import defaultdict

def parse_input(file = 'day08.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day08example.txt')

def format_input(inp: list[str]):
    return [tuple(map(int, line.split(','))) for line in inp]

def get_distance(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return ((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)**0.5

def solve(inp: list[tuple[int]], part, example):
    dist_dict = {}
    for i, pos1 in enumerate(inp):
        for pos2 in inp[i+1:]:
            d = get_distance(pos1, pos2)
            assert d not in dist_dict
            dist_dict[d] = (pos1, pos2)
    
    circuits = set(tuple([pos]) for pos in inp)
    seen = set()
    total_connections = 0
    for d in sorted(dist_dict.keys()):
        p1, p2 = dist_dict[d]
        to_connect = []
        for circ in circuits.copy():
            if p1 in circ:
                to_connect.append(circ)
            if p2 in circ:
                to_connect.append(circ)
            if len(to_connect) == 2:
                break

        total_connections += 1
        if to_connect[0] != to_connect[1]:
            circuits.remove(to_connect[0])
            circuits.remove(to_connect[1])
            circuits.add(to_connect[0] + to_connect[1])
            
        if part == 1 and total_connections == (10 if example else 1000):
            break
        elif part == 2 and len(circuits) == 1:
            return p1[0] * p2[0]
    
    sizes = sorted((len(circ) for circ in circuits), reverse = True)
    return sizes[0] * sizes[1] * sizes[2]

    

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
