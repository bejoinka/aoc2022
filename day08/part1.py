from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

import numpy as np
def compute(s: str) -> int:
    visible = 0
    rows = s.strip().split('\n')
    size_x, size_y = len(rows[0]), len(rows)
    coords = np.zeros((size_x, size_y))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            coords[i][j] = val
    visible += size_x * 2  # outer rows
    for i, row in enumerate(rows):
        if i == 0 or i == size_y - 1:
            continue
        visible += 2  # outer columns in inner rows
        for j, val in enumerate(row):
            if j == 0 or j == size_x - 1:
                continue
            # print(i, j, row, val)
            if any([
                all([val > col for col in row[:j]]),
                all([val > col for col in row[j+1:]]),
                all([val > r[j] for r in rows[:i]]),
                all([val > r[j] for r in rows[i+1:]]),
            ]):
                visible += 1
    return visible


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
