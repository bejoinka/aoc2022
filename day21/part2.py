from __future__ import annotations

import math
import argparse
import os.path

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def determine_value(monkeys: dict[str, int|str], k: str, hi: int) -> tuple[int, bool]:
    if k == 'humn':
        return hi, True
    if type(monkeys[k]) == int:
        return monkeys[k], False
    elif type(monkeys[k]) == str:
        value_inputs = monkeys[k].split(' ')
        monkey1, monkey2 = value_inputs[0], value_inputs[2]
        op = value_inputs[1]
        l, l_humn = determine_value(monkeys, monkey1, hi)
        r, r_humn = determine_value(monkeys, monkey2, hi)
        if k == 'root':
            adj = lambda x: x + 1
            his = []
            while l != r:
                his.append((l, r, l-r, hi))
                hi = adj(hi)
                dx = hi - his[-1][-1]
                l, l_humn = determine_value(monkeys, monkey1, hi)
                r, r_humn = determine_value(monkeys, monkey2, hi)
                
                if l_humn:
                    dy = l - his[-1][0]
                    adj = lambda x: x + math.ceil(dx * (r - l) / max(dy, 1))
                elif r_humn:
                    dy = r - his[-1][1]
                    adj = lambda x: x + math.ceil(dx * (l - r) / max(dy, 1))
                else:
                    raise AssertionError('what? no humans?')
            return hi
        eq = " ".join([str(l), op, str(r)])
        return float(eval(eq)), (l_humn or r_humn)

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
        if d[0] == 'root':
            monkeys[d[0]] = monkeys[d[0]].replace('+', '==')
    resp = int(determine_value(monkeys, 'root', monkeys['humn']))
    return resp


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
EXPECTED = 301


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