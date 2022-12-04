from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    n = 0
    l = s.strip().split('\n')
    for i, c in enumerate(l):
        job1, job2 = c.split(',')
        j11, j12 = job1.split('-')
        j21, j22 = job2.split('-')
        job_range_1 = set(range(int(j11), int(j12) + 1))
        job_range_2 = set(range(int(j21), int(j22) + 1))
        total_jobs = job_range_1 | job_range_2
        if len(total_jobs) < len(job_range_1) + len(job_range_2):
            n += 1
    return n


INPUT_S = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 4


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
