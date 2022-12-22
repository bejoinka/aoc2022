from __future__ import annotations

from collections import deque
from unittest import mock
import argparse
import os.path

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# going to implement as a series of linked nodes in a faster language

def compute(s: str) -> int:
    orig_numbers = [num * 811589153 for num in support.parse_numbers_split(s)]
    crypt = deque(list(enumerate(orig_numbers)))
    for _ in range(10):
        for i, num in enumerate(orig_numbers):
            idx = crypt.index((i, mock.ANY))  # love this use of mock.ANY
            crypt.rotate(-idx)
            crypt.popleft()
            crypt.rotate(-num)
            crypt.appendleft((i, num))

    idx_0 = crypt.index((mock.ANY, 0))
    return sum(crypt[(idx_0 + i) % len(crypt)][1] for i in (1000, 2000, 3000))

INPUT_S = '''\
1
2
-3
3
-2
0
4
'''
EXPECTED = 1623178306


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