from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def rps_value(v):
    if v == 'A' or v == 'X':
        return 1
    if v == 'B' or v == 'Y':
        return 2
    if v == 'C' or v == 'Z':
        return 3

def eval_rps(opp, you):
    dif = rps_value(you) - rps_value(opp)
    if dif == 1 or dif == -2:
        return 6 + rps_value(you)
    elif dif == 0:
        return 3 + rps_value(you)
    else:
        return 0 + rps_value(you)

def compute(s: str) -> int:
    n = 0
    l = s.strip().split('\n')
    for game in l:
        n += eval_rps(*game.split(' '))
    return n


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
