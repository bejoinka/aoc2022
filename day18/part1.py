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

def adj(cube: tuple[int, int, int], cubes):
    (x, y, z) = cube
    return {itm for itm in {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1),
        }
        if itm not in cubes
    }

def compute(s: str) -> int:
    ls = s.strip().splitlines()
    cubes = set()
    for l in ls:
        nums = l.split(',')
        cubes.add((int(nums[0]), int(nums[1]), int(nums[2])))
        # cubes.add((int(i) for i in l.split(',')))
    # print(cubes)
    adj_sides = 0
    for cube in cubes:
        # print(cube)
        # print([1 for c in adj(cube) if c not in cubes])
        adj_sides += len(adj(cube, cubes))
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
EXPECTED = 64


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