from __future__ import annotations
# from typing_extensions import Self

import heapq
import re
from dataclasses import dataclass
import argparse
import os.path
import itertools

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# I need to start on the outside and go in.
# ...what if the object is shaped like a crescent moon?

def surrounding_box(maxes, mins):
    coords = {}
    for x in range(mins[0] - 1, maxes[0] + 2):
        for y in range(mins[1] - 1, maxes[0] + 2):
            for z in range(mins[2] - 1, maxes[0] + 2):
                coords.add((x, y, z))
    return coords

def adj(cube: tuple[int, int, int]):
    (x, y, z) = cube
    return {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1),
    }


def compute(s: str) -> int:
    ls = s.strip().splitlines()
    cubes = set()
    for l in ls:
        nums = l.split(',')
        cubes.add((int(nums[0]), int(nums[1]), int(nums[2])))
    adj_sides = 0
    for c in cubes:
        adj_sides += adj_outside(c, cubes)
    # maxes = max({r[0] for r in cubes}) + 1, max({r[1] for r in cubes}) + 1, max({r[2] for r in cubes}) + 1
    # mins = min({r[0] for r in cubes}) - 1, min({r[1] for r in cubes}) - 1, min({r[2] for r in cubes}) - 1
    # todos = [(mins[0], mins[1], mins[2])]
    # visited = set()
    # while todos:
    #     coord = todos.pop()
    #     if coord in visited:
    #         continue
    #     visited.add(coord)
    #     if coord in cubes:
    #         continue
    #     for a in adj(coord):
    #         if a[0] > maxes[0] or a[1] > maxes[1] or a[2] > maxes[2] or a[0] < mins[0] or a[1] < mins[1] or a[2] < mins[2]:
    #             continue
    #         if a in cubes:
    #             adj_sides += 1
    #         todos.append(a)
    
    return adj_sides


INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 58


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