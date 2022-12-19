"""
This is a pretty slow representation. Took 15 seconds on my computer to get through it.

I implemented an idea to speed it up (keep track of a cumulative height `cum_h`
when the min-max changes and blow away the coords under that min-max height)
in my end-of-drop method but borked it when implementing this start-of-drop method.
"""


from __future__ import annotations

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
ROCKS = [support.parse_coords_hash(r) for r in [
        minus.strip(),
        plus.strip(),
        brack.strip(),
        line.strip(),
        square.strip(),
    ]]
AIR_D = {
    ">": (1, 0),
    "<": (-1, 0),
}
TRILLION = 1_000_000_000_000
DOWN = (0, 1)

def height(c: set[tuple[int, int]]):
    return abs(max({r[1] for r in c}) - min({r[1] for r in c})) + 1

def move_rock(
    dir: tuple[int, int],
    r: set[tuple[int, int]],
    wall: set[tuple[int, int]]
) -> set[tuple[int, int]]:
    potential = {(c[0]+dir[0], c[1]+dir[1]) for c in r}
    if any(
        [c[0] < 0 or c[0] > 6 for c in potential]
    ) or (wall & potential):
        return r.copy()
    else:
        return potential.copy()


def compute(s: str) -> int:
    ls = "".join(s.strip().splitlines()).strip()
    rock_wall = set([(x, 0) for x in range(7)])
    h = min([0] + [w[1] for w in rock_wall])
    a = itertools.cycle(enumerate(ls)) #next_air(ls)
    r = itertools.cycle(enumerate(ROCKS)) #next_rock()

    # we use these down below
    # rock_vals = lambda i: {x for x, y in rock_wall if y == i}
    # k = -1
    # start_point = None
    # cum_h = 0
    pattern_length = 1

    keys = {}
    pattern_found = False
    i = 1
    while i <= TRILLION:
        i_rock, currock = next(r)
        i_air, air_push = next(a)
        currock = {(r[0] + 2, -(-r[1] + height(currock) + abs(h) + 3)) for r in currock}
        
        height_above_top = max(min(r[1] for r in rock_wall if r[0] == i) for i in range(7))
        pat = (i_rock, i_air, min(y for _, y in currock) - height_above_top)
        if not pattern_found:
            if keys.get(pat):
                print("pattern found")
                pattern_length = i - keys[pat][0]
                pattern_height = abs(h) - keys[pat][1]
                print("Pattern length:", pattern_length, "Pattern height:", pattern_height)
                height_before_pattern = keys[pat][1]
                pattern_repeat = (TRILLION - height_before_pattern) // pattern_length
                height_from_pattern = pattern_repeat * pattern_height
                print("height from pattern", height_from_pattern)
                print("total before remainder", height_from_pattern + height_before_pattern)
                i = pattern_length * pattern_repeat + keys[pat][0]
                print("Bumping i to", i)
                pattern_found = True
            else:
                keys[pat] = (i, abs(h))
        # the rock can always move once and fall once.
        currock = move_rock(AIR_D[air_push], currock, rock_wall)
        currock = move_rock(DOWN, currock, rock_wall)
        while True:
            i_air, air_push = next(a)
            currock = move_rock(AIR_D[air_push], currock, rock_wall)
            # go down if you can
            # if the rock can't, then no more falling.
            if rock_wall & {(coord[0], coord[1] + 1) for coord in currock}:
                break
            currock = move_rock(DOWN, currock, rock_wall)
        
        # update the rockwall and height after the piece falls
        rock_wall |= currock
        h = min([0] + [w[1] for w in rock_wall])

        i += 1

    resp = abs(h) + height_from_pattern - pattern_height
    # print(abs(h))
    # print("ans", resp, "dif:", EXPECTED - resp)
    return resp
        ### THIS IS A LOT OF JUNK FROM A PREVIOUS METHOD OF LOOKING AT END OF THE DROP
        ### RATHER THAN AT THE BEGINNING OF THE DROP...
        # support.print_coords_hash(currock | rock_wall)
        # if start_point is None:
        #     maxes = []
        #     for i in range(7):
        #         maxes.append(min(r[1] for r in rock_wall if r[0] == i))
        #     start_point = max(maxes)
        #     if start_point == 0:
        #         start_point = None
        # while start_point and pattern_length < abs(h // 2 - start_point):
        #     # we'll be able to optimize later so we aren't re-writing
        #     # check -2 to -1... if not the same, then add 1 to pattern length and try next
        #     if rock_vals(k).difference(rock_vals(k - pattern_length)):
        #         print(pattern_length)
        #         pattern_length += 1
        #         continue
        #     # otherwise, essentially increment k and keep trying.
            
        #     for i in range(k, k-pattern_length, -1):
        #         breakpoint()
        #         if rock_vals(i).difference(rock_vals(i - pattern_length)):
        #             pattern_length += 1
        #             break
        #     else:
        #         print('found pattern length', pattern_length)
        #         number_of_patterns = TRILLION // pattern_length
        #         remainder = TRILLION - (number_of_patterns * pattern_length)
        #         print('remainder', remainder)
        #         return h * number_of_patterns


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 1514285714288


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