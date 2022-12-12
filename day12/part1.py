from __future__ import annotations

import argparse
import os.path
import heapq

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

D = {
    'S': 'a',
    'E': 'z',
}

def compute(s: str) -> int:
    start, end = None, None
    coords = dict()
    for y, row in enumerate(s.splitlines()):
        for x, char in enumerate(row):
            coords[(x, y)] = char
            if char == "E":
                end = (x, y)
            elif char == "S":
                start = (x, y)

    assert start is not None
    assert end is not None
    visited = set()
    queue = [(0, start)]

    while queue:
        steps, pos = heapq.heappop(queue)

        if pos == end:
            return steps
        elif pos in visited:
            continue
        else:
            visited.add(pos)

        for adj in support.adjacent_4(*pos):
            if adj in coords:
                current_c = D.get(coords[pos], coords[pos])
                adj_c = D.get(coords[adj], coords[adj])
                if ord(adj_c) - ord(current_c) <= 1:
                    heapq.heappush(queue, (steps + 1, adj))

    raise AssertionError('should have completed')


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


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
