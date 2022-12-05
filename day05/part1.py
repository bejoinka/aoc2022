from __future__ import annotations

import argparse
import os.path
from collections import deque
import pytest
import support
import re

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def command(s: str, cols: dict[int, deque]):
    _, no, _, from_col, _, to_col = s.split(' ')
    for _ in range(int(no)):
        cols[int(to_col)].appendleft(cols[int(from_col)].popleft())
    return no, from_col, to_col, cols

def parse_part1(s: str, stacks: dict[int, deque]):
    matches = re.finditer("[A-Z]", s)
    for match in matches:
        col_number = int((match.start() - 1) / 4) + 1
        stacks[col_number].append(match.string[match.start()])

def compute(s: str) -> int:
    l = s.split('\n')

    # find the number of stacks
    for c in l:
        if '1' in c:
            cols = { int(k): deque() for k in c.replace(" ", "")}
            break
    # build the stack
    for i, c in enumerate(l):
        if c == "":
            break
        parse_part1(c, cols)
    # run instructions
    for instr in l[i+1:]:
        if instr == "":
            break
        command(instr, cols)
    val = "".join(cols[key].popleft() for key in cols.keys())
    return val


INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'


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
