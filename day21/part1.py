from __future__ import annotations

from collections import deque
import argparse
import os.path

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def determine_value(monkeys: dict[str, int|str], k: str) -> int:
    if type(monkeys[k]) == int:
        return monkeys[k]
    elif type(monkeys[k]) == str:
        value_inputs = monkeys[k].split(' ')
        monkey1, monkey2 = value_inputs[0], value_inputs[2]
        op = value_inputs[1]
        eq = " ".join([str(determine_value(monkeys, monkey1)), op, str(determine_value(monkeys, monkey2))])
        return eval(eq)


def compute(s: str) -> int:
    monkeys = dict()
    monk_s = s.strip().splitlines()
    for m in monk_s:
        d = m.split(': ')
        try:
            d[1] = int(d[1].strip())
        except ValueError:
            d[1] = d[1].strip()
        monkeys[d[0]] = d[1]
    return int(determine_value(monkeys, 'root'))


INPUT_S = '''\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''
EXPECTED = 152


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