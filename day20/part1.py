from __future__ import annotations

from collections import deque
from unittest import mock
import argparse
import os.path

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from dataclasses import dataclass

class Number:
    flipped: bool
    shown: bool
    def __init__(self, val):
        self.val = int(val)
        self.flipped = False
        self.next = None
        self.prev = None
        self.shown = False

    def flip(self):
        d = -1 if self.val < 0 else 1
        for _ in range(0, self.val, d):
            self.prev.next = self.next
            self.prev = self.next
            self.next = self.next.next
            self.next.next = self
        self.flipped = True

    def unshow(self):
        if self.shown == False:
            return
        self.shown = False
        return self.next.unshow()

    def show(self, l):
        if self.shown:
            return
        l.append(self.val)
        self.shown = True
        return self.next.show(l)

    def __add__(self, other):
        return self.val + other.val

    def __str__(self):
        if self.next:
            nv = self.next.val
        else:
            nv = "None"
        if self.prev:
            pv = self.prev.val
        else:
            pv = "none"
        return f"<Num: {self.val}, Next: {nv}, Prev: {pv}>"


def compute(s: str) -> int:
    orig_numbers = support.parse_numbers_split(s)
    numbers = deque(list(enumerate(orig_numbers)))
    for i, num in enumerate(orig_numbers):
        idx = numbers.index((i, mock.ANY))  # love this use of mock.ANY
        numbers.rotate(-idx)
        numbers.popleft()
        numbers.rotate(-num)
        numbers.appendleft(num)

    idx_0 = numbers.index(0)
    return sum(numbers[(idx_0 + i) % len(numbers)] for i in (1000, 2000, 3000))

INPUT_S = '''\
1
2
-3
3
-2
0
4
'''
EXPECTED = 3


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