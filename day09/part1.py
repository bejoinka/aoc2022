from __future__ import annotations

import argparse
import os.path

import pytest
import numpy as np
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute_direction(instr: str) -> tuple[int, int]:
    direction, distance = instr.split()
    if direction == 'R':
        mvmt = (1, 0,)
    elif direction == 'U':
        mvmt = (0, 1,)
    elif direction == 'D':
        mvmt = (0, -1,)
    elif direction == 'L':
        mvmt = (-1, 0,)
    yield [mvmt for _ in range(int(distance))]

def move_tail(head, tail):
    # if sum is 3 then bring to 1
    # elif max is 2 then bring to 1
    # else do nothing
    if any(abs(h - t) == 2 for (h, t) in zip(head, tail)):
        # we're moving, so get down to zero if you can
        tail_move = [
            (head[i] - tail[i]) // 2 if abs(head[i] - tail[i]) == 2 else head[i] - tail[i] for i in range(2)
        ]
        return tuple([h + t for (h, t) in zip(tail, tail_move)])
    return tail

def compute(s: str) -> int:
    l = s.strip().split('\n')
    head, tail = ((0,0), (0,0))
    tail_positions = set()
    # we're going to make the starting position (0,0)
    # so we can model for any starting point on any grid
    for instr in l:
        for mvmt in next(compute_direction(instr)):
            head = (head[0] + mvmt[0], head[1] + mvmt[1])
            tail = move_tail(head, tail)
            tail_positions.add(tail)

    return len(tail_positions)


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
