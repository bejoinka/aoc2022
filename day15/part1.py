from __future__ import annotations

import argparse
import os.path
import ast
import itertools

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

import re

# sand moves down, then down/left, then down/right
def parse_line(s) -> tuple[tuple[int, int]]:
    p = re.compile(r"[0-9-]+")
    sx, sy, bx, by = p.findall(s)
    return (int(sx), int(sy)), (int(bx), int(by))

def compute(s: str, Y_VAL=2000000) -> int:
    ls = s.strip().splitlines()
    # print(len(ls))
    sensors, beacons = set(), set()
    not_beacons = set()
    for l in ls:
        sensor, beacon = parse_line(l)
        sensors.add(sensor)
        beacons.add(beacon)
        dif = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        sensor_checked = set([sensor])
        
        dif_vals = [sensor[1] - dif, sensor[1] + dif]
        print(l, "dif is", dif, dif_vals)
        # if max_dif > 0:
        #     for r in range(max_dif):
        if sensor[1] > Y_VAL and sensor[1] - dif <= Y_VAL:
            for r in range(Y_VAL - (sensor[1] - dif)+1):
                # print(sensor, beacon, dif, (sensor[0] + r, Y_VAL), (sensor[0] - r, Y_VAL))
                sensor_checked.add((sensor[0] + r, Y_VAL))
                sensor_checked.add((sensor[0] - r, Y_VAL))

        elif sensor[1] < Y_VAL and sensor[1] + dif >= Y_VAL:
            for r in range(sensor[1] + dif - Y_VAL +1):
                # print(sensor, beacon, dif, (sensor[0] + r, Y_VAL), (sensor[0] - r, Y_VAL))
                sensor_checked.add((sensor[0] + r, Y_VAL))
                sensor_checked.add((sensor[0] - r, Y_VAL))
        
        # print(sensor_checked)
        # todos = set([(dif, sensor)])
        # while todos:
        #     d, itm = todos.pop()
        #     for _ in range(d):
        #         for coord in support.adjacent_4(*itm):
        #             if coord not in sensor_checked:
        #                 todos.add((d - 1, coord))
        #                 sensor_checked.add(coord)
        not_beacons |= sensor_checked
    # print(not_beacons)
    # print(support.print_coords_hash(not_beacons))
    return len([d for d in (not_beacons - beacons) if d[1] == Y_VAL]) #- len([b for b in beacons if b[1] == 10])


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
EXPECTED = 26


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, Y_VAL=10) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
