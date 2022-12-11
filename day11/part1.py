from __future__ import annotations

import argparse
import os.path

import pytest

import support
import typing
from functools import partial
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# monkeys = [
#     {
#         "items": [79, 98],
#         "op": partial(lambda x: x * 29),
#         "test": partial(lambda x: 2 if x % 23 == 0 else 3)
#     },
#     {
#         "items": [54, 65, 75, 74],
#         "op": partial(lambda x: x + 6),
#         "test": partial(lambda x: 2 if x % 19 == 0 else 0)
#     },
#     {
#         "items": [79, 60, 97],
#         "op": partial(lambda x: x * x),
#         "test": partial(lambda x: 1 if x % 13 == 0 else 3)
#     },
#     {
#         "items": [74],
#         "op": partial(lambda x: x + 3),
#         "test": partial(lambda x: 0 if x % 17 == 0 else 1)
#     },
# ]

import re
from collections import deque
def parse_monkey(monkey_string):
    test_divis = int(re.search(r"[0-9]+", monkey_string[3])[0])
    true_monkey = int(re.search(r"[0-9]+", monkey_string[4])[0])
    false_monkey = int(re.search(r"[0-9]+", monkey_string[5])[0])
    
    return {
        "items": [int(itm.strip()) for itm in monkey_string[1].split(':')[1].strip().split(',')],
        "op": partial(lambda old: eval(monkey_string[2].split('=')[1].strip())),
        "test": partial(lambda x: true_monkey if not x % test_divis else false_monkey),
        "true": true_monkey,
        "false": false_monkey,
        "divisor": test_divis,
    }
import math
def compute(s: str) -> int:
    monkeys_unparsed = support.separate_by_newline(s.strip().split('\n'))
    monkeys_parsed = [parse_monkey(monkey) for monkey in monkeys_unparsed]
    monkey_touches = [0 for _ in range(len(monkeys_parsed))]
    big_divisor = math.prod([m['divisor'] for m in monkeys_parsed])
    # after each monkey inspects an item, but BEFORE it tests your worry, your worry 
    for round in range(10000):
        for i, monkey in enumerate(monkeys_parsed):
            for itm in monkey['items']:
                # print('inspecting itm', itm)
                monkey_touches[i] += 1
                # chg worry level
                itm = monkey["op"](itm)
                # print('adjusted worry', itm)
                # itm = itm // 3
                # print('divided by 3', itm)
                # print('sending to:', monkey['test'](itm))
                itm = itm % big_divisor
                monkeys_parsed[monkey['test'](itm)]['items'].append(itm)
            monkey['items'] = list()
        if not round % 100:
            print(round)
    return sorted(monkey_touches, reverse=True)[0] * sorted(monkey_touches, reverse=True)[1]


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 10605


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
