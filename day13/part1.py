from __future__ import annotations

import argparse
import os.path
import ast
import itertools

import pytest
import logging
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compare_lr(left, right):
    # convert to lists
    if isinstance(left, list) and not isinstance(right, list):
        right = [right]
    elif isinstance(right, list) and not isinstance(left, list):
        left = [left]
    # print("  - comparing", left, right)
    # handle those lists
    if isinstance(left, list) and isinstance(right, list):
        for l, r in itertools.zip_longest(left, right):
            # handle exhausted lists
            if l is None:
                return 1
            if r is None:
                return -1
            
            # ajksldfjklsadjfkl
            c = compare_lr(l, r)
            if c != 0:
                return c

    # simple int
    elif isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif right < left:
            return -1
        else:
            return 0
    return 0



def compute(s: str) -> int:
    ll = s.strip().splitlines()
    packets = support.separate_by_newline(ll)
    n = 0
    # print('\n====\n')
    for i, packet in enumerate(packets):
        # print('packet no', i+1)
        left, right = packet
        l = ast.literal_eval(left)
        r = ast.literal_eval(right)
        # print(f" left: {l}\n right: {r}")
        if compare_lr(l, r) == 1:
            # print(f"pair {i + 1} being added.", l, r, "\n")
            n += (i + 1)
    return n


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 13


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
