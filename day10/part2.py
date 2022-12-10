from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# addx V takes two cycles... adds register
# noop is one cycle
d = {
    'addx': 2,
    'noop': 1,
}

def do_op(cycles: int, value_chg: int):
    for i in range(cycles):
        yield (0, False) if i < cycles - 1 else (value_chg, True)

def parse_instruction(instr: str):
    if instr == 'noop':
        return do_op(1, 0)
    op, value_chg = instr.split()
    return do_op(d[op], int(value_chg))

def sprites(i: int) -> tuple[int]:
    return (i-1, i, i+1)

def compute(s: str) -> int:
    register_value = 1
    cycle = 0
    opcodes = s.strip().split('\n')
    def yield_op():
        for op in opcodes:
            yield op
    op_gen = yield_op()
    op = None
    signal_strengths = list()
    CRT = ''
    row = 1
    while True:
        sprite_loc = sprites(register_value)
        try:
            cycle += 1
            if op is None:
                instr = next(op_gen)
                op = parse_instruction(instr)
        except StopIteration:
            break
        try:
            v, next_code = next(op)
            # check to see the sprite's position
            if not (cycle - 1) % 40:
                CRT += "\n"
                row += 1
            column = (cycle - 1) % 40
            print('checking column against sprites', column, sprite_loc)
            CRT += "#" if any([column == s for s in sprite_loc]) else "."
            register_value += v
            # move the sprites
            if next_code:
                op = None
        except StopIteration:
            op = None

    return CRT.strip()


INPUT_S = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED = '''\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
'''


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
