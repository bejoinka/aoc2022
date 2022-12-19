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

minus = "####"
plus = """
.#.
###
.#.
"""
brack = """
..#
..#
###
"""
line = """
#
#
#
#
"""
square = """
##
##
"""

def next_rock():
    i = 0
    rocks = [support.parse_coords_hash(r) for r in [
        minus.strip(),
        plus.strip(),
        brack.strip(),
        line.strip(),
        square.strip(),
    ]]
    while True:
        yield rocks[i % 5]
        i += 1

AIR_D = {
    ">": (1, 0),
    "<": (-1, 0),
}

def next_air(s: str):
    i = 0
    while True:
        # print("AIR", s[i % len(s)])
        yield AIR_D[s[i % len(s)]]
        i += 1


def compute(s: str) -> int:
    ls = "".join(s.strip().splitlines()).strip()
    rock_wall = set(support.parse_coords_hash("#######"))
    h = min([0] + [w[1] for w in rock_wall])
    a = next_air(ls)
    r = next_rock()
    cum_h = 0
    for _ in range(20220):
        # print("\n==============\n")
        currock = next(r)
        # print(currock)
        height_currock = abs(max({r[1] for r in currock}) - min({r[1] for r in currock}))
        currock = {(r[0] + 2, -(-r[1] + height_currock + abs(h) + 4)) for r in currock}
        # print(abs(h), currock)
        # print(support.print_coords_hash(currock | rock_wall))
        is_falling = True
        while is_falling:

            air_push = next(a)
            potential = {(coord[0]+air_push[0], coord[1]) for coord in currock}
            if any(
                [coord[0] < 0 or coord[0] > 6 for coord in potential]
            ) or (rock_wall & potential):
                potential = currock.copy()
            currock = potential.copy()
            
            # go down if you can
            potential = {(coord[0], coord[1] + 1) for coord in currock}
            if rock_wall & potential:
                potential = currock.copy()
                is_falling = False

            currock = potential.copy()

        rock_wall |= currock
        # h = min([0] + [w[1] for w in rock_wall])
        # maxes = []
        # for i in range(7):
        #     maxes.append(min(r[1] for r in rock_wall if r[0] == i))
        # h_to_add = max(maxes)
        # if h_to_add < 0:
        #     # print(cum_h)
        #     cum_h += h_to_add
        #     rock_wall = {(r[0], r[1] - h_to_add) for r in rock_wall}
        #     rock_wall -= {r for r in rock_wall if r[1] > 0}
        h = min([0] + [y for _, y in rock_wall])
    with open('./end.txt', 'w') as f:
        f.write(support.format_coords_hash(rock_wall))
    # return abs(h + cum_h)

# chamber is 7 units wide


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 3068


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