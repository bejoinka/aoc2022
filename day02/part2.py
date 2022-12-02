from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def rps(a, b):
    if a == 'A':
        if b == 'X':
            return 3 + 0
            
        elif b == 'Y':
            return 1 + 3
        elif b == 'Z':
            return 2 + 6
    elif a == 'B':
        if b == 'X':
            return 1 + 0
        elif b == 'Y':
            return 2 + 3
        elif b == 'Z':
            return 3 + 6
    elif a == 'C':
        if b == 'Z':
            return 1 + 6
        elif b == 'X':
            return 2 + 0
        elif b == 'Y':
            return 3 + 3

def compute(s: str) -> int:
    n = 0
    l = s.strip().split('\n')
    for game in l:
        n += rps(*game.split(' '))
    return n


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


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
