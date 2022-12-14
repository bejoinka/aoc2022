from __future__ import annotations

import argparse
import os.path
import ast
import itertools

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# sand moves down, then down/left, then down/right

def dif(coord1, coord2):
    coords = set()
    xs = sorted([coord1[0], coord2[0]])
    ys = sorted([coord1[1], coord2[1]])
    for x in range(xs[0], xs[1] + 1):
        coords.add((x, coord1[1]))
    for y in range(ys[0], ys[1] + 1):
        coords.add((coord1[0], y))
    return coords

def compute(s: str) -> int:
    l = s.strip().splitlines()
    rock_coords = set()
    for line in l:
        coords = line.split(' -> ')
        first_coord = ast.literal_eval(coords[0])
        for i, next_coord in enumerate(coords[1:]):
            rock = dif(first_coord, ast.literal_eval(next_coord))
            rock_coords |= rock
            first_coord = ast.literal_eval(next_coord)
        # print(len(rock_coords))
        # print(support.print_coords_hash(rock_coords))
    max_depth = max(r[1] for r in rock_coords) + 2
    for i in range(10000):
        rock_coords.add((i, max_depth))
    n = 0
    sand_overflow = False
    sands = set()
    while not sand_overflow:
        n += 1
        sand_falling = True
        sand_coord = (500,0)
        while sand_falling:
            if (500,0) in sands:
                sand_overflow = True
                break
            sands.add(sand_coord)
            if (sand_coord[0], sand_coord[1] + 1) not in sands and (sand_coord[0], sand_coord[1] + 1) not in rock_coords:
                sands.remove(sand_coord)
                sand_coord = (sand_coord[0], sand_coord[1] + 1)
                continue
            elif (sand_coord[0] - 1, sand_coord[1] + 1) not in sands and (sand_coord[0] - 1, sand_coord[1] + 1) not in rock_coords:
                sands.remove(sand_coord)
                sand_coord = (sand_coord[0] - 1, sand_coord[1] + 1) 
                continue
            elif (sand_coord[0] + 1, sand_coord[1] + 1) not in sands and (sand_coord[0] + 1, sand_coord[1] + 1) not in rock_coords:
                sands.remove(sand_coord)
                sand_coord = (sand_coord[0] + 1, sand_coord[1] + 1)
                continue
            else:
                sand_falling = False
            
    return n - 1


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
