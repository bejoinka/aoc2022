from __future__ import annotations
import collections
import argparse
import os.path
import numpy as np
import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class ORating:
    bits = list()
    def __init__(self, bits: list[str]):
        self.bits = bits.copy()

    def calc(self, is_oxygen: bool = True):
        bitlen = len(self.bits[0])
        for i in range(bitlen):
            r = ''
            for b in self.bits:
                r += b[i]
            c = sorted(collections.Counter(r).most_common(2), key=lambda x: x[1], reverse=is_oxygen)
            if c[0][1] == c[1][1]:
                most_common = '1' if is_oxygen else '0'
            else:
                most_common = c[0][0]
            self.bits = list(filter(lambda x: x[i] == most_common, self.bits))
            if len(self.bits) == 1:
                return self.bits[0]
        return self.bits[0]


def compute(s: str) -> int:
    l = s.strip().split('\n')
    o_rating = ORating(l.copy())
    co_rating = ORating(l.copy())
    o = o_rating.calc()
    c = co_rating.calc(False)
    return int(o, 2) * int(c, 2)


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
EXPECTED = 230


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
