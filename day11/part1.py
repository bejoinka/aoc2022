from __future__ import annotations

import re
import argparse
import os.path
from functools import partial

import pytest

import support
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def parse_monkey(monkey_string):
    test_divis = int(re.search(r"[0-9]+", monkey_string[3])[0])
    true_monkey = int(re.search(r"[0-9]+", monkey_string[4])[0])
    false_monkey = int(re.search(r"[0-9]+", monkey_string[5])[0])
    
    return {
        "items": [int(itm.strip()) for itm in monkey_string[1].split(':')[1].strip().split(',')],
        "op": partial(lambda old: eval(monkey_string[2].split('=')[1].strip())),
        "test": partial(lambda x: true_monkey if not x % test_divis else false_monkey),
    }


def compute(s: str) -> int:
    monkeys_unparsed = support.separate_by_newline(s.strip().split('\n'))
    monkeys_parsed = [parse_monkey(monkey) for monkey in monkeys_unparsed]
    monkey_touches = [0 for _ in range(len(monkeys_parsed))]
    # after each monkey inspects an item, but BEFORE it tests your worry, your worry 
    for round in range(20):
        for i, monkey in enumerate(monkeys_parsed):
            for itm in monkey['items']:
                monkey_touches[i] += 1
                itm = monkey["op"](itm)
                itm = itm // 3
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
