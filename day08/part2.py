from __future__ import annotations

import argparse
import os.path
import math
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
    vis_coords = np.zeros((size_x, size_y))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            # looking up
            visibility_scores = [0, 0, 0, 0]
            for up in range(i - 1, -1, -1):
                visibility_scores[0] += 1
                if rows[up][j] >= val:
                    break
            for down in range(i + 1, size_y, 1):
                visibility_scores[1] += 1
                if rows[down][j] >= val:
                    break
            for left in range(j - 1, -1, -1):
                visibility_scores[2] += 1
                if row[left] >= val:
                    break
            for right in range(j + 1, size_x, 1):
                visibility_scores[3] += 1
                if row[right] >= val:
                    break
            if i == 0 or i == size_y - 1 or j == 0 or j == size_x - 1:
                visibility_scores = [0,0]
            vis_coords[i][j] = math.prod(visibility_scores)
    return int(np.max(vis_coords))


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
    # print(compute(INPUT_S))
    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
