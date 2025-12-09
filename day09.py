from copy import deepcopy
from collections import defaultdict

def parse_input(file = 'day09.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day09example.txt')

def format_input(inp: list[str]):
    return [tuple(map(int, line.split(','))) for line in inp]

def solve(inp, part, example):
    edges = defaultdict(set)
    if part == 2:
        for i, (x, y) in enumerate(inp):
            xp, yp = inp[i-1]
            if x == xp:
                for ye in range(min(y, yp) + 1, max(y, yp)):
                    edges[x].add(ye)
            else:
                assert y == yp
                for xe in range(min(x, xp) + 1, max(x, xp)):
                    edges[xe].add(y)
    
    max_area = 0
    
    for i, p1 in enumerate(inp):
        max_distances = {(False, False): (999_999, 999_999),
                         (True,  False): (999_999, 999_999),
                         (False, True ): (999_999, 999_999),
                         (True,  True ): (999_999, 999_999)}
            
        for p2 in inp[i+1:]:
            min_x = min(p1[0], p2[0])
            max_x = max(p1[0], p2[0])
            min_y = min(p1[1], p2[1])
            max_y = max(p1[1], p2[1])
            valid = True
            dx, dy = p1[0] - p2[0], p1[1] - p2[1]
            quadrant = (dx > 0, dy > 0)
            if part == 2:
                max_dist = max_distances[quadrant]
                if abs(dx) > max_dist[0] and abs(dy) > max_dist[1]:
                    continue
                for xe in range(min_x + 1, max_x):
                    for ye in edges[xe]:
                        if min_y < ye < max_y:
                            valid = False
                            if abs(dx) <= max_dist[0] and abs(dy) <= max_dist[1]:
                                max_distances[quadrant] = (abs(dx), abs(dy))
                            break
                    if not valid:
                        break
            if valid:
                area = (abs(dx) + 1) * (abs(dy) + 1)
                if area > max_area:
                    max_area = area
    return max_area
    


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
