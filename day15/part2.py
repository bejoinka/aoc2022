from __future__ import annotations

import argparse
import os.path
import ast
import itertools
import numpy as np
import math
import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

import re

from dataclasses import dataclass
@dataclass
class Sensor:
    x: int
    y: int
    bx: int
    by: int

    def out_of_reach(self):
        x, y = self.x, self.y + self.dif + 1
        s = {(x, y)}
        for clockwise in (
            (1, -1), (-1, -1), (-1, 1), (1, 1)
        ):
            for _ in range(1, self.dif + 2):
                x += clockwise[0]
                y += clockwise[1]
                s.add((x, y))
        return s

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def dif(self):
        return abs(self.x - self.bx) + abs(self.y - self.by)

    def distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

    @property
    def coord(self):
        return (self.x, self.y)
    @property
    def beacon(self):
        return (self.bx, self.by)

def parse_line(s) -> tuple[tuple[int, int]]:
    p = re.compile(r"[0-9-]+")
    sx, sy, bx, by = p.findall(s)
    return int(sx), int(sy), int(bx), int(by)

def compute(s: str, MAX_COORD=4000000) -> int:
    ls = s.strip().splitlines()
    # print(len(ls))
    sensors: set[Sensor] = set()
    MIN_COORD = 0
    
    for l in ls:
        sensor = Sensor(*parse_line(l))
        sensors.add(sensor)

    for sensor in sensors:
        for (x, y) in sensor.out_of_reach():
            if x < MIN_COORD or y < MIN_COORD or x > MAX_COORD or y > MAX_COORD:
                continue
            for other in sensors:
                if other.distance(x, y) < other.dif:
                    break
            else:
                return x * 4000000 + y
    raise AssertionError('wut')



INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 56000011


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, MAX_COORD=20) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
