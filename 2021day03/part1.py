from __future__ import annotations

import argparse
import os.path
import numpy as np
import pytest
import collections
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    l = s.strip().split('\n')
    arr = np.array([[int(s) for s in str] for str in l]).T
    ones = [np.count_nonzero(a) for a in arr]
    zeros = [len(l) - o for o in ones]
    # print(ones, zeros)
    game_rate = ''
    ep_rate = ''
    for (o, z) in zip(ones, zeros):
        if o > z:
            game_rate += '1'
            ep_rate += '0'
        else:
            game_rate += '0'
            ep_rate += '1'
    val = int(game_rate, 2) * int(ep_rate, 2)
    # print(val)
    return val


INPUT_S = '''\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''
EXPECTED = 198


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
